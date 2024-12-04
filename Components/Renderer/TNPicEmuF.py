#!/usr/bin/python
# -*- coding: utf-8 -*-
#Coders by Nikolasi
#EDit BY RAED foo QuickSignal 2018
#Update BY RAED for python3 QuickSignal 2020

from __future__ import print_function
from os import path as os_path

from enigma import eServiceCenter, eServiceReference, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable, ePixmap, ePicLoad, eTimer 
from Tools.LoadPixmap import LoadPixmap 
from Components.Pixmap import Pixmap 
from Components.Renderer.Renderer import Renderer
from Tools.Directories import SCOPE_CURRENT_SKIN, resolveFilename 
from Components.config import config
from Components.Element import cached
from Components.AVSwitch import AVSwitch
import os

try:
    from Components.Converter.Poll import PollConverter as Poll
    dreamos=True
except:
    from Components.Converter.Poll import Poll
    dreamos=False

class TNPicEmuF(Renderer, Poll):
        __module__ = __name__
        if not os.path.exists("/usr/lib64"):
                searchPaths = ('/data/%s/',
                '/usr/lib/enigma2/python/Plugins/Extensions/%s/',
                '/media/hdd/%s/',
                '/media/ba/%s/',
                '/media/sda1/%s/',
                '/media/cf/%s/',
                '/media/sdb1/%s/',
                '/media/usb/%s/',
                '/media/sda/%s/',
                '/etc/%s/',
                '/usr/share/enigma2/%s/',)
        else:
                searchPaths = ('/data/%s/',
                '/usr/lib64/enigma2/python/Plugins/Extensions/%s/',
                '/media/hdd/%s/',
                '/media/ba/%s/',
                '/media/sda1/%s/',
                '/media/cf/%s/',
                '/media/sdb1/%s/',
                '/media/usb/%s/',
                '/media/sda/%s/',
                '/etc/%s/',
                '/usr/share/enigma2/%s/',)
        
        def __init__(self):
                if dreamos:
                   Poll.__init__(self,type)
                else:
                   Poll.__init__(self)
                Renderer.__init__(self)
                self.path = 'emu'
                self.nameCache = {}
                self.pngname = ''
                self.picon_default = "picon_default.png"
                
        def applySkin(self, desktop, parent):
                attribs = []
                for (attrib, value,) in self.skinAttributes:
                        if (attrib == 'path'):
                                self.path = value
                        elif (attrib == 'picon_default'):
                                self.picon_default = value
                        else:
                                attribs.append((attrib, value))
                                
                self.skinAttributes = attribs
                return Renderer.applySkin(self, desktop, parent)
                
        GUI_WIDGET = ePixmap

        @cached
        def getText(self):
                service = self.source.service
                info = service and service.info()
                if not service:
                        return None
                camd = ""
                serlist = None
                camdlist = None
                nameemu = []
                nameser = []
                if not info:
                        return ""
                # PurE2
                if os.path.exists("/etc/clist.list") and os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.pyo") or os.path.exists("/etc/clist.list") and os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.pyc") or os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.py"):
                        try:
                                camdlist = open("/etc/clist.list", "r")
                        except:
                                return None
                # Alternative SoftCam Manager
                elif os.path.exists("/etc/clist.list") and checkclist() == True:
                        try:
                                camdlist = open("/etc/clist.list", "r")
                        except:
                                return None
                # Alternative SoftCam Manager
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/plugin.py"):
                        if config.plugins.AltSoftcam.actcam.value != "none": 
                                return config.plugins.AltSoftcam.actcam.value 
                        else: 
                                return None
                # VIX
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/ViX/SoftcamManager.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/ViX/SoftcamManager.pyc"):
                        try:
                                self.autostartcams = config.softcammanager.softcams_autostart.value
                                for softcamcheck in self.autostartcams:
                                        softcamcheck = softcamcheck.replace("/usr/softcams/", "")
                                        softcamcheck = softcamcheck.replace("\n", "")
                                        return softcamcheck
                        except:
                                return None
                #  GlassSysUtil 
                elif os.path.exists("/tmp/ucm_cam.info"):
                        return open("/tmp/ucm_cam.info").read()
                # egami
                elif os.path.exists("/etc/egami/emuname"):
                        try:
                                camdlist = open("/etc/egami/emuname", "r")
                        except:
                                camdlist = None
                # TS-Panel & Ts images
                elif os.path.exists("/etc/startcam.sh"):
                        try:
                                for line in open("/etc/startcam.sh"):
                                        if "script" in line:
                                                return "%s" % line.split("/")[-1].split()[0][:-3]
                        except:
                                camdlist = None
                # domica 8
                elif os.path.exists("/etc/init.d/cam"):
                        if config.plugins.emuman.cam.value: 
                                return config.plugins.emuman.cam.value
                #PKT
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/PKT/plugin.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/PKT/plugin.pyc"):
                        if config.plugins.emuman.cam.value: 
                                return config.plugins.emuman.cam.value
                #HDMU
                elif os.path.exists("/etc/.emustart") and os.path.exists("/etc/image-version"):
                        try:
                                for line in open("/etc/.emustart"):
                                        return line.split()[0].split('/')[-1]
                        except:
                                return None
                # Domica        
                elif os.path.exists("/etc/active_emu.list"):
                        try:
                                camdlist = open("/etc/active_emu.list", "r")
                        except:
                                return None
                # OpenSPA        
                elif os.path.exists("/etc/.ActiveCamd"):
                        try:
                                camdlist = open("/etc/.ActiveCamd", "r")
                        except:
                                return None
                # OoZooN
                elif os.path.exists("/tmp/cam.info"):
                        try:
                                camdlist = open("/tmp/cam.info", "r")
                        except:
                                return None
                # ItalySat
                elif os.path.exists("/etc/CurrentItalyCamName"):
                        try:
                                camdlist = open("/etc/CurrentItalyCamName", "r")
                        except:
                                return None
                # BlackHole OE2.0
                elif os.path.exists("/etc/CurrentBhCamName"):
                        try:
                                camdlist = open("/etc/CurrentBhCamName", "r")
                        except:
                                return None
                # BlackHole OE1.6
                elif os.path.exists("/etc/CurrentDelCamName"):
                        try:
                                camdlist = open("/etc/CurrentDelCamName", "r")
                        except:
                                return None
                # DE-OpenBlackHole      
                elif os.path.exists("/etc/BhFpConf"):
                        try:
                                camdlist = open("/etc/BhCamConf", "r")
                        except:
                                return None
                #Newnigma2
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/newnigma2/eCamdCtrl/eCamdctrl.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/newnigma2/eCamdCtrl/eCamdctrl.pyc"):
                        try:
                          from Plugins.newnigma2.eCamdCtrl.eCamdctrl import runningcamd
                          if config.plugins.camdname.skin.value: 
                                return runningcamd.getCamdCurrent()
                        except: 
                                return None
                #Newnigma2 OE2.5
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/newnigma2/camdctrl/camdctrl.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/newnigma2/camdctrl/camdctrl.pyc"):
                        if config.plugins.camdname.skin.value:
                            return config.usage.emu_name.value
                        return None
                # GP3 OE2.0
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
                        try:
                                from Plugins.Bp.geminimain.plugin import GETCAMDLIST
                                from Plugins.Bp.geminimain.lib import libgeminimain
                                camdl = libgeminimain.getPyList(GETCAMDLIST)
                                cam = None
                                for x in camdl:
                                        if x[1] == 1:
                                                cam = x[2] 
                                return cam
                        except:
                                return None
                # GP4 OE2.5
                elif os.path.exists("/usr/lib/enigma2/python/Plugins/GP4/geminicamswitch/gscamScreen.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/GP4/geminicamswitch/gscamScreen.pyc"):
                                #from Plugins.GP4.geminicamswitch.gscamScreen import Camswitch
                                from Plugins.GP4.geminicamswitch.gscamtools import gpconfset
                                if gpconfset.gcammanager.currentbinary.value: 
                                        return gpconfset.gcammanager.currentbinary.value
                                return None
                # Dream Elite
                elif os.path.exists("/usr/lib/enigma2/python/DE/DEPanel.so"):
                        try:
                                from DE.DELibrary import Tool
                                t = Tool()
                                emuname = t.readEmuName(t.readEmuActive()).strip()
                                emuactive = emuname != "None" and emuname or t.readEmuName(t.readCrdsrvActive()).strip()
                                return emuactive
                        except:
                                return None
                # ATV for 6.3 and later & Pli
                #elif os.path.exists("/etc/init.d/softcam") and not os.path.exists(BRANDPLI):
                elif os.path.exists("/etc/init.d/softcam") or os.path.exists("/etc/init.d/cardserver"):
                        try:
                                for line in open("/etc/init.d/softcam"):
                                        if "# Short-Description:" in line:
                                                return line.split(':')[-1].lstrip().strip('\n')
                        except:
                                pass
                # Pli/OV
                #elif os.path.exists(BRANDPLI) and os.path.exists("/etc/init.d/softcam") or os.path.exists("/etc/init.d/cardserver"):
                        try:
                                for line in open("/etc/init.d/softcam"):
                                        if "echo" in line:
                                                nameemu.append(line)
                                camdlist = "%s" % nameemu[1].split('"')[1]
                        except:
                                pass
                        try:
                                for line in open("/etc/init.d/cardserver"):
                                        if "echo" in line:
                                                nameser.append(line)
                                serlist = "%s" % nameser[1].split('"')[1]
                        except:
                                pass
                        if serlist is not None and camdlist is not None:
                                return ("%s %s" % (serlist, camdlist))
                        elif camdlist is not None:
                                return "%s" % camdlist
                        elif serlist is not None:
                                return "%s" % serlist
                        return ""
                # AAF & ATV old under 6.2 & VTI 
                elif os.path.exists("/etc/image-version") and not os.path.exists("/etc/.emustart"):
                        emu = ""
                        server = ""
                        for line in open("/etc/image-version"):
                                if "=AAF" in line or "=openATV" in line or "=opendroid" in line or "=openESI" in line or "=OpenPlus" in line:
                                        if config.softcam.actCam.value: 
                                                emu = config.softcam.actCam.value
                                        if config.softcam.actCam2.value: 
                                                server = config.softcam.actCam2.value
                                                if config.softcam.actCam2.value == "no CAM 2 active":
                                                        server = ""
                                elif "=vuplus" in line:
                                        if os.path.exists("/tmp/.emu.info"):
                                                for line in open("/tmp/.emu.info"):
                                                        emu = line.strip('\n')
                                # BlackHole     
                                elif "version=" in line and os.path.exists("/etc/CurrentBhCamName"):
                                        emu = open("/etc/CurrentBhCamName").read()
                        return "%s %s" % (emu, server)
                else:
                        return None
                        
                if serlist is not None:
                        try:
                                cardserver = ""
                                for current in serlist.readlines():
                                        cardserver = current
                                serlist.close()
                        except:
                                pass
                else:
                        cardserver = " "

                if camdlist is not None:
                        try:
                                emu = ""
                                for current in camdlist.readlines():
                                        emu = current
                                camdlist.close()
                        except:
                                pass
                else:
                        emu = " "
                        
                return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
                
        text = property(getText)

        def changed(self, what):
                self.poll_interval = 50
                self.poll_enabled = True
                if self.instance:
                        pngname = ''
                        if (what[0] != self.CHANGED_CLEAR):
                                sname = ""
                                service = self.source.service
                                if service:
                                        info = (service and service.info())

                                        if info:
                                            caids = info.getInfoObject(iServiceInformation.sCAIDs)
                                            if os.path.exists("/tmp/ecm.info"):
                                              try:
                                                 value = self.getText()
                                                 value = value.lower() #change value to small letters
                                                 if value == None:
                                                        print("no emu installed")
                                                        sname=''
                                                 else:
                                                        ## Should write name be small letters
                                                        if ("ncam" in value):
                                                                sname = "ncam"
                                                        elif ("oscam" in value):
                                                                sname = "oscam"
                                                        elif ("mgcamd" in value):
                                                                sname = "mgcamd"
                                                        elif ("wicard" in value or "wicardd" in value):
                                                                sname = "wicardd"
                                                        elif ("gbox" in value):
                                                                sname = "gbox"
                                                        elif ("camd3" in value):
                                                                sname = "camd3"
                                                        elif os.path.exists("/tmp/ecm.info"):
                                                             try:
                                                                f = open("/tmp/ecm.info", "r")
                                                                content = f.read()
                                                                f.close()
                                                             except:
                                                                content = ""
                                                             contentInfo = content.split("\n")
                                                             for line in contentInfo:
                                                                     if ("address" in line):
                                                                             sname = "CCcam"
                                              except:
                                                print("")

                                            if caids:
                                                   if (len(caids) > 0):
                                                       for caid in caids:
                                                         caid = self.int2hex(caid)
                                                         if (len(caid) == 3):
                                                             caid = ("0%s" % caid)
                                                         caid = caid[:2]
                                                         caid = caid.upper()
                                                         if (caid != "") and (sname == ""):
                                                                 sname = "Unknown"

                                pngname = self.nameCache.get(sname, '')
                                if (pngname == ''):
                                        pngname = self.findPicon(sname)
                                        if (pngname != ''):
                                                self.nameCache[sname] = pngname

                        if (pngname == ''):
                                pngname = self.nameCache.get('Fta', '')
                                if (pngname == ''):
                                        pngname = self.findPicon('Fta')
                                        if (pngname == ''):
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if os.path.exists(tmp):
                                                    pngname = tmp
                                            else:
                                                    pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/picon_default.png')
                                            self.nameCache['default'] = pngname

                        if (self.pngname != pngname):
                                self.picload = ePicLoad()
                                try:
                                        self.picload.PictureData.get().append(self.piconShow)
                                except:
                                        self.picload_conn = self.picload.PictureData.connect(self.piconShow)
                                scale = AVSwitch().getFramebufferScale()
                                # self.picload.setPara((self.instance.size().width(), self.instance.size().height(), scale[0], scale[1], False, 1, "#00000000"))
                                self.picload.startDecode(pngname)
                                self.pngname = pngname
                                self.instance.setPixmapFromFile(self.pngname)

        def piconShow(self, picInfo = None):
                ptr = self.picload.getData()
                if ptr != None:
                        self.instance.setPixmap(ptr.__deref__())
                return

        def int2hex(self, int):
            return ("%x" % int)
               
        def findPicon(self, serviceName):
                for path in self.searchPaths:
                        pngname = (((path % self.path) + serviceName) + '.png')
                        if os.path.exists(pngname):
                                return pngname
                return ''
