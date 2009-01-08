from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import Interface, implements

class IinfoGeneral(Interface):
	""" Marker interface """

class Icompetencies(Interface):
	""" Marker interface """

class Irequisits(Interface):
	""" Marker interface """

class infoGeneralView(BrowserView):
    implements(IinfoGeneral)
    __call__=ViewPageTemplateFile('info-general.pt')

class competenciesView(BrowserView):
	implements(Icompetencies)
	__call__=ViewPageTemplateFile('competencies.pt')
    
class requisitsView(BrowserView):
	implements(Irequisits)
	__call__=ViewPageTemplateFile('requisits.pt')
