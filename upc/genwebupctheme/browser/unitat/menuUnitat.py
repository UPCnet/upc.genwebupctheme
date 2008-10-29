from zope.interface import implements, alsoProvides
from zope.viewlet.interfaces import IViewlet
from zope.deprecation.deprecation import deprecate
from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from plone.app.layout.viewlets.common import GlobalSectionsViewlet

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

class GlobalSections(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('menuUnitat.pt')

    def esSeccio(self):
        if IPloneSiteRoot.providedBy(self.context):
            return False
        else:
            return True

    def claseDalt(self, esSelected, esPrimer):
        if esSelected and esPrimer:
            return 'daltMenu daltMenuPrimer'
        if not esSelected and esPrimer:
            return 'daltMenu daltMenuPrimer alpha'        
        if not esSelected:
            return 'daltMenu alpha'
        if esSelected:
            return 'daltMenu'

    def claseDaltUltim(self, esUltim):
        if esUltim:
            return '100%'
        