from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from PIL import Image

class Peu(ViewletBase):
    render = ViewPageTemplateFile('peu.pt')

    def bannersPeu(self):
        context = self.context
        catalog = getToolByName(self, 'portal_catalog')
        logos_container = catalog.searchResults(portal_type='Logos_Container',
                                                 review_state='published')
        if logos_container:
            return catalog.searchResults(portal_type='Logos_Footer',
                       review_state='published',
                       path=logos_container[0].getPath(),
                       sort_limit=5)[:5]
        else:
            return []
        
    def test(self, cond, a, b):
        if cond:
            return a
        return b
        
