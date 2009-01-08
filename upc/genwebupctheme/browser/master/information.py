from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IinfoGeneral(Interface):
   """ Marker interface """

class Icompetencies(Interface):
   """ Makrer"""

class infoGeneralView(BrowserView):
    implements(IinfoGeneral)
    __call__=ViewPageTemplateFile('info-general.pt')

class competenciesView(BrowserView):
    __call__=ViewPageTemplateFile('competencies.pt')
    
class requisitsView(BrowserView):
    __call__=ViewPageTemplateFile('requisits.pt')
