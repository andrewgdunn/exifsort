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
import shutil
import argparse
import exifread
import datetime


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
                        help='Sort by DateTime (to the minute)')
    parser.add_argument('-n', '--model', nargs=0, action=OrderedAction,
                        help='Sort by Camera Body')
    parser.add_argument('-l', '--lens', nargs=0, action=OrderedAction,
                        help='Sort by Lens')
    parser.add_argument('-o', '--orientation', nargs=0, action=OrderedAction,
                        help='Sort by Orientation')
    parser.add_argument('-a', '--aperture', nargs=0, action=OrderedAction,
                        help='Sort by Aperture')
    parser.add_argument('-f', '--fnumber', nargs=0, action=OrderedAction,
                        help='Sort by F-Number')
    parser.add_argument('-m', '--make', nargs=0, action=OrderedAction,
                        help='Sort by Make')

    args = parser.parse_args()

    # Need more sanity checks before dumping to main
    if not os.path.exists(args.input):
        print('Input path does not exist')
        return

    main(args.input, args.output, args.ordered_args)


def main(input, output, order):
    ext_img = ['jpg', 'jpeg', 'cr2', 'nef', 'rw2', 'arw', 'srf', 'sr2']
    ext_img += map(lambda x: x.upper(), ext_img)
    ext_vid = ['mov', 'avi', 'mkv', 'm4v', 'mpeg', 'ogg']
    ext_vid += map(lambda x: x.upper(), ext_vid)

    for image in search(input, ext_img):
        exif = exifread.process_file(open(image), details=False)
        # need to make a helper utility/catalog for different camera makes
        # right now we'll use Canon just to get the thing working
        camera = Canon()
        dest = [camera.process(key, camera.lookup(key, exif)) for key in order]
        copy(image, output, dest)


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


def copy(source, output, dest):
    path = os.path.join(os.path.abspath(output), *dest)
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.copy2(source, path)


def move(source, output, dest):
    path = os.path.join(os.path.abspath(output), *dest)
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.move(source, path)


class Canon(object):
    """ Each make will have its own object and we'll use the catalog pattern to
    call the methods statically from the main sorting loop.

    https://github.com/faif/python-patterns/blob/master/catalog.py
    """

    def __init__(self):
        self.staticmethods = {
            'date': self.format_date,
            'time': self.format_time,
            'model': self.format_model,
            'lens': self.format_lens,
            'orientation': self.format_orientation,
            'make': self.format_make
        }
        # likely need to load this from a file (JSON)
        self.metaindex = {
            'date': ['Image DateTime'],
            'time': ['Image DateTime'],
            'model': ['Image Model'],
            'lens': ['EXIF LensModel'],
            'orientation': ['Image Orientation'],
            'make': ['Image Make']
        }

    def lookup(self, meta, exif):
        if meta in self.metaindex.keys():
            # we really should do a search here, but instead we're going to
            # select the first element in the list. (for now)
            return str(exif[self.metaindex[meta][0]])
        else:
            print('lookup failed, that key is not in metaindex')

    def process(self, meta, payload):
        if meta in self.staticmethods.keys():
            return self.staticmethods[meta](payload)
        else:
            print('process failed, that key is not in staticmethods')

    @staticmethod
    def format_date(payload):
        """ example: '2013:08:05 17:39:46'
            return: '[2013, 8, 5]'
        """
        parse_format = '%Y:%m:%d %H:%M:%S'
        d = datetime.datetime.strptime(payload, parse_format)
        date = [d.year, d.month, d.day]
        return '/'.join(str(n) for n in date)

    @staticmethod
    def format_time(payload):
        """ example: '2013:08:05 17:39:46'
            return: 2013/8/5/17/39'
        """
        parse_format = '%Y:%m:%d %H:%M:%S'
        d = datetime.datetime.strptime(payload, parse_format)
        date = [d.year, d.month, d.day, d.hour, d.minute, d.second]
        return '/'.join(str(n) for n in date)

    @staticmethod
    def format_lens(payload):
        """ example: 'EF-S18-135mm f/3.5-, ... ]'
            result: ''EF-S18-135mm'
        """
        return payload.split()[0]

    @staticmethod
    def format_orientation(payload):
        """ example: 'Horizontal (normal)'
            result: 'Horizontal'
        """
        return payload.split()[0]

    @staticmethod
    def format_make(payload):
        return payload

    @staticmethod
    def format_model(payload):
        """ example: 'Canon EOS 60D'
            result: '60D'
        """
        return payload.split()[-1]
