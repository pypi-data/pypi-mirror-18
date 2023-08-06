__version__ = "0.6.0"

import collections
from .connection import ApiConnection
from .exceptions import SDKError
from .graph import Vertex, Edge
from .dictionary import Dictionary
from .sample import TimeSeriesSample
from .types import *
from .uploader import Uploader


_uploader = None  # type: Uploader


def init(collector_id, api_key=None, api_secret=None, server_url=None):
    """
    Initialize a global uploader that will be used to upload data to ITculate.

    The API key provided must have the 'upload' role (and associated with a single tenant).

    :param str collector_id: A unique (for this tenant) collector ID to use to identify the reporter
    :param str api_key: API key to use, if None, will try to use from ~/.itculate/credentials, section [upload]
    :param str api_secret: API secret, if None, will try to use from ~/.itculate/credentials, section [upload]
    :param str server_url: URL to use as API server. If None, will go to api.itculate.io
    """
    global _uploader
    _uploader = Uploader(collector_id, api_key=api_key, api_secret=api_secret, server_url=server_url)


def add_vertex(vertex_type, name, keys, primary_key_id=None, data=None, **kwargs):
    """
    Adds a vertex to the uploader

    :param str vertex_type: Vertex type
    :param str primary_key_id: Name of key (within 'keys') designated as primary key (must be globally unique)
    :param dict[str, str] keys: A set of unique keys identifying this vertex
    :param str name: Name for vertex
    :param dict data: Set of initial values to assign to vertex (optional)
    :param kwargs: Any additional key:value pairs that should be assigned to vertex.
    :rtype: Vertex
    """
    primary_key_id = primary_key_id or keys.keys()[0]

    v = Vertex(vertex_type=vertex_type,
               name=name,
               keys=keys,
               primary_key_id=primary_key_id,
               data=data,
               **kwargs)

    _uploader.update(vertices=[v])

    return v


def connect(source, target, edge_type):
    """
    Connect (create an edge between) two (or two sets of) vertices.
    Vertices are identified by either providing the Vertex object or only their keys.

    If source / target is a list of vertices (or keys), this will create a set of edges between all sources and all
    targets

    :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] source: Identify source/s
    :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] target: Identify target/s
    :type edge_type: str
    """

    if isinstance(source, list):
        source_keys = source
    else:
        source_keys = [source]

    source_keys = [k if not isinstance(k, Vertex) else k.keys for k in source_keys]

    if isinstance(target, list):
        target_keys = target
    else:
        target_keys = [target]

        target_keys = [k if not isinstance(k, Vertex) else k.keys for k in target_keys]

    edges = []
    for sk in source_keys:
        for tk in target_keys:
            edges.append(Edge(edge_type=edge_type, source_keys=sk, target_keys=tk))

    _uploader.update(edges=edges)


def add_samples(vertex, samples, vertex_type=None):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
    :param samples: A single (or list of) tuples, each containing timestamp and set of counters
    :param str vertex_type: (optional) Vertex type (if vertex is a str) to enable dictionary reporting
    :type (float,dict[str,float])|list[(float,dict[str,float])] samples
    """

    if isinstance(vertex, Vertex):
        vertex, vertex_type = (vertex.primary_key, vertex.type)

    else:
        vertex_type = vertex_type

    samples_to_update = []
    for ts, counters in samples if isinstance(samples, list) else (samples,):
        s = TimeSeriesSample(counters=counters,
                             timestamp=ts,
                             vertex=vertex,
                             vertex_type=vertex_type)

        samples_to_update.append(s)

    _uploader.update(samples=samples_to_update)


def add_sample_for_non_vertex_keys(non_vertex_keys, samples):
    """
    Add a time-series sample associated with a vertex or a key. If a non

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param (float,float)|list[(float,float)] samples: Single or list of tuples (ts, value)

    :param float timestamp: Time (unix time - seconds since epoch) of sample
    :param float value: Value for sample

    :return: True if mapping found, False otherwise
    :rtype: bool
    """

    vertex_key, vertex_type, counter = _uploader.lookup(non_vertex_keys)

    if vertex_key is None:
        return False

    def get_sample(t):
        ts, value = t
        return TimeSeriesSample(counters={counter: value},
                                timestamp=ts,
                                vertex=vertex_key,
                                vertex_type=vertex_type)

    samples = map(get_sample, samples if isinstance(samples, list) else [samples])
    _uploader.update(samples=samples)


def map_counter(non_vertex_keys, vertex, counter, vertex_type=None, data_type=None):
    """
    Map a set of non-vertex keys (like host, counter, tags from statsd) to a vertex & counter, with optional meta-data

    :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map back to vertex keys
    :param str counter: Name of counter write to in vertex
    :param DataType data_type: data type to use for this counter (this will automatically register in dictionary)
    :param Vertex|str vertex: Vertex object or vertex key to identify the vertex
    :param str vertex_type: If vertex is a str, this complements the vertex type to be able to update dictionary
    """

    if isinstance(vertex, Vertex):
        vertex_key = vertex.primary_key
        vertex_type = vertex.type

    else:
        vertex_key = vertex
        vertex_type = vertex_type

    _uploader.create_mapping(non_vertex_keys=non_vertex_keys,
                             counter=counter,
                             vertex_key=vertex_key,
                             vertex_type=vertex_type,
                             data_type=data_type)


def flush():
    _uploader.flush()


def flush_and_join():
    return _uploader.flush_and_join()
