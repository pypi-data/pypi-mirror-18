# -*- coding: utf-8 -*-
#
# Methods for generating quorra plot models.
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import json
import pandas


# models
# ------
def line():
    return Plot('line')


def density():
    return Plot('density')


def scatter():
    return Plot('scatter')


def bar():
    return Plot('bar')


def histogram():
    return Plot('histogram')


def pie():
    return Plot('pie')


def multiline():
    return Plot('multiline')


# objects
# -------
class Plot(object):

    def __init__(self, model):
        self.model = model
        self.attr = {}
        return

    def __getattr__(self, item):
        def func(value, key=item):
            self.attr[key] = value
            return self
        return func

    def __str__(self):
        ret = 'quorra.{}()'.format(self.model)
        for key in self.attr:
            ret += '\n.{}({})'.format(key, json.dumps(self.attr[key]))
        return ret

    def data(self, data, x=None, y=None, group=None, label=None):
        if isinstance(data, pandas.DataFrame):    
            self.attr['data'] = []
            for idx in range(0, len(data)):
                entry = {}
                if x is not None:
                    entry['x'] = data[x][idx]
                if y is not None:
                    entry['y'] = data[y][idx]
                if group is not None:
                    entry['group'] = data[group][idx]
                if label is not None:
                    entry['label'] = data[label][idx]
                self.attr['data'].append(entry)
        elif isinstance(data, list, tuple):
            self.attr['data'] = data
        else:
            raise AssertionError('Input data must be one of type: (list, tuple, pandas.DataFrame)')
        return self

