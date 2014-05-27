#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: exifsort.py
"""
exifsort.py
~~~~

Sort images into directories based on their exchangeable image file format

"""
__author__ = ["Andrew G. Dunn"]
__copyright__ = __author__
__license__ = "Check root folder LICENSE file"
__email__ = "andrew.g.dunn@gmail.com"

import os
import argparse
import exifread


def cli():
    description = """Organize a folder of images into sub-folders \
                    based on the order of sorting parameters."""
    parser = argparse.ArgumentParser(description=description)

    # Here we will our own argparse.Action so that we can store a list of the
    # optional arguments in their specific order.
    # From Jeff Terrace <jterrace@gmail.com>
    class OrderedAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', [])
            previous = namespace.ordered_args
            previous.append(self.dest)
            setattr(namespace, 'ordered_args', previous)

    parser.add_argument('input', help='path of images to be sorted')
    parser.add_argument('output', help='path to make a \'sorted\' into')
    # sort actions
    parser.add_argument('--move', action='store_true',
                        help='Move Files, default action is to copy')
    parser.add_argument('--video', action='store_true',
                        help='Find and copy/move video to the output_path')
    # sort parameters
    parser.add_argument('-d', '--date', nargs=0, action=OrderedAction,
                        help='Sort by Date')
    parser.add_argument('-t', '--time', nargs=0, action=OrderedAction,
                        help='Sort by Time (to the minute)')
    parser.add_argument('-c', '--camera', nargs=0, action=OrderedAction,
                        help='Sort by Camera Body')
    parser.add_argument('-l', '--lens', nargs=0, action=OrderedAction,
                        help='Sort by Lens')
    parser.add_argument('-o', '--orientation', nargs=0, action=OrderedAction,
                        help='Sort by Orientation')
    parser.add_argument('-a', '--aperture', nargs=0, action=OrderedAction,
                        help='Sort by Orientation')
    parser.add_argument('-f', '--fnumber', nargs=0, action=OrderedAction,
                        help='Sort by Orientation')
    parser.add_argument('-m', '--make', nargs=0, action=OrderedAction,
                        help='Sort by Orientation')

    args = parser.parse_args()

    # Need moar sanity checks before dumping to main
    if not os.path.exists(args.input):
        print('Input path does not exist')
        return

    main(args.input, args.output, args.ordered_args)


def main(input, output, order):
    """
    Do:
     - search for files to move
     - for each file:
        - read exif
        - match contents with known values
        - create path (based on order)
        - move file
    """
    # Move this to json!
    # meta is our canonical dictionary of things we can parse
    meta  = {
        'date': ['Image DateTime'],
        'time': ['Image DateTime'],
        'camera': ['Image Model'],
        'lens': ['Image Orientation'],
        'orientation': ['Image Orientation'],
        'aperture': ['EXIF ApertureValue'],
        'make': ['Image Make'],
        'fnumber': ['EXIF FNumber']
    }

    ordered = [el for el in order if el in meta.keys()]

    # Move this to JSON!
    ext_img = ['jpg', 'jpeg', 'cr2', 'nef', 'rw2', 'arw', 'srf', 'sr2']
    ext_img += map(lambda x: x.upper(), ext_img)
    # ext_vid = ['mov', 'avi', 'mkv', 'm4v', 'mpeg', 'ogg']
    # ext_vid += map(lambda x: x.upper(), ext_vid)

    for image in search(input, ext_img):
        exif_data = exifread.process_file(open(image), details=False,
                                          stop_tag='JPEGThumbnail')

        paths = []
        for meta_key in order:
            paths.append(str(exif_data[meta[meta_key][0]]))

        print paths


def search(path, extensions):
    """
    return a list of paths that matches the extensions
    """
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if not extensions:
                file_list.append(file_path)
            else:
                if os.path.splitext(file_path)[1][1:] in extensions:
                    file_list.append(file_path)
        elif os.path.isdir(file_path):
            file_list.extend(search(file_path, extensions))
    return sorted(file_list)
