#!/usr/bin/python
# -*- coding: utf-8 -*-
#Coded By KIMO and Bahaa
#modify it if you keep the licens
###########################################
from __future__ import absolute_import
from .__init__ import _
from os.path import join, isdir, exists, isfile, split
import sys
from enigma import eTimer, getDesktop,ePicLoad, eListboxPythonMultiContent, gFont
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.AVSwitch import AVSwitch
from Components.MultiContent import MultiContentEntryText
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
try:
    from Screens.SkinSelection import SkinSelection
except:
    from Screens.SkinSelector import SkinSelector as SkinSelection
from Tools.LoadPixmap import LoadPixmap
from Tools import Notifications
from Tools.Notifications import AddPopup
from Tools.Directories import *
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE, SCOPE_CONFIG, SCOPE_SKIN, SCOPE_CURRENT_SKIN
import re, os, shutil
from os import listdir, remove, rename, system, path, symlink, chdir, makedirs, mkdir
from os import path as os_path, remove as os_remove
from os import path, remove
from Plugins.Extensions.TeamNitro.Console import Console
from Plugins.Extensions.TeamNitro.WeatherMSN import WeatherMSN
from Plugins.Extensions.TeamNitro.changelog import TeamNitro_Changelog
from Plugins.Extensions.TeamNitro.about import TeamNitro_About
from Plugins.Plugin import PluginDescriptor
from smtplib import SMTP
from six.moves.urllib.request import urlretrieve
from .compat import compat_urlopen, compat_Request, compat_URLError, PY3
from .tools import getmDevices
#==========================================================================================#
cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')
reswidth = getDesktop(0).size().width()
config.plugins.TeamNitro = ConfigSubsection()
config.plugins.TeamNitro.update = ConfigYesNo(default=True)
config.plugins.TeamNitro.skin_selection = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK")) ])

config.plugins.TeamNitro.skin_TNCleaner= ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK")) ])

config.plugins.TeamNitro.MSNWeather = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.skinDownload = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.piconDownload= ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.TNChangelog = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.TNAbout = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.proMode = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.DesertFHD = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK")) ])
config.plugins.TeamNitro.RED_DRAGON_FHD = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.Skin_BoHLALA = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.NitroAdvanceFHD= ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.AL_AYAM_FHD = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])
config.plugins.TeamNitro.TNFonts = ConfigSelection(default="Press OK", choices = [
                                ("Press OK", _("Press OK"))
                                ])


# TNPath = ('/usr/share/enigma2/DesertFHD/',
#           '/usr/share/enigma2/RED_DRAGON_FHD/',
#           '/usr/share/enigma2/BoHLALA_FHD/',
#           '/usr/share/enigma2/NitroAdvanceFHD/',
#           '/usr/share/enigma2/AL_AYAM_FHD/',
#           '/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro')

#==========================================================================================#
### picon color##
COLOREPLUGIN=resolveFilename(SCOPE_PLUGINS, "Extensions/TeamNitro/PICONS/")

config.plugins.TeamNitro.piconpath = ConfigSelection(default = "PLUGIN", choices = [
    ("PLUGIN", _("PLUGIN")),
    ("MEDIA", _("MEDIA"))
    ])

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
mounted_devices = getmDevices()
config.plugins.TeamNitro.device_path = ConfigSelection(choices = mounted_devices)
if config.plugins.TeamNitro.piconpath.value == "MEDIA":
        PATHPICON = config.plugins.TeamNitro.device_path.value
elif config.plugins.TeamNitro.piconpath.value == "PLUGIN":
        PATHPICON = '/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro'

#==========================================================================================#
REDC = '\033[31m'
ENDC = '\033[m'
def cprint(text):
    print(REDC + text + ENDC)

def removeunicode(data):
    try:
        try:
                data = data.encode('utf', 'ignore')
        except:
                pass
        data = data.decode('unicode_escape').encode('ascii', 'replace').replace('?', '').strip()
    except:
        pass
    return data

def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/TeamNitro.log', 'a'))
    except:
        pass

def logdata(label_name = '', data = None):
    try:
        data=str(data)
        fp = open('/tmp/TeamNitro.log', 'a')
        fp.write( str(label_name) + ': ' + data+"\n")
        fp.close()
    except:
        trace_error()
        pass

def Plugins(**kwargs):
    return [PluginDescriptor(name=_("TeamNitro Control Center"), description=_("Access Multiple TeamNitro Options"), where = [PluginDescriptor.WHERE_PLUGINMENU],
    icon="plugin.png", fnc=main)]

def main(session, **kwargs):
    try:
        # Path to the plugin directory
        plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro"

        # Check for .pyc files in the plugin directory
        pyc_files = [f for f in os.listdir(plugin_path) if f.endswith(".pyc")]

        if pyc_files:
            # Remove all .py files if .pyc files exist
            py_files = [f for f in os.listdir(plugin_path) if f.endswith(".py")]
            for py_file in py_files:
                file_path = os.path.join(plugin_path, py_file)
                try:
                    os.remove(file_path)
                    #print(f"Deleted: {file_path}")
                    pass
                except Exception as e:
                    #print(f"Failed to delete {file_path}: {e}")
                    pass

        # Read the settings file
        with open("/etc/enigma2/settings", "r") as f:
            settings = f.readlines()

        # Find the current skin setting
        skin_setting = None
        for line in settings:
            if line.startswith("config.skin.primary_skin="):
                skin_setting = line.split("=")[1].strip()
                break

        # List of allowed skins
        allowed_skins = [
            "DesertFHD/skin.xml",
            "NitroAdvanceFHD/skin.xml",
            "RED_DRAGON_FHD/skin.xml",
            "BoHLALA_FHD/skin.xml",
            "AL_AYAM_FHD/skin.xml"
        ]

        # Check if the current skin is in the allowed list
        if skin_setting and skin_setting in allowed_skins:
            session.open(TeamNitro)  # Open the TeamNitro screen
        else:
            # Show error message
            session.open(MessageBox, _("This plugin requires a Team Nitro skin!"), type=MessageBox.TYPE_ERROR)

    except Exception as e:
        # Handle any unexpected errors
        session.open(MessageBox, _("An error occurred: ") + str(e), type=MessageBox.TYPE_ERROR)


def isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#==========================================================================================#
SKIN_VIEW = """
<screen name="MainSettingsView" position="0,0" size="1920,1080" title="Main Menu" flags="wfNoBorder" backgroundColor="transparent">
    <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
    <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
    <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
    <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
    <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
    <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
    <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
    <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
</screen>
    """

class TeamNitro(Screen, ConfigListScreen):

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.skin = SKIN_VIEW
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "ok": self.keyOk,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                        "green": self.keyGreen,
                }, -2)

        self["Picture"] = Pixmap()
        self.timer = eTimer()
        if config.plugins.TeamNitro.update.value:
            self.checkupdates()
        self.createConfigList()

    def createConfigList(self):
        self.set_proMode= getConfigListEntry(_("Pro. Additional Skins"), config.plugins.TeamNitro.proMode)
        self.set_skin_selection= getConfigListEntry(_("Change Skin"), config.plugins.TeamNitro.skin_selection)
        self.set_TNCleaner = getConfigListEntry(_("Delete Skin"), config.plugins.TeamNitro.skin_TNCleaner)
        self.set_MSNWeather= getConfigListEntry(_("WeatherMSN Settings"), config.plugins.TeamNitro.MSNWeather)
        self.set_skinDownload = getConfigListEntry(_("Download TeamNitro Skins "), config.plugins.TeamNitro.skinDownload)
        self.update = getConfigListEntry(_("Enable/Disable online update Info"), config.plugins.TeamNitro.update)
        self.set_TNChangelog= getConfigListEntry(_("Changelog"), config.plugins.TeamNitro.TNChangelog)
        self.set_TNAbout= getConfigListEntry(_("About TeamNitro"), config.plugins.TeamNitro.TNAbout)
        self.LackOfFile = ''
        self.list = []
        if config.skin.primary_skin.value == "DesertFHD/skin.xml":
             self.list.append(self.set_proMode)
        elif config.skin.primary_skin.value == "NitroAdvanceFHD/skin.xml":
             self.list.append(self.set_proMode)
        elif config.skin.primary_skin.value == "RED_DRAGON_FHD/skin.xml":
             self.list.append(self.set_proMode)
        elif config.skin.primary_skin.value == "BoHLALA_FHD/skin.xml":
             self.list.append(self.set_proMode)
        # elif config.skin.primary_skin.value == "KIII_PRO/skin.xml":
        #      self.list.append(self.set_proMode)
        elif config.skin.primary_skin.value == "AL_AYAM_FHD/skin.xml":
             self.list.append(self.set_proMode)
        else:
             pass
        self.list.append(self.set_skin_selection)
        self.list.append(self.set_TNCleaner)
        self.list.append(self.set_MSNWeather)
        self.list.append(self.set_skinDownload)
        self.list.append(self.update)
        self.list.append(self.set_TNChangelog)
        self.list.append(self.set_TNAbout)
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def keyGreen(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()
            self.restartGUI()

    def showSkinChoiceBox(self):
        self.guiRoot = resolveFilename(SCOPE_SKINS)
        choices = []
        for directory in [x for x in os.listdir(self.guiRoot) if os.path.isdir(os.path.join(self.guiRoot, x))]:
            skin_xml_path = os.path.join(self.guiRoot, directory, "skin.xml")
            if os.path.exists(skin_xml_path):
                label = _("< Default >") if directory == "skin_default" else directory
                choices.append((os.path.join(self.guiRoot, directory), label))
        self.session.openWithCallback(self.skinChoiceCallback, ChoiceBox, title=_("Select skin to delete"), list=choices)

    def skinChoiceCallback(self, choice):
        if choice:
            skinDirPath, skinLabel = choice
            print("[TeamNitro] Trying to delete skin: %s at %s" % (skinLabel, skinDirPath))
            if os.path.exists(skinDirPath):
                try:
                    shutil.rmtree(skinDirPath)
                    self.session.open(MessageBox, _("Skin '%s' has been deleted.") % skinLabel, MessageBox.TYPE_INFO)
                    print("[TeamNitro] Skin '%s' has been deleted." % skinLabel)
                except Exception as e:
                    self.session.open(MessageBox, _("Failed to delete skin '%s': %s") % (skinLabel, str(e)), MessageBox.TYPE_ERROR)
    def restartGUI(self):
        self.createConfigList()
        restartbox = self.session.openWithCallback(self.restartGUIcb, MessageBox, _("All Changes are Saved \n\n Restart necessary,\n PRESS OK to restart GUI now?"), MessageBox.TYPE_INFO)

    def restartGUIcb(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def cancel(self):

        if self["config"].isChanged():
            self.session.openWithCallback(self.cancelConfirm, MessageBox, _("DO you want to close without saving the settings?\n\n\n Press The Green Button for Saving the Settings"), MessageBox.TYPE_YESNO, default = False)
        else:
            for x in self["config"].list:
                x[1].cancel()
            if self.changed_screens:
                self.restartGUI()
            else:
                self.close()



    def keyOk(self):
        sel = self["config"].getCurrent()
        if sel is not None:
            if sel == self.set_proMode:
                self.session.open(TeamNitro_Config)
            elif sel == self.set_MSNWeather:
                self.session.open(WeatherMSN)
            elif sel == self.set_skinDownload:
                self.session.open(SkinDownload)
            elif sel == self.set_TNChangelog:
                self.session.open(TeamNitro_Changelog)
            elif sel == self.set_TNAbout:
                self.session.open(TeamNitro_About)
            elif sel == self.set_skin_selection:
                self.session.openWithCallback(self.skinChanged, SkinSelection)
            elif sel == self.set_TNCleaner:
                self.showSkinChoiceBox()

    def skinChanged(self, ret = None):
        global cur_skin
        cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')
        if cur_skin == "skin.xml":
            self.restartGUI()
        else:
            return

    def checkupdates(self):
        url1=[]
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/InstallerN.sh')
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh')
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerB.sh')
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh')
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerAL.sh')
        url1.append('https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/plugin.sh')
        for url in url1:
            self.callUrl(url, self.checkVer)

    def checkVer(self, data):
        import os
        currversion =[]
        version_file = '/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/TN_Skins_version'
        if os.path.exists(version_file):
                try:
                    fp = open(version_file, 'r').readlines()
                    for line in fp:
                        if 'versionNitro' in line:
                            currversion.append(line.split('=')[1].strip())
                        elif 'versionDragon' in line:
                            currversion.append(line.split('=')[1].strip())
                        elif 'versionBoHlala' in line:
                            currversion.append(line.split('=')[1].strip())
                        elif 'versionDesert' in line:
                            currversion.append(line.split('=')[1].strip())
                        elif 'versionPlugin' in line:
                            currversion.append(line.split('=')[1].strip())
                        elif 'versionAL_AYAM_FHD' in line:
                            currversion.append(line.split('=')[1].strip())
                except:
                    pass

        if PY3:
            data = data.decode("utf-8")
        else:
            data = data.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                   self.new_version = line.split("=")[1]
                if line.startswith("description"):
                   self.new_description = line.split("=")[1]
                   break
        new_descriptiona=self.new_description
        if new_descriptiona.find("Skin_Nitro")==1:
           Ver=currversion[0]
        elif new_descriptiona.find("Skin_Dragon")==1:
             Ver=currversion[1]
        elif new_descriptiona.find("BoHlala")==1:
             Ver=currversion[2]
        elif new_descriptiona.find("Skin_Desert")==1:
             Ver=currversion[3]
        elif new_descriptiona.find("ControlCenter")==1:
             Ver=currversion[4]
        elif new_descriptiona.find("AL_AYAM_FHD")==1:
             Ver=currversion[4]

        if float(Ver) == float(self.new_version) or float(Ver) > float(self.new_version):
            pass
        else:
            new_descriptiona=self.new_description
            self.session.open( MessageBox, _(' \n ========= An Update is available for========= \n\n%s\n\n  *****   Updates are in the plugin downloads     ***** \n\nPress (-OK or Exit-) to remove or view other INFO  ' % (new_descriptiona)), MessageBox.TYPE_INFO)

    def myCallback(self, result=None):
        return

    def callUrl(self, url, callback):
        try:
            from twisted.web.client import getPage
            getPage(str.encode(url), headers={b'Content-Type': b'application/x-www-form-urlencoded'}).addCallback(callback).addErrback(self.addErrback)
        except:
            pass

    def addErrback(self, error=None):
        pass
#==========================================================================================#
#Picon Download Screens
class PiconDownload(Screen):
        skin = """
        <screen name="PiconDownload" position="0,0" size="1920,1080" title="TeamNitro Picons Download" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget name="Picture" position="1186,137" size="680,400" alphatest="blend" />
            <widget source="Title" render="Label" position="288,116" size="752,68" zPosition="1" halign="center" font="Regular;36" backgroundColor="bglist" transparent="1" />
            <widget name="menu" position="247,199" size="830,622" font="Regular; 35" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" scrollbarMode="showNever" transparent="1" zPosition="1" />
        </screen>
            """
        def __init__(self, session, args = 0):
                self.session = session
                self.changed_screens = False
                Screen.__init__(self, session)
                self.TeamNitro_fake_entry = NoSave(ConfigNothing())
                self["setupActions"] = ActionMap(["SetupActions"],
                {
                        "cancel": self.cancel,
                        "ok": self.installPicon

                }, -1)
                self["Picture"] = Pixmap()
                list = []
                list.append((_("Black Picons"), "Black"))
                list.append((_("White Picons"), "White"))
                list.append((_("Transparent Picons"), "Transparent"))
                list.append((_("zelda Picon"), "zeldaPicon"))
                self["menu"] = MenuList(list)
                self["menu"].onSelectionChanged.append(self.Picture)
                self.onShow.append(self.Picture)
                self.onLayoutFinish.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("TeamNitro Satellite Provider Picons Download"))

        def Picture(self):
                try:
                        index = self["menu"].l.getCurrentSelection()[1]
                        if index == "Black":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/BlackPicon.png')
                        elif index == "White":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/WhitePicon.png')
                        elif index == "Transparent":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/TransparentPicon.png')
                        elif index == "zeldaPicon":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/zeldaPicon.png')
                        self['Picture'].instance.setPixmapFromFile(pic)
                except Exception as error:
                        logdata("Picture preview:", error)

        def installPicon(self):
                self.session.open(MessageBox, _('=======   Picon Downloads is Finished ======= '), MessageBox.TYPE_INFO, timeout=7)
                try:
                        index = self["menu"].l.getCurrentSelection()[1]
                        PICONTMP='/tmp/emu'
                        PICONTMP1='/tmp/piconCrypt'
                        PICONTMP2='/tmp/piconProv'
                        PICONTMP3='/tmp/piconSat'
                        if index == "Black":
                                os.system("wget --no-check-certificate -O '/tmp/BlackPicons2.tar.gz' 'https://github.com/biko-73/TeamNitro/raw/main/picon/BlackPicons2.tar.gz'")
                                os.system("tar -xzf /tmp/BlackPicons2.tar.gz -C /")

                        elif index == "White":
                                os.system("wget --no-check-certificate -O '/tmp/WhitePicons.tar.gz' 'https://github.com/biko-73/TeamNitro/raw/main/picon/WhitePicons.tar.gz'")
                                os.system("tar -xzf /tmp/WhitePicons.tar.gz -C /")
                        elif index == "Transparent":
                                os.system("wget --no-check-certificate -O '/tmp/TransparentPicons.tar.gz' 'https://github.com/biko-73/TeamNitro/raw/main/picon/TransparentPicons.tar.gz'")
                                os.system("tar -xzf /tmp/TransparentPicons.tar.gz -C /")
                        elif index == "zeldaPicon":
                                os.system("wget --no-check-certificate -O '/tmp/zeldaPicon.tar.gz' 'https://github.com/biko-73/TeamNitro/raw/main/picon/zeldaPicon.tar.gz'")
                                os.system("tar -xzf /tmp/zeldaPicon.tar.gz -C /")

                        if pathExists(PATHPICON + '/emu'):
                            shutil.rmtree(PATHPICON + '/emu')
                        if pathExists(PATHPICON + '/piconCrypt'):
                            shutil.rmtree(PATHPICON + '/piconCrypt')
                        if pathExists(PATHPICON + '/piconProv'):
                            shutil.rmtree(PATHPICON + '/piconProv')
                        if pathExists(PATHPICON + '/piconSat'):
                            shutil.rmtree(PATHPICON + '/piconSat')
                        shutil.move(PICONTMP, PATHPICON)
                        shutil.move(PICONTMP1, PATHPICON)
                        shutil.move(PICONTMP2, PATHPICON)
                        shutil.move(PICONTMP3, PATHPICON)
                        os.system("rm -rf /tmp/*emu*")
                        os.system("rm -rf /tmp/*piconCrypt*")
                        os.system("rm -rf /tmp/*piconProv*")
                        os.system("rm -rf /tmp/*piconSat*")
                        self.session.open(MessageBox, _('=== Picon Downloads is Started ===>> ===>>'), MessageBox.TYPE_INFO, timeout=5)
                except:
                       self.session.open(MessageBox, _('=======   Picon Downloads is Failed ======= '), MessageBox.TYPE_INFO, timeout=3)
                       pass
        def myCallback(self, result=None):
            return
        def cancel(self):
                self.close()

#==========================================================================================#
#Skin Download Screens
class SkinDownload(Screen):
        skin = """
        <screen name="SkinDownload" position="0,0" size="1920,1080" title="TeamNitro Skin Download" backgroundColor="transparent">
                <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
                <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
                <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
                <widget name="Picture" position="1186,137" size="680,400" alphatest="blend" />
                <widget source="Title" render="Label" position="288,116" size="752,68" zPosition="1" halign="center" font="Regular;36" backgroundColor="bglist" transparent="1" />
                <widget name="menu" position="247,199" size="830,622" font="Regular; 35" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" scrollbarMode="showNever" transparent="1" zPosition="1" />
                <eLabel text="Select and Press OK to Download Skins" position="252,856" size="820,40" font="Regular; 32" foregroundColor="#ff2525" backgroundColor="#16000000" valign="center" halign="center" transparent="1" zPosition="5" />
                <eLabel text="Select TeamNitro Skins Form the Plugin Skin Selector Main Menu" position="251,915" size="820,90" font="Regular; 38" foregroundColor="#bab329" backgroundColor="#16000000" valign="center" halign="center" transparent="1" zPosition="5" />
        </screen>
            """
        def __init__(self, session, args = 0):
                self.session = session
                self.changed_screens = False
                Screen.__init__(self, session)
                self.TeamNitro_fake_entry = NoSave(ConfigNothing())
                self["setupActions"] = ActionMap(["SetupActions"],
                {
                        "cancel": self.cancel,
                        "ok": self.DownloadSkin
                }, -1)

                self["Picture"] = Pixmap()
                list = []
                list.append((_("TeamNitro Control Center"), "ControlCenter"))
                list.append((_("NitroAdvance FHD"), "NitroAdvanceFHD"))
                list.append((_("Dragon FHD"), "DragonFHD"))
                list.append((_("Team_Nitro-by_BoHlala-V_1.2L"), "BoHlalaFHD"))
                list.append((_("Desert FHD"), "DesertFHD"))
                # list.append((_("KIII PRO"), "KIII_PRO"))
                list.append((_("AL AYAM FHD"), "AL_AYAM_FHD"))
                list.append((_("skyTeamNitro"), "skyTeamNitro"))
                self["menu"] = MenuList(list)
                self["menu"].onSelectionChanged.append(self.Picture)
                self.onShow.append(self.Picture)
                self.onLayoutFinish.append(self.setWindowTitle)

        def setWindowTitle(self):
                self.setTitle(_("TeamNitro Skins Download"))

        def Picture(self):
                try:
                        index = self["menu"].l.getCurrentSelection()[1]
                        if index == "DragonFHD":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/DragonFHD.png')
                        elif index == "NitroAdvanceFHD":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/NitroAdvanceFHD.png')
                        elif index == "DesertFHD":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/DesertFHD.png')
                        elif index == "BoHlalaFHD":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/BoHlala_FHD.png')
                        # elif index == "KIII_PRO":
                        #         pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/KIII_PRO.png')
                        elif index == "AL_AYAM_FHD":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/AL_AYAM_FHD.png')
                        elif index == "ControlCenter":
                                pic = resolveFilename(SCOPE_PLUGINS, 'Extensions/TeamNitro/images/preview/ControlCenter.png')
                        self['Picture'].instance.setPixmapFromFile(pic)
                except Exception as error:
                        logdata("Picture preview:", error)

        def DownloadSkin(self):
                self.session.openWithCallback(self.installSkin, MessageBox, _('Do you want to Download it now ?!!'), MessageBox.TYPE_YESNO)

        def installSkin(self, answer=False):
                try:
                        if answer:
                            cmdlist = []
                            index = self["menu"].l.getCurrentSelection()[1]
                            if index == "DragonFHD":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh -O - | /bin/sh')
                                self.session.open(Console, title='Download TeamNitro Skin DragonFHD', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "NitroAdvanceFHD":
                                cmdlist.append('wget -q "--no-check-certificate"  https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerN.sh -O - | /bin/sh ')
                                self.session.open(Console, title='Download TeamNitro Skin NitroAdvanceFHD', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "DesertFHD":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh -O - | /bin/sh')
                                self.session.open(Console, title='Download TeamNitro Skin DesertFHD', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "BoHlalaFHD":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerB.sh -O - | /bin/sh')
                                self.session.open(Console, title='Download TeamNitro Skin BoHlala_FHD', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            # elif index == "KIII_PRO":
                            #     cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerKIII.sh -O - | /bin/sh')
                            #     self.session.open(Console, title='Download TeamNitro Skin KIII_PRO', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "AL_AYAM_FHD":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerAL.sh -O - | /bin/sh')
                                self.session.open(Console, title='Download TeamNitro Skin AL_AYAM_FHD', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "skyTeamNitro":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerSky.sh -O - | /bin/sh')
                                self.session.open(Console, title='Update TeamNitro Sky', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)

                            elif index == "ControlCenter":
                                cmdlist.append('wget -q "--no-check-certificate" https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/plugin.sh -O - | /bin/sh')
                                self.session.open(Console, title='Download TeamNitro Control Center', cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)
                        else:
                            self.close()
                except:
                    trace_error()
                    pass

        def myCallback(self, result=None):
            return

        def cancel(self):
            self.close()



#==========================================================================================#

SKIN_VIEW = """
<screen name="TeamNitro_Config" position="0,0" size="1920,1080" title="TeamNitro ProMode" flags="wfNoBorder" backgroundColor="transparent">
    <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
    <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
    <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
    <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
    <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
    <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
    <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
    <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
</screen>
    """
class TeamNitro_Config(Screen, ConfigListScreen):

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.skin = SKIN_VIEW
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "ok": self.keyOk,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                        "green": self.keyGreen,
                }, -2)

        self["Picture"] = Pixmap()
        self.createConfigList()


    def createConfigList(self):
        self.set_DesertFHD = getConfigListEntry(_("DesertFHD "), config.plugins.TeamNitro.DesertFHD)
        self.set_RED_DRAGON_FHD = getConfigListEntry(_("RED_DRAGON_FHD"), config.plugins.TeamNitro.RED_DRAGON_FHD)
        self.set_NitroAdvanceFHD = getConfigListEntry(_("NitroAdvanceFHD"), config.plugins.TeamNitro.NitroAdvanceFHD)
        self.set_BoHLALA_FHD = getConfigListEntry(_("BoHLALA_FHD"), config.plugins.TeamNitro.Skin_BoHLALA)
        # self.set_KIII_PRO = getConfigListEntry(_("KIII_PRO "), config.plugins.TeamNitro.KIII_PRO)
        self.set_AL_AYAM_FHD = getConfigListEntry(_("AL_AYAM_FHD"), config.plugins.TeamNitro.AL_AYAM_FHD)
        self.set_TNFonts = getConfigListEntry(_("TNFonts "), config.plugins.TeamNitro.TNFonts)
        self.set_piconDownload = getConfigListEntry(_("Download TeamNitro Picon "), config.plugins.TeamNitro.piconDownload)
        self.set_piconpath = getConfigListEntry(_("Select Path of Picons Folder"), config.plugins.TeamNitro.piconpath)
        self.set_mounted_devices = getConfigListEntry(_("Select mount device"), config.plugins.TeamNitro.device_path)
        self.LackOfFile = ''
        self.list = []
        if  os.path.isdir("/usr/share/enigma2/DesertFHD/"):
            self.list.append(self.set_DesertFHD)
        if  os.path.isdir("/usr/share/enigma2/BoHLALA_FHD/"):
            self.list.append(self.set_BoHLALA_FHD)
        if  os.path.isdir("/usr/share/enigma2/RED_DRAGON_FHD/"):
            self.list.append(self.set_RED_DRAGON_FHD)
        if  os.path.isdir("/usr/share/enigma2/NitroAdvanceFHD/"):
            self.list.append(self.set_NitroAdvanceFHD)
        # if  os.path.isdir("/usr/share/enigma2/KIII_PRO/"):
        #     self.list.append(self.set_KIII_PRO)
        if  os.path.isdir("/usr/share/enigma2/AL_AYAM_FHD/"):
            self.list.append(self.set_AL_AYAM_FHD)
        self.list.append(self.set_TNFonts)
        self.list.append(self.set_piconDownload)
        self.list.append(self.set_piconpath)
        if config.plugins.TeamNitro.piconpath.value == 'MEDIA':
            self.list.append(self.set_mounted_devices)
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def keyGreen(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()
            self.restartGUI()


    def cancel(self):
        self.session.openWithCallback(self.cancelConfirm, MessageBox, _("DO you want close without saving the settings?"), MessageBox.TYPE_YESNO, default = False)
        # self.session.open(MessageBox, _('=======   Picon Downloads is Finished ======= '), MessageBox.TYPE_INFO, timeout=7)

    def cancelConfirm(self, result):
        if result == None or result == False:
            print("[%s]: Cancel confirmed." % cur_skin)
        else:
            print("[%s]: Cancel confirmed. Config changes will be lost." % cur_skin)
            for x in self["config"].list:
                x[1].cancel()
            self.close()


    def restartGUI(self):
        myMessage = ''
        if self.LackOfFile != '':
            cprint("missing components: %s" % self.LackOfFile)
            myMessage += _("Missing components found: %s\n\n") % self.LackOfFile
            myMessage += _("Skin will NOT work properly!!!\n\n")
        restartbox = self.session.openWithCallback(self.restartGUIcb, MessageBox, _("Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Message"))

    def restartGUIcb(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def keyOk(self):
        sel =  self["config"].getCurrent()
        if sel != None and sel == self.set_DesertFHD:
            self.session.open(DesertFHD)

        elif sel != None and sel == self.set_RED_DRAGON_FHD:
            self.session.open(RED_DRAGON_FHD)

        elif sel != None and sel == self.set_BoHLALA_FHD:
            self.session.open(BoHLALA_FHD)

        elif sel != None and sel == self.set_NitroAdvanceFHD:
            self.session.open(NitroAdvanceFHD)

        elif sel != None and sel == self.set_AL_AYAM_FHD:
            self.session.open(AL_AYAM_FHD)

        # elif sel != None and sel == self.set_KIII_PRO:
        #     self.session.open(KIII_PRO)

        elif sel != None and sel == self.set_TNFonts:
            self.session.open(TNFonts)

        elif sel != None and sel == self.set_piconDownload:
            self.session.open(PiconDownload)
        else:
            pass


#==========================================================================================#
class DesertFHD(Screen, ConfigListScreen):

    skin = """

        <screen name="DesertFHD" position="0,0" size="1920,1080" title="DesertFHD PRO-MOD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO SKINS Setup")
        self.skin_base_dir = "/usr/share/enigma2/DesertFHD/"
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
#DesertFHD
        self.default_DesertFHD_file = "DesertFHD_Original.xml"
        self.DesertFHD_file = "skin_user_DesertFHD.xml"
        current, choices = self.getSettings(self.default_DesertFHD_file, self.DesertFHD_file)
        self.TeamNitro_DesertFHD = NoSave(ConfigSelection(default=current, choices = choices))
#Basic
        self.default_Basic_file = "Basic_Original.xml"
        self.Basic_file = "skin_user_Basic.xml"
        current, choices = self.getSettings(self.default_Basic_file, self.Basic_file)
        self.TeamNitro_Basic = NoSave(ConfigSelection(default=current, choices = choices))
#TNPosterX
        self.default_TNPosterX_file = "TNPosterX_Original.xml"
        self.TNPosterX_file = "skin_user_TNPosterX.xml"
        current, choices = self.getSettings(self.default_TNPosterX_file, self.TNPosterX_file)
        self.TeamNitro_TNPosterX = NoSave(ConfigSelection(default=current, choices = choices))
#xtraEvent
        self.default_xtraEvent_file = "xtraEvent_Original.xml"
        self.xtraEvent_file = "skin_user_xtraEvent.xml"
        current, choices = self.getSettings(self.default_xtraEvent_file, self.xtraEvent_file)
        self.TeamNitro_xtraEvent = NoSave(ConfigSelection(default=current, choices = choices))
#PluginBrowser
        self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
        self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
        current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
        self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
#skyTeamNitro
        self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
        self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
        current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
        self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())




    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Selections")
                except:
                    pass

    def createConfigList(self):
        self.set_DesertFHD = getConfigListEntry(_("DesertFHD:"), self.TeamNitro_DesertFHD)
        self.set_Basic = getConfigListEntry(_("Basic:"), self.TeamNitro_Basic)
        self.set_TNPosterX = getConfigListEntry(_("TNPosterX:"), self.TeamNitro_TNPosterX)
        self.set_xtraEvent = getConfigListEntry(_("xtraEvent:"), self.TeamNitro_xtraEvent)
        self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
        self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []



        if len(self.TeamNitro_DesertFHD.choices)>1:
            self.list.append(self.set_DesertFHD)
        if len(self.TeamNitro_Basic.choices)>1:
            self.list.append(self.set_Basic)
        if len(self.TeamNitro_TNPosterX.choices)>1:
            self.list.append(self.set_TNPosterX)
        if len(self.TeamNitro_xtraEvent.choices)>1:
            self.list.append(self.set_xtraEvent)
        if len(self.TeamNitro_PluginBrowser.choices)>1:
            self.list.append(self.set_PluginBrowser)
        if len(self.TeamNitro_skyTeamNitro.choices)>1:
            self.list.append(self.set_skyTeamNitro)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_DesertFHD:
            self.setPicture(self.TeamNitro_DesertFHD.value)
        elif self["config"].getCurrent() == self.set_Basic:
            self.setPicture(self.TeamNitro_Basic.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_DesertFHD:
            self.setPicture(self.TeamNitro_DesertFHD.value)
        elif self["config"].getCurrent() == self.set_Basic:
            self.setPicture(self.TeamNitro_Basic.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_DesertFHD, self.DesertFHD_file)
            self.makeSettings(self.TeamNitro_Basic, self.Basic_file)
            self.makeSettings(self.TeamNitro_TNPosterX, self.TNPosterX_file)
            self.makeSettings(self.TeamNitro_xtraEvent, self.xtraEvent_file)
            self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
            self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)

            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.DesertFHD_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.DesertFHD_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.Basic_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.Basic_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.TNPosterX_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.TNPosterX_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.xtraEvent_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.xtraEvent_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.PluginBrowser_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent


#==========================================================================================#
class NitroAdvanceFHD(Screen, ConfigListScreen):

    skin = """

        <screen name="NitroAdvanceFHD" position="0,0" size="1920,1080" title="NitroAdvanceFHD PRO-MOD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO SKINS Setup")
        self.skin_base_dir = "/usr/share/enigma2/NitroAdvanceFHD/"
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
#NitroAdvanceFHD
        self.default_NitroAdvanceFHD_file = "NitroAdvanceFHD_Original.xml"
        self.NitroAdvanceFHD_file = "skin_user_NitroAdvanceFHD.xml"
        current, choices = self.getSettings(self.default_NitroAdvanceFHD_file, self.NitroAdvanceFHD_file)
        self.TeamNitro_NitroAdvanceFHD = NoSave(ConfigSelection(default=current, choices = choices))
#color
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
        current, choices = self.getSettings(self.default_color_file, self.color_file)
        self.TeamNitro_color = NoSave(ConfigSelection(default=current, choices = choices))
#interface
        self.default_interface_file = "interface_Original.xml"
        self.interface_file = "skin_user_interface.xml"
        current, choices = self.getSettings(self.default_interface_file, self.interface_file)
        self.TeamNitro_interface = NoSave(ConfigSelection(default=current, choices = choices))
#posterX
        self.default_posterX_file = "posterX_Original.xml"
        self.posterX_file = "skin_user_posterX.xml"
        current, choices = self.getSettings(self.default_posterX_file, self.posterX_file)
        self.TeamNitro_posterX = NoSave(ConfigSelection(default=current, choices = choices))
#xtraEvent
        self.default_xtraEvent_file = "xtraEvent_Original.xml"
        self.xtraEvent_file = "skin_user_xtraEvent.xml"
        current, choices = self.getSettings(self.default_xtraEvent_file, self.xtraEvent_file)
        self.TeamNitro_xtraEvent = NoSave(ConfigSelection(default=current, choices = choices))
#PluginBrowser
        self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
        self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
        current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
        self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
#skyTeamNitro
        self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
        self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
        current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
        self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())




    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Selections")
                except:
                    pass

    def createConfigList(self):
        self.set_NitroAdvanceFHD = getConfigListEntry(_("NitroAdvanceFHD:"), self.TeamNitro_NitroAdvanceFHD)
        self.set_color = getConfigListEntry(_("Colors:"), self.TeamNitro_color)
        self.set_interface = getConfigListEntry(_("Interface:"), self.TeamNitro_interface)
        self.set_posterX = getConfigListEntry(_("posterX:"), self.TeamNitro_posterX)
        self.set_xtraEvent = getConfigListEntry(_("xtraEvent:"), self.TeamNitro_xtraEvent)
        self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
        self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []



        if len(self.TeamNitro_NitroAdvanceFHD.choices)>1:
            self.list.append(self.set_NitroAdvanceFHD)
        if len(self.TeamNitro_color.choices)>1:
            self.list.append(self.set_color)
        if len(self.TeamNitro_interface.choices)>1:
            self.list.append(self.set_interface)
        if len(self.TeamNitro_posterX.choices)>1:
            self.list.append(self.set_posterX)
        if len(self.TeamNitro_xtraEvent.choices)>1:
            self.list.append(self.set_xtraEvent)
        if len(self.TeamNitro_PluginBrowser.choices)>1:
            self.list.append(self.set_PluginBrowser)
        if len(self.TeamNitro_skyTeamNitro.choices)>1:
            self.list.append(self.set_skyTeamNitro)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_NitroAdvanceFHD:
            self.setPicture(self.TeamNitro_NitroAdvanceFHD.value)
        elif self["config"].getCurrent() == self.set_color:
            self.setPicture(self.TeamNitro_color.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_posterX:
            self.setPicture(self.TeamNitro_posterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_NitroAdvanceFHD:
            self.setPicture(self.TeamNitro_NitroAdvanceFHD.value)
        elif self["config"].getCurrent() == self.set_color:
            self.setPicture(self.TeamNitro_color.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_posterX:
            self.setPicture(self.TeamNitro_posterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def cancelConfirm(self, result):
        if result == None or result == False:
            print("[%s]: Cancel confirmed." % cur_skin)
        else:
            print("[%s]: Cancel confirmed. Config changes will be lost." % cur_skin)
            for x in self["config"].list:
                x[1].cancel()
            self.close()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_NitroAdvanceFHD, self.NitroAdvanceFHD_file)
            self.makeSettings(self.TeamNitro_color, self.color_file)
            self.makeSettings(self.TeamNitro_interface, self.interface_file)
            self.makeSettings(self.TeamNitro_posterX, self.posterX_file)
            self.makeSettings(self.TeamNitro_xtraEvent, self.xtraEvent_file)
            self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
            self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)
            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.NitroAdvanceFHD_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.NitroAdvanceFHD_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.color_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.color_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.interface_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.interface_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.posterX_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.posterX_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.xtraEvent_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.xtraEvent_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.PluginBrowser_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent


#==========================================================================================#
class RED_DRAGON_FHD(Screen, ConfigListScreen):

    skin = """

        <screen name="RED_DRAGON_FHD" position="0,0" size="1920,1080" title="RED_DRAGON_FHD PRO-MOD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO SKINS Setup")
        self.skin_base_dir = "/usr/share/enigma2/RED_DRAGON_FHD/"
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
#channelselection
        self.default_channelselections_file = "channelselections_Original.xml"
        self.channelselections_file = "skin_user_channelselections.xml"
        current, choices = self.getSettings(self.default_channelselections_file, self.channelselections_file)
        self.TeamNitro_channelselections = NoSave(ConfigSelection(default=current, choices = choices))
#infobar
        self.default_infobars_file = "infobars_Original.xml"
        self.infobars_file = "skin_user_infobars.xml"
        current, choices = self.getSettings(self.default_infobars_file, self.infobars_file)
        self.TeamNitro_infobars = NoSave(ConfigSelection(default=current, choices = choices))
#interface
        self.default_interface_file = "interface_Original.xml"
        self.interface_file = "skin_user_interface.xml"
        current, choices = self.getSettings(self.default_interface_file, self.interface_file)
        self.TeamNitro_interface = NoSave(ConfigSelection(default=current, choices = choices))
#posterX
        self.default_posterX_file = "posterX_Original.xml"
        self.posterX_file = "skin_user_posterX.xml"
        current, choices = self.getSettings(self.default_posterX_file, self.posterX_file)
        self.TeamNitro_posterX = NoSave(ConfigSelection(default=current, choices = choices))
#secondinfobar
        self.default_secondinfobar_file = "secondinfobar_Original.xml"
        self.secondinfobar_file = "skin_user_secondinfobar.xml"
        current, choices = self.getSettings(self.default_secondinfobar_file, self.secondinfobar_file)
        self.TeamNitro_secondinfobar = NoSave(ConfigSelection(default=current, choices = choices))
#PluginBrowser
        self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
        self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
        current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
        self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
#skyTeamNitro
        self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
        self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
        current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
        self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())




    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Selections")
                except:
                    pass

    def createConfigList(self):
        self.set_interface = getConfigListEntry(_("interface:"), self.TeamNitro_interface)
        self.set_infobars = getConfigListEntry(_("infobars:"), self.TeamNitro_infobars)
        self.set_secondinfobar = getConfigListEntry(_("secondinfobar:"), self.TeamNitro_secondinfobar)
        self.set_channelselections = getConfigListEntry(_("channelselections:"), self.TeamNitro_channelselections)
        self.set_posterX = getConfigListEntry(_("posterX:"), self.TeamNitro_posterX)
        self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
        self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []
        if len(self.TeamNitro_channelselections.choices)>1:
            self.list.append(self.set_channelselections)
        if len(self.TeamNitro_infobars.choices)>1:
            self.list.append(self.set_infobars)
        if len(self.TeamNitro_interface.choices)>1:
            self.list.append(self.set_interface)
        if len(self.TeamNitro_posterX.choices)>1:
            self.list.append(self.set_posterX)
        if len(self.TeamNitro_secondinfobar.choices)>1:
            self.list.append(self.set_secondinfobar)
        if len(self.TeamNitro_PluginBrowser.choices)>1:
            self.list.append(self.set_PluginBrowser)
        if len(self.TeamNitro_skyTeamNitro.choices)>1:
            self.list.append(self.set_skyTeamNitro)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_channelselections:
            self.setPicture(self.TeamNitro_channelselections.value)
        elif self["config"].getCurrent() == self.set_infobars:
            self.setPicture(self.TeamNitro_infobars.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_posterX:
            self.setPicture(self.TeamNitro_posterX.value)
        elif self["config"].getCurrent() == self.set_secondinfobar:
            self.setPicture(self.TeamNitro_secondinfobar.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_channelselections:
            self.setPicture(self.TeamNitro_channelselections.value)
        elif self["config"].getCurrent() == self.set_infobars:
            self.setPicture(self.TeamNitro_infobars.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_posterX:
            self.setPicture(self.TeamNitro_posterX.value)
        elif self["config"].getCurrent() == self.set_secondinfobar:
            self.setPicture(self.TeamNitro_secondinfobar.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def cancelConfirm(self, result):
        if result == None or result == False:
            print("[%s]: Cancel confirmed." % cur_skin)
        else:
            print("[%s]: Cancel confirmed. Config changes will be lost." % cur_skin)
            for x in self["config"].list:
                x[1].cancel()
            self.close()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_channelselections, self.channelselections_file)
            self.makeSettings(self.TeamNitro_infobars, self.infobars_file)
            self.makeSettings(self.TeamNitro_interface, self.interface_file)
            self.makeSettings(self.TeamNitro_posterX, self.posterX_file)
            self.makeSettings(self.TeamNitro_secondinfobar, self.secondinfobar_file)
            self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
            self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)
            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.channelselections_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.channelselections_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.infobars_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.infobars_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.interface_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.interface_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.posterX_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.posterX_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.secondinfobar_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.secondinfobar_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.PluginBrowser_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent
#==========================================================================================#
# class KIII_PRO(Screen, ConfigListScreen):

#     skin = """

#         <screen name="KIII_PRO" position="0,0" size="1920,1080" title="KIII_PRO" backgroundColor="transparent">
#             <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
#             <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
#             <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
#             <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
#             <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
#             <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
#             <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
#             <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
#             <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
#             <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
#         </screen>
#     """

#     def __init__(self, session, args = 0):
#         self.session = session
#         self.changed_screens = False
#         Screen.__init__(self, session)
#         self.start_skin = config.skin.primary_skin.value
#         if self.start_skin != "skin.xml":
#             self.getInitConfig()
#         self.list = []
#         ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
#         self.configChanged = False
#         self["key_red"] = Label(_("Cancel"))
#         self["key_green"] = Label(_("Save Changes"))
#         self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
#                 {
#                         "green": self.keyGreen,
#                         "red": self.cancel,
#                         "cancel": self.cancel,
#                         "right": self.keyRight,
#                         "left": self.keyLeft,
#                 }, -2)
#         self["Picture"] = Pixmap()
#         self.createConfigList()

#     def getInitConfig(self):
#         global cur_skin
#         self.title = _("PRO SKINS Setup")
#         self.skin_base_dir = "/usr/share/enigma2/KIII_PRO/"
#         cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
#         self.default_font_file = "font_Original.xml"
#         self.font_file = "skin_user_font.xml"
#         self.default_color_file = "color_Original.xml"
#         self.color_file = "skin_user_color.xml"
# #KIII_PRO
#         self.default_KIII_PRO_file = "KIII_PRO_Original.xml"
#         self.KIII_PRO_file = "skin_user_KIII_PRO.xml"
#         current, choices = self.getSettings(self.default_KIII_PRO_file, self.KIII_PRO_file)
#         self.TeamNitro_KIII_PRO = NoSave(ConfigSelection(default=current, choices = choices))
# #interface
#         self.default_interface_file = "interface_Original.xml"
#         self.interface_file = "skin_user_interface.xml"
#         current, choices = self.getSettings(self.default_interface_file, self.interface_file)
#         self.TeamNitro_interface = NoSave(ConfigSelection(default=current, choices = choices))
# #TNPosterX
#         self.default_TNPosterX_file = "TNPosterX_Original.xml"
#         self.TNPosterX_file = "skin_user_TNPosterX.xml"
#         current, choices = self.getSettings(self.default_TNPosterX_file, self.TNPosterX_file)
#         self.TeamNitro_TNPosterX = NoSave(ConfigSelection(default=current, choices = choices))
# #xtraEvent
#         self.default_xtraEvent_file = "xtraEvent_Original.xml"
#         self.xtraEvent_file = "skin_user_xtraEvent.xml"
#         current, choices = self.getSettings(self.default_xtraEvent_file, self.xtraEvent_file)
#         self.TeamNitro_xtraEvent = NoSave(ConfigSelection(default=current, choices = choices))
# #PluginBrowser
#         self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
#         self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
#         current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
#         self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
# #skyTeamNitro
#         self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
#         self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
#         current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
#         self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# # myatile
#         myatile_active = self.getmyAtileState()
#         self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
#         self.TeamNitro_fake_entry = NoSave(ConfigNothing())




#     def getSettings(self, default_file, user_file):
#         # default setting
#         default = ("default", _("Default"))

#         # search typ
#         styp = default_file.replace('_Original.xml', '')
#         search_str = '%s_' % styp

#         # possible setting
#         choices = []
#         files = listdir(self.skin_base_dir)
#         if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
#             files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
#         for f in sorted(files, key=str.lower):
#             if f.endswith('.xml') and f.startswith(search_str):
#                 friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
#                 if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
#                     choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
#                 else:
#                     choices.append((self.skin_base_dir + f, friendly_name))
#         choices.append(default)

#         # current setting
#         myfile = self.skin_base_dir + user_file
#         current = ''
#         if not path.exists(myfile):
#             if path.exists(self.skin_base_dir + default_file):
#                 if path.islink(myfile):
#                     remove(myfile)
#                 chdir(self.skin_base_dir)
#                 symlink(default_file, user_file)
#             elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
#                 if path.islink(myfile):
#                     remove(myfile)
#                 chdir(self.skin_base_dir)
#                 symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
#             else:
#                 current = None
#         if current is None:
#             current = default
#         else:
#             filename = path.realpath(myfile)
#             friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
#             current = (filename, friendly_name)

#         return current[0], choices
#         if path.exists(self.skin_base_dir + "mySkin_off"):
#             if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
#                 chdir(self.skin_base_dir)
#                 try:
#                     rename("mySkin_off", "TeamNitro_Selections")
#                 except:
#                     pass

#     def createConfigList(self):
#         self.set_KIII_PRO = getConfigListEntry(_("KIII_PRO:"), self.TeamNitro_KIII_PRO)
#         self.set_Basic = getConfigListEntry(_("Interface:"), self.TeamNitro_interface)
#         self.set_TNPosterX = getConfigListEntry(_("TNPosterX:"), self.TeamNitro_TNPosterX)
#         self.set_xtraEvent = getConfigListEntry(_("xtraEvent:"), self.TeamNitro_xtraEvent)
#         self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
#         self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
#         self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
#         self.LackOfFile = ''
#         self.list = []



#         if len(self.TeamNitro_KIII_PRO.choices)>1:
#             self.list.append(self.set_KIII_PRO)
#         if len(self.TeamNitro_interface.choices)>1:
#             self.list.append(self.set_Basic)
#         if len(self.TeamNitro_TNPosterX.choices)>1:
#             self.list.append(self.set_TNPosterX)
#         if len(self.TeamNitro_xtraEvent.choices)>1:
#             self.list.append(self.set_xtraEvent)
#         if len(self.TeamNitro_PluginBrowser.choices)>1:
#             self.list.append(self.set_PluginBrowser)
#         if len(self.TeamNitro_skyTeamNitro.choices)>1:
#             self.list.append(self.set_skyTeamNitro)
#         else:
#               pass
#         self["config"].list = self.list
#         self["config"].l.setList(self.list)

#     def changedEntry(self):
#         self.configChanged = True
#         if self["config"].getCurrent() == self.set_KIII_PRO:
#             self.setPicture(self.TeamNitro_KIII_PRO.value)
#         elif self["config"].getCurrent() == self.set_Basic:
#             self.setPicture(self.TeamNitro_interface.value)
#         elif self["config"].getCurrent() == self.set_TNPosterX:
#             self.setPicture(self.TeamNitro_TNPosterX.value)
#         elif self["config"].getCurrent() == self.set_xtraEvent:
#             self.setPicture(self.TeamNitro_xtraEvent.value)
#         elif self["config"].getCurrent() == self.set_PluginBrowser:
#             self.setPicture(self.TeamNitro_PluginBrowser.value)
#         elif self["config"].getCurrent() == self.set_skyTeamNitro:
#             self.setPicture(self.TeamNitro_skyTeamNitro.value)
#         elif self["config"].getCurrent() == self.set_myatile:
#             if self.TeamNitro_active.value == True:
#                 self.createConfigList()
#             else:
#                 pass
#             self.createConfigList()

#     def selectionChanged(self):
#         if self["config"].getCurrent() == self.set_KIII_PRO:
#             self.setPicture(self.TeamNitro_KIII_PRO.value)
#         elif self["config"].getCurrent() == self.set_Basic:
#             self.setPicture(self.TeamNitro_interface.value)
#         elif self["config"].getCurrent() == self.set_TNPosterX:
#             self.setPicture(self.TeamNitro_TNPosterX.value)
#         elif self["config"].getCurrent() == self.set_xtraEvent:
#             self.setPicture(self.TeamNitro_xtraEvent.value)
#         elif self["config"].getCurrent() == self.set_PluginBrowser:
#             self.setPicture(self.TeamNitro_PluginBrowser.value)
#         elif self["config"].getCurrent() == self.set_skyTeamNitro:
#             self.setPicture(self.TeamNitro_skyTeamNitro.value)
#         else:
#             self["Picture"].hide()

#     def keyLeft(self):
#         ConfigListScreen.keyLeft(self)
#         self.createConfigList()

#     def keyRight(self):
#         ConfigListScreen.keyRight(self)
#         self.createConfigList()

#     def cancel(self):
#         self.keyGreen()

#     def getmyAtileState(self):
#         chdir(self.skin_base_dir)
#         if path.exists("mySkin"):
#             return True
#         else:
#             return False

#     def setPicture(self, f):
#         pic = f.split('/')[-1].replace(".xml", ".png")
#         preview = self.skin_base_dir + "preview/preview_" + pic
#         if path.exists(preview):
#             self["Picture"].instance.setPixmapFromFile(preview)
#             self["Picture"].show()
#         else:
#             self["Picture"].hide()


#     def keyGreen(self):
#         if self["config"].isChanged():
#             for x in self["config"].list:
#                 x[1].save()
#                 configfile.save()
#             chdir(self.skin_base_dir)
#             self.makeSettings(self.TeamNitro_KIII_PRO, self.KIII_PRO_file)
#             self.makeSettings(self.TeamNitro_interface, self.interface)
#             self.makeSettings(self.TeamNitro_TNPosterX, self.TNPosterX_file)
#             self.makeSettings(self.TeamNitro_xtraEvent, self.xtraEvent_file)
#             self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
#             self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)

#             if not path.exists("mySkin_off"):
#                 mkdir("mySkin_off")
#                 print("makedir mySkin_off")
#             if self.TeamNitro_active.value:
#                 if not path.exists("mySkin") and path.exists("mySkin_off"):
#                     symlink("mySkin_off", "mySkin")
#             else:
#                 if path.exists("mySkin"):
#                     if path.exists("mySkin_off"):
#                         if path.islink("mySkin"):
#                             remove("mySkin")
#                         else:
#                             shutil.rmtree("mySkin")
#                     else:
#                         rename("mySkin", "mySkin_off")
#             self.update_user_skin()
#             self.close()
#         elif  config.skin.primary_skin.value != self.start_skin:
#             self.update_user_skin()
#             self.close()
#         else:
#             if self.changed_screens:
#                 self.update_user_skin()
#                 self.close()
#             else:
#                 self.close()

#     def makeSettings(self, config_entry, user_file):
#         if path.exists(user_file):
#             remove(user_file)
#         if path.islink(user_file):
#             remove(user_file)
#         if config_entry.value != 'default':
#             symlink(config_entry.value, user_file)

#     def TeamNitroScreenCB(self):
#         self.changed_screens = True
#         self["config"].setCurrentIndex(0)

#     def update_user_skin(self):
#         global cur_skin
#         user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
#         if path.exists(user_skin_file):
#             remove(user_skin_file)
#         cprint("update_user_skin.self.TeamNitro_active.value")
#         user_skin = ""
#         if path.exists(self.skin_base_dir + self.KIII_PRO_file):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.KIII_PRO_file, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + self.interface):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.interface, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + self.TNPosterX_file):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.TNPosterX_file, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + self.xtraEvent_file):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.xtraEvent_file, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + self.PluginBrowser_file):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
#             user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
#         if path.exists(self.skin_base_dir + 'mySkin'):
#             for f in listdir(self.skin_base_dir + "mySkin/"):
#                 user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
#         if user_skin != '':
#             user_skin = "<skin>\n" + user_skin
#             user_skin = user_skin + "</skin>\n"
#             with open(user_skin_file, "w") as myFile:
#                 cprint("update_user_skin.self.TeamNitro_active.value write myFile")
#                 myFile.write(user_skin)
#                 myFile.flush()
#                 myFile.close()
#         self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
#         self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
#         self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

#     def checkComponent(self, myContent, look4Component, myPath):
#         def updateLackOfFile(name, mySeparator =', '):
#                 cprint("Missing component found:%s\n" % name)
#                 if self.LackOfFile == '':
#                         self.LackOfFile = name
#                 else:
#                         self.LackOfFile += mySeparator + name

#         r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
#         r=list(set(r))

#         cprint("Found %s:\n" % (look4Component))
#         print(r)
#         if r:
#                 for myComponent in set(r):
#                         if look4Component == 'pixmap':
#                                 if myComponent.startswith('/'):
#                                         if not path.exists(myComponent):
#                                                 updateLackOfFile(myComponent, '\n')
#                                 else:
#                                         if not path.exists(myPath + myComponent):
#                                                 updateLackOfFile(myComponent)
#                         else:
#                                 if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
#                                         updateLackOfFile(myComponent)
#         return

#     def save(self):
#         for x in self['config'].list:
#             x[1].save()
#             configfile.save()

#     def readXMLfile(self, XMLfilename, XMLsection):
#         myPath=path.realpath(XMLfilename)
#         if not path.exists(myPath):
#                 remove(XMLfilename)
#                 return ''
#         filecontent = ''
#         if XMLsection == 'ALLSECTIONS':
#                 sectionmarker = True
#         else:
#                 sectionmarker = False
#         with open (XMLfilename, "r") as myFile:
#                 for line in myFile:
#                         if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
#                                 continue
#                         if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
#                                 sectionmarker = True
#                         elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
#                                 sectionmarker = False
#                                 filecontent = filecontent + line
#                         if sectionmarker == True:
#                                 filecontent = filecontent + line
#                 myFile.close()
#         return filecontent


#==========================================================================================#
class AL_AYAM_FHD(Screen, ConfigListScreen):

    skin = """

        <screen name="AL_AYAM_FHD" position="0,0" size="1920,1080" title="AL_AYAM_FHD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO SKINS Setup")
        self.skin_base_dir = "/usr/share/enigma2/AL_AYAM_FHD/"
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
#AL_AYAM_FHD
        self.default_AL_AYAM_FHD_file = "AL_AYAM_FHD_Original.xml"
        self.AL_AYAM_FHD_file = "skin_user_AL_AYAM_FHD.xml"
        current, choices = self.getSettings(self.default_AL_AYAM_FHD_file, self.AL_AYAM_FHD_file)
        self.TeamNitro_AL_AYAM_FHD = NoSave(ConfigSelection(default=current, choices = choices))
#interface
        self.default_interface_file = "interface_Original.xml"
        self.interface_file = "skin_user_interface.xml"
        current, choices = self.getSettings(self.default_interface_file, self.interface_file)
        self.TeamNitro_interface = NoSave(ConfigSelection(default=current, choices = choices))
#TNPosterX
        self.default_TNPosterX_file = "TNPosterX_Original.xml"
        self.TNPosterX_file = "skin_user_TNPosterX.xml"
        current, choices = self.getSettings(self.default_TNPosterX_file, self.TNPosterX_file)
        self.TeamNitro_TNPosterX = NoSave(ConfigSelection(default=current, choices = choices))
#xtraEvent
        self.default_xtraEvent_file = "xtraEvent_Original.xml"
        self.xtraEvent_file = "skin_user_xtraEvent.xml"
        current, choices = self.getSettings(self.default_xtraEvent_file, self.xtraEvent_file)
        self.TeamNitro_xtraEvent = NoSave(ConfigSelection(default=current, choices = choices))
#PluginBrowser
        self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
        self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
        current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
        self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
#skyTeamNitro
        self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
        self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
        current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
        self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())




    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Selections")
                except:
                    pass

    def createConfigList(self):
        self.set_AL_AYAM_FHD = getConfigListEntry(_("AL_AYAM_FHD:"), self.TeamNitro_AL_AYAM_FHD)
        self.set_interface = getConfigListEntry(_("Interface:"), self.TeamNitro_interface)
        self.set_TNPosterX = getConfigListEntry(_("TNPosterX:"), self.TeamNitro_TNPosterX)
        self.set_xtraEvent = getConfigListEntry(_("xtraEvent:"), self.TeamNitro_xtraEvent)
        self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
        self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []



        if len(self.TeamNitro_AL_AYAM_FHD.choices)>1:
            self.list.append(self.set_AL_AYAM_FHD)
        if len(self.TeamNitro_interface.choices)>1:
            self.list.append(self.set_interface)
        if len(self.TeamNitro_TNPosterX.choices)>1:
            self.list.append(self.set_TNPosterX)
        if len(self.TeamNitro_xtraEvent.choices)>1:
            self.list.append(self.set_xtraEvent)
        if len(self.TeamNitro_PluginBrowser.choices)>1:
            self.list.append(self.set_PluginBrowser)
        if len(self.TeamNitro_skyTeamNitro.choices)>1:
            self.list.append(self.set_skyTeamNitro)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_AL_AYAM_FHD:
            self.setPicture(self.TeamNitro_AL_AYAM_FHD.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_AL_AYAM_FHD:
            self.setPicture(self.TeamNitro_AL_AYAM_FHD.value)
        elif self["config"].getCurrent() == self.set_interface:
            self.setPicture(self.TeamNitro_interface.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_AL_AYAM_FHD, self.AL_AYAM_FHD_file)
            self.makeSettings(self.TeamNitro_interface, self.interface_file)
            self.makeSettings(self.TeamNitro_TNPosterX, self.TNPosterX_file)
            self.makeSettings(self.TeamNitro_xtraEvent, self.xtraEvent_file)
            self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
            self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)

            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.AL_AYAM_FHD_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.AL_AYAM_FHD_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.interface_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.interface_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.TNPosterX_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.TNPosterX_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.xtraEvent_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.xtraEvent_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.PluginBrowser_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent


#==========================================================================================#

#==========================================================================================#
class BoHLALA_FHD(Screen, ConfigListScreen):

    skin = """

        <screen name="BoHLALA_FHD" position="0,0" size="1920,1080" title="BoHLALA_FHD PRO-MOD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO SKINS Setup")
        self.skin_base_dir = "/usr/share/enigma2/BoHLALA_FHD/"
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"
#BoHLALA_FHD
        self.default_BoHLALA_FHD_file = "BoHLALA_FHD_Original.xml"
        self.BoHLALA_FHD_file = "skin_user_BoHLALA_FHD.xml"
        current, choices = self.getSettings(self.default_BoHLALA_FHD_file, self.BoHLALA_FHD_file)
        self.TeamNitro_BoHLALA_FHD = NoSave(ConfigSelection(default=current, choices = choices))
#Basic
        self.default_Basic_file = "Basic_Original.xml"
        self.Basic_file = "skin_user_Basic.xml"
        current, choices = self.getSettings(self.default_Basic_file, self.Basic_file)
        self.TeamNitro_Basic = NoSave(ConfigSelection(default=current, choices = choices))
#TNPosterX
        self.default_TNPosterX_file = "TNPosterX_Original.xml"
        self.TNPosterX_file = "skin_user_TNPosterX.xml"
        current, choices = self.getSettings(self.default_TNPosterX_file, self.TNPosterX_file)
        self.TeamNitro_TNPosterX = NoSave(ConfigSelection(default=current, choices = choices))
#xtraEvent
        self.default_xtraEvent_file = "xtraEvent_Original.xml"
        self.xtraEvent_file = "skin_user_xtraEvent.xml"
        current, choices = self.getSettings(self.default_xtraEvent_file, self.xtraEvent_file)
        self.TeamNitro_xtraEvent = NoSave(ConfigSelection(default=current, choices = choices))
#PluginBrowser
        self.default_PluginBrowser_file = "PluginBrowser_Original.xml"
        self.PluginBrowser_file = "skin_user_PluginBrowser.xml"
        current, choices = self.getSettings(self.default_PluginBrowser_file, self.PluginBrowser_file)
        self.TeamNitro_PluginBrowser = NoSave(ConfigSelection(default=current, choices = choices))
#skyTeamNitro
        self.default_skyTeamNitro_file = "skyTeamNitro_Original.xml"
        self.skyTeamNitro_file = "skin_user_skyTeamNitro.xml"
        current, choices = self.getSettings(self.default_skyTeamNitro_file, self.skyTeamNitro_file)
        self.TeamNitro_skyTeamNitro = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())




    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Selections"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Selections")
                except:
                    pass

    def createConfigList(self):
        self.set_BoHLALA_FHD = getConfigListEntry(_("BoHLALA_FHD:"), self.TeamNitro_BoHLALA_FHD)
        self.set_Basic = getConfigListEntry(_("Basic:"), self.TeamNitro_Basic)
        self.set_TNPosterX = getConfigListEntry(_("TNPosterX:"), self.TeamNitro_TNPosterX)
        self.set_xtraEvent = getConfigListEntry(_("xtraEvent:"), self.TeamNitro_xtraEvent)
        self.set_PluginBrowser = getConfigListEntry(_("PluginBrowser:"), self.TeamNitro_PluginBrowser)
        self.set_skyTeamNitro = getConfigListEntry(_("skyTeamNitro:"), self.TeamNitro_skyTeamNitro)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []



        if len(self.TeamNitro_BoHLALA_FHD.choices)>1:
            self.list.append(self.set_BoHLALA_FHD)
        if len(self.TeamNitro_Basic.choices)>1:
            self.list.append(self.set_Basic)
        if len(self.TeamNitro_TNPosterX.choices)>1:
            self.list.append(self.set_TNPosterX)
        if len(self.TeamNitro_xtraEvent.choices)>1:
            self.list.append(self.set_xtraEvent)
        if len(self.TeamNitro_PluginBrowser.choices)>1:
            self.list.append(self.set_PluginBrowser)
        if len(self.TeamNitro_skyTeamNitro.choices)>1:
            self.list.append(self.set_skyTeamNitro)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_BoHLALA_FHD:
            self.setPicture(self.TeamNitro_BoHLALA_FHD.value)
        elif self["config"].getCurrent() == self.set_Basic:
            self.setPicture(self.TeamNitro_Basic.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_BoHLALA_FHD:
            self.setPicture(self.TeamNitro_BoHLALA_FHD.value)
        elif self["config"].getCurrent() == self.set_Basic:
            self.setPicture(self.TeamNitro_Basic.value)
        elif self["config"].getCurrent() == self.set_TNPosterX:
            self.setPicture(self.TeamNitro_TNPosterX.value)
        elif self["config"].getCurrent() == self.set_xtraEvent:
            self.setPicture(self.TeamNitro_xtraEvent.value)
        elif self["config"].getCurrent() == self.set_PluginBrowser:
            self.setPicture(self.TeamNitro_PluginBrowser.value)
        elif self["config"].getCurrent() == self.set_skyTeamNitro:
            self.setPicture(self.TeamNitro_skyTeamNitro.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_BoHLALA_FHD, self.BoHLALA_FHD_file)
            self.makeSettings(self.TeamNitro_Basic, self.Basic_file)
            self.makeSettings(self.TeamNitro_TNPosterX, self.TNPosterX_file)
            self.makeSettings(self.TeamNitro_xtraEvent, self.xtraEvent_file)
            self.makeSettings(self.TeamNitro_PluginBrowser, self.PluginBrowser_file)
            self.makeSettings(self.TeamNitro_skyTeamNitro, self.skyTeamNitro_file)

            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.BoHLALA_FHD_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.BoHLALA_FHD_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.Basic_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.Basic_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.TNPosterX_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.TNPosterX_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.xtraEvent_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.xtraEvent_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.PluginBrowser_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.PluginBrowser_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + self.skyTeamNitro_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.skyTeamNitro_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent



class TNFonts(Screen, ConfigListScreen):

    skin = """

        <screen name="TNFonts" position="0,0" size="1920,1080" title="TNFonts PRO-MOD" backgroundColor="transparent">
            <widget source="session.VideoPicture" render="Pig" position="1186,609" size="672,389" zPosition="3" backgroundColor="transparent" />
            <ePixmap position="0,0" size="1920,1086" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" alphatest="off" transparent="1" />
            <ePixmap position="263,106" size="800,80" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/bar.png" alphatest="off" transparent="1" />
            <widget source="Title" render="Label" position="288,111" size="752,68" zPosition="1" halign="center" font="Regular;46" backgroundColor="bglist" transparent="1" />
            <widget name="config" position="247,199" size="830,761" font="Regular;34" itemHeight="45" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/barr.png" enableWrapAround="1" transparent="1" />
            <widget name="Picture" position="1184,130" scale="1" size="671,436" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="275,970" size="48,48" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/green48x48.png" position="772,970" size="48,48" alphatest="blend" />
            <widget name="key_red" position="332,970" size="300,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="key_green" position="830,970" size="230,48" zPosition="1" font="Regular; 35" halign="left" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#05A115" />
        </screen>
    """

    def __init__(self, session, args = 0):
        self.session = session
        self.changed_screens = False
        Screen.__init__(self, session)
        self.start_skin = config.skin.primary_skin.value
        if self.start_skin != "skin.xml":
            self.getInitConfig()
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.configChanged = False
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save Changes"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
                {
                        "green": self.keyGreen,
                        "red": self.cancel,
                        "cancel": self.cancel,
                        "right": self.keyRight,
                        "left": self.keyLeft,
                }, -2)
        self["Picture"] = Pixmap()
        self.createConfigList()

    def getInitConfig(self):
        global cur_skin
        self.title = _("PRO FONTS Setup")
        self.skin_base_dir = '/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/'
        cprint("self.skin_base_dir=%s, skin=%s, currentSkin=%s" % (self.skin_base_dir, config.skin.primary_skin.value, cur_skin))
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_font.xml"
        self.default_color_file = "color_Original.xml"
        self.color_file = "skin_user_color.xml"

#Fonts
        self.default_Fonts_file = "Fonts_Original.xml"
        self.Fonts_file = "skin_user_Fonts.xml"
        current, choices = self.getSettings(self.default_Fonts_file, self.Fonts_file)
        self.TeamNitro_Fonts = NoSave(ConfigSelection(default=current, choices = choices))
# myatile
        myatile_active = self.getmyAtileState()
        self.TeamNitro_active = NoSave(ConfigYesNo(default=True))
        self.TeamNitro_fake_entry = NoSave(ConfigNothing())


    def getSettings(self, default_file, user_file):
        # default setting
        default = ("default", _("Default"))

        # search typ
        styp = default_file.replace('_Original.xml', '')
        search_str = '%s_' % styp

        # possible setting
        choices = []
        files = listdir(self.skin_base_dir)
        if path.exists(self.skin_base_dir + 'allScreens/%s/' % styp):
            files += listdir(self.skin_base_dir + 'allScreens/%s/' % styp)
        for f in sorted(files, key=str.lower):
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "").replace(".xml", "").replace("_", " ")
                if path.exists(self.skin_base_dir + 'allScreens/%s/%s' %(styp, f)):
                    choices.append((self.skin_base_dir + 'allScreens/%s/%s' %(styp, f), friendly_name))
                else:
                    choices.append((self.skin_base_dir + f, friendly_name))
        choices.append(default)

        # current setting
        myfile = self.skin_base_dir + user_file
        current = ''
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + default_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(default_file, user_file)
            elif path.exists(self.skin_base_dir + 'allScreens/%s/%s' % (styp, default_file)):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.skin_base_dir + 'allScreens/%s/%s' %(styp, default_file), user_file)
            else:
                current = None
        if current is None:
            current = default
        else:
            filename = path.realpath(myfile)
            friendly_name = path.basename(filename).replace(search_str, "").replace(".xml", "").replace("_", " ")
            current = (filename, friendly_name)

        return current[0], choices
        if path.exists(self.skin_base_dir + "mySkin_off"):
            if not path.exists(self.skin_base_dir + "TeamNitro_Fonts"):
                chdir(self.skin_base_dir)
                try:
                    rename("mySkin_off", "TeamNitro_Fonts")
                except:
                    pass

    def createConfigList(self):

        self.set_Fonts = getConfigListEntry(_("TNFonts:"), self.TeamNitro_Fonts)
        self.set_myatile = getConfigListEntry(_("Enable %s pro:") % cur_skin, self.TeamNitro_active)
        self.LackOfFile = ''
        self.list = []

        if len(self.TeamNitro_Fonts.choices)>1:
            self.list.append(self.set_Fonts)
        else:
              pass
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def changedEntry(self):
        self.configChanged = True
        if self["config"].getCurrent() == self.set_Fonts:
            self.setPicture(self.TeamNitro_Fonts.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.TeamNitro_active.value == True:
                self.createConfigList()
            else:
                pass
            self.createConfigList()

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_Fonts:
            self.setPicture(self.TeamNitro_Fonts.value)
        else:
            self["Picture"].hide()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createConfigList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createConfigList()

    def cancel(self):
        self.keyGreen()

    def getmyAtileState(self):
        chdir(self.skin_base_dir)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def setPicture(self, f):
        pic = f.split('/')[-1].replace(".xml", ".png")
        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()


    def keyGreen(self):
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()
                configfile.save()
            chdir(self.skin_base_dir)
            self.makeSettings(self.TeamNitro_Fonts, self.Fonts_file)

            if not path.exists("mySkin_off"):
                mkdir("mySkin_off")
                print("makedir mySkin_off")
            if self.TeamNitro_active.value:
                if not path.exists("mySkin") and path.exists("mySkin_off"):
                    symlink("mySkin_off", "mySkin")
            else:
                if path.exists("mySkin"):
                    if path.exists("mySkin_off"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "mySkin_off")
            self.update_user_skin()
            self.close()
        elif  config.skin.primary_skin.value != self.start_skin:
            self.update_user_skin()
            self.close()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.close()
            else:
                self.close()

    def makeSettings(self, config_entry, user_file):
        if path.exists(user_file):
            remove(user_file)
        if path.islink(user_file):
            remove(user_file)
        if config_entry.value != 'default':
            symlink(config_entry.value, user_file)

    def TeamNitroScreenCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def update_user_skin(self):
        global cur_skin
        user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user_' + cur_skin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
        cprint("update_user_skin.self.TeamNitro_active.value")
        user_skin = ""
        if path.exists(self.skin_base_dir + self.Fonts_file):
            user_skin = user_skin + self.readXMLfile(self.skin_base_dir + self.Fonts_file, 'ALLSECTIONS')
        if path.exists(self.skin_base_dir + 'mySkin'):
            for f in listdir(self.skin_base_dir + "mySkin/"):
                user_skin = user_skin + self.readXMLfile(self.skin_base_dir + "mySkin/" + f, 'screen')
        if user_skin != '':
            user_skin = "<skin>\n" + user_skin
            user_skin = user_skin + "</skin>\n"
            with open(user_skin_file, "w") as myFile:
                cprint("update_user_skin.self.TeamNitro_active.value write myFile")
                myFile.write(user_skin)
                myFile.flush()
                myFile.close()
        self.checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
        self.checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/') )
        self.checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_SKIN, '') )

    def checkComponent(self, myContent, look4Component, myPath):
        def updateLackOfFile(name, mySeparator =', '):
                cprint("Missing component found:%s\n" % name)
                if self.LackOfFile == '':
                        self.LackOfFile = name
                else:
                        self.LackOfFile += mySeparator + name

        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component, myContent )
        r=list(set(r))

        cprint("Found %s:\n" % (look4Component))
        print(r)
        if r:
                for myComponent in set(r):
                        if look4Component == 'pixmap':
                                if myComponent.startswith('/'):
                                        if not path.exists(myComponent):
                                                updateLackOfFile(myComponent, '\n')
                                else:
                                        if not path.exists(myPath + myComponent):
                                                updateLackOfFile(myComponent)
                        else:
                                if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py") and not path.exists(myPath + myComponent + ".pyc"):
                                        updateLackOfFile(myComponent)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()
            configfile.save()

    def readXMLfile(self, XMLfilename, XMLsection):
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
                remove(XMLfilename)
                return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
                sectionmarker = True
        else:
                sectionmarker = False
        with open (XMLfilename, "r") as myFile:
                for line in myFile:
                        if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                                continue
                        if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                                sectionmarker = True
                        elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                                sectionmarker = False
                                filecontent = filecontent + line
                        if sectionmarker == True:
                                filecontent = filecontent + line
                myFile.close()
        return filecontent