from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName

class Peu(ViewletBase):
    render = ViewPageTemplateFile('peu.pt')

    def bannersPeu(self):
        context = self.context
        urltool = getToolByName(context, 'portal_url')
        path_to_banners = urltool.getPortalPath() + '/' + 'logos_peu'        
        portal_catalog = getToolByName(self, 'portal_catalog')
        banners = portal_catalog.searchResults(portal_type = 'Logos Footer',
                                               depth = 1,
                                               path = path_to_banners,
                                               review_state='published',
                                               sort_limit=5)[:5]  
        return banners
        
