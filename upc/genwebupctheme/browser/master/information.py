from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import Interface, implements

class IinfoGeneral(Interface):
	""" Marker interface """

class Icompetencies(Interface):
	""" Marker interface """

class Irequisits(Interface):
	""" Marker interface """

class Ipreinscripcio(Interface):
	""" Marker interface """

class infoGeneralView(BrowserView):
    implements(IinfoGeneral)
    __call__=ViewPageTemplateFile('info-general.pt')

    def get_fitxa_lang(self,code):
        fitxa_codes = { 'en' : 'eng', 'ca':'cat', 'es' :'esp'}
        if code in fitxa_codes:
           return fitxa_codes[code]
        else:
           return fitxa_codes['es']