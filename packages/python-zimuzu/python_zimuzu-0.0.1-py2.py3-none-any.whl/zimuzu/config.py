# -*- coding:utf-8 -*-
import json
import os
import sys
from importlib import import_module

from .core import ZIMUZU
from .env import env
from .exception import APIInitFailed

DEFAULT_CONFIG = {
    'latest_id': 0,
    'plugin_path': [],
    'filters': {},
    'handlers': [
        {'class': 'handler.PPrintHandler'}
    ]
}


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s 似乎不是一个模块路径" % dotted_path
        raise ImportError(msg).with_traceback(sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = '模块 "%s" 没有定义 "%s" 属性/类' % (module_path, class_name)
        raise ImportError(msg).with_traceback(sys.exc_info()[2])


def initialize_obj(dict_conf, cls=None, args=None, kwargs=None):
    cls = cls or import_string(dict_conf['class'])
    args = args or dict_conf.get('args', tuple())
    kwargs = kwargs or dict_conf.get('kwargs', {})
    return cls(*args, **kwargs)


def dict_configure(config=None, default=DEFAULT_CONFIG):
    conf = {}
    conf.update(default)
    conf.update(config or {})

    # 初始化接口
    api_conf = conf.get('api')
    if api_conf:
        api = initialize_obj(api_conf, cls=ZIMUZU)
    else:
        api = env.get('api')
    if not api:
        raise APIInitFailed('API 初始化失败')

    # 注册插件路径
    for path in conf['plugin_path']:
        if os.path.isdir(path):
            sys.path.insert(0, path)
        else:
            raise ValueError('错误的插件导入路径')

    # 初始化过滤器
    filters = {}
    for key, c in conf['filters'].items():
        filter = initialize_obj(c)
        filters[key] = filter

    # 初始化处理器
    for c in conf['handlers']:
        hdlr = initialize_obj(c)
        filter_keys = c.get('filters', [])
        for key in filter_keys:
            hdlr.add_filter(filters[key])
        api.add_handler(hdlr)
    env['config'] = conf

    if not api.handlers:
        api.handlers = env['default_handlers']
    env['api'] = api
    return api


def export_config(fp, **kwargs):
    api = env['api']
    config = {}
    config.update(env['config'])
    config['latest_id'] = api.latest_id
    json.dump(config, fp, **kwargs)
