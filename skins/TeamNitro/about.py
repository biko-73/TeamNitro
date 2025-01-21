#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import _
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen

 
class TeamNitro_About(Screen):
    skin = """
        <screen name="TN_About" position="0,0" size="1920,1080" backgroundColor="#232323" flags="wfNoBorder">
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" position="0,0" size="1920,1080" alphatest="blend" zPosition="-10" />
            <widget source="session.VideoPicture" render="Pig" position="1187,606" size="671,393" zPosition="3" backgroundColor="transparent" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="488,960" size="48,48" alphatest="blend" />
            <widget source="key_red" render="Label" position="560,960" size="300,48" zPosition="1" font="Regular; 35" halign="center" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="about" position="262,167" size="806,757" font="Regular;28" foregroundColor="yellow" backgroundColor="#000000" transparent="1" zPosition="1" scrollbarMode="showNever" />
        </screen>
    """

    def createSetup(self):
        self.credit = '********************************************* \n'
        self.credit += '                                    TeamNitro Control Center           \n'
        self.credit += '*********************************************\n\n'
        self.credit += 'INTRODUCTION\n'
        self.credit += 'When Designing the first version of Nitro Skin the need increased for two plugins\n'
        self.credit += 'that could show the additional screen of the skin as these properties were not available\n'
        self.credit += 'on the images by default except for the image OpenATV – OpenDroid\n\n'
        self.credit += 'The sources and codes were searched until the appropriate formula was found for work and \n'
        self.credit += 'compatibility with the different images. At first stage we made NitroAdvanceFHD Plugin\n'
        self.credit += 'which is only for Nitro skin and testing version. For the time being now we develop most\n'
        self.credit += 'updated version of plugin which called TeamNitro Control Center in this plugin you can\n' 
        self.credit += 'access many options and skins\n\n'
        self.credit += 'in pro mode you can chose different type of infobars, Channel Selection,\n'
        self.credit += 'Menu, PosterX and xtraEvent different interfaces of skins\n\n\n'
        self.credit += 'EXAMPLES\n'
        self.credit += '1-  You can access different shapes of TeamNitro Skins\n'
        self.credit += '2-  You can directly apply skin from inside plugin\n'
        self.credit += '3-  You can access MSN Weather from inside plugin\n'
        self.credit += '4-  You can download TeamNitro skins directly from inside plugin\n'
        self.credit += '5-  You can download Crypt, Provider & Satellite picons from inside plugin\n'
        self.credit += '6-  You can Specify the desired path for picons download\n'
        self.credit += '7-  Skins & Plugin auto update option\n\n\n'
        self.credit += 'ABOUT TeamNitro\n'
        self.credit += 'The Nitro team consists a group of designers who love to develop\n'
        self.credit += 'Kaleem(KIMOO)\n'
        self.credit += 'BoHlala\n'
        self.credit += 'Zelda77\n'
        self.credit += 'BIKOO\n\n\n'
        self.credit += 'TeamNitro SKINS\n'
        self.credit += '1- NitroAdvanceFHD BY (KIMOO)\n'
        self.credit += '2- Skin BoHlala\n'
        self.credit += '3- DragonFHD BY (Zelda777 and BIKO-73)\n'
        self.credit += '4- DesertFHD BY (KIMOO)\n'
        self.credit += '5- AL_AYAM_FHD BY (BIKO-73 and BoHlala)\n'
        self.credit += '6- KIII-Pro BY (KIMOO)\n\n\n'
        self.credit += 'OUR AIM\n'
        self.credit += 'To provide quality of work\n'
        self.credit += 'To make skin which able to work on all open source images without exception\n'
        self.credit += 'Add all that is needed to change the Skin and use it in a distinct and easy way\n\n\n'
        self.credit += 'Spacial Thanks to....\n'
        self.credit += 'Brother Hussain (FairBird)\n'
        self.credit += 'Brother Raduan\n'
        self.credit += 'Brother Oktus (Linuxsat)\n'
        self['about'].setText(self.credit)

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.setup_title = _('About TeamNitro')
        self['about'] = ScrollLabel('')
        self['actions'] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"], {
            'ok': self.quit,
            'cancel': self.quit,
			"up": self.scrollup,
			"down": self.scrolldown}, -1)
        self['key_red'] = StaticText(_('Close'))
        self.onFirstExecBegin.append(self.createSetup)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)
    
    def scrollup(self):
        self["about"].pageUp()
    def scrolldown(self):    
        self["about"].pageDown()

    def quit(self):
        self.close()