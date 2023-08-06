# -*- coding:utf-8 -*-
import json
import logging
import time
from pprint import pformat

import click
import schedule

from zimuzu.core import ZIMUZU
from .config import dict_configure
from .env import env
from .exception import APIInitFailed
from .log import logger


def echo(message, *args, **style):
    message = str(message)
    if args:
        click.echo(click.style(message % args, **style))
    else:
        click.echo(click.style(message, **style))


def echo_info(message, *args, **style):
    echo(message, *args, fg='green', **style)


def echo_warning(message, *args, **style):
    echo(message, *args, fg='yellow', **style)


def echo_error(message, *args, **style):
    echo(message, *args, fg='red', **style)


@click.group()
@click.option('-c', '--config', type=click.File(), help='配置文件路径')
@click.option('--cid', type=click.STRING, help='cid')
@click.option('--key', type=click.STRING, help='accesskey')
@click.option('--host', type=click.STRING, help='accesskey')
@click.option('-v', '--verbose', count=True, help='显示更多信息', callback=lambda ctx, param, value: min(value, 2))
def cli(config, cid, key, host, verbose):
    """
    字幕组网站(www.zimuzu.tv)接口
    """
    if verbose == 1:
        logger.setLevel(logging.INFO)
        logger.info('日志级别设为 INFO')
    elif verbose == 2:
        logger.setLevel(logging.DEBUG)
        logger.info('日志级别设为 DEBUG')

    input_required = False
    config_dict = {}
    if config:
        config_dict = json.load(config)
        try:
            dict_configure(config_dict)
        except APIInitFailed:
            input_required = True
    else:
        input_required = True
    if input_required:
        if cid and key and host:
            api = ZIMUZU(cid, key, host)
            env['api'] = api
            dict_configure(config_dict)
        else:
            cid = click.prompt('CID', cid)
            key = click.prompt('ACCESSKEY', key)
            host = click.prompt('HOST', host)
            api = ZIMUZU(cid, key, host)
            env['api'] = api
            dict_configure(config_dict)


def split_opts(ctx, param, value):
    data = {}
    for v in value:
        kv = v.split('=', 1)
        if len(kv) != 2:
            raise click.BadParameter('表单参数为"key=value"的形式')
        data[kv[0]] = kv[1]
    return data


@cli.command()
@click.argument('path')
@click.option('-f', '--form', multiple=True, help='额外的请求参数,为"key=value"的形式', callback=split_opts)
def api(path, form):
    """
    请求字幕组网站接口
    """
    api = env['api']
    echo_info(pformat(api.request(path, form)))


@cli.command()
@click.option('-p', '--period', type=click.IntRange(1, 24 * 60 - 1), default=5, help='额外的请求参数,为"key=value"的形式')
def daemon(period):
    """
    字幕组网站资源后台更新后台服务
    """
    # 零点之前更新一次避免跳过任务
    api = env['api']
    logger.info('资源更新任务每 %d 分钟执行一次', period)
    schedule.every().day.at('23:59').do(api.task)
    schedule.every(period).minutes.do(api.task)
    while True:
        schedule.run_pending()
        time.sleep(1)
