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
                                                 review_state=['published','intranet'],)
						 #review_state='published',)
        if logos_container:
            return catalog.searchResults(portal_type='Logos_Footer',
                       review_state=['published','intranet'],
		       #review_state='published',
                       path=logos_container[0].getPath(),
                       sort_on='getObjPositionInParent',
                       sort_limit=5)[:5]
        else:
            return []
        
    def test(self, cond, a, b):
        if cond:
            return a
        return b
        

    def linksPeu(self):
        """ links fixats per accessibilitat/rss/about
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        
        if idioma == 'ca':
            rss_link = "rss-ca"
            about_link = "sobre-el-web"
            access_link = "accessibilitat"
        if idioma == 'es':
            rss_link = "rss-es"
            about_link = "acerca-del-web"
            access_link = "accesibilidad"
        if idioma == 'en':
            rss_link = "rss-en"
            about_link = "about-the-web"
            access_link = "accessibility"    

        return dict(rss=rss_link, about=about_link, access=access_link)