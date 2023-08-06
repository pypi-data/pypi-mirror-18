def remove_none_values_from_dict(dict_obj):
    return dict((k, v) for k, v in dict_obj.items() if v)
