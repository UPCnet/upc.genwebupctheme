from time import localtime

from Acquisition import aq_inner
from DateTime import DateTime
from StringIO import StringIO

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from zope.component import getUtility, getMultiAdapter
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import safe_unicode

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import cache
from plone.app.portlets.portlets import base
from plone.app.portlets.portlets.calendar import Renderer as CalendarRenderer

from Products.PythonScripts.standard import url_quote_plus

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('upc.genweb.banners')
PLMF = MessageFactory('plonelocales')

# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.

class IAgendaPortlet(IPortletDataProvider):
    """ Interface for the Agenda Portlet
    """

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(IAgendaPortlet)

    @property
    def title(self):
        return _(u"Agenda Portlet")

# copy from plone.app.portlets
def _render_cachekey(fun, self):
    context = aq_inner(self.context)
    if not self.updated:
        self.update()

    if self.calendar.getUseSession():
        raise ram.DontCache()
    else:
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        key = StringIO()
        print >> key, portal_state.navigation_root_url()
        print >> key, cache.get_language(context, self.request)
        print >> key, self.calendar.getFirstWeekDay()

        year, month = self.getYearAndMonthToDisplay()
        print >> key, year
        print >> key, month

        navigation_root_path = portal_state.navigation_root_path()
        start = DateTime('%s/%s/1' % (year, month))
        end = DateTime('%s/%s/1' % self.getNextMonth(year, month)) - 1

        def add(brain):
            key.write(brain.getPath())
            key.write('\n')
            key.write(brain.modified)
            key.write('\n\n')

        catalog = getToolByName(context, 'portal_catalog')
        path = navigation_root_path
        brains = catalog(
            portal_type=self.calendar.getCalendarTypes(),
            review_state=self.calendar.getCalendarStates(),
            start={'query': end, 'range': 'max'},
            end={'query': start, 'range': 'min'},
            path=path)

        for brain in brains:
            add(brain)

        return key.getvalue()
    
# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).

class Renderer(base.Renderer):
    """This is a pseudo-mixin class of the plone.app.portlet calendar renderer class,
       and methods from the upc.genwebupctheme calendar boxlet.
    """
    
    #
    # METHODS COPIED FROM: plone.app.portlets/plone/app/portlets/portlets/calendar.py
    #    

    _template = ViewPageTemplateFile('agenda.pt')
    updated = False


    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.updated = False

        self.utils = getMultiAdapter((self.context, self.request),
                                        name=u'upc.genweb.utils')
        self.now = localtime()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()
        self.have_events_folder = 'esdeveniments' in self.portal.objectIds()
        
    def update(self):
        if self.updated:
            return
        self.updated = True

        context = aq_inner(self.context)
        self.calendar = getToolByName(context, 'portal_calendar')
        self._ts = getToolByName(context, 'translation_service')
        self.url_quote_plus = url_quote_plus

        self.now = localtime()
        self.yearmonth = yearmonth = self.getYearAndMonthToDisplay()
        self.year = year = yearmonth[0]
        self.month = month = yearmonth[1]

        self.showPrevMonth = yearmonth > (self.now[0]-1, self.now[1])
        self.showNextMonth = yearmonth < (self.now[0]+1, self.now[1])

        self.prevMonthYear, self.prevMonthMonth = self.getPreviousMonth(year, month)
        self.nextMonthYear, self.nextMonthMonth = self.getNextMonth(year, month)

        self.monthName = PLMF(self._ts.month_msgid(month),
                              default=self._ts.month_english(month))

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def getEventsForCalendar(self):
        context = aq_inner(self.context)
        year = self.year
        month = self.month
        weeks = self.calendar.getEventsForCalendar(month, year)
        for week in weeks:
            for day in week:
                daynumber = day['day']
                if daynumber == 0:
                    continue
                day['is_today'] = self.isToday(daynumber)
                if day['event']:
                    cur_date = DateTime(year, month, daynumber)
                    localized_date = [self._ts.ulocalized_time(cur_date, context=context, request=self.request)]
                    day['eventstring'] = '\n'.join(localized_date+[self.getEventString(e) for e in day['eventslist']])
                    day['date_string'] = '%s-%s-%s' % (year, month, daynumber)

        return weeks

    def getEventString(self, event):
        start = event['start'] and ':'.join(event['start'].split(':')[:2]) or ''
        end = event['end'] and ':'.join(event['end'].split(':')[:2]) or ''
        title = safe_unicode(event['title']) or u'event'

        if start and end:
            eventstring = "%s-%s %s" % (start, end, title)
        elif start: # can assume not event['end']
            eventstring = "%s - %s" % (start, title)
        elif event['end']: # can assume not event['start']
            eventstring = "%s - %s" % (title, end)
        else: # can assume not event['start'] and not event['end']
            eventstring = title

        return eventstring

    def getYearAndMonthToDisplay(self):
        session = None
        request = self.request

        # First priority goes to the data in the REQUEST
        year = request.get('year', None)
        month = request.get('month', None)

        # Next get the data from the SESSION
        if self.calendar.getUseSession():
            session = request.get('SESSION', None)
            if session:
                if not year:
                    year = session.get('calendar_year', None)
                if not month:
                    month = session.get('calendar_month', None)

        # Last resort to today
        if not year:
            year = self.now[0]
        if not month:
            month = self.now[1]

        year, month = int(year), int(month)

        # Store the results in the session for next time
        if session:
            session.set('calendar_year', year)
            session.set('calendar_month', month)

        # Finally return the results
        return year, month

    def getPreviousMonth(self, year, month):
        if month==0 or month==1:
            month, year = 12, year - 1
        else:
            month-=1
        return (year, month)

    def getNextMonth(self, year, month):
        if month==12:
            month, year = 1, year + 1
        else:
            month+=1
        return (year, month)

    def getWeekdays(self):
        """Returns a list of Messages for the weekday names."""
        weekdays = []
        # list of ordered weekdays as numbers
        for day in self.calendar.getDayNumbers():
            weekdays.append(PLMF(self._ts.day_msgid(day, format='s'),
                                 default=self._ts.weekday_english(day, format='a')))

        return weekdays

    def isToday(self, day):
        """Returns True if the given day and the current month and year equals
           today, otherwise False.
        """
        return self.now[2]==day and self.now[1]==self.month and \
               self.now[0]==self.year

    def getReviewStateString(self):
        states = self.calendar.getCalendarStates()
        return ''.join(map(lambda x : 'review_state=%s&amp;' % self.url_quote_plus(x), states))

    def getQueryString(self):
        request = self.request
        query_string = request.get('orig_query',
                                   request.get('QUERY_STRING', None))
        if len(query_string) == 0:
            query_string = ''
        else:
            query_string = '%s&amp;' % query_string
        return query_string

    #
    # METHODS COPIED FROM: upc.genwebupctheme/upc/genwebupctheme/browser/boxletviews.py
    #
    
    #funciones correspondientes a la parte genweb del boxlet    

    def mes(self, mes):
        return self.utils.mes(mes)
    
    def dia_semana(self, dia):
        return self.utils.dia_semana(dia)

    #funciones correspondientes a la parte de adquisicion de eventos    

    #@property
    #def available(self):
    #    return len(self._data())
    
    def published_events(self):
        return self._data()

    def all_events_link(self):
        if self.have_events_folder:
            events = self.portal.esdeveniments.getTranslation()
            return '%s' % events.absolute_url()
        else:
            return '%s/events_listing' % self.portal_url

    def prev_events_link(self):
        previous_events = self.portal.esdeveniments.aggregator.anteriors.getTranslation()
        if self.have_events_folder:
            return '%s' % previous_events.absolute_url()
        else:
            return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = 5
        state = ['published','intranet']
        return catalog(portal_type=('Event','Meeting'),
                       review_state=state,
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       sort_limit=limit)[:limit]
                               
# Define the add forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
