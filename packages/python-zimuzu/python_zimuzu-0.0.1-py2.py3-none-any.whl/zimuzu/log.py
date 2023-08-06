# -*- coding:utf-8 -*-
import logging

from colorlog import ColoredFormatter

__all__ = ['logger']

logger = logging.Logger('zimuzu', level=logging.WARNING)
# https://docs.python.org/3/library/logging.html#logrecord-attributes
fmt = ColoredFormatter('%(log_color)s%(asctime)s [%(levelname)s]: %(message)s', '%y/%m/%d %H:%M')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
logger.addHandler(sh)
