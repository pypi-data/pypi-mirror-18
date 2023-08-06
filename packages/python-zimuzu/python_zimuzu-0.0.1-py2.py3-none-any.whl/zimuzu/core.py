# -*- coding:utf-8 -*-
import json
import time
from hashlib import md5
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen

from .exception import RequestFailed
from .log import logger


class Filter(object):
    def filter(self, record):
        return True

    def __call__(self, record):
        return self.filter(record)


class Filterer(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        if not (filter in self.filters):
            self.filters.append(filter)

    def remove_filter(self, filter):
        if filter in self.filters:
            self.filters.remove(filter)

    def filter(self, record):
        rv = True
        for f in self.filters:
            if hasattr(f, 'filter'):
                result = f.filter(record)
            else:
                result = f(record)  # assume callable - will raise if not
            if not result:
                rv = False
                break
        return rv


class Handler(Filterer):
    def __init__(self):
        super(Handler, self).__init__()

        self._name = None

    def emit(self, record):
        raise NotImplementedError('emit 由 Handler 的子类实现')

    def handle(self, record):
        rv = self.filter(record)
        if rv:
            self.emit(record)
        return rv


class ZIMUZU(object):
    def __init__(self, cid, accesskey, host):
        super(ZIMUZU, self).__init__()
        self.cid = cid
        self.accesskey = accesskey
        self.host = host
        self.latest_id = '0'
        self.handlers = []

    def make_signature(self):
        timestamp = str(int(time.time() * 1000))
        s = ''.join([self.cid, '$$', self.accesskey, '&&', timestamp]).encode()
        md5sum = md5(s).hexdigest()
        return {'cid': self.cid, 'timestamp': timestamp, 'accesskey': md5sum}

    def request(self, path, data=None):
        data = data or {}
        sig = self.make_signature()
        data.update(sig)
        data = urlencode(data).encode()
        response = urlopen(urljoin(self.host, path), data=data)
        text = response.read().decode()
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            raise RequestFailed('响应解析失败: %s' % text)
        if result['status'] != 1:
            raise RequestFailed('接口权限验证错误: %d-%s', result['status'], result['info'])
        return result

    def task(self):
        logger.info('开始获取更新')
        data = self.request('/resource/today')
        handled = 0
        for record in data['data']:
            if record['id'] == self.latest_id:
                break
            self.handle(record)
            handled += 1

        if handled > 0:
            new_latest_id = data['data'][0]['id']
            logger.debug('最新资源ID更新: %s -> %s', self.latest_id, new_latest_id)
            self.latest_id = new_latest_id
        logger.info('更新了 %d 个资源', handled)

    def handle(self, record):
        found = 0
        for hdlr in self.handlers:
            found += 1
            hdlr.handle(record)

    def add_handler(self, hdlr):
        if not (hdlr in self.handlers):
            self.handlers.append(hdlr)

    def remove_handler(self, hdlr):
        if hdlr in self.handlers:
            self.handlers.remove(hdlr)
