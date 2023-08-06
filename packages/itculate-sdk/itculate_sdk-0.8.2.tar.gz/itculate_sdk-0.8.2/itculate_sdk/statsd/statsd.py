#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#


import random
from socket import socket, AF_INET, SOCK_DGRAM
import logging

from itculate_sdk import Vertex

logger = logging.getLogger(__name__)


def decrement(vertex, metric, delta=1, sample_rate=None):
    _client.decr(vertex, metric, delta, sample_rate)


def increment(vertex, metric, delta=1, sample_rate=None):
    _client.incr(vertex, metric, delta, sample_rate)


def gauge(vertex, metric, value, sample_rate=None):
    _client.gauge(vertex, metric, value, sample_rate)


def timing(vertex, metric, ms, sample_rate=None):
    _client.timing(vertex, metric, ms, sample_rate)


class ITculateStatsdClient(object):
    def __init__(self, host, port):
        self._agent = (host, port,)
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def decrement(self, vertex, metric, delta=1, sample_rate=None):
        value = str(-1 * delta).encode("utf8") + b"|c"
        self._send(vertex, metric, value, sample_rate)

    def increment(self, vertex, metric, delta=1, sample_rate=None):
        value = str(delta).encode("utf8") + b"|c"
        self._send(vertex, metric, value, sample_rate)

    def gauge(self, vertex, metric, value, sample_rate=None):
        str_value = str(value).encode("utf8") + b"|g"
        self._send(vertex, metric, str_value, sample_rate)

    def _send(self, vertex, metric, value, sample_rate=None):
        """

        :param str|Vertex vertex: Key / Vertex that this metric should be mapped to
        :param str metric: Name of counter
        :param str value: Encoded utf-8 str with value and type
        :param float sample_rate: Sample rate
        """
        try:
            metric = metric if isinstance(metric, bytes) else metric.encode("utf8")

            if sample_rate and 1.0 > sample_rate > 0:
                if random.random() <= sample_rate:
                    # Add rate to sample
                    value = value + b"|@" + str(sample_rate).encode("utf8")
                else:
                    # Skip sample!
                    return

            # Send the data
            if isinstance(vertex, Vertex):
                vertex = vertex.primary_key

            vertex_key = b"_it{%d:%s}|" % (len(vertex), vertex)
            self._socket.sendto(vertex_key + metric + b":" + value, self._agent)

        except:
            logger.exception("Failed to send to ITculate agent")

    def timing(self, bucket, ms, sample_rate=None):
        """Creates a timing sample.
        """
        value = str(ms).encode("utf8") + b"|ms"
        self._send(bucket, value, sample_rate)


def init(host="127.0.0.1", port=8125):
    global _client
    _client = ITculateStatsdClient(host=host, port=port)


_client = None