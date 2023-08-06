import pytest
from obpy import util

data_without_none = {
    'cities': 60,
    'countries': 20,
    'providers': 17,
    'stations': 6200
}

data_with_none = {
    'cities': 60,
    'countries': 20,
    'providers': 17,
    'stations': 6200,
    'noneKey': None
}


def test_data_is_a_dict():
    ''' Check returned data is a dict. '''
    data = util.remove_none_values_from_dict(data_without_none)
    assert type(data) == dict


def test_dict_has_no_none_values():
    ''' Check dict has not None values. '''
    data = util.remove_none_values_from_dict(data_without_none)
    for key, value in data.items():
        assert value is not None


def test_dict_has_none_values():
    ''' Check dict has None values. '''
    data = util.remove_none_values_from_dict(data_without_none)
    for key, value in data.items():
        if not value:
            assert value is None
