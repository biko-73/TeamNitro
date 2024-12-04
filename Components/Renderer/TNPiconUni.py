#!/usr/bin/python
# -*- coding: utf-8 -*-
# PiconUni
# Copyright (c) 2boom 2012-15
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# 26.09.2012 added search mountpoints
# 25.06.2013 added resize picon
# 26.11.2013 code optimization
# 02.12.2013 added compatibility with CaidInfo2 (SatName)
# 18.12.2013 added picon miltipath
# 27.12.2013 added picon reference
# 27.01.2014 added noscale parameter (noscale="0" is default, scale picon is on)
# 28.01.2014 code otimization
# 02.04.2014 added iptv ref code
# 17.04.2014 added path in plugin dir...
# 02.07.2014 small fix reference
# 09.01.2015 redesign code
# 17.08.2018 Update by mfraja to RAEDQuickSignal plugins
# 07.12.2018 Update by mfraja to RAEDQuickSignal plugins fix picon show on DreamOS
# 12.01.2022 Update by RAED to remove "sub-network" from namespace
# 12.01.2022 Update by RAED to support picon for channels name

import unicodedata
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePicLoad
from Components.AVSwitch import AVSwitch
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, resolveFilename
from ServiceReference import ServiceReference
from os import path as os_path
import os, re, sys

try:
        from Components.Converter.Poll import PollConverter as Poll
        dreamos=True
except:
        from Components.Converter.Poll import Poll
dreamos=False

#searchPaths = []

#def initPiconPaths():
#global searchPaths
#if os.path.isfile('/proc/mounts'):
#       for line in open('/proc/mounts'):
#               if '/dev/sd' in line:
#                       piconPath = line.split()[1].replace('\\040', ' ') + '/%s/'
#                       searchPaths.append(piconPath)
#searchPaths.append(resolveFilename(SCOPE_CURRENT_SKIN, '%s/'))
#searchPaths.append(resolveFilename(SCOPE_PLUGINS, '%s/'))

def getchannelName(serviceName):
        return ServiceReference(serviceName).getServiceName()


class TNPiconUni(Renderer, Poll):
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
                '/media/mmc/%s/',
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
                '/media/mmc/%s/',
                '/etc/%s/',
                '/usr/share/enigma2/%s/',)

        def __init__(self):
                Renderer.__init__(self)
                if dreamos:
                        Poll.__init__(self,type)
                else:
                        Poll.__init__(self)
                self.path = 'picon'
                self.scale = '0'
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
        def changed(self, what):
                self.poll_interval = 50
                self.poll_enabled = True
                if self.instance:
                        #print("raedwhat2",str(what),"**",str(self.CHANGED_CLEAR))
                        pngname = ''
                        if what[0] != self.CHANGED_CLEAR:
                                sname = self.source.text
                                sname = sname.upper().replace('.', '').replace('\xc2\xb0', '')
                                fields = sname.upper().replace('.', '').replace('\xc2\xb0', '').split(':', 10)[:10]
                                if sname.startswith('4097'):
                                        sname = sname.replace('4097', '1', 1)
                                if ':' in sname:
                                        sname = '_'.join(sname.split(':')[:10])
                                pngname = self.nameCache.get(sname, '')
                                if pngname == '' and len(fields) >= 10:
                                        if not fields[6].endswith("0000"): #remove "sub-network" from namespace
                                                fields[6] = fields[6][:-4] + "0000"
                                                sname2 = '_'.join(fields)
                                                pngname = self.findPicon(sname2)
                                if pngname == '': # picon by channel Reference
                                        pngname = self.findPicon(sname)
                                        if pngname != '':
                                                self.nameCache[sname] = pngname
                                if pngname == '': # picon by channel Name
                                        channelname = getchannelName(self.source.text)
                                        if sys.version_info[0] >= 3:
                                            channelname = channelname = unicodedata.normalize('NFKD', str(channelname)).encode('ASCII', 'ignore').decode('ASCII', 'ignore')
                                        else:
                                            channelname = unicodedata.normalize('NFKD', unicode(channelname, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
                                        channelname = re.sub('[^a-z0-9]', '', channelname.replace('&', 'and').replace('+', 'plus').replace('*', 'star').lower())
                                        if len(channelname) > 0:
                                                pngname = self.findPicon(channelname)
                                                if pngname == '' and len(channelname) > 2 and channelname.endswith('hd'):
                                                        pngname = self.findPicon(channelname[:-2])
                                                if pngname == '' and len(channelname) > 6:
                                                        series = re.sub(r's[0-9]*e[0-9]*$', '', channelname)
                                                        pngname = self.findPicon(series)

                        if pngname == '':
                                pngname = self.nameCache.get('default', '')
                                if pngname == '':
                                        pngname = self.findPicon('picon_default')
                                        if pngname == '':
                                                tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                                if os.path.isfile(tmp):
                                                        pngname = tmp
                                                else:
                                                        pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/picon_default.png')
                                        self.nameCache['default'] = pngname

                        #print("raedpngnameself.pngname",str(pngname),"**",self.pngname) 
                        if self.pngname != pngname:
                                #print("raedpngnameself.pngname2",str(pngname),"**",self.pngname)
                                self.picload = ePicLoad()
                                try:
                                        self.picload.PictureData.get().append(self.piconShow)
                                except:
                                        self.picload_conn = self.picload.PictureData.connect(self.piconShow)
                                scale = AVSwitch().getFramebufferScale()
                                self.instance.setScale(1)
                                #0=Width 1=Height 2=Aspect 3=use_cache 4=resize_type 5=Background(#AARRGGBB)
                                #self.picload.setPara((self.instance.size().width(), self.instance.size().height(), 1, 1, False, 1, "#00000000"))
                                self.picload.startDecode(pngname)
                                self.pngname = pngname
                                self.instance.setPixmapFromFile(self.pngname)

        def piconShow(self, picInfo = None):
                ptr = self.picload.getData()
                if ptr != None:
                        self.instance.setPixmap(ptr.__deref__())
                return

        def findPicon(self, serviceName):
                if os_path.isabs(self.path):  # Absolute path case
                        pngname = os_path.join(self.path, serviceName + '.png')
                        #print(f"Checking absolute path: {pngname}")  # Debugging
                        if fileExists(pngname):
                                #print(f"Found icon in absolute path: {pngname}")  # Debugging
                                return pngname

                # Check in the search paths
                for path in self.searchPaths:
                        if "%s" in path:
                                pngname = os_path.join(path % self.path, serviceName + '.png')
                        else:
                                pngname = os_path.join(path, serviceName + '.png')

                        #print(f"Checking path: {pngname}")  # Debugging
                        if fileExists(pngname):
                                #print(f"Found icon: {pngname}")  # Debugging
                                return pngname

                #print(f"No icon found for {serviceName}")  # Debugging
                return ''




#initPiconPaths()
