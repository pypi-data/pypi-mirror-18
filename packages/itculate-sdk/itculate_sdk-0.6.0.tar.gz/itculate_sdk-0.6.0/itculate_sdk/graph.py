from .dictionary import Dictionary
from .utils import ReadOnlyDict, check_keys

_VERTEX_NAME_ATTR = "_name"
_VERTEX_TYPE_ATTR = "_type"
_VERTEX_KEYS_ATTR = "_keys"
_VERTEX_PRIMARY_KEY_ATTR = "_primary_key"


class Vertex(object):
    def __init__(self, vertex_type, name, keys, primary_key_id, data=None, **kwargs):
        """
        Defines a client-side vertex. This is basically a set of attributes (with special ones prefixed with '_').

        :param str vertex_type: Vertex type
        :param str primary_key_id: Name of key (within 'keys') designated as primary key (must be globally unique)
        :param dict keys: A set of unique keys identifying this vertex
        :param str name: Name for vertex
        :param dict data: Set of initial values to assign to vertex (optional)
        :param kwargs: Any additional key:value pairs that should be assigned to vertex.
        """
        assert vertex_type, "Type is mandatory"
        assert name, "Name is mandatory"

        check_keys(keys)
        assert primary_key_id, "primary_key_id is mandatory"
        assert primary_key_id in keys, "primary_key_id {} must point to a key in keys {}".format(primary_key_id, keys)

        if data is not None:
            assert isinstance(data, dict), "data must be of type dict"
            d = data

        else:
            d = {}

        # Add any keyword args to the dictionary
        if kwargs:
            d.update(kwargs)

        # Get the meta-data from each of the attributes
        for k, v in d.iteritems():
            stripped_value = Dictionary.update_and_strip(dictionary_type=Dictionary.D_TYPE_VERTEX,
                                                         vertex_type=vertex_type,
                                                         attribute=k,
                                                         value=v)
            d[k] = stripped_value

        # Add the essentials (to make sure they override everything)
        d.update({
            _VERTEX_TYPE_ATTR: vertex_type,
            _VERTEX_KEYS_ATTR: ReadOnlyDict(keys),
            _VERTEX_NAME_ATTR: name,
            _VERTEX_PRIMARY_KEY_ATTR: primary_key_id,
        })

        # Finally - update self and set the dirty flag (False as this is the initial setting)
        self._d = d

        self._frozen = False

    def freeze(self):
        # Make sure this vertex is now immutable!
        self._frozen = True
        return self

    @property
    def type(self):
        return self._d[_VERTEX_TYPE_ATTR]

    @property
    def name(self):
        return self._d[_VERTEX_NAME_ATTR]

    @name.setter
    def name(self, name):
        assert not self._frozen, "Vertex is frozen!"
        self[_VERTEX_NAME_ATTR] = name

    @property
    def keys(self):
        """
        :rtype: dict
        :return The vertex keys (DO NOT CHANGE - use add_key instead!!!)
        """
        return ReadOnlyDict(self._d[_VERTEX_KEYS_ATTR])

    @property
    def primary_key(self):
        return self.keys[self.primary_key_id]

    @property
    def primary_key_id(self):
        return self._d[_VERTEX_PRIMARY_KEY_ATTR]

    @property
    def document(self):
        """
        Provides access to internal document representing this vertex

        :rtype: dict[str, str]
        """
        return ReadOnlyDict(self._d)

    def update(self, d):
        """
        Override the default set to handle dirty flag

        :param dict[str, str] d: Dict to update with
        """
        assert not self._frozen, "Vertex is frozen!"
        assert isinstance(d, dict), "Expecting dict"
        assert _VERTEX_KEYS_ATTR not in d, "Cannot update keys!"
        self._d.update(d)

    def __setitem__(self, key, value):
        """
        Override the default set to handle dirty flag
        """
        assert not self._frozen, "Vertex is frozen!"
        assert not key.startswith("_"), "Cannot modify a special/internal attribute"
        self._d.__setitem__(key, value)

    def __getitem__(self, item):
        return self._d.__getitem__(item)

    def __delitem__(self, key):
        assert not key.startswith("_"), "Cannot delete a special/internal attribute"
        return self._d.__delitem__(key)

    def __contains__(self, item):
        return self._d.__contains__(item)

    def get(self, key, default=None):
        return self._d.get(key, default)

    def __cmp__(self, other):
        assert isinstance(other, Vertex), "Only Vertex comparisons are supported"
        return cmp(self._d, other._d)

    def __str__(self):
        return "Vertex ({}) {}: {}".format(self.type, self.name, self.keys)


_EDGE_TYPE_ATTR = "_type"
_EDGE_SOURCE_KEYS_ATTR = "_source_keys"
_EDGE_TARGET_KEYS_ATTR = "_target_keys"


class Edge(object):
    def __init__(self, edge_type, source_keys=None, source_vertex=None, target_keys=None, target_vertex=None):
        """
        :param str edge_type: Edge type
        :param dict[str, str] source_keys: Dictionary of source keys to point to a vertex (can be a partial set of keys)
        :param Vertex source_vertex: Alternative to source_keys - provide a vertex to take keys from
        :param dict[str, str] target_keys: Same as source_keys - but for target vertex
        :param Vertex target_vertex: Alternative to target_keys - provide a vertex to take keys from
        """

        if source_keys is not None:
            check_keys(source_keys)

        else:
            assert source_vertex is not None, "Must provide either source_keys or source_vertex"
            source_keys = source_vertex.keys

        if target_keys is not None:
            check_keys(target_keys)

        else:
            assert target_vertex is not None, "Must provide either source_keys or source_vertex"
            target_keys = target_vertex.keys

        assert source_keys != target_keys, "Source and target are the same (Edge cannot point to itself)"

        self._d = ReadOnlyDict({
            _EDGE_TYPE_ATTR: edge_type,
            _EDGE_SOURCE_KEYS_ATTR: source_keys,
            _EDGE_TARGET_KEYS_ATTR: target_keys,
        })

    def __str__(self):
        return "Edge {}: {} => {}".format(self.type, self.source_keys, self.target_keys)

    @property
    def type(self):
        """ :rtype: str """
        return self._d[_EDGE_TYPE_ATTR]

    @property
    def source_keys(self):
        """ :rtype: dict[str, str] """
        return self._d[_EDGE_SOURCE_KEYS_ATTR]

    @property
    def target_keys(self):
        """ :rtype: dict[str, str] """
        return self._d[_EDGE_TARGET_KEYS_ATTR]

    # noinspection PyProtectedMember
    def __cmp__(self, other):
        c = cmp(self.source_keys, other.source_keys)
        if c != 0:
            return c

        return cmp(self.target_keys, other.target_keys)

    @property
    def document(self):
        """
        :rtype: dict[str, str]
        :return: Document (Read-only) representing this edge
        """
        return self._d