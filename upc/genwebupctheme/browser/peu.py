from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from PIL import Image

class Peu(ViewletBase):
    render = ViewPageTemplateFile('peu.pt')

    def bannersPeu(self):
        context = self.context
        urltool = getToolByName(context, 'portal_url')
        path_to_banners = urltool.getPortalPath() + '/' + 'logospeu'        
        portal_catalog = getToolByName(self, 'portal_catalog')
        banners = portal_catalog.searchResults(sort_on = 'getObjPositionInParent',
                                               portal_type = 'Logos Footer',
                                               path = path_to_banners,
                                               review_state='published',
                                               sort_limit=5)[:5]
        return banners
    
    
        
    def test(self, cond, a, b):
        if cond:
            return a
        return b
    
    def resizeImage(self, obj, alto, ancho):
        import pdb;pdb.set_trace()
        return obj
#        return obj.resize((ancho, alto), Image.NEAREST)