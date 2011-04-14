#!/usr/bin/env python
# encoding: utf-8

__VERSION__ = 0.3
__AUTHOR__ = "pascal raszyk <posixpascal@googlemail.com>"
__COPYRIGHT__ = __AUTHOR__
__DOC__ = """
Flask Utilities ermoeglicht es einfach und schnell Formulare zu verarbeiten.
Folgendes Szenario:
	i = request.form["i"]
	
Falls das Form-Element "i" allerdings nicht gesetzt ist, gibts eine haessliche 400-Fehlerseite.
Alternativ gibt es mehrere Moeglichkeiten:

try: i = request.form["i"]
except KeyError: i = 0

Aber bei 10 Formular-Items wird das ganze etwas unuebersichtlich.

Da kommen die Flask Utilities ins Spiel.

from utils import FormParser
f = FormParser.new(request.form)

i = f.get("i", 0)

Hier holen wir mit "get" das Element "i", falls das aber nicht vorhanden ist, nutzen wir 0 stattdessen.
Der FormParser kann auch Mappen:

Um jedes Element in einem Formular gross zu schreiben muss man nicht lange rum-if-en sondern:

def upx(item): return item.upper()
i = f.map(upx)

f.map(function, 1) form(i) => Hallo Welt => HALLO WELT
0 => form(i) => i => I
	.. function(item1)
	.. function(item2)
	.. function(item3)
"""



class FormParser(object):
	def __init__(self):
		pass
		
	@staticmethod
	class FormObject():
		def __init__(self, fo):
			self.FormObject = fo
		
		def isset(self, lists):
			for item in lists:
				print item
				try: i = self.get(item)
				except KeyError: return False
			return True
		
		def get(self, key, default="KEYERROR"):
			try:
				return self.FormObject[key]
			except: 
				if default == "KEYERROR": raise KeyError
				else: return default 
	
	@staticmethod
	def new(formobject):
		return FormParser.FormObject(formobject)