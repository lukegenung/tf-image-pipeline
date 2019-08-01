"""Convert all MP4 files given on the command line to JPEG images. """

from multiprocessing import cpu_count
from time import sleep
import logging
import os
import sys
import cv2


def main(argv):
    """
    Entry point for mp4_to_jpeg.

    Arguments:
        argv: All command line arguments.
    """
    if len(argv) == 1:
        binary = os.path.basename(argv[0])
        print("Usage: {} [file ...]".format(binary), file=sys.stderr)
        sys.exit(0)
    logging.basicConfig(level="INFO", format='%(levelname)s: %(message)s')
    vids = check_format(argv[1:])
    for ifile in vids:
        convert_video(ifile)


def check_format(args):
    """
    Check that arguments are MP4 files. If not, remove them from the list.

    Arguments:
        args: A list of strings from command line arguments.
    
    Returns:
        args: A list of strings that represent mp4 files.
    """
    i = 0
    for ifile in args:
        if os.path.splitext(ifile)[1] != '.mp4':
            print('File is not an MP4:', ifile)
            input('Press Enter to skip this file...')
            args.pop(i)
        i += 1
    return args


def convert_video(file_path):
    """
    Save frames from a video as JPEG files in same location as video.

    Arguments:
        file_path: Path of the file to convert.
    """
    vidcap = cv2.VideoCapture(file_path)
    success, image = vidcap.read()
    file_name = os.path.splitext(file_path)[0]
    count = 0
    while success:
        cv2.imwrite(file_name + "_frame %d.jpg" % count, image)
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


if __name__ == '__main__':
    main(sys.argv)