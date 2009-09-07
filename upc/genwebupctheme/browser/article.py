from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter, getUtility


class ArticleView(BrowserView):
    
    def __init__(self,context,request):
        self.context = context
        self.request = request
    
    def getImageBrains(self):
        catalog = self.context.portal_catalog;
        folder_path = '/'.join(self.context.getPhysicalPath()[:-1])
        return catalog.searchResults(path=folder_path,portal_type='Image')

    def getFileBrains(self):
        catalog = self.context.portal_catalog;
        folder_path = '/'.join(self.context.getPhysicalPath()[:-1])
        return catalog.searchResults(path=folder_path,portal_type='File')
        
