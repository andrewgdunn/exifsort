# -*- coding: utf-8 -*-
# Filename: ui.py
"""
ui
~~~~

"""
__author__ = ["Andrew G. Dunn"]
__copyright__ = __author__
__license__ = "Check root folder LICENSE file"
__email__ = "andrew.g.dunn@gmail.com"

import argparse
import os

from exifsort.util import config_read_meta
from exifsort.util import config_read_extensions
from exifsort.util import search_path_by_extension
from exifsort.util import sort_path
from exifsort.util import copy_image, move_image

import exifread


def main():
    """
    - parse arguments
    - parse sort order (from input order (sys.argv))    - test input_path
    - load meta-dictionary for search
    - recursively enumerate files
    - for each file
        - Read exif
        - exif contains entries in meta-dictionary
        - create proper directory path
        - move or copy file
    """
    description = """Organize a folder of images into sub-folders based on the order of sorting parameters."""

    parser = argparse.ArgumentParser(description=description)

    # From Jeff Terrace <jterrace@gmail.com>
    class OrderedAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', [])
            previous = namespace.ordered_args
            previous.append((self.dest, values))
            setattr(namespace, 'ordered_args', previous)

    parser.add_argument('input_path', help='The path of images to be sorted recursively')
    parser.add_argument('output_path', help='The path to make a \'sorted\' directory structure')
    # sort actions
    parser.add_argument('--move', action='store_true', help='Move Files, default action is to copy')
    parser.add_argument('--video', action='store_true', help='Find and move video to the output_path')
    # sort parameters
    parser.add_argument('-d', '--date', nargs=0, action=OrderedAction, help='Sort by Date')
    parser.add_argument('-c', '--camera', nargs=0, action=OrderedAction, help='Sort by Camera Body')
    parser.add_argument('-l', '--lens', nargs=0, action=OrderedAction, help='Sort by Lens')
    parser.add_argument('-o', '--orientation', nargs=0, action=OrderedAction, help='Sort by Orientation')

    args = parser.parse_args()
    meta_dictionary = config_read_meta(args.ordered_args)
    image_extensions = config_read_extensions('image')


    if os.path.exists(args.input_path):
        image_list = search_path_by_extension(args.input_path, True, image_extensions)

        for image in image_list:
            image_path = os.path.join(args.input_path, image)
            exif = exifread.process_file(open(image_path), details=False, stop_tag='JPEGThumbnail')
            dest_path = sort_path(args.output_path, meta_dictionary, exif)
            print dest_path

            # if args.move:
            #     move_image(image_path, dest_path)
            # else:
            #     copy_image(image_path, dest_path)
    else:
        print 'Path does not exist'
        return


# FOR VIDEO MOVEMENT            
# video_extensions = config_read_extensions('video')
# video_list = search_path_by_extension(args.input_path, True, video_extensions)
    

# if not args.video and args.cut and video_list:
#     print 'The Following Videos will be left behind:\n'
#     for video in video_list:
#         print video

# if args.video and video_list:
#     for video in video_list:
#         # move to base destination directo
#         pass