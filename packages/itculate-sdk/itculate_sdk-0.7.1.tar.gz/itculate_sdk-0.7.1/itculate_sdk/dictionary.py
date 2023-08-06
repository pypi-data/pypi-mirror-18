from collections import defaultdict

from .types import TypedValue


class Dictionary(object):
    D_TYPE_VERTEX = "vertex"
    D_TYPE_TIMESERIES = "timeseries"

    # Maintain a static version of the dictionary (so we don't keep on sending updates)
    dictionary = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    dictionary_changed = False

    @classmethod
    def reset_dictionary(cls):
        cls.dictionary = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        cls.dictionary_changed = False

    @classmethod
    def update_and_strip(cls, dictionary_type, vertex_type, attribute, value):
        """
        Updates the dictionary repository with new meta data, then return a simple value (instead of TypedValue object)

        :param str dictionary_type: Dictionary item type. Either "vertex" or "timeseries"
        :param str vertex_type: Vertex Type. If None, value will be stripped, but dictinoary not updated
        :param str attribute: Name of attribute
        :param value: Value of attribute (if TypedValue, this will be used to extract meta-data)

        :return: The plain value (stripped off TypedValue)
        """
        if isinstance(value, TypedValue):
            if vertex_type is not None:
                cls.update_data_type(dictionary_type=dictionary_type,
                                     vertex_type=vertex_type,
                                     attribute=attribute,
                                     data_type=value.data_type)

            value = value.value

        return value

    @classmethod
    def update_data_type(cls, dictionary_type, vertex_type, attribute, data_type):
        """
        Updates the dictionary repository with new meta data

        :param str dictionary_type: Dictionary item type. Either "vertex" or "timeseries"
        :param str vertex_type: Vertex Type. If None, value will be stripped, but dictinoary not updated
        :param str attribute: Name of attribute
        :param DataType data_type: data type to set

        :return: The plain value (stripped off TypedValue)
        """
        meta_data = data_type.meta_data
        current_meta_data = cls.dictionary[dictionary_type][vertex_type][attribute]

        if current_meta_data != meta_data:
            current_meta_data.update(meta_data)
            cls.dictionary_changed = True

    @classmethod
    def flush(cls):
        if cls.dictionary_changed:
            local_dictionary, cls.dictionary = \
                (cls.dictionary, defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

            cls.dictionary_changed = False

            return local_dictionary

        else:
            return None
