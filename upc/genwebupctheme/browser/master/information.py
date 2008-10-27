from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class infoGeneralView(BrowserView):
    __call__=ViewPageTemplateFile('info-general.pt')

