# This file is part of jenkins-epo
#
# jenkins-epo is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# jenkins-epo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# jenkins-epo.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import asyncio
import datetime
import fnmatch
import logging
import random
import time
import sys

from github import ApiError
from http.client import HTTPException
import retrying
from requests import HTTPError


logger = logging.getLogger(__name__)


class ARetrying(retrying.Retrying):
    def call(self, fn, *args, **kwargs):
        if asyncio.iscoroutinefunction(fn):
            return self.acall(fn, *args, **kwargs)
        else:
            return super(ARetrying, self).call(fn, *args, **kwargs)

    def acall(self, fn, *args, **kwargs):
        start_time = int(round(time.time() * 1000))
        attempt_number = 1
        while True:
            try:
                result = yield from fn(*args, **kwargs)
                attempt = retrying.Attempt(result, attempt_number, False)
            except:
                tb = sys.exc_info()
                attempt = retrying.Attempt(tb, attempt_number, True)

            if not self.should_reject(attempt):
                return attempt.get(self._wrap_exception)

            delay_since_first_attempt_ms = (
                int(round(time.time() * 1000)) - start_time
            )
            if self.stop(attempt_number, delay_since_first_attempt_ms):
                if not self._wrap_exception and attempt.has_exception:
                    # get() on an attempt with an exception should cause it to
                    # be raised, but raise just in case
                    raise attempt.get()
                else:
                    raise retrying.RetryError(attempt)
            else:
                sleep = self.wait(attempt_number, delay_since_first_attempt_ms)
                if self._wait_jitter_max:
                    jitter = random.random() * self._wait_jitter_max
                    sleep = sleep + max(0, jitter)
                time.sleep(sleep / 1000.0)

            attempt_number += 1


def retry(*dargs, **dkw):
    defaults = dict(
        retry_on_exception=filter_exception_for_retry,
        wait_exponential_multiplier=500,
        wait_exponential_max=15000,
    )

    if len(dargs) == 1 and callable(dargs[0]):
        def wrap_simple(f):
            def wrapped_f(*args, **kw):
                return ARetrying(**defaults).call(f, *args, **kw)
            return wrapped_f
        return wrap_simple(dargs[0])
    else:
        dkw = dict(defaults, **dkw)

        def wrap(f):
            def wrapped_f(*args, **kw):
                return ARetrying(*dargs, **dkw).call(f, *args, **kw)

            return wrapped_f

        return wrap


def filter_exception_for_retry(exception):
    from .github import wait_rate_limit_reset

    if isinstance(exception, ApiError):
        try:
            message = exception.response['json']['message']
        except KeyError:
            # Don't retry on ApiError by default. Things like 1000 status
            # update must be managed by code.
            return False
        if 'API rate limit exceeded for' in message:
            wait_rate_limit_reset()
            return True
        # If not a rate limit error, don't retry.
        return False

    if not isinstance(exception, (IOError, HTTPException, HTTPError)):
        return False

    if isinstance(exception, HTTPError):
        if exception.response.status_code < 500:
            return False

    logger.warn(
        "Retrying on %r: %s",
        type(exception), str(exception) or repr(exception)
    )
    return True


def format_duration(duration):
    duration = datetime.timedelta(seconds=duration / 1000.)
    h, m, s = str(duration).split(':')
    h, m, s = int(h), int(m), float(s)
    duration = '%.1f sec' % s
    if h or m:
        duration = '%d min %s' % (m, duration)
    if h:
        duration = '%d h %s' % (h, duration)
    return duration.replace('.0', '')


def match(item, patterns):
    matched = not patterns
    for pattern in patterns:
        negate = False
        if pattern.startswith('-') or pattern.startswith('!'):
            negate = True
            pattern = pattern[1:]
        if pattern.startswith('+'):
            pattern = pattern[1:]

        local_matched = fnmatch.fnmatch(item, pattern)
        if negate:
            matched = matched and not local_matched
        else:
            matched = matched or local_matched

    return matched


def parse_datetime(formatted):
    return datetime.datetime.strptime(
        formatted, '%Y-%m-%dT%H:%M:%SZ'
    )


def parse_patterns(raw):
    return [p for p in str(raw).split(',') if p]


class Bunch(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
