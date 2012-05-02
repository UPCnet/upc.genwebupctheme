from zope.i18nmessageid import MessageFactory
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from AccessControl import getSecurityManager

import MySQLdb

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

    def connectDatabase(self):
        return MySQLdb.connect(host='nucli.upc.edu', user='cons-webupc', passwd='qstacll', db='www-webupc')
        #return MySQLdb.connect(host='raiden.upc.es',user='consulta',passwd='c0ns4lt4',db='www-estudis')

    def change2UTF(self, c):
        c.execute('SET NAMES utf8;')
        c.execute('SET CHARACTER SET utf8;')
        c.execute('SET character_set_connection=utf8;')
        return c

    def recodifica(self, str):
        return str.decode('iso-8859-1').encode('utf-8')

    def verificaIdUnitat(self, id):
        try:
            db = self.connectDatabase()
            c = db.cursor()
            c = self.change2UTF(c)
            c.execute("""SELECT id_unitat FROM upc_unitat WHERE id_unitat = %s""", (id,))
            results = c.fetchone()
        except:
            results = None
        return results

    def verificaIdEnlace(self, id):
        db = self.connectDatabase()
        c = db.cursor()
        c = self.change2UTF(c)
        c.execute("""SELECT personal FROM upc_unitat WHERE id_unitat = %s""", (id,))
        results = c.fetchone()
        dictKeys = ('personal',)
        _result = self.remapList2Dic(dictKeys, results)
        if _result['personal'] == None:
            return "http://directori.upc.edu/directori/dadesUE.jsp?id=" + id
        else:
            return _result['personal']

    def getContacteDataSql(self, id):
        """ Retorna un diccionario con datos de la tabla upc.unitat de la base de datos www-estudis
            de acuerdo a un id.
        """
        db = self.connectDatabase()
        c = db.cursor()
        c = self.change2UTF(c)
        c.execute("""SELECT nom_cat, nom_esp, nom_ing, direccion, telefono, fax, email, web, director, personal FROM upc_unitat WHERE id_unitat = %s""", (id,))

        results = c.fetchone()
        dictKeys = ('nom_cat', 'nom_esp', 'nom_ing', 'direccion', 'telefono', 'fax', 'email', 'web', 'director', 'personal')

        return self.remapList2Dic(dictKeys, results)

    def getContacteDireccion(self, id):
        db = self.connectDatabase()
        c = db.cursor()
        c = self.change2UTF(c)
        c.execute("""SELECT ue.codi_edifici, ue.nom_cat AS nomEdifici,ue.direccio, ue.codi_postal, ue.id_campus, uc.nom_cat AS nomCampus, ul.nom AS nomLocalitat FROM upc_unitat_edifici uue, upc_edifici ue, upc_campus uc, upc_localitats ul WHERE uue.id_unitat=%s AND uue.es_seu=1 AND uue.id_edifici=ue.id_edifici AND ue.id_campus=uc.id_campus AND uc.id_localitats=ul.id_localitats""", (id,))
        try:
            results = c.fetchone()
            dictKeys = ('codi_edifici', 'nomEdifici', 'ue.direccio', 'ue.codi_postal', 'ue.id_campus', 'nomCampus', 'nomLocalitat')
            return self.remapList2Dic(dictKeys, results)
        except:
            return None

    def cambiaPrefijo(self, lang):
        tmp = 'ing'
        if lang == 'ca':
            tmp = 'cat'
        elif lang == 'es':
            tmp = 'esp'

        return tmp

    def getTextMaster(self, str, lang):

        db = self.connectDatabase()
        c = db.cursor()
        c = self.change2UTF(c)
        c.execute("""SELECT cat,esp,ing FROM upc_textos WHERE id = %s""", (str,))
        results = c.fetchone()

        dictKeys = ('cat', 'esp', 'ing',)

        _result = self.remapList2Dic(dictKeys, results)

        tmp = self.cambiaPrefijo(lang)

        return _result[tmp]


        
    def fields2Dic(self, dc, de, di):
        tmp = (dc, de, di)
        dictKeys = ('doc_ca', 'doc_es', 'doc_en',)    
        
        return self.remapList2Dic(dictKeys,tmp)

    def test(self, value, trueVal, falseVal):
        """
            helper method, mainly for setting html attributes.
        """
        if value:
            return trueVal
        else:
            return falseVal
    
    def getSectionFromURL(self):
        context=self.context
        #portal_url=getToolByName(context, 'portal_url')
        tools = getMultiAdapter((self.context, self.request),
                                        name=u'plone_tools')       
        
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        contentPath = tools.url().getRelativeContentPath(context)
        if not contentPath:
            return ''
        else:
            return portal_state.portal()[contentPath[0]].Title().replace('&nbsp;','')

    def getFlavour(self):
        portal_skins=getToolByName(self.context, 'portal_skins')
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
            url = 'http://www.upc.edu/saladepremsa/?set_language='+idioma
        return url

    def premsa_PDIPAS_url(self):
        """Funcio que extreu idioma actiu
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        if idioma == 'zh':            
            url = 'http://www.upc.edu/saladepremsa/pdi-pas/?set_language=en'
        else:           
            url = 'http://www.upc.edu/saladepremsa/pdi-pas/?set_language='+idioma
        return url
