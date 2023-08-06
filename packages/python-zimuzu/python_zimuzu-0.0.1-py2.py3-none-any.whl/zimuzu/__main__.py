# -*- coding:utf-8 -*-
import os
import sys

if not __package__:
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from zimuzu.command import cli  # noqa

if __name__ == '__main__':
    cli()
