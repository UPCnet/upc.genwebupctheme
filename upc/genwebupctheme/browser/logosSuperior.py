from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName

class logosSuperior(ViewletBase):
    render = ViewPageTemplateFile('logosSuperior.pt')