# -*- coding: utf-8 -*-
# @author: Peter Lamut
# Modified by Haipeng Tang to solve errors due to Python version conflict
'''
This code split a large # of files into folders. If the # cannot be devided evenly, the last folder will contain the files left
1. Decide how many files each folder will hold, then modify N to that number
2. Specify the folder containing the files to be split to variable src_dir
3. Last time this program successfully split 1,132,336 files
4. This is based on Python version 3

'''

import argparse
import os
import shutil

N = 113234  # the number of files in each subfolder folder


def move_files(abs_dirname):
    """Move files into subdirectories."""

    files = [os.path.join(abs_dirname, f) for f in os.listdir(abs_dirname)]

    i = 0
    curr_subdir = None

    for f in files:
        # create new subdir if necessary
        if i % N == 0:
            subdir_name = os.path.join(abs_dirname, '{0:03d}'.format(i // N + 1))
            os.mkdir(subdir_name)
            curr_subdir = subdir_name

        # move file to current dir
        f_base = os.path.basename(f)
        shutil.move(f, os.path.join(subdir_name, f_base))
        i += 1
        print(i)


def parse_args():
    """Parse command line arguments passed to script invocation."""
    parser = argparse.ArgumentParser(
        description='Split files into multiple subfolders.')

    parser.add_argument('src_dir', help='source directory')

    return parser.parse_args()


def main():
    """Module's main entry point (zopectl.command)."""
#    args = parse_args()
#    src_dir = args.src_dir

    src_dir = "C:\\Users\\liux29\\OneDrive - National Institutes of Health\\Research\\Community_Mine\\GSV_Images\\gsv_images\\images\\gsv"
    
    if not os.path.exists(src_dir):
        raise Exception('Directory does not exist ({0}).'.format(src_dir))

    move_files(os.path.abspath(src_dir))


if __name__ == '__main__':
    main()