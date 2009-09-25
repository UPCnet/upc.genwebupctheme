from zope.interface import implements, alsoProvides
from zope.viewlet.interfaces import IViewlet
from zope.deprecation.deprecation import deprecate
from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from plone.app.layout.viewlets.common import GlobalSectionsViewlet

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName


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
        
    def UnitatsPortal_tabs(self):
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        
        path = urltool.getPortalPath()        
        folders = portal_catalog.searchResults(portal_type = 'Seccio',                                                                                       
                                               path = dict(query=path, depth=1),     
                                               review_state=['internally_published','external','published'],
                                               sort_on='getObjPositionInParent')           
        
        results = []
        for fold in folders:  
            if fold.exclude_from_nav == False:                  
                results.append(dict(name = fold.getObject().getText,
                                    url = fold.getURL(),
                                    id = fold.getId,
                                    description = fold.Description
                                   )
                               )
        return results      
