from plone.app.portlets.portlets.rss import Renderer
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class customRendererRSS(Renderer):
    render_full = ZopeTwoPageTemplateFile('rss.pt')
    