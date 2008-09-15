from plone.app.portlets.portlets.navigation import Renderer as navigation_render
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(navigation_render):
    """ Classe que sobreescriu la original del portlet navigation 
    """
    def render(self):
        return self._template()

    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')