from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter

from plone.app.layout.viewlets import common

class capsaleraSuperior(common.SiteActionsViewlet, common.SearchBoxViewlet):
    render = ViewPageTemplateFile('capsaleraSuperior.pt')

#    def update(self):
#        context_state = getMultiAdapter((self.context, self.request),
#                                        name=u'plone_context_state')
#        self.site_actions = context_state.actions().get('site_actions', None)

        