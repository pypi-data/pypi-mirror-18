# -*- coding: utf-8 -*-

import sys
import bisect
import threading

from . import hash_f

def is_py2():
    return sys.version_info[0] == 2


def is_py3():
    return sys.version_info[0] == 3

class _Point(object):

    def __init__(self, value, desc):
        self.value = value
        self.desc = desc

    def __str__(self):
        return '_Point(%d,%s)' % (self.value, self.desc)

    def __cmp__(self, other):
        """
        兼容py2
        """
        return self.value - other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return (self.value == other.value) and (self.desc == other.desc)

    def __hash__(self):
        return hash(self.value) + hash(self.desc)


class Continuum(object):

    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.points = []
        self.desc_capacity = {}  # desc:capacity

    def get_name(self):
        return self.name

    def Size(self):
        with self.lock:
            return len(self.points)

    def Locate(self, hash_value):
        with self.lock:
            if not self.points:
                return None
            p = _Point(hash_value, "")
            i = bisect.bisect_right(self.points, p)
            point_size = len(self.points)
            if i != point_size:
                return self.points[i % point_size].desc
            else:
                return self.points[0].desc

    def Rebuild(self):
        with self.lock:
            total_value = 0
            for v in self.desc_capacity.values():
                total_value += v

            if total_value == 0:
                return False

            new_points = []
            for desc, val in self.desc_capacity.items():
                for i in range(val):
                    # very important!!!
                    replicated_desc = '%s-%x' % (desc, i)
                    hash_value = Continuum.Hash(replicated_desc)
                    # very important!!!
                    bisect.insort(new_points, _Point(hash_value, desc))
            self.points = new_points
            return True

    def Add(self, desc, capacity):
        with self.lock:
            self.desc_capacity[desc] = capacity

    def Remove(self, desc):
        with self.lock:
            if desc in self.desc_capacity:
                del self.desc_capacity[desc]

    def Clear(self):
        with self.lock:
            self.desc_capacity.clear()

    @staticmethod
    def Hash(key):
        if is_py2():
            if not isinstance(key, basestring):
                key = str(key)
            return hash_f.get_unsigned_hash32(key, len(key), 0)
        elif is_py3():
            if isinstance(key, bytes):
                key = key.decode()
            return hash_f.get_unsigned_hash32(key, len(key), 0)
