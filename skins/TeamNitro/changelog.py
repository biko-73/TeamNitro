# coding: utf-8
#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import _
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen

 
class TeamNitro_Changelog(Screen):
    skin = """
        <screen name="Changelog" position="0,0" size="1920,1080" backgroundColor="#232323" flags="wfNoBorder">
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/images/mn.png" position="0,0" size="1920,1080" alphatest="off" zPosition="-10" />
            <widget source="session.VideoPicture" render="Pig" position="1187,606" size="671,393" zPosition="3" backgroundColor="transparent" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TeamNitro/pic/red48x48.png" position="488,960" size="48,48" alphatest="blend" />
            <widget source="key_red" render="Label" position="560,960" size="300,48" zPosition="1" font="Regular; 35" halign="center" valign="center" backgroundColor="#000000" transparent="1" foregroundColor="#FA0909" />
            <widget name="about" position="262,167" size="806,757" font="Regular;28" foregroundColor="white" backgroundColor="#000000" transparent="1" zPosition="1" scrollbarMode="showNever" />
        </screen>
    """

    def createSetup(self):
        self.credit = '********************************************* \n'
        self.credit += '                             TeamNitro Control Center Update           \n'
        self.credit += '                                  Changelog 05-07-2024         \n'
        self.credit += '*********************************************\n\n'
        self.credit += 'Fix some minor bugs\n'
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







