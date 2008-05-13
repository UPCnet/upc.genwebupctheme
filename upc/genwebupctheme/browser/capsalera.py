from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common

class capsaleraSuperior(ViewletBase):
    render = ViewPageTemplateFile('capsaleraSuperior.pt')

    def update(self):
        
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.site_actions = context_state.actions().get('site_actions', None)
        
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')

        self.portal_url = portal_state.portal_url()

        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = ""

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())

        