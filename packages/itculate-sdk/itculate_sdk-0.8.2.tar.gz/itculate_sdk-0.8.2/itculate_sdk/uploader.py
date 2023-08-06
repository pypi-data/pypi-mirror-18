#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#

import logging
import re
import binascii
import itertools
from collections import defaultdict
from .graph import Vertex, Edge
from .sample import TimeSeriesSample
from .dictionary import Dictionary
from .local_credentials import read_local_credentials
from . import __version__

_VALID_COLLECTOR_ID = re.compile(r"^[a-zA-Z0-9_]+$")
_DEFAULT_API_URL = "https://api.itculate.io/api/v1"
_DEFAULT_PK = "pk"

logger = logging.getLogger(__name__)


class Payload(object):
    agent_api = None  # Indicates which agent API to call when forwarding this payload

    def __init__(self, collector_id, collector_version=None, **kwargs):
        assert _VALID_COLLECTOR_ID.match(collector_id), "Invalid collector ID (must be [a-zA-Z0-9_]+)"
        self._collector_id = collector_id
        self._collector_version = collector_version or __version__
        self._data = kwargs

    @classmethod
    def get_type(cls):
        return cls.__name__

    @property
    def collector_id(self):
        return self._collector_id

    @property
    def collector_version(self):
        return self._collector_version

    @property
    def data(self):
        return self._data


class TopologyPayload(Payload):
    agent_api = "upload"

    def __init__(self, collector_id, vertices, edges):
        super(TopologyPayload, self).__init__(collector_id, vertices=vertices, edges=edges)

    @property
    def vertices(self):
        return self.data["vertices"]

    @property
    def edges(self):
        return self.data["edges"]


class TimeseriesPayload(Payload):
    agent_api = "upload"

    def __init__(self, samples):
        # collector_id is meaningless with with timeseries reports (except for logging). Hard code to 'sdk'
        super(TimeseriesPayload, self).__init__("sdk", samples=samples)

    @property
    def samples(self):
        return self.data["samples"]


class DictionaryPayload(Payload):
    agent_api = "upload"

    def __init__(self, dictionary):
        super(DictionaryPayload, self).__init__("sdk", dictionary=dictionary)

    @property
    def dictionary(self):
        return self.data["dictionary"]


class MappingsPayload(Payload):
    agent_api = "mappings"

    def __init__(self, collector_id, mappings):
        super(MappingsPayload, self).__init__(collector_id, mappings=mappings)


class PayloadGenerator(object):
    def flush(self):
        """ :rtype: Payload """
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


class TopologyPayloadGenerator(PayloadGenerator):
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

        :param source: Identify source/s
        :type source: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
        :param target: Identify target/s
        :type target: str|dict|Vertex|collections.Iterable[dict]|collections.Iterable[Vertex]|collections.Iterable[str]
        :param str topology: Topology (edge type) to use for this connection
        """

        source = source if isinstance(source, list) else [source]
        target = target if isinstance(target, list) else [target]

        edges = []
        for sk, tk in itertools.product(source, target):
            if isinstance(sk, str):
                sk = {"pk": sk}

            if isinstance(tk, str):
                tk = {"pk": tk}

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

        if not local_vertices_by_pk and not local_edges:
            return None

        return TopologyPayload(collector_id=self._collector_id,
                               vertices=[v.document for v in local_vertices_by_pk.values()],
                               edges=[e.document for e in local_edges])


class TimeSeriesPayloadGenerator(PayloadGenerator):
    def __init__(self):
        self._samples = []

    def add_samples(self, vertex, samples):
        """
        Add a set of time-series samples associated with a vertex or a key.

        :param Vertex|str vertex: Vertex object or vertex key, if None, non_vertex_key will be used
        :param samples: A list of tuples, each containing timestamp and set of counters
        :type (float,dict[str,float])|list[(float,dict[str,float])] samples
        """

        if isinstance(vertex, Vertex):
            vertex = vertex.primary_key

        def create_sample((ts, counters)):
            return TimeSeriesSample(counters=counters, timestamp=ts, vertex=vertex)

        samples_to_update = itertools.imap(create_sample, samples if isinstance(samples, list) else (samples,))
        self.update(samples=samples_to_update)

    def update(self, samples):
        """
        Update with new samples.

        :param collections.Iterable[TimeSeriesSample] samples: Collection of samples
        """
        assert samples, "No data provided"
        self._samples.extend(samples)

    def flush(self):
        """
        Called is when the reported is ready to report the timeseries accumulated since last time.
        After this call, the internal state will be cleared (ready for building a new report).

        :return: A Payload object with the timeseries - ready to be uploaded
        :rtype: Payload
        """
        local_samples, self._samples = (self._samples, [])
        if not local_samples:
            return None

        return TimeseriesPayload(samples=[ts.document for ts in local_samples])


class DictionaryPayloadGenerator(PayloadGenerator):
    def flush(self):
        """
        Called is when the reported is ready to report the dictionary.

        The dictionary is a global data structure. It keeps on getting updated. Everytime there is a change, the entire
        dictionary will be sent (to avoid painful merges). We expect these updates to become less and less frequent
        since the dictionary is the meta-data of the different counters and attributes provided.

        :return: A Payload object with the dictionary - ready to be uploaded
        :rtype: DictionaryPayload
        """

        local_dictionary = Dictionary.flush()

        if not local_dictionary:
            return None

        # Send items as list of pairs (to avoid json serialization issues)
        return DictionaryPayload(dictionary=local_dictionary)


class MappingsPayloadGenerator(PayloadGenerator):
    def __init__(self):
        self.mappings = defaultdict(list)  # type: dict[unicode, tuple]
        self.mappings_changed = False

    def map_counter_to_vertices(self, non_vertex_keys, vertex_counters):
        """
        Allows mapping more than one vertex counter to a set of non-vertex-keys.

        This will replace any existing mapping for that set of non-vertex keys

        :param non_vertex_keys: Set of arbitrary values identifying this vertex (for mapping back to vertex)
        :type non_vertex_keys: tuple[str]|list[str]
        :param collections.Iterable[Vertex|str, str, DataType] vertex_counters: Iterable over counter identifiers
        """

        assert isinstance(non_vertex_keys, tuple), "'non_vertex_keys' must be a tuple"

        vertex_counter_identifiers = []

        for vertex, counter, data_type in vertex_counters:
            if isinstance(vertex, Vertex):
                vertex_key = vertex.primary_key

            else:
                vertex_key = vertex

            if data_type is not None:
                # Update dictionary with this type!
                Dictionary.update_data_type(dictionary_type=Dictionary.D_TYPE_TIMESERIES,
                                            vertex_key=vertex_key,
                                            attribute=counter,
                                            data_type=data_type)

            vertex_counter_identifiers.append((vertex_key, counter,))

            self.mappings[self.generate_key(non_vertex_keys)] = vertex_counter_identifiers
            self.mappings_changed = True

    def lookup(self, non_vertex_keys, default_vertex_key=None):
        """
        Convert a tuple of non-vertex keys to its associated vertex key

        :param non_vertex_keys: Set of arbitrary values identifying this vertex (for mapping back to vertex)
        :type non_vertex_keys: tuple[str]|list[str]
        :param str default_vertex_key: If provided, samples will associated with this vertex when lookup fails
        :rtype: (str, str)
        :return: tuple (vertex_key, counter) or (None, None) if no association found
        """
        assert isinstance(non_vertex_keys, (tuple, list)), "'non_vertex_keys' must be a tuple or list"

        key = self.generate_key(non_vertex_keys)
        mappings = self.mappings.get(key, (None, None,))

        if mappings is None and default_vertex_key is not None:
            # Lookup failed, map to the default vertex (keep vertex_type None - because there is no meta-data)
            # We will use the key as the counter name
            mappings = (default_vertex_key, key,)

        return mappings

    def flush(self):
        """
        Called is when the reported is ready to report the timeseries accumulated since last time.
        After this call, the internal state will be cleared (ready for building a new report).

        The mappings are kept in static memory for future calls.

        :return: A Payload object with the timeseries - ready to be uploaded
        :rtype: Payload
        """

        if not self.mappings_changed:
            return None

        local_mappings = self.mappings if self.mappings_changed else None
        self.mappings_changed = False

        # Send items as list of pairs (to avoid json serialization issues)
        return MappingsPayload(collector_id="sdk",  # Collector id is not critical with timeseries
                               mappings=local_mappings.items())

    @staticmethod
    def generate_key(non_vertex_keys):
        """
        Convert the set of keys to a string (sort them first) to allow consistent hashing

        :rtype: unicode
        """
        return unicode("|".join(sorted(non_vertex_keys)))


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

        self._name_to_payload_generator = {}

    @classmethod
    def factory(cls, settings):
        provider_class_name = settings.get("provider", "SynchronousApiUploader")
        assert provider_class_name in ProviderRegister.registry, \
            "provider can be one of {}".format(ProviderRegister.registry.keys())

        provider_class = ProviderRegister.registry[provider_class_name]
        return provider_class(settings)

    def handle_payload(self, payload):
        raise NotImplementedError()

    def flush_now(self, payload_generators):
        """
        Sends all unsent data without waiting

        :param: collections.Iterable[PayloadProvider]: iterable to allow us to get all payloads to flush
        :return: number of payloads flushed
        """
        count = 0

        for payload_generator in payload_generators:
            payload = payload_generator.flush()
            if payload is not None:
                self.handle_payload(payload)
                count += 1

        return count


class AgentForwarder(Provider):
    """
    Forward payloads over HTTP to the ITculate agent.

    This is typically used to forward topology, dictionary and mappings.

    Time series samples are typically forwarded using the 'statsd' protocol (via UDP) and the agent will use the
    mappings to convert these samples to ITculate time series sample objects.

    Expected settings:
        provider:               "AgentForwarder"
        host:                   (will default to hostname)
        server_url:             (defaults to 'http://127.0.0.1:8000/upload')
    """

    def __init__(self, settings):
        super(AgentForwarder, self).__init__(settings)
        self.server_url = settings.get("server_url", "http://127.0.0.1:8000")

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
            "collector_version": payload.collector_version,
            "host": self.host,
            "payload_type": payload.get_type(),
        }

        # Add the payload flat with the data (don't compress or pack)
        data_to_upload.update(payload.data)

        # Use the 'agent_api' attribute to figure out where to route this payload
        r = self.session.post("{}/{}".format(self.server_url, payload.agent_api), json=data_to_upload)
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
        https_proxy_url         (if applicable URL (including credentials) for HTTPS proxy)
        api_key:                (will try to use local credentials if not provided)
        api_secret:             (will try to use local credentials if not provided)
    """

    def __init__(self, settings):
        super(SynchronousApiUploader, self).__init__(settings)

        self.api_key = self.settings.get("api_key")
        self.api_secret = self.settings.get("api_secret")
        self.server_url = self.settings.get("server_url", _DEFAULT_API_URL)
        self.https_proxy_url = self.settings.get("https_proxy_url")

        if self.api_key is None or self.api_secret is None:
            # Read permissions from local file (under ~/.itculate/credentials)
            self.api_key, self.api_secret = read_local_credentials(role="upload")

        assert self.api_key and self.api_secret, \
            "API key/secret have to be provided (either in config or in local credentials file)"

    def handle_payload(self, payload):
        """
        Upload a payload to ITculate API

        :param Payload payload: payload to upload
        """

        # Don't upload the mappings to the API (these are needed only by the agent)
        if isinstance(payload, MappingsPayload):
            # TODO: Do we want to change the API to accept mappings as well?
            return

        # Only now import the requirements for sending data to the cloud
        import msgpack
        import zlib
        from .connection import ApiConnection
        connection = ApiConnection(api_key=self.api_key,
                                   api_secret=self.api_secret,
                                   server_url=self.server_url,
                                   https_proxy_url=self.https_proxy_url)

        data_to_upload = {
            "collector_id": payload.collector_id,
            "collector_version": __version__,
            "host": self.host,
            "compressed_payload": binascii.hexlify(zlib.compress(msgpack.dumps(payload.data))),
        }

        return connection.post("upload", json_obj=data_to_upload)


class InMemory(Provider):
    """
    Stores the latest payload (by collector) in memory for later retrieval (used by the agent).

    This provider keeps the latest topology by collector, the latest dictionary and an accumulated set of the
    samples.

    Expected settings:
        provider:               "StoreInMemory"
    """

    def __init__(self, settings):
        super(InMemory, self).__init__(settings)
        self._topology_by_collector_id = {}
        self._dictionary = {}
        self._samples = []

    def handle_payload(self, payload):
        """
        Sends (over TCP) the payload to the agent. This is supposed to end as quickly as possible and take as little
        overhead as possible from the client side

        :type payload: Payload
        """

        if isinstance(payload, TopologyPayload):
            # Update the latest version of the topology from this collector
            self._topology_by_collector_id[payload.collector_id] = (payload.vertices, payload.edges)

        elif isinstance(payload, TimeseriesPayload):
            self._samples.extend(payload.samples)

        elif isinstance(payload, DictionaryPayload):
            self._dictionary = payload.dictionary

        elif isinstance(payload, MappingsPayload):
            # Do nothing with mappings...
            pass

        else:
            assert "Unidentified payload '{}'".format(payload)

    def pop(self):
        """
        Gets (and removes) the data stored in memory

        :rtype: list[Payload]
        """

        # First move all data to local
        local_topology, self._topology_by_collector_id = self._topology_by_collector_id, {}
        local_dictionary, self._dictionary = self._dictionary, {}
        local_samples, self._samples = self._samples, []

        # Now generate the payloads needed to submit this report
        payloads = []
        for collector_id, (vertices, edges) in local_topology.iteritems():
            payloads.append(TopologyPayload(collector_id=collector_id, vertices=vertices, edges=edges))

        if local_dictionary:
            payloads.append(DictionaryPayload(dictionary=local_dictionary))

        if local_samples:
            payloads.append(TimeseriesPayload(samples=local_samples))

        return payloads
