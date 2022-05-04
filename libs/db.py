# -*- coding: utf-8 -*-
# Autor: christian
from django.db import connection
from django.core.cache import cache
from django.db import models


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict
    :param cursor: cr database
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def raw_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return dictfetchall(cursor)


class CacheManager(models.Manager):

    def _getCacheKey(self, id, subset='s'):
        return "%s_%s_%s" % (self.model._meta.object_name, subset, id)

    def all_cached(self):
        if self.__class__.__name__ == 'RelatedManager':
            key = "".join(["%s%s" % el for el in self.core_filters.items()])
            cacheKey = self._getCacheKey(0, key)
        else:
            cacheKey = self._getCacheKey(0, 'all')
        qs = cache.get(cacheKey)
        if qs is None:
            qs = list(self.get_query_set())
            for element in qs:
                if hasattr(element,'_init_instance_cache'):
                    element._init_instance_cache()
            cache.set(cacheKey, qs)
        return qs

    def get_cached(self, *args, **kwargs):
        cacheKey = cat = None
        if self.__class__.__name__ == 'RelatedManager':
            key = "".join(["%s%s" % el for el in self.core_filters.items()])
        else:
            key = ""
        lst = map(lambda x:(x[0],x[1].pk if isinstance(x[1],models.Model) else str(x[1])),kwargs.items())
        key += "_" + "_".join(list(map(unicode,args))+list(map(lambda x:"%s:%s"%x,lst)))
        key = key.replace(" ","")
        cacheKey = self._getCacheKey(key)

        # check if we have a result already ached
        if cacheKey is not None:
            element = cache.get(cacheKey)

        # no results, try to get it from cache
        if element is None:
            element = self.get_query_set().get(*args, **kwargs)
            if hasattr(element,'_init_instance_cache'):
                element._init_instance_cache()
            # if this should be cached, write it to the cache
            if cacheKey is not None:
                cache.set(cacheKey, element)

        return element