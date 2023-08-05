import asyncio
import imp
import json
import os
import logging
import socket
import sys
import time
import traceback
from aiohttp import web
try:
    from functools import reduce
except Exception:
    pass


def basic_exception_handler(_, e):
    return False, str(e)


def json_success_handler(results):
    data = {
        'hostname': socket.gethostname(),
        'status': 'success',
        'timestamp': time.time(),
        'results': results,
    }

    return json.dumps(data)


def json_failed_handler(results):
    data = {
        'hostname': socket.gethostname(),
        'status': 'failure',
        'timestamp': time.time(),
        'results': results,
    }

    return json.dumps(data)


def check_reduce(passed, result):
    return passed and result.get('passed')


class HealthCheck(object):
    def __init__(self, success_status=200, success_headers=None,
                 success_handler=json_success_handler, success_ttl=27,
                 failed_status=500, failed_headers=None,
                 failed_handler=json_failed_handler, failed_ttl=9,
                 exception_handler=basic_exception_handler, checkers=None,
                 logger=None, **options):
        self.cache = dict()

        self.success_status = success_status
        self.success_headers = success_headers or {'Content-Type': 'application/json'}
        self.success_handler = success_handler
        self.success_ttl = float(success_ttl or 0)

        self.failed_status = failed_status
        self.failed_headers = failed_headers or {'Content-Type': 'application/json'}
        self.failed_handler = failed_handler
        self.failed_ttl = float(failed_ttl or 0)

        self.exception_handler = exception_handler

        self.options = options
        self.checkers = checkers or []

        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger('HealthCheck')

    @asyncio.coroutine
    def __call__(self, request):
        message, status, headers = yield from self.check()
        return web.Response(text=message, status=status, headers=headers)

    def add_check(self, func):
        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)

        self.checkers.append(func)

    @asyncio.coroutine
    def check(self):
        results = []
        for checker in self.checkers:
            if checker in self.cache and self.cache[checker].get('expires') >= time.time():
                result = self.cache[checker]
            else:
                result = yield from self.run_check(checker)
                self.cache[checker] = result
            results.append(result)

        passed = reduce(check_reduce, results, True)

        if passed:
            message = "OK"
            if self.success_handler:
                message = self.success_handler(results)

            return message, self.success_status, self.success_headers
        else:
            message = "NOT OK"
            if self.failed_handler:
                message = self.failed_handler(results)

            return message, self.failed_status, self.failed_headers

    @asyncio.coroutine
    def run_check(self, checker):
        try:
            passed, output = yield from checker()
        except Exception:
            traceback.print_exc()
            e = sys.exc_info()[0]
            self.logger.exception(e)
            passed, output = self.exception_handler(checker, e)

        if not passed:
            msg = 'Health check "{}" failed with output "{}"'.format(checker.__name__, output)
            self.logger.error(msg)

        timestamp = time.time()
        if passed:
            expires = timestamp + self.success_ttl
        else:
            expires = timestamp + self.failed_ttl

        result = {'checker': checker.__name__,
                  'output': output,
                  'passed': passed,
                  'timestamp': timestamp,
                  'expires': expires}
        return result


class EnvironmentDump(object):
    def __init__(self,
                 include_os=True,
                 include_python=True,
                 include_process=True):
        self.functions = {}
        if include_os:
            self.functions['os'] = self.get_os
        if include_python:
            self.functions['python'] = self.get_python
        if include_process:
            self.functions['process'] = self.get_process

    @asyncio.coroutine
    def __call__(self, request):
        data = yield from self.dump_environment()
        return web.json_response(data)

    def add_section(self, name, func):
        if name in self.functions:
            raise Exception('The name "{}" is already taken.'.format(name))

        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)

        self.functions[name] = func

    @asyncio.coroutine
    def dump_environment(self):
        data = {}
        for name, func in self.functions.items():
            data[name] = yield from func()

        return data

    @asyncio.coroutine
    def get_os(self):
        return {'platform': sys.platform,
                'name': os.name,
                'uname': os.uname()}

    @asyncio.coroutine
    def get_python(self):
        result = {'version': sys.version,
                  'executable': sys.executable,
                  'pythonpath': sys.path,
                  'version_info': {'major': sys.version_info.major,
                                   'minor': sys.version_info.minor,
                                   'micro': sys.version_info.micro,
                                   'releaselevel': sys.version_info.releaselevel,
                                   'serial': sys.version_info.serial}}
        if imp.find_module('pip'):
            import pip
            packages = dict([(p.project_name, p.version) for p in pip.get_installed_distributions()])
            result['packages'] = packages

        return result

    @asyncio.coroutine
    def get_login(self):
        # Based on https://github.com/gitpython-developers/GitPython/pull/43/
        # Fix for 'Inappopropirate ioctl for device' on posix systems.
        if os.name == "posix":
            import pwd
            username = pwd.getpwuid(os.geteuid()).pw_name
        else:
            username = os.environ.get('USER', os.environ.get('USERNAME', 'UNKNOWN'))
            if username == 'UNKNOWN' and hasattr(os, 'getlogin'):
                username = os.getlogin()
        return username

    @asyncio.coroutine
    def get_process(self):
        return {'argv': sys.argv,
                'cwd': os.getcwd(),
                'user': (yield from self.get_login()),
                'pid': os.getpid(),
                'environ': self.safe_dump(os.environ)}

    def safe_dump(self, dictionary):
        result = {}
        for key in dictionary.keys():
            if 'key' in key.lower() or 'token' in key.lower() or 'pass' in key.lower():
                # Try to avoid listing passwords and access tokens or keys in the output
                result[key] = "********"
            else:
                try:
                    json.dumps(dictionary[key])
                    result[key] = dictionary[key]
                except TypeError:
                    pass
        return result
