from StringIO import StringIO
from time import localtime
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter, getUtility
from upc.genwebupc.browser.interfaces import IgenWebUtility, IExtractInfo
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

PLMF = MessageFactory('plonelocales')

class utilitats(BrowserView):

    def portal_url(self):
        """ Funcion a que retorna el path 
        """
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.current_base_url()

    def dia_semana(self,day):
        """ Funcion a la que le pasas el dia y te lo devuelve en modo texto
        """
        _ts = getToolByName(self, 'translation_service')
        dia = day+1
        if dia == 7:
            dia = 0
        return PLMF(_ts. day_msgid(dia), default=_ts.weekday_english(dia, format='a'))
        
    def mes(self,month):
        """ Funcion a la que le pasas el mes y te lo devuelve en modo texto
        """
        _ts = getToolByName(self, 'translation_service')
        return PLMF(_ts.month_msgid(month), default=_ts.month_english(month, format='a'))
    
    def pref_lang(self):
        """Funcio que extreu idioma actiu
        """
        lt = getToolByName(self, 'portal_languages')
        return lt.getPreferredLanguage()

    def getGWConfig(self):
        """ Funcio que retorna la utility que conte les configuracions del controlpanel
        """
        gwconfig = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gwconfig
    
    def isFolder(self):
        """ Funcio que retorna si es carpeta per tal de mostrar o no el last modified
        """
        if  IATFolder.providedBy(self.context) or IPloneSiteRoot.providedBy(self.context):
            return True

    def getDatabaseInformation(self, id):
        """ Retorna un objeto con las columnas de la tabla upc.unitat de la base de datos www-estudis 
            de acuerdo al id de la escuela.
        """
        util = getUtility(IExtractInfo)
        return util.getDatos(id)

