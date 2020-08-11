from collections import OrderedDict


class OrderedDictCache:
    def __init__(self, cache_size, ttl):
        self.cache_size = cache_size
        self.ttl = ttl
        self.cache = OrderedDict()

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            value = None
        return self._touch_cache(key, value)

    def __setitem__(self, key, value):
        self._touch_cache(key, (value, time() + self.ttl))

    def __str__(self):
        return str(self.cache)

    def _touch_cache(self, key, value):
        try:
            del self.cache[key]
        except KeyError:
            pass

        if value and time() < value[1]:
            self.cache[key] = value
            to_del = len(self.cache) - self.cache_size
            if to_del > 0:
                for k in self.cache.keys()[:to_del]:
                    del self.cache[k]
            return value
        return None
