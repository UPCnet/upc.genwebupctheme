from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class capsaleraSuperior(ViewletBase):
    render = ViewPageTemplateFile('capsaleraSuperior.pt')
#
#    def update(self):