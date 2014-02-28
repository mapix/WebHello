# -*- coding:utf-8 -*-

from functools import wraps
from inspect import getcallargs, getargspec

__all__ = ['Cache', 'PLCache', 'TPLCache']

class Cache(object):

    def __init__(self, mc, key_pattern, expire=0):
        self.mc = mc
        self.key_pattern = key_pattern
        self.expire = expire

    def __call__(self, func):
        @wraps(func)
        def _(*args, **kwargs):
            _, mc_key = self._gen_key(func, args, kwargs)
            result = self.mc.get(mc_key)
            if result is None:
                result = func(*args, **kwargs)
                if result is not None:
                    self.mc.set(mc_key, result, expire=expire)
            return result
        return _

    def _gen_key(self, func, fargs, fkwargs):
        call_args = getcallargs(func, *fargs, **fkwargs)
        if callable(self.key_pattern):
            pattern_args = getargspec(self.key_pattern).args
            mc_key = self.key_pattern(*[call_args.get(i) for i in pattern_args])
        else:
            mc_key = self.key_pattern.format(**call_args)
        return call_args, mc_key


class PLCache(Cache):
    """ partial-list cache """

    def __init__(self, mc, key_pattern, expire=0, count=400):
        super(PLCache, self).__init__(mc, key_pattern, expire=expire)
        self.count = count

    def __call__(self, func):
        @wraps(func)
        def _(*args, **kwargs):
            call_args, mc_key = self._gen_key(func, args, kwargs)
            start = call_args.pop('start', 0)
            limit = call_args.pop('limit')
            if limit is None or start + limit > count:
                return f(*args, **kwargs)
            result = self.mc.get(mc_key)
            if result is None:
                result = func(*args, limit=count, **kwargs)
                self.mc.set(mc_key, result, expire=expire)
            return result[start:start+limit]
        return _

class TPLCache(PLCache):
    """ partial-list cache with total """

    def __call__(self, func):
        @wraps(func)
        def _(*args, **kwargs):
            call_args, mc_key = self._gen_key(func, args, kwargs)
            start = call_args.pop('start', 0)
            limit = call_args.pop('limit')
            if limit is None or start + limit > count:
                return f(*args, **kwargs)
            cached_result = self.mc.get(mc_key)
            if cached_result is None:
                total, result = func(*args, limit=count, **kwargs)
                self.mc.set(mc_key, (total, result), expire=expire)
            else:
                total, result = cached_result
            return total, result[start:start+limit]
        return _
