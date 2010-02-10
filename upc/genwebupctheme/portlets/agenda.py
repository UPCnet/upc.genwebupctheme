from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('upc.genweb.banners')

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
        return _(u"Agenda Porlet")

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).

class Renderer(base.Renderer):

    # render() will be called to render the portlet

    render = ViewPageTemplateFile('agenda.pt')

    # The following functions have been copied from 
    # upc.genwebupctheme.browser.boxlets.boxletsviews.agenda

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
