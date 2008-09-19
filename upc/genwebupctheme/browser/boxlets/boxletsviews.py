from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from Products.CMFPlone import PloneMessageFactory as _
from Acquisition import aq_inner
from time import localtime
import feedparser

from zope import schema
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Products.CMFCore.utils import getToolByName

from StringIO import StringIO
from zope.i18nmessageid import MessageFactory
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from Products.PythonScripts.standard import url_quote_plus
from plone.app.portlets import cache

from plone.app.portlets.portlets.calendar import Renderer as calendar_render
from plone.app.portlets.portlets.news import Renderer as news_render

#productes addicionals amb salvaguardes
try:
    from Products.PlonePopoll.browser.popoll import Renderer as enquesta_render
except ImportError:
    HAS_POPOLL = False
    enquesta_render = news_render
else:
    HAS_POPOLL = True

PLMF = MessageFactory('plonelocales')

class enquesta(BrowserView,enquesta_render):
	_template = ViewPageTemplateFile('enquesta.pt')

	def __init__(self, context, request):
		self.polls = self._polls()
		return

	def __call__(self):
		return xhtml_compress(self._template())


# Vistes de agenda i calendari
class agenda(BrowserView,calendar_render):
    _template = ViewPageTemplateFile('agenda.pt')
    updated = False
    
    def __init__(self, context, request):
        
        BrowserView.__init__(self, context, request)
        #del portlet de calendar
        calendar_render.update(self)
     
        self.utils = getMultiAdapter((self.context, self.request),
                                        name=u'upc.genweb.utils')
        self.now = localtime()

        #del portlet de events
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()

        self.have_events_folder = 'events' in self.portal.objectIds()

    def __call__(self):
        return xhtml_compress(self._template())

#funciones correspondientes a la parte genweb del boxlet    

    def mes(self, mes):
        return self.utils.mes(mes)
    
    def dia_semana(self, dia):
        return self.utils.dia_semana(dia)
        
#funciones correspondientes a la parte de adquisicion de eventos    

    @property
    def available(self):
        return len(self._data())

    def published_events(self):
        return self._data()

    def all_events_link(self):
        if self.have_events_folder:
            return '%s/events' % self.portal_url
        else:
            return '%s/events_listing' % self.portal_url

    def prev_events_link(self):
        if (self.have_events_folder and
            'aggregator' in self.portal['events'].objectIds() and
            'previous' in self.portal['events']['aggregator'].objectIds()):
            return '%s/events/aggregator/previous' % self.portal_url
            
        elif (self.have_events_folder and
            'previous' in self.portal['events'].objectIds()):
            return '%s/events/previous' % self.portal_url
        else:
            return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = 5
        state = 'published'
        return catalog(portal_type='Event',
                       review_state=state,
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       sort_limit=limit)[:limit]

class agendamini(agenda):
    _template = ViewPageTemplateFile('agenda_mini.pt')
   
class agendaCalendariPetit(agenda):
    _template = ViewPageTemplateFile('agenda_calendari_petit.pt')

class noticies(BrowserView, news_render):
    _template = ViewPageTemplateFile('noticies.pt')
    
    def __call__(self):
        return xhtml_compress(self._template())
    
    @memoize
    def _data(self):       
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = 5
        state = 'published'
        return catalog(portal_type='News Item',
                       review_state=state,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=limit)[:limit]

# Vistes de noticies

class noticies_actualitat(noticies):
    _template = ViewPageTemplateFile('noticies_actualitat.pt')
    
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

class noticies_actualitat_petit(noticies_actualitat):
    _template = ViewPageTemplateFile('actualitat_noticies_petit.pt')

class noticies_actualitat_mini(noticies_actualitat):
    _template = ViewPageTemplateFile('actualitat_noticies_mini.pt')

class actualitat_petit(noticies_actualitat):
    _template = ViewPageTemplateFile('actualitat_petit.pt')

class noticies_petit(noticies):
    _template = ViewPageTemplateFile('noticies_petit.pt')