from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter

class DynamicCssView(BrowserView):
    __call__ = ViewPageTemplateFile('dynamic.css.pt')

    def portal_url(self):
        """ Funcion a que retorna el path 
        """
        portal_state = getMultiAdapter((self.context, self.request),
                                    name=u'plone_portal_state')
        return portal_state.portal_url()
    
    def es_anonim(self):
        context_state = getMultiAdapter((self.context, self.request),
                                    name=u'plone_portal_state')
        return context_state.anonymous()        