from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class homePageView(BrowserView):
    
    template = ViewPageTemplateFile('homepage.pt')

    def test(self, value, trueVal, falseVal):
        """
            helper method, mainly for setting html attributes.
        """
        if value:
            return trueVal
        return falseVal