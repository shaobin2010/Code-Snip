#!/user/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

def main(workspace, cfg_file):
    print(workspace)
    print(cfg_file)
    sys.exit(0)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="build", description="build the image based on the configuration file and collect them into a file")
    parser.add_argument("workspace", nargs="?", help="workspace directory", default=r"D:\work\aidk_2.2.2")
    parser.add_argument("cfg_file", nargs="?", help="build configuration file", default=r"test.txt")
    args = parser.parse_args()
    main(args.workspace, args.cfg_file)