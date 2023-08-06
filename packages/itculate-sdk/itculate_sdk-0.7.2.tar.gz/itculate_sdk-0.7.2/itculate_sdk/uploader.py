import logging
import re
import binascii
import itertools
# noinspection PyPackageRequirements
from unix_dates import UnixDate
from .graph import Vertex, Edge
from .sample import TimeSeriesSample
from .dictionary import Dictionary
from .local_credentials import read_local_credentials
from . import __version__

_VALID_COLLECTOR_ID = re.compile(r"^[a-zA-Z0-9_]+$")
_DEFAULT_API_URL = "https://api.itculate.io/api/v1"

logger = logging.getLogger(__name__)


class Payload(object):
    def __init__(self, collector_id, **kwargs):
        assert _VALID_COLLECTOR_ID.match(collector_id), "Invalid collector ID (must be [a-zA-Z0-9_]+)"
        self._collector_id = collector_id
        self._data = kwargs

    @property
    def collector_id(self):
        return self._collector_id

    @property
    def data(self):
        return self._data


class TopologyPayload(Payload):
    def __init__(self, collector_id, vertices, edges, dictionary):
        super(TopologyPayload, self).__init__(collector_id, vertices=vertices, edges=edges, dictionary=dictionary)


class TimeseriesPayload(Payload):
    def __init__(self, collector_id, samples, dictionary):
        super(TimeseriesPayload, self).__init__(collector_id, samples=samples, dictionary=dictionary)


class PayloadProvider(object):
    def flush(self):
        """ :rtype: Payload """
        raise NotImplementedError()


class Topology(PayloadProvider):
    def __init__(self, collector_id):
        """
        :param str collector_id: Unique (within tenant) name for this topology
        """
        assert collector_id, "Collector id must be provided"

        self._collector_id = collector_id
        self._vertices_by_pk = {}
        self._edges = []

    def __str__(self):
        return "{}-{}".format(self.__class__.__name__, self._collector_id)

    def add_vertex(self, vertex_type, name, keys, primary_key_id=None, data=None, **kwargs):
        """
        Adds a vertex to the topology

        :param str vertex_type: Vertex type
        :param str primary_key_id: Name of key (within 'keys') designated as primary key (must be globally unique)
        :param dict[str,str]|str keys: A set of unique keys identifying this vertex. If str, 'pk' will be used as key
        :param str name: Name for vertex
        :param dict data: Set of initial values to assign to vertex (optional)
        :param kwargs: Any additional key:value pairs that should be assigned to vertex.
        :rtype: Vertex
        """

        if isinstance(keys, str):
            assert primary_key_id is None or primary_key_id == "pk", \
                "Expecting primary_key_id to be None or 'pk' when providing keys as a str"
            keys = {"pk": keys}
            primary_key_id = "pk"

        else:
            primary_key_id = primary_key_id or keys.keys()[0]

        v = Vertex(vertex_type=vertex_type,
                   name=name,
                   keys=keys,
                   primary_key_id=primary_key_id,
                   data=data,
                   **kwargs)

        self.update(vertices=[v])

        return v

    def connect(self, source, target, topology):
        """
        Connect (create an edge between) two (or two sets of) vertices.
        Vertices are identified by either providing the Vertex object or only their keys.

        If source / target is a list of vertices (or keys), this will create a set of edges between all sources and all
        targets

        :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] source: Identify source/s
        :param dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex] target: Identify target/s
        :param str topology: Topology (edge type) to use for this connection
        """

        source = source if isinstance(source, list) else [source]
        target = target if isinstance(target, list) else [target]

        edges = []
        for sk, tk in itertools.product(source, target):
            edges.append(Edge(edge_type=topology, source=sk, target=tk))

        self.update(edges=edges)

    def update(self, vertices=None, edges=None):
        """
        Update the uploader with new information.

        :param collections.Iterable[Vertex] vertices: Collection of vertices
        :param collections.Iterable[Edge] edges: Collection of edges
        """
        assert vertices or edges, "No data provided"

        if vertices:
            self._vertices_by_pk.update({v.primary_key: v.freeze() for v in vertices})

        if edges:
            self._edges.extend(edges)

    def flush(self):
        """
        Called is when the builder of the topology is ready for it to be uploaded. All the vertices and edges are in
        and no further modifications are necessary.

        After this call, the internal state will be cleared (ready for building a new report).

        Be careful not to call flush unless the full data is populated. The ITculate server expects full reports to be
        made for the topology.

        :return: A Payload object with the topology - ready to be uploaded, None if nothing to flush
        :rtype: Payload
        """
        local_vertices_by_pk, self._vertices_by_pk = (self._vertices_by_pk, {})
        local_edges, self._edges = (self._edges, [])
        local_dictionary = Dictionary.flush()

        if not local_vertices_by_pk and not local_edges and not local_dictionary:
            return None

        return TopologyPayload(collector_id=self._collector_id,
                               vertices=[v.document for v in local_vertices_by_pk.values()],
                               edges=[e.document for e in local_edges],
                               dictionary=local_dictionary)


class TimeSeries(PayloadProvider):
    mappings = {}

    def __init__(self):
        self._samples = []

    def __str__(self):
        return self.__class__.__name__

    def add_sample(self, vertex, counters, timestamp=None, vertex_type=None):
        """
        Add a time-series sample associated with a vertex or a key.

        :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
        :param dict[str, float] counters: Set of counter and values
        :param float timestamp: A unix timestamp (seconds since epoch). If None, current time is taken.
        :param str vertex_type: (optional) Vertex type (if vertex is a str) to enable dictionary reporting
        """

        if isinstance(vertex, Vertex):
            vertex, vertex_type = (vertex.primary_key, vertex.type)

        else:
            vertex_type = vertex_type

        s = TimeSeriesSample(counters=counters,
                             timestamp=timestamp or UnixDate.now(),
                             vertex=vertex,
                             vertex_type=vertex_type)

        self.update(samples=[s])

    def add_samples(self, vertex, samples, vertex_type=None):
        """
        Add a set of time-series samples associated with a vertex or a key.

        :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
        :param samples: A list of tuples, each containing timestamp and set of counters
        :type (float,dict[str,float])|list[(float,dict[str,float])] samples
        :param str vertex_type: (optional) Vertex type (if vertex is a str) to enable dictionary reporting
        """

        if isinstance(vertex, Vertex):
            vertex, vertex_type = (vertex.primary_key, vertex.type)

        else:
            vertex_type = vertex_type

        def create_sample((ts, counters)):
            return TimeSeriesSample(counters=counters,
                                    timestamp=ts,
                                    vertex=vertex,
                                    vertex_type=vertex_type)

        samples_to_update = map(create_sample, samples if isinstance(samples, list) else (samples,))
        self.update(samples=samples_to_update)

    def add_sample_for_non_vertex_keys(self, non_vertex_keys, timestamp, value):
        """
        Add a time-series sample associated with a vertex or a key.

        Timestamps are Unix timestamps (seconds (float) since epoch)

        :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map to vertex keys
        :param float timestamp: Unix timestamp (seconds since epoch)
        :param float value: Value to set

        :return: True if mapping found, False otherwise
        :rtype: bool
        """

        vertex_key, vertex_type, counter = self.lookup(non_vertex_keys)
        if vertex_key is None:
            return False

        t = TimeSeriesSample(counters={counter: value},
                             timestamp=timestamp,
                             vertex=vertex_key,
                             vertex_type=vertex_type)
        self.update(samples=[t])
        return True

    def add_samples_for_non_vertex_keys(self, non_vertex_keys, samples):
        """
        Add a time-series sample associated with a vertex or a key.

        Timestamps are Unix timestamps (seconds (float) since epoch)

        :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex. Used to map to vertex keys
        :param (float,float)|list[(float,float)] samples: Single or list of tuples (ts, value)

        :return: True if mapping found, False otherwise
        :rtype: bool
        """

        vertex_key, vertex_type, counter = self.lookup(non_vertex_keys)

        if vertex_key is None:
            return False

        def get_sample(t):
            ts, value = t
            return TimeSeriesSample(counters={counter: value},
                                    timestamp=ts,
                                    vertex=vertex_key,
                                    vertex_type=vertex_type)

        samples = map(get_sample, samples if isinstance(samples, list) else [samples])
        self.update(samples=samples)
        return True

    def update(self, samples):
        """
        Update with new samples.

        :param collections.Iterable[TimeSeriesSample] samples: Collection of samples
        """
        assert samples, "No data provided"
        self._samples.extend(samples)

    def map_counter(self, non_vertex_keys, vertex, counter, vertex_type=None, data_type=None):
        """
        Map a set of non-vertex keys (like host, counter, tags from statsd) to a vertex & counter, with optional
        meta-data

        :param tuple[str] non_vertex_keys: Set of values identifying this vertex. Used to map back to vertex keys
        :param str counter: Name of counter write to in vertex
        :param DataType data_type: data type to use for this counter (this will automatically register in dictionary)
        :param Vertex|str vertex: Vertex object or vertex key to identify the vertex
        :param str vertex_type: If vertex is a str, this complements the vertex type to be able to update dictionary
        """

        assert isinstance(non_vertex_keys, tuple), "'non_vertex_keys' must be a tuple"

        if isinstance(vertex, Vertex):
            vertex_key = vertex.primary_key
            vertex_type = vertex.type

        else:
            vertex_key = vertex
            vertex_type = vertex_type

        if vertex_type is not None and data_type is not None:
            # Update dictionary with this type!
            Dictionary.update_data_type(dictionary_type=Dictionary.D_TYPE_TIMESERIES,
                                        vertex_type=vertex_type,
                                        attribute=counter,
                                        data_type=data_type)

        self.mappings[non_vertex_keys] = (vertex_key, vertex_type, counter)

    def lookup(self, non_vertex_keys):
        """
        Convert a tuple of non-vertex keys to its associated vertex key

        :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex (for mapping back to vertex)
        :rtype: (str, str, str)
        :return: tuple (vertex_key, vertex_type, counter) or (None, None, None) if no association found
        """
        assert isinstance(non_vertex_keys, tuple), "'non_vertex_keys' must be a tuple"
        return self.mappings.get(non_vertex_keys, (None, None, None))

    def flush(self):
        """
        Called is when the reported is ready to report the timeseries accumulated since last time.
        After this call, the internal state will be cleared (ready for building a new report).

        The mappings are kept in static memory for future calls.

        :return: A Payload object with the timeseries - ready to be uploaded
        :rtype: Payload
        """
        local_samples, self._samples = (self._samples, [])
        local_dictionary = Dictionary.flush()

        if not local_samples and not local_dictionary:
            return None

        return TimeseriesPayload(collector_id="sdk_timeseries",  # Collector id is not critical with timeseries
                                 samples=[ts.document for ts in local_samples],
                                 dictionary=local_dictionary)


class ProviderRegister(type):
    registry = {}

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)

        if name != "Provider":
            mcs.registry[name] = new_cls

        return new_cls


class Provider(object):
    __metaclass__ = ProviderRegister

    def __init__(self, settings):
        self.settings = settings
        self.host = settings.get("host")

        self._name_to_payload_provider = {}

    @classmethod
    def factory(cls, settings):
        provider_class_name = settings.get("provider", "SynchronousApiUploader")
        assert provider_class_name in ProviderRegister.registry, \
            "provider can be one of {}".format(ProviderRegister.registry.keys())

        provider_class = ProviderRegister.registry[provider_class_name]
        return provider_class(settings)

    def handle_payload(self, payload):
        raise NotImplementedError()

    def flush_now(self, payload_providers):
        """
        Sends all unsent data without waiting

        :param: collections.Iterable[PayloadProvider]: iterable to allow us to get all payloads to flush
        :return: number of payloads flushed
        """
        count = 0

        for payload_provider in payload_providers:
            payload = payload_provider.flush()
            if payload is not None:
                self.handle_payload(payload)
                count += 1

        return count


class AgentForwarder(Provider):
    """
    Forward payloads to the ITculate agent.
    Typically, time series samples are forwarded using the statsd agent, and topology payloads are forwarded manually.

    Expected settings:
        provider:               "AgentForwarder"
        host:                   (will default to hostname)
        server_url:             (defaults to 'http://127.0.0.1:8000/upload')
    """

    def __init__(self, settings):
        super(AgentForwarder, self).__init__(settings)
        self.server_url = settings.get("server_url", "http://127.0.0.1:8000/upload")

        import requests
        self.session = requests.session()
        self.session.verify = True
        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Accept"] = "application/json"

    def handle_payload(self, payload):
        """
        Sends (over TCP) the payload to the agent. This is supposed to end as quickly as possible and take as little
        overhead as possible from the client side

        :type payload: Payload
        """
        data_to_upload = {
            "collector_id": payload.collector_id,
            "collector_version": __version__,
            "host": self.host,
        }

        # Add the payload flat with the data (don't compress or pack)
        data_to_upload.update(payload.data)

        r = self.session.post(self.server_url, json=data_to_upload)
        r.raise_for_status()

        return r.json()


class SynchronousApiUploader(Provider):
    """
    Upload a payload to an ITculate REST API server.
    This is used to upload immediately the payload. For better performance, use the ITculate agent instead.

    Expected settings:
        provider:               "SynchronousApiUploader"
        host:                   (will default to hostname)
        server_url:             (will default to public REST API)
        api_key:                (will try to use local credentials if not provided)
        api_secret:             (will try to use local credentials if not provided)
    """

    def __init__(self, settings):
        super(SynchronousApiUploader, self).__init__(settings)

        self.api_key = self.settings.get("api_key")
        self.api_secret = self.settings.get("api_secret")
        self.server_url = self.settings.get("server_url", _DEFAULT_API_URL)

        if self.api_key is None or self.api_secret is None:
            # Read permissions from local file (under ~/.itculate/credentials)
            self.api_key, self.api_secret = read_local_credentials(role="upload")

        assert self.api_key and self.api_secret, "API key/secret have to be provided!"

    def handle_payload(self, payload):
        """
        Upload a payload to ITculate API

        :param Payload payload: payload to upload
        """

        # Only now import the requirements for sending data to the cloud
        import msgpack
        import zlib
        from .connection import ApiConnection
        connection = ApiConnection(api_key=self.api_key, api_secret=self.api_secret, server_url=self.server_url)

        data_to_upload = {
            "collector_id": payload.collector_id,
            "collector_version": __version__,
            "host": self.host,
            "compressed_payload": binascii.hexlify(zlib.compress(msgpack.dumps(payload.data))),
        }

        return connection.post("upload", json_obj=data_to_upload)
