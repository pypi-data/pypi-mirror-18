# -*- coding:utf-8 -*-
import re

from .core import Filter


class ReFilter(Filter):
    def __init__(self, **kwargs):
        self.patterns = kwargs

    def filter(self, record):
        for key, pattern in self.patterns.items():
            if not re.search(pattern, str(record[key])):
                return False
        return True
