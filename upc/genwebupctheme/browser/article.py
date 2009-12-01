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
        return catalog.searchResults(path=dict(query=folder_path,depth=1),portal_type='Image',sort_on='getObjPositionInParent')

    def getFiles(self):
        items = self.context.getRelatedItems()
        result = [dict(title=item.title_or_id(),url=item.absolute_url()) for item in items]
        return result
        
