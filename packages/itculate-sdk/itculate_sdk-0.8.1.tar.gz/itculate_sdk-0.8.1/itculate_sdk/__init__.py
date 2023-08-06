#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#

__version__ = "0.8.1"

import logging
import collections
from .exceptions import SDKError
from .graph import Vertex, Edge
from .dictionary import Dictionary
from .sample import TimeSeriesSample
from .types import *
from .uploader import (
    Provider,
    TopologyPayloadGenerator,
    TimeSeriesPayloadGenerator,
    MappingsPayloadGenerator,
    DictionaryPayloadGenerator,
)
import statsd


logger = logging.getLogger(__name__)
_provider = None
_topologies = {}  # Topologies by collector_id
_timeseries = TimeSeriesPayloadGenerator()  # Need to keep track of only one timeseries
_dictionary = DictionaryPayloadGenerator()  # Need to keep track of only one timeseries
_mappings = MappingsPayloadGenerator()


class Flusher(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Make sure all changes are flushed
        flush_all()


def init(provider=None, host=None, **kwargs):
    """
    Initialize a global uploader that will be used to upload data to ITculate.

    The API key provided must have the 'upload' role (and associated with a single tenant).

    Possible providers are:
        'SynchronousApiUploader' (default) - Upload straight to the ITculate API server
        'AgentForwarder' - Forwards payload to an ITculate agent
        'InMemory' - Accumulates latest status in memory

    :param str provider: Name of the provider class to use (defaults to 'SynchronousApiUploader')
    :param str host: Identifier of host reporting (defaults to hostname)
    :param kwargs: Provider-specific settings

    :return A flusher instance (to be able to use with the 'with' statement)
    """

    provider = provider or "SynchronousApiUploader"

    if host is None:
        import socket
        host = socket.gethostname()

    provider_settings = {
        "provider": provider,
        "host": host,
    }

    provider_settings.update(kwargs)

    # Create the provider (will assert if provider not supported)
    global _provider
    _provider = Provider.factory(provider_settings)

    global _topologies
    _topologies = {}  # Topologies by collector_id

    global _timeseries
    _timeseries = TimeSeriesPayloadGenerator()  # Need to keep track of only one timeseries

    return Flusher()


def add_vertex(collector_id, vertex_type, name, keys, primary_key_id=None, data=None, **kwargs):
    """
    Adds a vertex to the uploader

    :param str collector_id: Unique name identifying the reporter of this topology
    :param str vertex_type: Vertex type
    :param str primary_key_id: Name of key (within 'keys') designated as primary key (must be globally unique)
    :param dict[str,str]|str keys: A set of unique keys identifying this vertex. If str, 'pk' will be used as key
    :param str name: Name for vertex
    :param dict data: Set of initial values to assign to vertex (optional)
    :param kwargs: Any additional key:value pairs that should be assigned to vertex.
    :rtype: Vertex
    """

    topology_provider = _topologies.get(collector_id)
    if topology_provider is None:
        topology_provider = TopologyPayloadGenerator(collector_id=collector_id)
        _topologies[collector_id] = topology_provider

    return topology_provider.add_vertex(vertex_type=vertex_type,
                                        name=name,
                                        keys=keys,
                                        primary_key_id=primary_key_id,
                                        data=data,
                                        **kwargs)


def connect(collector_id, source, target, topology):
    """
    Connect (create an edge between) two (or two sets of) vertices.
    Vertices are identified by either providing the Vertex object or only their keys.

    If source / target is a list of vertices (or keys), this will create a set of edges between all sources and all
    targets

    :param str collector_id: Unique name identifying the reporter of this topoology
    :param source: Identify source/s
    :type source: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
    :param target: Identify target/s
    :type target: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
    :param str topology: Topology (edge type) to use
    """

    topology_provider = _topologies.get(collector_id)
    if topology_provider is None:
        topology_provider = TopologyPayloadGenerator(collector_id=collector_id)
        _topologies[collector_id] = topology_provider

    topology_provider.connect(source=source, target=target, topology=topology)


def add_sample(vertex, counters, timestamp=None):
    """
    Add a time-series sample associated with a vertex or a key.

    :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
    :param dict[str, float] counters: Set of counter and values
    :param float timestamp: A unix timestamp (seconds since epoch). If None, current time is taken.
    """

    _timeseries.add_samples(vertex=vertex, samples=[(timestamp, counters)])


def add_samples(vertex, samples):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
    :param samples: A list of tuples, each containing timestamp and set of counters
    :type (float,dict[str,float])|list[(float,dict[str,float])] samples
    """

    _timeseries.add_samples(vertex=vertex, samples=samples)


def add_sample_for_non_vertex_keys(non_vertex_keys, timestamp, value, default_vertex_key=None):
    """
    Add a time-series sample associated with a vertex or a key.

    Timestamps are Unix timestamps (seconds (float) since epoch)

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map to vertex keys
    :param float timestamp: Unix timestamp (seconds since epoch)
    :param float|TypedValue value: Value to set
    :param str default_vertex_key: If provided, when lookup fails, the sample will be associated with this vertex

    :return: True if mapping found, False otherwise
    :rtype: bool
    """

    return add_samples_for_non_vertex_keys(non_vertex_keys=non_vertex_keys,
                                           samples=[(timestamp, value)],
                                           default_vertex_key=default_vertex_key)


def add_samples_for_non_vertex_keys(non_vertex_keys, samples, default_vertex_key=None):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param samples: Single or list of tuples (ts, value)
    :type samples: (float,float)|(float,TypedValue)|list
    :param str default_vertex_key: If provided, samples will associated with this vertex when lookup fails

    :return: True if mapping found, False otherwise
    :rtype: bool
    """

    vertex_counter_mappings = _mappings.lookup(non_vertex_keys, default_vertex_key=default_vertex_key)

    if vertex_counter_mappings:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Found mapping for '{}'".format(non_vertex_keys))

        ts_samples = []
        for timestamp, value in samples:
            for vertex_key, counter in vertex_counter_mappings:
                ts_samples.append(TimeSeriesSample(vertex=vertex_key,
                                                   timestamp=timestamp,
                                                   counters={counter: value}))

        if ts_samples:
            _timeseries.update(samples=ts_samples)
            return True

    return False


VertexCounterInfo = collections.namedtuple("VertexCounterInfo", ["vertex", "counter", "data_type"])
VertexCounterInfo.__new__.__defaults__ = (None, None)  # Set the default of the last two values to None


def map_counter(non_vertex_keys, vertex=None, counter=None, data_type=None, vertex_counters=None):
    """
    Map a set of non-vertex keys (like host, counter, tags from statsd) to a vertex + counter (with optional meta-data)
    or a list of such vertices.

    Using a list ('vertex_counters') allows to put a single counter on more than one vertex. This can be useful for
    different use cases, in particular in cluster situations when you might want to see the same counter at the cluster
    level AND at the individual node level.

    The 'vertex_counters' attribute is mutually exclusive with ('vertex', 'counter', 'data_type')

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param str counter: Name of counter write to in vertex
    :param DataType data_type: data type to use for this counter (this will automatically register in dictionary)
    :param Vertex|str vertex: Vertex object or vertex key to identify the vertex
    :param collections.Iterable[VertexCounterInfo] vertex_counters: Iterable over counter identifiers
    """

    if vertex_counters is None:
        vertex_counters = (VertexCounterInfo(vertex=vertex, counter=counter, data_type=data_type),)

    else:
        assert (vertex == counter == data_type == None), \
            "When 'vertex_counters' is provided, 'vertex', 'counter', 'data_type' should not be"

    _mappings.map_counter_to_vertices(non_vertex_keys=non_vertex_keys, vertex_counters=vertex_counters)


def flush_topology(collector_id):
    """
    Flush a topology collected by the given collector id

    :param collector_id:
    :return: True if any data was flushed
    :rtype: bool
    """
    assert collector_id in _topologies, "Collector ID '{}' not recognized".format(collector_id)

    topology_provider = _topologies[collector_id]
    return _provider.flush_now((topology_provider, _dictionary,)) > 0


def flush_timeseries():
    """
    Flush any collected timeseries data

    :return: True if any data was flushed
    :rtype: bool
    """
    return _provider.flush_now((_timeseries, _dictionary,)) > 0


def flush_mappings():
    """
    Flush mappings

    :return: True if any data was flushed
    :rtype: bool
    """
    return _provider.flush_now((_mappings,)) > 0


def flush_dictionary():
    """
    Flush dictionary

    :return: True if any data was flushed
    :rtype: bool
    """
    return _provider.flush_now((_dictionary,)) > 0


def flush_all():
    """
    Flushes all unsent data without waiting for the next interval
    :return: number of payloads flushed
    """

    def all_payload_providers():
        for topology_provider in _topologies.itervalues():
            yield topology_provider

        yield _dictionary
        yield _timeseries
        yield _mappings

    return _provider.flush_now(all_payload_providers())
