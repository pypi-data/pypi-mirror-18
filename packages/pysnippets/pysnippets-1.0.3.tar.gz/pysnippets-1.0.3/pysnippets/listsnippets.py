# -*- coding: utf-8 -*-


all_ = all
any_ = any


class ListSnippets(object):
    def all(self, list_, eles):
        return all_([ele in list_ for ele in eles])

    def any(self, list_, eles):
        return any_([ele in list_ for ele in eles])


_global_instance = ListSnippets()
all = _global_instance.all
any = _global_instance.any
