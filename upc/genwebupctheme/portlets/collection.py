from plone.portlet.collection.collection import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class customRendererCollection(Renderer):
    _template = ViewPageTemplateFile('collection.pt')
    render = _template