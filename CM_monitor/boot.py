import os
import network
import webrepl
import urequests
import machine
import time

from machine import RTC
from machine import Pin, SoftI2C
p2 = Pin(2, Pin.OUT)
red = Pin(13, Pin.OUT)
green = Pin(14, Pin.OUT)
blue = Pin(27, Pin.OUT)

machine.freq(240000000)

##################################
##    Network Configuration     ##
##################################
from password import *
SSID_NAME_HOME = ['oh_sour']
SSID_NAME_LAB = ['CDSL-A910-11n']
SSID_NAME_ESP = ['ESP_F']

wifiStatus = True
wifi = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

##################################
##    Establish Connection      ##
##################################
# Search Wi-Fi Networks
def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode('utf-8') != '':
            wifiAPDict.append(wl[0].decode('utf-8'))
    return wifiAPDict

def connect_lab_wifi(timeout = 10):
    global wifi

    wifi.active(False)
    time.sleep(1)
    wifi.active(True)

    
    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    endFlag = False
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_NAME_LAB:
            print(f"[{wn}]に接続します")
            wifi.connect(wn, LAB_WIFI_PASS)
            while True:
                
                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    endFlag = True
                    print("----  wifi is connected -----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    webrepl.start(password = WEBREPL_PASS)
                    break
                else:
                    time.sleep(1)
            if endFlag == True:
                break
        if endFlag == True:
            break

def connect_home_wifi(timeout = 10):
    global wifi

    wifi.active(False)
    time.sleep(1)
    wifi.active(True)

    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    endFlag = False
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_NAME_HOME:
            print(f"[{wn}]に接続します")
            wifi.connect(wn, HOME_WIFI_PASS)
            while True:
                
                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    endFlag = True
                    print("----  wifi is connected -----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    webrepl.start(password = WEBREPL_PASS)
                    break
                else:
                    time.sleep(1)
            if endFlag == True:
                break
        if endFlag == True:
            break

def connect_esp_wifi(timeout = 10):
    global wifi

    wifi.active(True)

    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    wifiName = wifiscan()
    #print(wifiName) #羅列が煩わしいので，デバッグ時は#外す

    for wn in wifiName:
        if wn in SSID_NAME_ESP:
            print(f"---ESPのWi-Fi[{wn}]に接続します---")
            wifi.connect(wn)
            while True:

                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    
                    print("---- wifi is connected ----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    
                    return True

                else:
                    time.sleep(1)


def ap_activate():
    global ap
    ap.active(False)
    time.sleep(1)
    ap.active(True)
    p2.on()
    print("----  AP is activated -----")
    ap.config(essid = 'ESP_F') #change_here
    config = ap.ifconfig()
    print(config)

def ap_deactivate():
    ap.active(False)
    p2.off()
    print("----  AP is deactivated -----")

##################################
##    System     ##
##################################
print('booted system')

if __name__ == '__main__':
    execfile('get_current.py')
    # execfile('cm_main.py')
    # execfile('debug.py')
