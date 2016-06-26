#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import subprocess
import shutil

COPY_SUFFIX = [".bin", ".hex", ".cgs"]

def delete_all_file(path):
    "delete all folers and files"
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itemsrc = os.path.join(path, item)
            delete_all_file(itemsrc)
        try:
            os.rmdir(path)
        except:
            pass


def copy_output_files(from_dir, to_dir):
    for item in from_dir:
        sub_dir = item.split('.')
        tmp_dir = ""
        for i in sub_dir:
            tmp_dir = os.path.join(tmp_dir, i)
        tmp_dir = os.path.join(os.getcwd(), tmp_dir)

        for each_file in os.listdir(tmp_dir):
            if not os.path.isdir(each_file):
                if os.path.splitext(each_file)[1] in COPY_SUFFIX:
                    shutil.copy(os.path.join(tmp_dir, each_file), to_dir)

def Create_Output_Dir(dest_dir, js_obj):
    # Create all output directories
    for builditem in js_obj["BuildList"]:
        if builditem["Platform"].strip() != "":
            # 1st Dir
            output_dir = os.path.join(dest_dir, builditem["Platform"])
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            # 2nd Dir
            output_dir = os.path.join(output_dir, builditem["AppName"])
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

if __name__ == "__main__":
    dirname = 'build'
    delete_all_file(dirname) 