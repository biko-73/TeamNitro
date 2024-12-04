# LabelDuoColors Render
# Copyright (c) 2boom 2014-22
# v.0.3-r0
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
# 22.12.2018 code optimization mod by Sirius
# 05.01.2022 space fix - 2boom
# 07.01.2022 add '*' and '|' as separator & code optimization


from Components.VariableText import VariableText
from Components.Renderer.Renderer import Renderer

from enigma import eLabel

class TN_L2Colors(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.colors = self.firstColor = self.secondColor = self.tmptext = self.text = ""
		self.separatorsymbol = '|*'
		self.separator = '|'

	GUI_WIDGET = eLabel

	def convert_color(self, color_in):
		return '\c' + color_in.lower().replace('#','').replace('a',':').replace('b',';').replace('c','<').replace('d','=').replace('e','>').replace('f','?')

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'foregroundColor':
				self.colors = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		self.tmptext = self.text = ''
		self.firstColor = self.convert_color(self.colors.split(',')[0].strip())
		self.secondColor = self.convert_color(self.colors.split(',')[-1].strip())
		if what[0] == self.CHANGED_CLEAR:
			self.text = ''
		else:
			self.text = ''
		for i in range(len(self.separatorsymbol)):
			if self.separatorsymbol[i] in self.source.text:
				self.separator = self.separatorsymbol[i]
			
		if self.separator in self.source.text:
			for i in range(self.source.text.count(self.separator) + 1):
				try:
					if i % 2 == 0: 
						self.tmptext += '%s%s' % (self.firstColor, self.source.text.split(self.separator)[i])
					else:
						if i % 2 == 0: 
							self.tmptext += '%s%s%s' % (self.secondColor, self.separator, self.source.text.split(self.separator)[i])
						else:
							self.tmptext += '%s%s%s%s' % (self.secondColor, self.separator, self.source.text.split(self.separator)[i], self.separator)
				except:
					pass
			self.tmptext = self.tmptext.rstrip(self.separator)
				
		else:
			for i in range(len(self.source.text.split())):
				try:
					if i % 2 == 0: 
						self.tmptext += '%s%s ' % (self.firstColor, self.source.text.split()[i])
					else:
						self.tmptext += '%s%s ' % (self.secondColor, self.source.text.split()[i])
				except:
					pass
		self.text = '  '.join(self.tmptext.strip().replace('_', ' ').split())
		#self.text = self.tmptext.strip().replace('_', ' ')
