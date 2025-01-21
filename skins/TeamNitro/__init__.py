# -*- coding: utf-8 -*-
from __future__ import print_function
from Components.Language import language
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigNumber, ConfigSelectionNumber, ConfigYesNo, ConfigText, ConfigInteger
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import os, gettext
from os import path
import gettext
try:
	from boxbranding import getBoxType
except:
	pass
PluginLanguageDomain = 'ArabicSavior'
PluginLanguagePath = 'Extensions/TeamNitro/locale'

def localeInit():
    lang = language.getLanguage()[:2]
    os.environ['LANGUAGE'] = lang
    print('[WebInterface] set language to ', lang)
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        print('[%s] fallback to default translation for %s' % (PluginLanguageDomain, txt))
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)