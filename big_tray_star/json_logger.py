# -*- coding: utf-8 -*-

import datetime
import logging
import sys

from pythonjsonlogger import jsonlogger


# https://github.com/madzak/python-json-logger#customizing-fields


class JsonFormatter(jsonlogger.JsonFormatter):

    def parse(self):
        """
        他に出したいフィールドがあったらこのリストに足す
        https://docs.python.jp/3/library/logging.html
        """
        return [
            'timestamp',
            'level',
            'name',
            'message',
            'stack_info',
        ]

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            now = dt_now_jst.strftime('%Y-%m-%dT%H:%M:%S%z')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


def get_logger(module_name):
    formatter = JsonFormatter(json_ensure_ascii=False)

    # INFO以下のログを標準出力する
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stdout_handler.setFormatter(formatter)

    # WARNING以上のログを標準エラー出力する
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    logger = logging.getLogger(module_name)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
    logger.setLevel(logging.DEBUG)
    return logger
