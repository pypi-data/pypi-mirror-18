#
# (C) ITculate, Inc. 2015-2017
# All rights reserved
# Licensed under MIT License (see LICENSE)
#

import re


class ReadOnlyDict(dict):
    def __init__(self, dict_to_protect=None):
        super(ReadOnlyDict, self).__init__(dict_to_protect)

    def __setitem__(self, key, value):
        raise TypeError("__setitem__ is not permitted")

    def __delitem__(self, key):
        raise TypeError("__delitem__ is not permitted")

    def update(self, other=None, **kwargs):
        raise TypeError("update is not permitted")


def check_keys(keys, check_primary=False, primary_key_id=None):
    """
    Given a dict of keys, make sure they follow the required pattern and constraints

    :param dict[str, str] keys: Set of keys to check
    :param bool check_primary: If True, will check primary key
    :param str primary_key_id: Primary key to check
    """
    assert keys and isinstance(keys, dict) and len(keys) > 0, "Keys are mandatory (non empty dict)"

    # Make sure values are unique
    assert len(set(keys.viewvalues())) == len(keys), "Same value for more than one key"

    if check_primary:
        assert primary_key_id, "primary_key_id is mandatory"
        assert primary_key_id in keys, "primary_key_id {} must point to a key in keys {}".format(primary_key_id, keys)
