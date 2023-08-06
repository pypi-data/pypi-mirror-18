import requests
import logging
import time
from datetime import datetime
import socket

from py_zipkin.util import generate_random_64bit_string

class Zipkin(object):

    @classmethod
    def set_config(cls, cfg):
        Zipkin.cfg = cfg

    def __init__(self, service_name, span_name, trace_id=None, parent_id=None, is_sampled=False):
        if trace_id:
            self.trace_id = trace_id
        else:
            self.trace_id = generate_random_64bit_string()
        self.span_id = generate_random_64bit_string()
        self.parent_id = parent_id
        self.is_sampled = is_sampled
        self.flags = 0
        self.annotations = []
        self.binaryAnnotations = []
        self.service_name = service_name
        self.span_name = span_name
        start_time = datetime.now()
        self.timestamp = time.mktime(start_time.timetuple()) * 1000 * 1000 # micro seconds
        self.annotations.append({
            'endpoint': {
                'serviceName': self.service_name
            },
            'timestamp': self.timestamp,
            'value': 'sr'
        })

    def get_trace_id(self):
        return self.trace_id

    def get_span_id(self):
        return self.span_id

    def add_binary_annotation(self, key, value):
        if not key or not value:
            return
        self.binaryAnnotations.append({
            'key': key,
            'value': value
        })

    def add_send_annotation(self, endpoint, key=None, value=None):
        cur_time = datetime.now()
        timestamp = time.mktime(cur_time.timetuple()) * 1000 * 1000 # micro seconds
        self.annotations.append({
            'endpoint': {
                'serviceName': endpoint
            },
            'timestamp': timestamp,
            'value': 'cs'
        })
        if key and value:
            self.binaryAnnotations.append({
                'endpoint': {
                    'serviceName': endpoint
                },
                'key': key,
                'value': value
            })

    def add_receive_annotation(self, endpoint, key=None, value=None):
        cur_time = datetime.now()
        timestamp = time.mktime(cur_time.timetuple()) * 1000 * 1000 # micro seconds
        self.annotations.append({
            'endpoint': {
                'serviceName': endpoint
            },
            'timestamp': timestamp,
            'value': 'cr'
        })
        if key and value:
            self.binaryAnnotations.append({
                'endpoint': {
                    'serviceName': endpoint
                },
                'key': key,
                'value': value
            })

    def trace(self):
        if 'zipkin' not in Zipkin.cfg or 'url' not in Zipkin.cfg['zipkin'] or not Zipkin.cfg['zipkin']['url']:
            logging.warn('Zipkin not configured, skipping...')
            return
        end_time = datetime.now()
        end_timestamp = time.mktime(end_time.timetuple()) * 1000 * 1000 # micro seconds

        span = {
            'traceId': self.trace_id,
            'name': self.span_name,
            'parentId': self.parent_id,
            'id': self.span_id,
            'timestamp': self.timestamp,
            'duration': end_timestamp - self.timestamp,
            'debug': self.is_sampled,
            'annotations': self.annotations,
            'binaryAnnotations': self.binaryAnnotations
        }
        self.annotations.append({
                    'endpoint': {
                        'serviceName': self.service_name
                    },
                    'timestamp': end_timestamp,
                    'value': 'ss'
        })

        r = requests.post(Zipkin.cfg['zipkin']['url'] + '/api/v1/spans', json=[span])
        if not r.status_code == 202:
            logging.error('Failed to send span')
            logging.debug(r.status_code)
            return
        logging.debug(r.text)
