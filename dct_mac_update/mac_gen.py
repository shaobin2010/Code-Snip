#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

import ctypes

DEFAULT_OUI = "020AF7"

def char_checksum(data):
    length = len(data)
    check_sum = 0
    for i in range(0, length, 2):
        x = int(data[i:i+2], 16)
        check_sum = check_sum + x

    check_sum_str = "%02X"%ctypes.c_ubyte(ctypes.c_ubyte(~check_sum).value + 1).value
    return check_sum_str

def gen_dct(from_file, dest_file, offset, oui=DEFAULT_OUI):
    from_file.seek(0)
    lines = from_file.readlines()
    for line in lines:
        oui_idx = line.find(oui)
        if oui_idx == -1:
             dest_file.write(line)
        else:
            replace_line = line
            ori_mac = replace_line[oui_idx : oui_idx + 12]
            replace_mac = oui + "%06d" % offset
            new_line = replace_line.replace(ori_mac, replace_mac)
            check_sum_data = new_line[1:-3]
            print(check_sum_data)
            new_line = new_line.replace(new_line[-3:-1], char_checksum(check_sum_data))
            print(new_line)
            dest_file.write(new_line)

def mac_gen(start, end):
    with open("DCT.hex") as from_file:
        for a in range(start, end):
            dest_file_name =  "DCT_" + str(a) + ".hex"
            with open(dest_file_name, "w") as dest_file:
                gen_dct(from_file, dest_file, a)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="mac_gen", description='generate some DCT files based on a DCT.hex file')
    parser.add_argument('start', type=int, help='MAC address start offset')
    parser.add_argument('end', type=int, help='MAC address end offset')
    args = parser.parse_args()
    mac_gen(args.start, args.end)
