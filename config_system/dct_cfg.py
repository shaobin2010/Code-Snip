#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import ctypes

CONFIG_START = "434647535953"  #"CFGSYS"
CONTENT_LEN = 32
CONTENT_END_LEN = 3 # checksum + \n
CONTENT_START_LEN = 9
CONTENT_OTHER = 12

from cfg_gen import *

def char_checksum(data):
    length = len(data)
    check_sum = 0
    for i in range(0, length, 2):
        x = int(data[i:i+2], 16)
        check_sum = check_sum + x

    check_sum_str = "%02X"%ctypes.c_ubyte(ctypes.c_ubyte(~check_sum).value + 1).value
    return check_sum_str

def gen_dct_cfg(from_file, cfg_file, dest_file):
    from_file.seek(0)
    cfg_file.seek(0)
    lines = from_file.readlines()
    find_start = 0
    for line in lines:
        if find_start == 0:
            start_idx = line.find(CONFIG_START)
            if start_idx == -1:
                dest_file.write(line)
            else:
                find_start = 1
                read_num = (len(line) - CONTENT_OTHER) - (start_idx - CONTENT_START_LEN)
                read_data = cfg_file.read(read_num)
                if not read_data:
                    print("ERROR.......")
                    exit()
                write_line = line[0 : start_idx] + read_data + line[-3 : ]
                check_sum_data = write_line[1:-3]
                write_line = write_line[0 : -3] + char_checksum(check_sum_data) + write_line[-1 : ]
                dest_file.write(write_line)
        else:
            read_num = (len(line) - CONTENT_OTHER)
            read_data = cfg_file.read(read_num)
            if read_data:
                if len(read_data) < read_num:
                    write_line = line[0 : CONTENT_START_LEN] + read_data + line[(len(read_data) + CONTENT_START_LEN) : ]
                    check_sum_data = write_line[1:-3]
                    write_line = write_line[0 : -3] + char_checksum(check_sum_data) + write_line[-1 : ]
                    dest_file.write(write_line)
                else:
                    write_line = line[0 : CONTENT_START_LEN] + read_data + line[-3 : ]
                    check_sum_data = write_line[1:-3]
                    write_line = write_line[0 : -3] + char_checksum(check_sum_data) + write_line[-1 : ]
                    dest_file.write(write_line)
            else:
                dest_file.write(line)

def main():
    gen_cfg_file()
    with open("DCT.hex") as from_file:
        with open("tmp.txt") as cfg_file:
            dest_file_name =  "DCT_cfg.hex"
            with open(dest_file_name, "w") as dest_file:
                gen_dct_cfg(from_file, cfg_file, dest_file)

if __name__=='__main__':
    main()
