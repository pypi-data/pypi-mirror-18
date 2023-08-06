from unix_dates import UnixDate

from .graph import Vertex
from .dictionary import Dictionary
from .utils import check_key, ReadOnlyDict

_SAMPLE_KEY_ATTR = "_key"
_SAMPLE_TYPE_ATTR = "_type"
_SAMPLE_TYPE_TIMESTAMP = "_timestamp"
_SAMPLE_TYPE_COUNTERS = "_counters"


class TimeSeriesSample(object):
    def __init__(self, counters, timestamp=None, vertex=None, vertex_type=None):
        """
        the key should match one of the vertex keys
        :param str|Vertex vertex: Vertex (or key) to associate counters with
        :param str vertex_type: If vertex is a string, vertex_type is an optional attribute to use to update dictionary
        :param float timestamp: Unix timestamp (seconds since epoch) of sample. None will use current time
        :param dict[str, float] counters: Counters (name and value)
        """
        assert isinstance(counters, dict) and len(counters) > 0, "Counters are mandatory (non empty dict)"

        if isinstance(vertex, Vertex):
            key = vertex.primary_key
            vertex_type = vertex.type

        else:
            key = vertex
            check_key(key)

        if timestamp is None:
            timestamp = UnixDate.now()

        # Get the meta-data from each of the counters
        for k, v in counters.iteritems():
            stripped_value = Dictionary.update_and_strip(dictionary_type=Dictionary.D_TYPE_TIMESERIES,
                                                         vertex_type=vertex_type,
                                                         attribute=k,
                                                         value=v)

            counters[k] = stripped_value

        self._d = ReadOnlyDict({
            _SAMPLE_KEY_ATTR: key,
            _SAMPLE_TYPE_TIMESTAMP: timestamp,
            _SAMPLE_TYPE_COUNTERS: counters,
        })

    @property
    def key(self):
        """ :rtype: str """
        return self._d[_SAMPLE_KEY_ATTR]

    @property
    def type(self):
        """ :rtype: str """
        return self._d[_SAMPLE_TYPE_ATTR]

    @property
    def timestamp(self):
        """ :rtype: float """
        return self._d[_SAMPLE_TYPE_TIMESTAMP]

    @property
    def counters(self):
        """ :rtype: dict """
        return self._d[_SAMPLE_TYPE_COUNTERS]

    @property
    def document(self):
        """
        :rtype: dict[str, str]
        :return: Document (Read-only) representing this edge
        """
        return self._d

    def __str__(self):
        return "{} - {} - {}".format(self.timestamp, self.key, self.counters)

    def __isub__(self, other):
        """
        Subtract 'other' from self.

        This will only subtract values of counters - assuming everything matches
        """
        assert isinstance(other, TimeSeriesSample), "Only TimeSeriesSample object subtraction is supported"
        assert self.key == other.key, "Only samples with same key can be subtracted"
        assert self.type == other.type, "Only samples with same type can be subtracted"

        # Calculate the diff of all counters
        for key in self.counters.keys():
            self.counters[key] -= other.counters.get(key, 0)

        return self

    def __sub__(self, other):
        new_sample = TimeSeriesSample(key=self.key,
                                      vertex_type=self.type,
                                      timestamp=self.timestamp,
                                      counters=dict(self.counters))

        new_sample -= other

        return new_sample
