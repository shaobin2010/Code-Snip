#!/user/bin/env python
# -*- coding: UTF-8 -*-

CFG_SYS_HEADER_LEN = 16
CFG_SYS_SSID_MAX_LEN = 32
CFG_SYS_PASSWORD_MAX_LEN = 64
CFG_SYS_TM_AP_NUM = 1


cfg_header = "_cfg_sys_header_"

app_dict = {"APP_ACM":0, "APP_TM":1}

start_dict = {"START_ACM":0, "START_TM":1, "START_FLASHLINK":2}

bool_dict = {"FLASE":0, "TRUE":1}

tm_port_dict = {"UART":0, "SPI":1, "USB":2}

server_type_dict = {"UDP":0, "TCP":1}

sec_dict = {
"OPEN":0x00000000, 
"WEP_PSK" : 0x00000001,
"WEP_SHARED" : 0x00008001,
"WPA_TKIP_PSK" : 0x00200002,
"WPA_AES_PSK" : 0x00200004,
"WPA2_AES_PSK" : 0x00400004,
"WPA2_TKIP_PSK" : 0x00400002,
"WPA2_MIXED_PSK" : 0x00400006
}