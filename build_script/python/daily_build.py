#!/user/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import subprocess
import json

from daily_build_file import *

TARGETS    = "targets"

script_top_dir = ""
script_src_dir = ""
script_cfg_dir = ""
work_dir       = ""
image_dir      = ""

def set_build_env(workspace):
    global script_top_dir
    global script_src_dir
    global script_cfg_dir
    global work_dir
    global image_dir

    script_top_dir  = os.path.dirname(os.getcwd())
    script_src_dir = os.path.join(script_top_dir, "python")
    script_cfg_dir = os.path.join(script_top_dir, "cfg")
    work_dir       = workspace
    # Create output directory
    image_dir      = os.path.join(work_dir, "tmp")
    if os.path.exists(image_dir):
        delete_all_file(image_dir)
    os.mkdir(image_dir)

def build_one(builditem, cl):
    output_dir = os.path.join(image_dir, builditem["Platform"])
    output_dir = os.path.join(output_dir, builditem["AppName"])

    # Change to build directory
    os.chdir(os.path.join(work_dir, TARGETS, builditem["Platform"]))
    # # Clean old build
    p = subprocess.Popen(builditem["Clean"], shell=True)
    p.wait()

    # Run build commands
    build_cmd_cl = builditem["Command"] + ' "BUILD_CHANGE_LIST=' + cl + '"'
    p = subprocess.Popen(build_cmd_cl, stderr=subprocess.PIPE, shell=True)
    (stdoutput,erroroutput) = p.communicate()
    if p.returncode != 0:
        print(erroroutput.decode())
    else:
        copy_output_files(builditem["Output"], output_dir)

    return p.returncode


def Clean_Project(js_obj):
    for builditem in js_obj["BuildList"]:
        if builditem["Platform"].strip() != "":
            # Change to build directory
            os.chdir(os.path.join(work_dir, TARGETS, builditem["Platform"]))
            # # Clean old build
            p = subprocess.Popen(builditem["Clean"], shell=True)
            p.wait()

def main(workspace, cfg_file, cl):
    set_build_env(workspace)
    cfg_file = os.path.join(script_cfg_dir, cfg_file)
    with open(cfg_file) as json_file:
        js = json.load(json_file)
        Create_Output_Dir(image_dir, js)
        Clean_Project(js)

        # Building.....
        for builditem in js["BuildList"]:
            if builditem["Platform"].strip() != "":
                err_code = build_one(builditem, cl)
                if err_code == 0:
                    print("success")
                else:
                    print("failed")
                    sys.exit(err_code)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="build", description="build the image based on the configuration file and collect them into a file")
    parser.add_argument("workspace", nargs="?", help="workspace directory", default=r"D:\work\aidk_2.2.2")
    parser.add_argument("cfg_file", nargs="?", help="build configuration file", default=r"test.txt")
    parser.add_argument("cl", nargs="?", help="build change list", default="1000")
    args = parser.parse_args()
    main(args.workspace, args.cfg_file, args.cl)