from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class infoGeneral(BrowserView):
   implements(INavigationBreadcrumbs)

   def breadcrumbs(self):
       base = ({'absolute_url': 'info-general',
                'Title' : 'Informacio general'})    
       return base 
