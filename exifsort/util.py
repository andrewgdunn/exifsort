#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: util.py
"""
util.py
~~~~

"""
__author__ = ["Andrew G. Dunn"]
__copyright__ = __author__
__license__ = "Check root folder LICENSE file"
__email__ = "andrew.g.dunn@gmail.com"


import os
import datetime
import json


def config_read_meta(ordered_args):
    """
    Takes in the custom OrderedAction created ordered_args and creates a
    dictionary that respects the original order while associating the necessary
    exif lookup keys.
    """
    config_file = json.load(open(os.path.join(os.path.dirname(__file__), '../config.json')))

    clean_ordered_args = []

    for arg in ordered_args:
        clean_ordered_args.append(arg[0])

    meta_dictionary = {}

    for key in clean_ordered_args:
        key_meta = config_file['meta'][key]
        meta_dictionary[key] = key_meta

    return meta_dictionary


def config_read_extensions(extension):
    """
    Returns a list of possible extensions for each media type {image, video}.
    Makes sure to do both lower and upper case.
    """
    config_file = json.load(open(os.path.join(os.path.dirname(__file__), '../config.json')))
    config_extensions = config_file['extensions'][extension].split()

    extensions = []

    for extension in config_extensions:
        extensions.append(str(extension))
        extensions.append(str(extension.upper()))

    return extensions


def search_path_by_extension(path, recurse, extension_list):
    """
    Return a list of file paths found in dirPath.
    If recurse is true, then move into the sub directories
    if there are no extensions, all files will be returned.
    """
    file_list = []
    
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
    
        if os.path.isfile(file_path):
            if not extension_list:
                file_list.append(file_path)
            else:
    
                if os.path.splitext(file_path)[1][1:] in extension_list:
                    file_list.append(file_path)
        elif os.path.isdir(file_path) and recurse:
            file_list.extend(search_path_by_extension(file_path, recurse, extension_list))
    
    return sorted(file_list)


def sort_path(output_path, meta_dictionary, exif):

    sort_keys = []

    for key in meta_dictionary.keys():
        for meta in meta_dictionary[key]:
            if meta in exif:
                if key == 'date':
                    sort_keys.append(parse_date(str(exif[meta])))
                elif key == 'lens':
                    sort_keys.append(parse_lens(str(exif[meta])))
                else:
                    sort_keys.append(str(exif[meta]))
                break        

    return os.path.join(output_path, *sort_keys)



def copy_image(image_path, destination_path):
    pass


def move_image(image_path, destination_path):
    pass


def parse_date(exif_datetime):
    parse_format = '%Y:%m:%d %H:%M:%S'
    return datetime.datetime.strptime(exif_datetime, parse_format)


def parse_lens(exif_lens):
    return exif_lens.split(',')[0]


    

