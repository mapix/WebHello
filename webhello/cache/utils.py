# -*- coding:utf-8 -*-

__all__ = ['LocalCached']


class LocalCached(LogMixin):

    def __init__(self, mc, size=10000):
        self.mc = mc
        self.dataset = {}
        self.size = size

    def __repr__(self):
        return "Locally Cached " + str(self.mc)

    def _cache(self, key, value):
        if len(self.dataset) >= self.size:
            self.dataset.clear()
        self.dataset[key] = value

    def get(self, key):
        if key in self.dataset:
            return self.dataset[key]
        r = self.mc.get(key)
        if r is not None:
            self._cache(key, r)
        return r

    def gets(self, key):
        return self.mc.gets(key)

    def get_multi(self, keys):
        ds = self.dataset
        ds_get = ds.get
        r = dict((k, ds[k]) for k in keys if ds_get(k) is not None)
        missed = [k for k in keys if k not in ds]
        if missed:
            rs = self.mc.get_multi(missed)
            r.update(rs)
            ds.update(dict((k, rs.get(k)) for k in missed))
        return r

    def get_list(self, keys):
        rs = self.get_multi(keys)
        return [rs.get(k) for k in keys]

    def set(self, key, value, time=0, compress=True):
        self._cache(key, value)
        return self.mc.set(key, value, time, compress)

    def cas(self, key, value, time=0, cas=0):
        if self.mc.cas(key, value, time, cas):
            self._cache(key, value)
            return True
        else:
            self.dataset.pop(key, None)
            return False

    def clear(self):
        self.dataset.clear()
        if hasattr(self.mc, 'clear'):
            self.mc.clear()

    def __getattr__(self, name):
        attr = getattr(self.mc, name, None)
        if name in ('add', 'replace', 'delete', 'incr', 'decr', 'prepend', 'append', 'touch', 'expire'):
            @wraps(attr)
            def func(key, *args, **kwargs):
                self.dataset.pop(key, None)
                return attr(key, *args, **kwargs)
            return func
        elif name in ('append_multi', 'prepend_multi', 'delete_multi', 'set_multi'):
            @wraps(attr)
            def func(keys, *args, **kwargs):
                for k in keys:
                    self.dataset.pop(k, None)
                return attr(keys, *args, **kwargs)
            return func
        elif not name.startswith('__'):
            return attr
        raise AttributeError(name)
