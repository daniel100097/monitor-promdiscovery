# -*- coding: utf-8 -*-
"""
    Copyright (C) 2019  Opsdis AB

    This file is part of monitor-exporter.

    monitor-promdiscovery is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    monitor-promdiscovery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with monitor-exporter.  If not, see <http://www.gnu.org/licenses/>.

"""

import logging
import datetime
from pythonjsonlogger import jsonlogger

logger = logging.getLogger('monitor-promdiscovery')


#def configure_logger(log_level="INFO", log_filename=None, format=None):
def configure_logger(config):
    format, log_filename, log_level = read_config(config)

    if format == "day" and log_filename:
        hdlr = logging.FileHandler(log_filename + '_{:%Y-%m-%d}.log'.format(datetime.datetime.now()))
    elif log_filename:
        hdlr = logging.FileHandler(log_filename + '.log')
    else:
        hdlr = logging.StreamHandler()

    formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')

    # formatter = logger.Formatter('%(asctime)s|%(levelname)s|%(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(log_level)


def read_config(config):
    log_filename = None
    format = None
    log_level = 'INFO'
    if 'logger' in config:
        if 'logfile' in config['logger']:
            log_filename = config['logger']['logfile']
        if 'format' in config['logger']:
            log_filename = config['logger']['format']
            format = config['logger']['format']
        if 'level' in config['logger']:
            log_filename = config['logger']['level']
            log_level = config['logger']['level']
    return format, log_filename, log_level


def error(message):
    logger.error('{}'.format(message))


def info(message, json_dict=None):
    if json_dict:
        logger.info('{}'.format(message), extra=json_dict)
    else:
        logger.info('{}'.format(message))


def info_response_time(message: str, r_time: float):
    response_time = {"response_time_seconds": r_time}
    logger.info('{}'.format(message), extra=response_time)


def warn(message):
    logger.warning('{}'.format(message))


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
