#!/user/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import json

import struct
import binascii
import ctypes

from cfg_info import *

def gen_cfg_header(js_file, target_file):
    header_fmt = str(CFG_SYS_HEADER_LEN)+'s'
    s = struct.Struct(header_fmt)
    prebuffer = ctypes.create_string_buffer(s.size)
    s.pack_into(prebuffer, 0, bytes(js_file["header"], 'UTF-8'))
    print("header: ", binascii.hexlify(prebuffer).decode("UTF-8"))
    target_file.write(binascii.hexlify(prebuffer).decode("UTF-8"))

def ip_str_to_bin(ip_str):
    ip_cuple = ip_str.split('.')
    return ((int(ip_cuple[0]) << 24) | (int(ip_cuple[1]) << 16) | (int(ip_cuple[2]) << 8) | int(ip_cuple[3]))

def gen_cfg_body(js_file, target_file):
    mode_fmt = "BB"
    s = struct.Struct(mode_fmt)
    prebuffer = ctypes.create_string_buffer(s.size)
    s.pack_into(prebuffer, 0, app_dict[js_file["appmode"]], start_dict[js_file["Startmode"]])
    target_file.write(binascii.hexlify(prebuffer).decode("UTF-8"))
    print("mode: ", binascii.hexlify(prebuffer).decode("UTF-8"))

    fl_ap_fmt = "<B" + str(CFG_SYS_SSID_MAX_LEN) +"sIB" + str(CFG_SYS_PASSWORD_MAX_LEN) + 's'
    fl_net_fmt = "<BIH"
    fl_ap = struct.Struct(fl_ap_fmt)
    fl_net = struct.Struct(fl_net_fmt)
    fl_ap_prebuffer = ctypes.create_string_buffer(fl_ap.size)
    fl_net_prebuffer = ctypes.create_string_buffer(fl_net.size)
    ap_info = js_file["fl_info"]["ap_info"]
    net_info = js_file["fl_info"]["network_info"]
    if ap_info["ssid"] != "":
        fl_ap.pack_into(fl_ap_prebuffer, 0, len(ap_info["ssid"]), bytes(ap_info["ssid"], "UTF-8"), sec_dict[ap_info["security"]], len(ap_info["password"]), bytes(ap_info["password"], "UTF-8"))
        fl_net.pack_into(fl_net_prebuffer, 0, server_type_dict[net_info["server_type"]], ip_str_to_bin(net_info["server_ip"]), int(net_info["server_port"]))
    else:
        pass
    target_file.write(binascii.hexlify(fl_ap_prebuffer).decode("UTF-8"))
    target_file.write(binascii.hexlify(fl_net_prebuffer).decode("UTF-8"))
    print("fl_ap: ", binascii.hexlify(fl_ap_prebuffer).decode("UTF-8"))
    print("fl_net: ", binascii.hexlify(fl_net_prebuffer).decode("UTF-8"))

    pin_cfg_fmt = "7B"
    port_cfg_fmt = "<BI"
    pin_cfg = struct.Struct(pin_cfg_fmt)
    port_cfg = struct.Struct(port_cfg_fmt)
    pin_cfg_buffer = ctypes.create_string_buffer(pin_cfg.size)
    port_cfg_buffer = ctypes.create_string_buffer(port_cfg.size)
    pin_cfg_info = js_file["tm_cfg"]["pin_cfg"]
    port_cfg_info = js_file["tm_cfg"]["port_cfg"]
    pin_cfg.pack_into(pin_cfg_buffer, 0, bool_dict[js_file["tm_cfg"]["enable"]], 
        int(pin_cfg_info["restore_pin"]), int(pin_cfg_info["ota_pin"]), int(pin_cfg_info["ap_pin"]),
        int(pin_cfg_info["server_pin"]),int(pin_cfg_info["ps_state_pin"]),int(pin_cfg_info["ps_wakeup_pin"]))
    port_cfg.pack_into(port_cfg_buffer, 0, tm_port_dict[port_cfg_info["type"]], int(port_cfg_info["rate"]))
    target_file.write(binascii.hexlify(pin_cfg_buffer).decode("UTF-8"))
    target_file.write(binascii.hexlify(port_cfg_buffer).decode("UTF-8"))
    print("pin_cfg: ", binascii.hexlify(pin_cfg_buffer).decode("UTF-8"))
    print("port_cfg: ", binascii.hexlify(port_cfg_buffer).decode("UTF-8"))

def gen_cfg_file():
    cfg_file = "config.json"
    with open("tmp.txt", 'w') as tmp_file:
        with open(cfg_file) as json_file:
            js = json.load(json_file)
            gen_cfg_header(js, tmp_file)
            gen_cfg_body(js, tmp_file)

if __name__ == '__main__':
    gen_cfg_file()