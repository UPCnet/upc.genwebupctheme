from zope.i18nmessageid import MessageFactory
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from AccessControl import getSecurityManager

import json
import urllib2

PLMF = MessageFactory('plonelocales')


def getGWConfig(context):
    """ Funcio que retorna les configuracions del controlpanel
    """
    ptool = getToolByName(context, 'portal_properties')
    try:
        gwconfig = ptool.genwebupc_properties
    except:
        gwconfig = None
    return gwconfig


def havePermissionAtRoot(self):
    """Funcio que retorna si es Editor a l'arrel"""

    pm = getToolByName(self, 'portal_membership')
    tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
    proot = tools.url().getPortalObject()
    #proot=pu.getPortalObject()
    sm = getSecurityManager()
    user = pm.getAuthenticatedMember()

    return sm.checkPermission('Modify portal content', proot) or ('WebMaster' in user.getRoles())


def portal_url(self):
    """ Funcion a que retorna el path"""
    context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
    return context_state.current_base_url()


class utilitats(BrowserView):

    _dadesUnitat = None

    def _getDadesUnitat(self):
        """ Retorna les dades proporcionades pel WebService del SCP
        """
        id = self.getGWConfig().contacteid
        if id:
            if self._dadesUnitat == None:
                try:
                    url = urllib2.urlopen('https://bus-soa.upc.edu/SCP/InfoUnitatv1?id=' + id, timeout=10)
                    respuesta = url.read()
                    self._dadesUnitat = json.loads(respuesta)
                except:
                    pass
        if 'error' in self._dadesUnitat:
            if  self._dadesUnitat['error'] == 'La unitat no existeix':
                return False
        else:
            return self._dadesUnitat

    def getTitol(self):
        lt = getToolByName(self, 'portal_languages')
        lang = lt.getPreferredLanguage()
        gw_config = self.getGWConfig()
        titol = getattr(gw_config, 'titolespai_%s' % lang)
        return titol

    def getGWProperty(self, gwproperty):
        """Retorna de manera segura una propietat del GW"""
        property_value = getattr(self.getGWConfig(), gwproperty, '')
        if property_value is None:
            property_value = ''
        return property_value

    def llistaEstats(self):
        """Retorna una llista dels estats dels workflows indicats
        """
        wtool = getToolByName(self, 'portal_workflow')
        workflows = ['genweb_simple', 'genweb_review']
        estats = []
        for w in workflows:
            estats = estats + [s[0] for s in wtool.getWorkflowById(w).states.items()]

        return [w for w in wtool.listWFStatesByTitle() if w[0] in estats]

    def llistaContents(self):
        """Retorna tots els tipus de contingut, exclosos els de la llista types_to_exclude"""
        types_to_exclude = ['Banner', 'BannerContainer', 'CollageAlias', 'CollageColumn', 'CollageRow', 'Favorite', 'Large Plone Folder', 'Logos_Container', 'Logos_Footer', 'PoiPscTracker', 'SubSurvey', 'SurveyMatrix', 'SurveyMatrixQuestion', 'SurveySelectQuestion', 'SurveyTextQuestion', ]
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        ptypes = portal_state.friendly_types()
        for typeEx in types_to_exclude:
            if typeEx in ptypes:
                ptypes.remove(typeEx)

        return ptypes

    def portal_url(self):
        """ Funcion a que retorna el path"""
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.current_base_url()

    def dia_semana(self, day):
        """ Funcion a la que le pasas el dia y te lo devuelve en modo texto"""
        _ts = getToolByName(self, 'translation_service')
        dia = day + 1
        if dia == 7:
            dia = 0
        return PLMF(_ts. day_msgid(dia), default=_ts.weekday_english(dia, format='a'))

    def mes(self, month):
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
        """ Funcio que retorna les configuracions del controlpanel
        """
        ptool = getToolByName(self.context, 'portal_properties')
        try:
            gwconfig = ptool.genwebupc_properties
        except:
            gwconfig = None

        return gwconfig

    def isFolder(self):
        """ Funcio que retorna si es carpeta per tal de mostrar o no el last modified
        """
        if  IATFolder.providedBy(self.context) or IPloneSiteRoot.providedBy(self.context):
            return True

    def remapList2Dic(self, dictkeys, results):
        _dictResult = {}
        _dictKeys = dictkeys
        _results = results
        c = 0
        for ii in _dictKeys:
            _dictResult[ii] = _results[c]
            c = c + 1
        return _dictResult

    def recodifica(self, str):
        return str.decode('iso-8859-1').encode('utf-8')

    def getDirectori(self):
        try:
            ue = self._dadesUnitat['codi_upc']
            directori = "http://directori.upc.edu/directori/dadesUE.jsp?id=" + ue
        except:
            directori = ""
        return directori

    def getNomCentre(self):
        """ Retorna el nom del centre segons l'idioma
        """
        lang = self.pref_lang()
        try:
            nom_centre = self._dadesUnitat['nom_' + lang]
        except:
            nom_centre = ""
        return nom_centre

    def getEdifici(self):
        """Retorna edifici en l'idioma del portal
        """
        lang = self.pref_lang()
        try:
            edifici = self._dadesUnitat['edifici_' + lang]
        except:
            edifici = ""
        return edifici

    def getCampus(self):
        """Retorna edifici en l'idioma del portal
        """
        lang = self.pref_lang()
        try:
            campus = self._dadesUnitat['campus_' + lang]
        except:
            campus = ""
        return campus

    def fields2Dic(self, dc, de, di):
        tmp = (dc, de, di)
        dictKeys = ('doc_ca', 'doc_es', 'doc_en',)
        return self.remapList2Dic(dictKeys, tmp)

    def test(self, value, trueVal, falseVal):
        """
            helper method, mainly for setting html attributes.
        """
        if value:
            return trueVal
        else:
            return falseVal

    def getSectionFromURL(self):
        context = self.context
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')

        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        contentPath = tools.url().getRelativeContentPath(context)
        if not contentPath:
            return ''
        else:
            return portal_state.portal()[contentPath[0]].Title().replace('&nbsp;', '')

    def getFlavour(self):
        portal_skins = getToolByName(self.context, 'portal_skins')
        return portal_skins.getDefaultSkin()

    def assignAltAcc(self):
        """ Assignar alt per accessibilitat a links en finestra nova
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        label = "(obriu en una finestra nova)"
        if idioma == 'ca':
            label = "(obriu en una finestra nova)"
        if idioma == 'es':
            label = "(abre en ventana nueva)"
        if idioma == 'en':
            label = "(open in new window)"
        return label

    def premsa_url(self):
        """Funcio que extreu idioma actiu
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        if idioma == 'zh':
            url = 'http://www.upc.edu/saladepremsa/?set_language=en'
        else:
            url = 'http://www.upc.edu/saladepremsa/?set_language=' + idioma
        return url

    def premsa_PDIPAS_url(self):
        """Funcio que extreu idioma actiu
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        if idioma == 'zh':
            url = 'http://www.upc.edu/saladepremsa/pdi-pas/?set_language=en'
        else:
            url = 'http://www.upc.edu/saladepremsa/pdi-pas/?set_language=' + idioma
        return url

    def SearchUrl(self):
        idioma = self.pref_lang()
        url = "http://www.upc.edu/cerca"
        if idioma == 'ca':
            url = "http://www.upc.edu/cerca"
        if idioma == 'es':
            url = "http://www.upc.edu/busqueda"
        if idioma == 'en':
            url = "http://www.upc.edu/search-upc"
        return url
