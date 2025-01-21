# coding: utf-8
#!/usr/bin/python
# RAED (c) 2018

from Tools.Directories import fileExists

import os, traceback

logfile="/tmp/NitroAdvanceFHD.log"

def logdata(label='', data=None):
    try:
        bfile=open(logfile, 'a')
        bfile.write( str(label) + ' : ' + str(data) + "\n")
        bfile.close()
    except:
        pass

def trace_error():
    try:
        traceback.print_exc(file=sys.stdout)
        if os.path.exists(logfile):
            pass
        else:
            return
        traceback.print_exc(file=open(logfile, 'a'))
    except:
        pass

def getmDevices():
        myusb = myusb1 = myhdd = myhdd2 = mysdcard = mysd = myuniverse = myba = mydata =''
        mdevices = []
        myusb=None
        myusb1=None
        myhdd=None
        myhdd2=None
        mysdcard=None
        mysd=None
        myuniverse=None
        myba=None
        mydata=None
        if fileExists('/proc/mounts'):
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb'
                elif line.find('/media/usb1') != -1:
                    myusb1 = '/media/usb1'
                elif line.find('/media/hdd') != -1:
                    myhdd = '/media/hdd'
                elif line.find('/media/hdd2') != -1:
                    myhdd2 = '/media/hdd2'
                elif line.find('/media/sdcard') != -1:
                    mysdcard = '/media/sdcard'
                elif line.find('/media/sd') != -1:
                    mysd = '/media/sd'
                elif line.find('/universe') != -1:
                    myuniverse = '/universe'
                elif line.find('/media/ba') != -1:
                    myba = '/media/ba'
                elif line.find('/data') != -1:
                    mydata = '/data'
            f.close()
        if myusb:
            mdevices.append((myusb, myusb))
        if myusb1:
            mdevices.append((myusb1, myusb1))
        if myhdd:
            mdevices.append((myhdd, myhdd))
        if myhdd2:
            mdevices.append((myhdd2, myhdd2))
        if mysdcard:
            mdevices.append((mysdcard, mysdcard))
        if mysd:
            mdevices.append((mysd, mysd))
        if myuniverse:
            mdevices.append((myuniverse, myuniverse))
        if myba:
            mdevices.append((myba, myba))
        if mydata:
            mdevices.append((mydata, mydata))
        return mdevices

