from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements, Interface

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.app.portlets.utils import assignment_from_key
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.utils import unhashPortletInfo
from plone.portlets.interfaces import IPortletManager, IPortletRenderer

from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from datetime import datetime
from time import localtime

import feedparser

class ActualitatUPCview(BrowserView):

    #__call__ = ViewPageTemplateFile('actualitatUPC.pt')   
    
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