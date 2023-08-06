import logging
import re
import threading
from Queue import Queue, Empty
# noinspection PyPackageRequirements
import binascii
import msgpack
import zlib
from unix_dates import UnixDate
from .connection import ApiConnection
from .graph import Vertex, Edge
from .sample import TimeSeriesSample
from .dictionary import Dictionary
from .local_credentials import read_local_credentials
from . import __version__

_VALID_COLLECTOR_ID = re.compile(r"^[a-zA-Z0-9_]+$")

logger = logging.getLogger(__name__)


class Uploader(object):
    """
    Utility to easily upload data into ITculate.

    This will accumulate the different data reported and send it to the server in the background.
    """
    _vertices_by_pk = {}
    _edges = []
    _samples = []
    _dictionary = []
    _mappings = {}

    def __init__(self, collector_id, host=None, api_key=None, api_secret=None, server_url=None, flush_interval=300):
        """
        Uploader

        :param str collector_id: Collector ID (unique within tenant) for this report
        :param str host: Information about the host reporting
        :param str api_key: (optional) API key to use (will use local_credentials otherwise)
        :param str api_secret:  (optional) API secret to use (will use local_credentials otherwise)
        :param str server_url: (optional) server URL to connect to (will default to api.itculate.io)
        :param int flush_interval: Interval (seconds) between flushes (upload data to ITculate)
        """
        assert _VALID_COLLECTOR_ID.match(collector_id), "Invalid collector ID (must be [a-zA-Z0-9_]+)"
        self._collector_id = collector_id
        self._host = host

        if api_key is None or api_secret is None:
            # Read permissions from local file (under ~/.itculate/credentials)
            api_key, api_secret = read_local_credentials(role="upload")

        self._api_key = api_key

        self._upload_queue = Queue()

        self._uploader_thread = UploaderThread(collector_id=collector_id,
                                               host=host,
                                               api_key=api_key,
                                               api_secret=api_secret,
                                               server_url=server_url,
                                               flush_interval=flush_interval,
                                               queue=self._upload_queue)
        self._uploader_thread.start()

    @property
    def collector_id(self):
        return self._collector_id

    @property
    def api_key(self):
        return self._api_key

    @property
    def host(self):
        return self._host

    def update(self, vertices=None, edges=None, samples=None):
        """
        Update the uploader with new information.

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
            # Simply copy over the full dictionary (changes detection was already done - so we will not get redundant
            # updates)
            self._dictionary = Dictionary.dictionary
            Dictionary.dictionary_changed = False

    def create_mapping(self, non_vertex_keys, counter, vertex_key, vertex_type=None, data_type=None):
        """
        Map a set of non-vertex keys (like host, counter, tags from statsd) to a vertex & counter, with
        optional meta-data.

        :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex (for mapping back to vertex)
        :param str counter: Name of counter write to in vertex
        :param str vertex_key: Vertex key to identify the vertex
        :param str vertex_type: (optional) Vertex type to be able to update dictionary
        :param DataType data_type: data type to use for this counter (this will automatically register in dictionary)
        """
        assert isinstance(non_vertex_keys, tuple), "'non_vertex_keys' must be a tuple"

        if vertex_type is not None and data_type is not None:
            # Update dictionary with this type!
            Dictionary.update_data_type(dictionary_type=Dictionary.D_TYPE_TIMESERIES,
                                        vertex_type=vertex_type,
                                        attribute=counter,
                                        data_type=data_type)

        # Remember the mapping
        self._mappings[non_vertex_keys] = (vertex_key, vertex_type, counter)

    def lookup(self, non_vertex_keys):
        """
        Convert a tuple of non-vertex keys to its associated vertex key

        :param tuple[str] non_vertex_keys: Set of arbitrary values identifying this vertex (for mapping back to vertex)
        :rtype: (str, str, str)
        :return: tuple (vertex_key, vertex_type, counter) or (None, None, None) if no association found
        """
        assert isinstance(non_vertex_keys, tuple), "'non_vertex_keys' must be a tuple"
        return self._mappings.get(non_vertex_keys, (None, None, None))

    def flush(self):
        """
        Post accumulated data for sending (when the next send is scheduled to happen)
        """

        # Get local copies of anything accumulated to far and clean buffers (as atomic as possible)
        l_vertices_by_pk, l_edges, l_samples, l_dictionary = \
            (self._vertices_by_pk, self._edges, self._samples, self._dictionary)

        self._vertices_by_pk, self._edges, self._samples, self._dictionary = ({}, [], [], [],)

        if l_vertices_by_pk or l_edges or l_samples or l_dictionary:
            data = {
                "vertices": [v.document for v in l_vertices_by_pk.itervalues()],
                "edges": [e.document for e in l_edges],
                "samples": [s.document for s in l_samples],
                "dictionary": l_dictionary,
            }

            self._upload_queue.put(data)

    def join(self):
        self._uploader_thread.join()

    def flush_and_join(self):
        return self._uploader_thread.flush_and_join()


class UploaderThread(threading.Thread):
    def __init__(self, collector_id, host, queue, api_key, api_secret, server_url, flush_interval):
        super(UploaderThread, self).__init__()
        self.setDaemon(True)  # This will stop the thread when parent exits
        self.flush_interval = flush_interval
        self.collector_id = collector_id
        self.host = host
        self.api_key = api_key
        self.api_secret = api_secret
        self.server_url = server_url

        self.queue = queue  # type: Queue
        self.stop = False
        self.upload = True
        self.last_flush_successful = False

    def run(self):
        # Main loop
        next_flush = UnixDate.now() + self.flush_interval

        while not self.stop:
            try:
                # Accumulate data until it is time for next flush
                payload = {
                    "vertices": [],
                    "edges": [],
                    "samples": [],
                    "dictionary": {},
                }

                time_remaining = next_flush - UnixDate.now()

                while time_remaining > 0 and not self.stop:
                    try:
                        new_payload = self.queue.get(block=True, timeout=time_remaining)

                        if new_payload is not None:
                            payload["vertices"].extend(new_payload["vertices"])
                            payload["edges"].extend(new_payload["edges"])
                            payload["samples"].extend(new_payload["samples"])
                            payload["dictionary"].update(new_payload["dictionary"])

                    except Empty:
                        break

                    finally:
                        time_remaining = next_flush - UnixDate.now()

                if self.upload:
                    self.last_flush_successful = False

                    # It is time! Upload.
                    logger.debug("Uploading!")
                    connection = ApiConnection(api_key=self.api_key,
                                               api_secret=self.api_secret,
                                               server_url=self.server_url)

                    data = {
                        "collector_id": self.collector_id,
                        "collector_version": __version__,
                        "host": self.host,
                        # Use an optimized way to send the payload
                        "compressed_payload": binascii.hexlify(zlib.compress(msgpack.dumps(payload))),
                    }

                    connection.post("upload", json_obj=data)
                    self.last_flush_successful = True

            except Exception as e:
                logger.exception("Failed to upload data with {} ({})".format(repr(self), e.message))

            finally:
                next_flush = UnixDate.now() + self.flush_interval

        logger.warn("Uploader thread exited!")

    def flush_and_join(self):
        """
        Join, but block until all data is flushed
        :rtype: bool
        :return: True if data was flushed successfully, False otherwise
        """
        self.upload = True
        self.stop = True
        self.queue.put(None)  # Release any blocking on queue action

        super(UploaderThread, self).join(timeout=100)

        return self.last_flush_successful

    def join(self, timeout=None):
        self.upload = False  # Prevent next upload
        self.stop = True  # Signal main event loop to stop
        self.queue.put(None)  # Release any blocking on queue action

        super(UploaderThread, self).join(timeout=timeout)

    def __repr__(self):
        return "UploaderThread: {} [{}]".format(self.server_url, self.api_key)
