import os
import json

class FacebookException(Exception):

    """
    A custom Facebook Exception class

    """

    def __init__(self, message, code=None):
        custom_message = "Facebook API Error: " + message
        if code:
            custom_message += "\nError Code: " + str(code)

        Exception.__init__(self, custom_message)

def first_item(list_or_dict):
    """
    If passed a list, this returns the first item of the list.
    If passed a dict, this returns the value of the first key of the dict.

    :param < list | dict > list_or_dict: A list or a dict.
    :rtype obj: The first item of the list, or the first value of the dict
    """
    if isinstance(list_or_dict, list):
        return next(iter(list_or_dict), None)
    elif isinstance(list_or_dict, dict):
        return next(iter(list_or_dict.values()), None)
    else:
        raise Exception("Must pass a list or a dict to first_item")


def delete_shelf_files(filename):
    """
    Delete the shelf dumbdbm files if they exist.

    """
    shelf_extensions = ['.bak', '.dat', '.dir']
    for ext in shelf_extensions:
        try:
            os.remove(filename + ext)
        except OSError:
            pass


def json_to_objects(list_or_dict, model):
    """
    Translates a list or a dict of json objects into a list or a dict of TinyModel objects
    :param < list | dict > list_or_dict: A list or a dict of JSON objects

    :rtype < list | dict >: A list or a dict of TinyModel objects
    """
    if isinstance(list_or_dict, list):
        for index, obj in enumerate(list_or_dict):
            list_or_dict[index] = model(from_json=json.dumps(obj))
    elif isinstance(list_or_dict, dict):
        for key, val in list_or_dict.items():
            list_or_dict[key] = model(from_json=json.dumps(val))
    else:
        raise Exception("Facebook data returned in an unrecognized type: " + str(type(list_or_dict)))

    return list_or_dict
