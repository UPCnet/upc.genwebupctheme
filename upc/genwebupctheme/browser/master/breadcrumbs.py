from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from zope.interface import implements
from Acquisition import aq_inner

class infoGeneral(BrowserView):
	implements(INavigationBreadcrumbs)

	def breadcrumbs(self):
		base = [{'absolute_url': 'info-general',
				'Title' : 'Informacio general'}]
		return base 

class competencies(BrowserView):
	implements(INavigationBreadcrumbs)

	def breadcrumbs(self):
		base = [{'absolute_url': 'competencies',
				'Title' : 'Competencies'}]
		return base 

class requisits(BrowserView):
	implements(INavigationBreadcrumbs)

	def breadcrumbs(self):
		base = [{'absolute_url': 'requisits',
				'Title' : 'Requisits'}]
		return base 


