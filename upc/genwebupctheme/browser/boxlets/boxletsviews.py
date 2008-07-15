from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from Products.CMFPlone import PloneMessageFactory as _
from Acquisition import aq_inner

from time import localtime

import feedparser

class agenda(BrowserView):
    template=ViewPageTemplateFile('agenda.pt')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.utils = getMultiAdapter((self.context, self.request),
                                        name=u'upc.genweb.utils')
        self.now = localtime()
        
    def mes(self, mes):
        return self.utils.mes(mes)
    
    def dia_semana(self, dia):
        return self.utils.dia_semana(dia)
    
    def getRSS (self):
        items = []
        url = 'http://www.upc.edu/catala/RSS/actualitatUpc.php'

        d = feedparser.parse(url)

        for item in d['items']:
            try:
                link = item.links[0]['href']
                itemdict = {
                    'title' : item.title,
                    'url' : link,
                    'summary' : item.get('description',''),
                }
            except AttributeError:
                continue
            items.append(itemdict)
        return items