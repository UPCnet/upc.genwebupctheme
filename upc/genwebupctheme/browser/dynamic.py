from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

class DynamicCssView(BrowserView):
    __call__ = ViewPageTemplateFile('dynamic.css.pt')