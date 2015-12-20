#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
from collections import OrderedDict
import json

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
RUNNING_PATH = sys.path[0] + os.sep


class ZLReflection(object):
    @classmethod
    def to_value(cls, obj):
        result = None
        if obj == None:
            result = None
        elif isinstance(obj, (int, float, long, str, bool)):
            result = obj
        elif isinstance(obj, list):
            if len(obj) > 0:
                result = list()
                for list_item in obj:
                    if list_item:
                        result.append(ZLReflection.to_value(list_item))
        elif hasattr(obj, '__call__'):
            result = None
        elif hasattr(obj, '__class__'):
            result = dict()
            class_items = dir(obj)
            try:
                for class_item in class_items:
                    if hasattr(obj, class_item) and not class_item[:1] == '_':
                        value = getattr(obj, class_item)
                        if value:
                            result_value = ZLReflection.to_value(value)
                            if result_value: result[class_item] = result_value
            except:
                print class_items
        else:
            result = obj
        return result

    @classmethod
    def to_dict(cls, class_obj):
        result = dict()
        class_items = dir(class_obj)
        for class_item in class_items:
            if not class_item[:2] == '__':
                value = getattr(class_obj, class_item)
                if not value:
                    continue
                if isinstance(value, list):
                    result[class_item] = list()
                    for list_item in value:
                        result[class_item].append(list_item)
                result[class_item] = value
        return result

    @classmethod
    def from_dict(cls, class_type, dict_obj):
        result = class_type()
        for key in dict_obj:
            if dict_obj[key]:
                setattr(result, key, dict_obj[key])
        return result

    @classmethod
    def to_ordered_dict(cls, class_obj):
        result = OrderedDict()
        class_items = dir(class_obj)
        for class_item in class_items:
            if not class_item[:2] == '__':
                value = getattr(class_obj, class_item)
                if value:
                    result[class_item] = value
        return result

    @classmethod
    def to_json_string(cls, obj):
        result = ''
        if isinstance(obj, (list, dict, OrderedDict)):
            return json.dumps(obj, indent=4, sort_keys=True)
        return result
