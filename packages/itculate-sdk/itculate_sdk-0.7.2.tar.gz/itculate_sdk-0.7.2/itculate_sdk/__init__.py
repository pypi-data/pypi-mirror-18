__version__ = "0.7.2"

import collections
import socket
from .exceptions import SDKError
from .graph import Vertex, Edge
from .dictionary import Dictionary
from .sample import TimeSeriesSample
from .types import *
from .uploader import Topology, TimeSeries, Provider

_provider = None  # type: Provider
_topologies = {}  # Topologies by collector_id
_timeseries = TimeSeries()  # Need to keep track of only one timeseries


def init(provider=None, host=None, **kwargs):
    """
    Initialize a global uploader that will be used to upload data to ITculate.

    The API key provided must have the 'upload' role (and associated with a single tenant).

    :param str provider: Name of the provider class to use (defaults to 'SynchronousApiUploader')
    :param str host: Identifier of host reporting (defaults to hostname)
    :param kwargs: Provider-specific settings
    """

    provider = provider or "SynchronousApiUploader"
    host = host or socket.gethostname()

    provider_settings = {
        "provider": provider,
        "host": host,
    }

    provider_settings.update(kwargs)

    # Create the provider
    global _provider
    _provider = Provider.factory(provider_settings)

    global _topologies
    _topologies = {}  # Topologies by collector_id

    global _timeseries
    _timeseries = TimeSeries()  # Need to keep track of only one timeseries


def add_vertex(collector_id, vertex_type, name, keys, primary_key_id=None, data=None, **kwargs):
    """
    Adds a vertex to the uploader

    :param str collector_id: Unique name identifying the reporter of this topoology
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
        topology_provider = Topology(collector_id=collector_id)
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
    :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] source: Identify source/s
    :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] target: Identify target/s
    :param str topology: Topology (edge type) to use
    """

    topology_provider = _topologies.get(collector_id)
    if topology_provider is None:
        topology_provider = Topology(collector_id=collector_id)
        _topologies[collector_id] = topology_provider

    topology_provider.connect(source=source, target=target, topology=topology)


def add_sample(vertex, counters, timestamp=None, vertex_type=None):
    """
    Add a time-series sample associated with a vertex or a key.

    :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
    :param dict[str, float] counters: Set of counter and values
    :param float timestamp: A unix timestamp (seconds since epoch). If None, current time is taken.
    :param str vertex_type: (optional) Vertex type (if vertex is a str) to enable dictionary reporting
    """

    _timeseries.add_sample(vertex=vertex, counters=counters, timestamp=timestamp, vertex_type=vertex_type)


def add_samples(vertex, samples, vertex_type=None):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
    :param samples: A list of tuples, each containing timestamp and set of counters
    :type (float,dict[str,float])|list[(float,dict[str,float])] samples
    :param str vertex_type: (optional) Vertex type (if vertex is a str) to enable dictionary reporting
    """

    _timeseries.add_samples(vertex=vertex, samples=samples, vertex_type=vertex_type)


def add_sample_for_non_vertex_keys(non_vertex_keys, timestamp, value):
    """
    Add a time-series sample associated with a vertex or a key.

    Timestamps are Unix timestamps (seconds (float) since epoch)

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map to vertex keys
    :param float timestamp: Unix timestamp (seconds since epoch)
    :param float value: Value to set

    :return: True if mapping found, False otherwise
    :rtype: bool
    """

    return _timeseries.add_sample_for_non_vertex_keys(non_vertex_keys=non_vertex_keys, timestamp=timestamp, value=value)


def add_samples_for_non_vertex_keys(non_vertex_keys, samples):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param (float,float)|list[(float,float)] samples: Single or list of tuples (ts, value)

    :return: True if mapping found, False otherwise
    :rtype: bool
    """

    return _timeseries.add_samples_for_non_vertex_keys(non_vertex_keys=non_vertex_keys, samples=samples)


def map_counter(non_vertex_keys, vertex, counter, vertex_type=None, data_type=None):
    """
    Map a set of non-vertex keys (like host, counter, tags from statsd) to a vertex & counter, with optional meta-data

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param str counter: Name of counter write to in vertex
    :param DataType data_type: data type to use for this counter (this will automatically register in dictionary)
    :param Vertex|str vertex: Vertex object or vertex key to identify the vertex
    :param str vertex_type: If vertex is a str, this complements the vertex type to be able to update dictionary
    """

    _timeseries.map_counter(non_vertex_keys=non_vertex_keys,
                            vertex=vertex,
                            counter=counter,
                            vertex_type=vertex_type,
                            data_type=data_type)


def flush_collector_id(collector_id):
    """
    Flush a topology collected by the given collector id

    :param collector_id:
    :return: True if any data was flushed
    :rtype: bool
    """
    assert collector_id in _topologies, "Collector ID '{}' not recognized".format(collector_id)

    topology_provider = _topologies[collector_id]
    return _provider.flush_now((topology_provider,)) > 0


def flush_timeseries():
    """
    Flush any collected timeseries data

    :return: True if any data was flushed
    :rtype: bool
    """
    return _provider.flush_now((_timeseries,)) > 0


def flush_all():
    """
    Flushes all unsent data without waiting for the next interval
    :return: number of payloads flushed
    """

    def all_payload_providers():
        for topology_provider in _topologies.itervalues():
            yield topology_provider

        yield _timeseries

    return _provider.flush_now(all_payload_providers())
