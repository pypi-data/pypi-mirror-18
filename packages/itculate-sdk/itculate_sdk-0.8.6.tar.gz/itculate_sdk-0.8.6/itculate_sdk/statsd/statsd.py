#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#


import random
from socket import socket, AF_INET, SOCK_DGRAM
import logging

import time

from itculate_sdk import Vertex

logger = logging.getLogger(__name__)
_client = None  # type: ITculateStatsdClient


def decrement(metric, delta=1, sample_rate=None, vertex=None):
    """
    Decrement a counter

    :param str metric: Name of counter
    :param int delta: Amount to decrement
    :param float sample_rate: (optional) between 0 and 1
    :param Vertex|str vertex: Key of vertex to associate counter with
    """
    _client.decrement(metric=metric, delta=delta, sample_rate=sample_rate, vertex=vertex)


def increment(metric, delta=1, sample_rate=None, vertex=None):
    """
    Increment a counter

    :param str metric: Name of counter
    :param int delta: Amount to increment
    :param float sample_rate: (optional) between 0 and 1
    :param Vertex|str vertex: Key of vertex to associate counter with
    """
    _client.increment(metric=metric, delta=int(delta), sample_rate=sample_rate, vertex=vertex)


def gauge(metric, value, sample_rate=None, vertex=None):
    """
    Report a gauge

    :param str metric: Name of counter
    :param int value: Value for gauge
    :param float sample_rate: (optional) between 0 and 1
    :param Vertex|str vertex: Key of vertex to associate counter with
    """
    _client.gauge(metric=metric, value=int(value), sample_rate=sample_rate, vertex=vertex)


def timing(metric, time_ms, sample_rate=None, vertex=None):
    _client.timing(metric=metric, time_ms=int(time_ms), sample_rate=sample_rate, vertex=vertex)


def set(metric, value, sample_rate=None, vertex=None):
    _client.set(metric=metric, value=value, sample_rate=sample_rate, vertex=vertex)


# noinspection PyPep8Naming
class time_and_count(object):
    """
    Convenience decorator to wrap a function and report the time it took + increment a metric when done
    """

    def __init__(self, time_metric, increment_metric_on_success=None, increment_metric_on_exception=None, vertex=None):
        self.vertex = vertex
        self.time_metric = time_metric
        self.increment_metric_on_success = increment_metric_on_success
        self.increment_metric_on_exception = increment_metric_on_exception

    def __call__(self, wrapped_func):
        def wrapped_f(*args, **kwargs):
            start = time.time() * 1000

            raised = False
            try:
                return wrapped_func(*args, **kwargs)

            except:
                raised = True
                raise

            finally:
                timing(vertex=self.vertex, metric=self.time_metric, time_ms=time.time() * 1000 - start)

                if raised and self.increment_metric_on_exception is not None:
                    increment(vertex=self.vertex, metric=self.increment_metric_on_exception)

                else:
                    increment(vertex=self.vertex, metric=self.increment_metric_on_success)

        return wrapped_f


class ITculateStatsdClient(object):
    def __init__(self, host, port):
        self._agent = (host, port,)
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def decrement(self, metric, delta=1, sample_rate=None, vertex=None):
        self._send_metric(vertex=vertex, metric=metric, value="{}|c".format(-delta), sample_rate=sample_rate)

    def increment(self, metric, delta=1, sample_rate=None, vertex=None):
        self._send_metric(vertex=vertex, metric=metric, value="{}|c".format(delta), sample_rate=sample_rate)

    def gauge(self, metric, value, sample_rate=None, vertex=None):
        self._send_metric(vertex=vertex, metric=metric, value="{}|g".format(value), sample_rate=sample_rate)

    def timing(self, metric, time_ms, sample_rate=None, vertex=None):
        self._send_metric(vertex=vertex, metric=metric, value="{}|ms".format(time_ms), sample_rate=sample_rate)

    def set(self, metric, value, sample_rate=None, vertex=None):
        self._send_metric(vertex=vertex, metric=metric, value="{}|s".format(value), sample_rate=sample_rate)

    def _send_metric(self, metric, value, sample_rate=None, vertex=None):
        """
        Sends a UDP datagram to the ITculate agent

        :param str|Vertex vertex: Key / Vertex that this metric should be mapped to
        :param str metric: Name of counter
        :param str value: Encoded utf-8 str with value and type
        :param float sample_rate: Sample rate
        """

        try:
            if sample_rate and 1.0 > sample_rate > 0:
                if random.random() <= sample_rate:
                    # Add rate to sample
                    value = "{}|@{}".format(value, sample_rate)
                else:
                    # Skip sample!
                    return

            if isinstance(metric, bytes):
                metric = metric.encode("utf-8")

            # Regular statsd
            statsd_packet = "{}:{}".format(metric, value)

            if vertex is not None:
                if isinstance(vertex, Vertex):
                    vertex = vertex.primary_key

                # Add our own secret sauce...
                statsd_packet = "_it{%s:%s}|%s" % (len(vertex), vertex, statsd_packet)

            # Finally, send the packet
            self._socket.sendto(statsd_packet, self._agent)

        except:
            # Log, but don't throw!
            logger.exception("Failed to send metric '{}' to ITculate agent".format(metric))


def init(host="127.0.0.1", port=8125):
    global _client
    _client = ITculateStatsdClient(host=host, port=port)
