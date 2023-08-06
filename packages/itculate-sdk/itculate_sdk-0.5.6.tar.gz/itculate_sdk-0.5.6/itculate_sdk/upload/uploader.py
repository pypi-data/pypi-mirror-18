import re
# noinspection PyPackageRequirements
from unix_dates import UnixDate
from .. import __version__
from ..api import ApiConnection
from ..data_types import Vertex, Edge, TimeSeriesSample
from ..data_types.dictionary import Dictionary

_VALID_COLLECTOR_ID = re.compile(r"^[a-zA-Z0-9_]+$")


class Uploader(object):
    """
    Utility to easily upload data into ITculate.

    This will accumulate the different data reported and send it to the server in the background.
    """
    _vertices_by_pk = {}
    _edges = []
    _samples = []
    _dictionary = []
    _last_update_time = None

    def __init__(self, tenant_id, collector_id, host=None, api_key=None, api_secret=None, server_url=None):
        """
        Uploader

        :param str tenant_id: Tenant ID to report for (user must have permissions to access this tenant)
        :param str collector_id: Collector ID (unique within tenant) for this report
        :param str host: Information about the host reporting
        :param str api_key: (optional) API key to use (will use local_credentials otherwise)
        :param str api_secret:  (optional) API secret to use (will use local_credentials otherwise)
        :param str server_url: (optional) server URL to connect to (will default to api.itculate.io)
        """
        assert tenant_id and collector_id, "Tenant ID and collector ID are mandatory"

        self._tenant_id = tenant_id

        assert _VALID_COLLECTOR_ID.match(collector_id), "Invalid collector ID (must be [a-zA-Z0-9_]+)"
        self._collector_id = collector_id
        self._host = host

        # Create a connection with the 'upload' role
        self._connection = ApiConnection(api_key=api_key, api_secret=api_secret, role="upload", server_url=server_url)

    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def collector_id(self):
        return self._collector_id

    @property
    def host(self):
        return self._host

    def update(self, vertices=None, edges=None, samples=None):
        """
        :param collections.Iterable[Vertex] vertices: Collection of vertices
        :param collections.Iterable[Edge] edges: Collection of edges
        :param collections.Iterable[TimeSeriesSample] samples: Collection of samples
        """
        assert vertices or edges or samples, "No data provided"

        if vertices:
            self._vertices_by_pk.update({v.primary_key: v.freeze() for v in vertices})

        if edges:
            self._edges.extend(edges)

        if samples:
            self._samples.extend(samples)

        if Dictionary.dictionary_changed:
            self._dictionary = Dictionary.dictionary
            Dictionary.dictionary_changed = False

    def create_vertex(self, vertex_type, name, keys, primary_key_id=None, **kwargs):
        """
        Helper function to quickly get or create a vertex with the uploader

        :param vertex_type:
        :param name:
        :param keys:
        :param primary_key_id:
        :param kwargs:
        :return:
        """
        primary_key_id = primary_key_id or next(keys.iterkeys())
        primary_key = keys[primary_key_id]

        vertex = self._vertices_by_pk.get(primary_key)
        if vertex is None:
            vertex = Vertex(vertex_type=vertex_type,
                            name=name,
                            keys=keys,
                            primary_key_id=primary_key_id,
                            **kwargs)

            self._vertices_by_pk[primary_key] = vertex

        return vertex

    def connect(self, source_keys, target_keys, edge_type):
        """
        Helper function to quickly connect (create an edge) between groups of vertices (or set of keys).

        If lists are provided, this will create an edge between each source and all the targets.

        :type source_keys: dict|Vertex|list[dict]|list[Vertex]
        :type target_keys: dict|Vertex|list[dict]|list[Vertex]
        :type edge_type: str
        """
        source_keys = source_keys if isinstance(source_keys, list) else [source_keys]
        target_keys = target_keys if isinstance(target_keys, list) else [target_keys]

        # If from_keys or to_keys is a list of Vertex object, convert to keys
        source_keys = [k if not isinstance(k, Vertex) else k.keys for k in source_keys]
        target_keys = [k if not isinstance(k, Vertex) else k.keys for k in target_keys]

        for sks in source_keys:
            for tks in target_keys:
                self._edges.append(Edge(edge_type=edge_type, source_keys=sks, target_keys=tks))

    def add_samples(self, vertex_or_key, timestamp_and_counters_tuples=None, ):
        """
        Helper function to quickly add samples to the uploader

        :type vertex_or_key: str|Vertex
        :param timestamp_and_counters_tuples: collections.Iterable[(float,dict[str,float])]
        """
        key = vertex_or_key.primary_key if isinstance(vertex_or_key, Vertex) else vertex_or_key

        for timestamp, counters in timestamp_and_counters_tuples:
            ts = TimeSeriesSample(key=key,
                                  timestamp=timestamp,
                                  counters=counters)
            self._samples.append(ts)

    def upload(self):
        # Get local copies of anything accumulated to far and clean buffers (as atomic as possible)
        l_vertices_by_pk, l_edges, l_samples, l_dictionary = \
            (self._vertices_by_pk, self._edges, self._samples, self._dictionary)

        self._vertices_by_pk, self._edges, self._samples, self._dictionary = ({}, [], [], [],)
        self._last_update_time = UnixDate.now()

        if l_vertices_by_pk or l_edges or l_samples or l_dictionary:
            data = {
                "collector_id": self.collector_id,
                "collector_version": __version__,
                "host": self.host,
                "vertices": [v.document for v in l_vertices_by_pk.itervalues()],
                "edges": [e.document for e in l_edges],
                "samples": [s.document for s in l_samples],
                "dictionary": l_dictionary,
            }

            self._connection.post("tenants/{}/upload".format(self.tenant_id), json_obj=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.upload()
