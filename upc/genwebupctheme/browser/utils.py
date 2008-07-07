from StringIO import StringIO
from time import localtime

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from zope.i18nmessageid import MessageFactory
from zope.interface import implements

from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import url_quote_plus

from plone.app.portlets import cache
from plone.app.portlets.portlets import base

from Products.Five.browser import BrowserView

PLMF = MessageFactory('plonelocales')

class utilitats(BrowserView):
    

    
    def dia_semana(self,day):
        """ le paso el dia y me lo pasa a texto"""
        _ts = getToolByName(self, 'translation_service')
        dia = day+1
        if dia == 7:
            dia = 0
        return PLMF(_ts. day_msgid(dia), default=_ts.weekday_english(dia, format='a'))
        
    def mes(self,month):
        """ le paso el mes y me lo pasa a texto"""
        _ts = getToolByName(self, 'translation_service')
        return PLMF(_ts.month_msgid(month), default=_ts.month_english(month, format='a'))