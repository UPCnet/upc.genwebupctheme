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
from upc.genwebupctheme.browser.interfaces import IgenWebUtility
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from AccessControl import getSecurityManager

import MySQLdb

PLMF = MessageFactory('plonelocales')


def getGWConfig(self):
    """ Funcio que retorna les configuracions del controlpanel
    """
    ptool = getToolByName(self.context, 'portal_properties')    
    try:
        gwconfig = ptool.genwebupc_properties
    except:
        gwconfig = None
    
    return gwconfig        

def havePermissionAtRoot(self):
     """Funcio que retorna si es Editor a l'arrel"""
     
     pm= getToolByName(self, 'portal_membership')   
     tools = getMultiAdapter((self.context, self.request),
                                        name=u'plone_tools')       
     proot = tools.url().getPortalObject()
     #proot=pu.getPortalObject()
     sm = getSecurityManager()
     user = pm.getAuthenticatedMember()
     
     return sm.checkPermission('Modify portal content', proot) or ('WebMaster' in user.getRoles())    

def portal_url(self):
        """ Funcion a que retorna el path 
        """
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.current_base_url()

class utilitats(BrowserView):

    def llistaEstats(self):
        """Retorna una llista dels estats dels workflows indicats
        """
        wtool = getToolByName(self,'portal_workflow')
        workflows = ['genweb_simple','genweb_review']
        estats = []
        for w in workflows:
            estats = estats + [s[0] for s in wtool.getWorkflowById(w).states.items()]
    
        return [w for w in wtool.listWFStatesByTitle() if w[0] in estats]

    def llistaContents(self):
        """Retorna tots els tipus de contingut, exclosos els de la llista types_to_exclude 
        """
        types_to_exclude = ['Banner', 'BannerContainer', 'CollageAlias', 'CollageColumn', 'CollageRow', 'Favorite', 'Large Plone Folder', 'Logos_Container', 'Logos_Footer', 'PoiPscTracker', 'SubSurvey', 'SurveyMatrix', 'SurveyMatrixQuestion', 'SurveySelectQuestion', 'SurveyTextQuestion',]
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        ptypes = portal_state.friendly_types()
        for typeEx in types_to_exclude:
            if typeEx in ptypes:
                ptypes.remove(typeEx)
        
        return ptypes
        
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
        c=0
        
        for ii in _dictKeys: 
            _dictResult[ii]=_results[c]
            c=c+1        

        return _dictResult

    def connectDatabase(self):
        return MySQLdb.connect(host='raiden.upc.es',user='cons-webupc',passwd='qstacll',db='www-webupc')
        #return MySQLdb.connect(host='raiden.upc.es',user='consulta',passwd='c0ns4lt4',db='www-estudis')

    def change2UTF(self,c):
        c.execute('SET NAMES utf8;')
        c.execute('SET CHARACTER SET utf8;')
        c.execute('SET character_set_connection=utf8;')  
        return c
 
    def recodifica(self, str):
        return str.decode('iso-8859-1').encode('utf-8')

    def verificaIdUnitat(self, id):
        try:
            db = self.connectDatabase()
            c=db.cursor()   
            c=self.change2UTF(c)  
            c.execute("""SELECT id_unitat FROM upc_unitat WHERE id_unitat = %s""", (id,))
            results = c.fetchone()
        except:
            results = None
        return results

    def verificaIdEnlace(self, id):
        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT personal FROM upc_unitat WHERE id_unitat = %s""", (id,))
        results = c.fetchone()
        dictKeys = ('personal',)     
        _result = self.remapList2Dic(dictKeys,results)     
        if _result['personal'] == None:
            return "http://directori.upc.edu/directori/dadesUE.jsp?id=" + id
        else:
            return _result['personal']

          
    def getContacteDataSql(self, id):
        """ Retorna un diccionario con datos de la tabla upc.unitat de la base de datos www-estudis 
            de acuerdo a un id.
        """      
        db = self.connectDatabase()
        c=db.cursor()
        c=self.change2UTF(c)
        c.execute("""SELECT nom_cat, nom_esp, nom_ing, direccion, telefono, fax, email, web, director, personal FROM upc_unitat WHERE id_unitat = %s""", (id,))


        results = c.fetchone()
        dictKeys = ('nom_cat', 'nom_esp', 'nom_ing', 'direccion', 'telefono', 'fax', 'email', 'web', 'director', 'personal')
           
        return self.remapList2Dic(dictKeys,results)

    def getContacteDireccion(self, id): 
        db = self.connectDatabase()
        c=db.cursor()
        c=self.change2UTF(c)
        c.execute("""SELECT ue.codi_edifici, ue.nom_cat AS nomEdifici,ue.direccio, ue.codi_postal, ue.id_campus, uc.nom_cat AS nomCampus, ul.nom AS nomLocalitat FROM upc_unitat_edifici uue, upc_edifici ue, upc_campus uc, upc_localitats ul WHERE uue.id_unitat=%s AND uue.es_seu=1 AND uue.id_edifici=ue.id_edifici AND ue.id_campus=uc.id_campus AND uc.id_localitats=ul.id_localitats""", (id,)) 
        try:
            results = c.fetchone()
            dictKeys = ('codi_edifici','nomEdifici','ue.direccio', 'ue.codi_postal', 'ue.id_campus','nomCampus','nomLocalitat')
            return self.remapList2Dic(dictKeys,results)
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
        c=db.cursor()  
        c=self.change2UTF(c)
        c.execute("""SELECT cat,esp,ing FROM upc_textos WHERE id = %s""", (str,))
        results = c.fetchone()

        dictKeys = ('cat', 'esp', 'ing',)    
             
        _result = self.remapList2Dic(dictKeys,results)

        tmp = self.cambiaPrefijo(lang)
        
        return _result[tmp]        
        
        
    def getMasterInfoGeneral(self, id_titulacio, id_estudi):
        
        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT upc_titulacio.*,upc_estudi.*, orientacio_cat, orientacio_esp, orientacio_ing, up.nom_cat pNom_cat,up.nom_esp pNom_esp, up.nom_ing pNom_ing, unitat.nom_cat uNom_cat, unitat.nom_esp uNom_esp, unitat.nom_ing uNom_ing, unitat.sigles,m_destinataris_cat, m_destinataris_esp, m_destinataris_ing, m_criteris_adm_cat, m_criteris_adm_esp, m_criteris_adm_ing,m_competencies_cat, m_competencies_esp, m_competencies_ing, m_professorat_cat, m_professorat_esp, m_professorat_ing, m_preu_cat, m_preu_esp, m_preu_ing FROM upc_titulacio,upc_titulacio_orientacio, upc_presencialitat up, upc_titulacio_plus plus,upc_estudi_plus plusEstudi, upc_estudi LEFT JOIN upc_unitat unitat ON upc_estudi.m_uni_coordinadora=unitat.id_unitat WHERE upc_titulacio.id_titulacio=%s AND upc_estudi.id_estudi=%s AND upc_titulacio_orientacio.m_id_orientacio=upc_titulacio.m_id_orientacio AND upc_estudi.id_presencialitat=up.id_presencialitat AND plus.id_titulacio=%s AND plusEstudi.id_estudi=%s""", (id_titulacio,id_estudi,id_titulacio,id_estudi,))
        results = c.fetchone()
        dictKeys = ('id_titulacio',
                    'nom_cat',
                    'nom_esp', 
                    'nom_ing', 
                    'descripcio_promocional_cat', 
                    'descripcio_promocional_esp', 
                    'descripcio_promocional_ing', 
                    'acces_cat',                  
                    'acces_esp',                  
                    'acces_ing',                   
                    'objectius_docents_cat',       
                    'objectius_docents_esp',       
                    'objectius_docents_ing',       
                    'sortides_professionals_cat',  
                    'sortides_professionals_esp',  
                    'sortides_professionals_ing',  
                    'm_id_orientacio',             
                    'id_cicle',                    
                    'es_master',                   
                    'id_tipus',                    
                    'id_ambit',                 
                    'id_estudi',                
                    'id_presencialitat',        
                    'nom_abreujat_cat',         
                    'nom_abreujat_esp',         
                    'nom_abreujat_ing',         
                    'carrega_lectiva',         
                    'horaris_cat',              
                    'horaris_esp',              
                    'horaris_ing',              
                    'nota_tall_PAU',            
                    'nota_tall_CFGS',           
                    'nota_tall_PAU_ad',         
                    'nota_tall_CFGS_ad',        
                    'places',                   
                    'preu',                     
                    'm_interuniversitari',      
                    'm_erasmus_mundus',         
                    'm_pla_estudis_cat',        
                    'm_email',                  
                    'm_data_inici_cat',         
                    'm_data_inici_esp',         
                    'm_data_inici_ing',         
                    'm_web',                    
                    'm_genweb',
                    'm_web_preinscripcio',      
                    'paraules_clau',            
                    'cfis',                     
                    'codi_preinscripcio',       
                    'm_activar_preinscripcio',  
                    'm_llistat_admesos',        
                    'm_uni_coordinadora',       
                    'm_lloc_imp_cat',           
                    'm_lloc_imp_esp',           
                    'm_lloc_imp_ing',           
                    'm_empreses',               
                    'm_pla_estudis_esp',        
                    'm_pla_estudis_ing',        
                    'doble_titulacio',          
                    'visible_web',              
                    'resolucio',                
                    'durada_cat',               
                    'durada_esp',               
                    'durada_ing',               
                    'places_cat',               
                    'places_esp',               
                    'places_ing',               
                    'beques_cat',               
                    'beques_esp',               
                    'beques_ing',               
                    'nota_pla_estudis_cat',     
                    'nota_pla_estudis_esp',     
                    'nota_pla_estudis_ing', 
                    'id_titulacio',
                    'orientacio_cat', 
                    'orientacio_esp', 
                    'orientacio_ing', 
                    'up.nom_cat pNom_cat',
                    'up.nom_esp pNom_esp', 
                    'up.nom_ing pNom_ing', 
                    'unitat.nom_cat uNom_cat',
                    'unitat.nom_esp uNom_esp', 
                    'unitat.nom_ing uNom_ing', 
                    'unitat.sigles',
                    'm_destinataris_cat', 
                    'm_destinataris_esp', 
                    'm_destinataris_ing', 
                    'm_criteris_adm_cat', 
                    'm_criteris_adm_esp', 
                    'm_criteris_adm_ing',
                    'm_competencies_cat', 
                    'm_competencies_esp', 
                    'm_competencies_ing', 
                    'm_professorat_cat', 
                    'm_professorat_esp', 
                    'm_professorat_ing',
                    'm_preu_cat',
                    'm_preu_esp',
                    'm_preu_ing',)
        
        return self.remapList2Dic(dictKeys,results)

    def getMobilitatEstudis(self, id_titulacio):

        db = self.connectDatabase()
        c=db.cursor()
        c=self.change2UTF(c)
        c.execute("""SELECT m_movilitat_cat,m_movilitat_esp,m_movilitat_ing FROM upc_titulacio_plus WHERE id_titulacio=%s""", (id_titulacio,))

        results = c.fetchone()
        dictKeys = (
                    'm_movilitat_cat',
                    'm_movilitat_esp',
                    'm_movilitat_ing',
                    )

        return self.remapList2Dic(dictKeys,results)

    def getPreinscripcioData(self, id_estudi):
 
        db = self.connectDatabase()
        cond = True
        c=db.cursor()
        c=self.change2UTF(c)
        c.execute("""SELECT m_web_preinscripcio FROM upc_estudi WHERE id_estudi=%s""", (id_estudi,))
        results = c.fetchone()
        dictKeys = (
                    'm_web_preinscripcio',
                    )
        tmp = self.remapList2Dic(dictKeys,results)
        condicion =  True 
        idioma = self.pref_lang()

        if len(tmp['m_web_preinscripcio']) == 0:
            if idioma == 'ca':
                url = 'http://www.upc.edu/aprendre/estudis/acces/masters_universitaris_quecalfer#preinscripcio_mu'
            elif idioma == 'es':
                url = 'http://www.upc.edu/aprender/estudios/acceso/masters-universitarios-queserequiere#preinscripcion_mu'
            elif idioma == 'en':
                url = 'http://www.upc.edu/master/preinscripcio_ing.php'                
            
            condicion = False
            return dict(preinscripcio = url, condicion = condicion)
        else:
            return dict(preinscripcio = tmp, condicion = condicion)

    def getMasterRequisits(self, id_titulacio, id_estudi):
        
        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT acces_cat,acces_esp,acces_ing,m_criteris_adm_cat,m_criteris_adm_esp,m_criteris_adm_ing FROM upc_titulacio,upc_titulacio_orientacio, upc_presencialitat up, upc_titulacio_plus plus,upc_estudi_plus plusEstudi, upc_estudi LEFT JOIN upc_unitat unitat ON upc_estudi.m_uni_coordinadora=unitat.id_unitat WHERE upc_titulacio.id_titulacio=%s AND upc_estudi.id_estudi=%s AND upc_titulacio_orientacio.m_id_orientacio=upc_titulacio.m_id_orientacio AND upc_estudi.id_presencialitat=up.id_presencialitat AND plus.id_titulacio=%s AND plusEstudi.id_estudi=%s""", (id_titulacio,id_estudi,id_titulacio,id_estudi,))
        results = c.fetchone()
        dictKeys = (    
                    'acces_cat',                  
                    'acces_esp',                  
                    'acces_ing', 
                    'm_criteris_adm_cat', 
                    'm_criteris_adm_esp', 
                    'm_criteris_adm_ing',
                    )
                               
        return self.remapList2Dic(dictKeys,results)

    def getMasterCompentencies(self, id_titulacio, id_estudi):
        
        db = self.connectDatabase()
        c=db.cursor()    
        c=self.change2UTF(c) 
        c.execute("""SELECT sortides_professionals_cat,sortides_professionals_cat,sortides_professionals_ing,m_competencies_cat, m_competencies_esp, m_competencies_ing FROM upc_titulacio,upc_titulacio_orientacio, upc_presencialitat up, upc_titulacio_plus plus,upc_estudi_plus plusEstudi, upc_estudi LEFT JOIN upc_unitat unitat ON upc_estudi.m_uni_coordinadora=unitat.id_unitat WHERE upc_titulacio.id_titulacio=%s AND upc_estudi.id_estudi=%s AND upc_titulacio_orientacio.m_id_orientacio=upc_titulacio.m_id_orientacio AND upc_estudi.id_presencialitat=up.id_presencialitat AND plus.id_titulacio=%s AND plusEstudi.id_estudi=%s""", (id_titulacio,id_estudi,id_titulacio,id_estudi,))
        results = c.fetchone()
        dictKeys = (    
                    'sortides_professionals_cat',  
                    'sortides_professionals_esp',  
                    'sortides_professionals_ing',  
                    'm_competencies_cat', 
                    'm_competencies_esp', 
                    'm_competencies_ing', 
                    )

        return self.remapList2Dic(dictKeys,results)

    def select_idiomes(self, id_estudi):
        
        db = self.connectDatabase()
        c=db.cursor()  
        c=self.change2UTF(c)
        c.execute("""SELECT ui.nom_cat, ui.nom_esp, ui.nom_ing FROM upc_estudis_idioma uei, upc_idioma ui WHERE uei.id_estudi=%s AND uei.id_idioma=ui.id_idioma""", (id_estudi,))
        results = c.fetchall()

        dictKeys = ('ui.nom_cat', 'ui.nom_esp', 'ui.nom_ing',)    
        _result = []
        j=0
        for i in results:
            _result.append(self.remapList2Dic(dictKeys,results[j]))
            j=j+1

        return _result



    def select_organitzadors(self, id_estudi):

        db = self.connectDatabase()
        c=db.cursor() 
        c=self.change2UTF(c)
        c.execute("""SELECT DISTINCT uu.id_unitat, uu.nom_cat, uu.nom_esp, uu.nom_ing, uu.sigles, CASE WHEN sub.id=2 THEN 1 WHEN sub.id=1 THEN 2 ELSE 99 END orden_tipus FROM upc_on_simparteix uos,upc_unitat uu LEFT JOIN scp_unitat_basiques sub ON uu.id_unitat=sub.id_unitat WHERE uos.id_estudi=%s AND uos.id_unitat=uu.id_unitat ORDER BY uu.nom_cat""", (id_estudi,))
        results = c.fetchall()

        dictKeys = ('uu.id_unitat', 'uu.nom_cat', 'uu.nom_esp', 'uu.nom_ing', 'uu.sigles','orden_tipus',)    

        _result = []
        j=0
        for i in results:
            _result.append(self.remapList2Dic(dictKeys,results[j]))
            j=j+1

        return _result 
    
    def select_organitzadors_old(self, id_estudi):

        db = self.connectDatabase()
        c=db.cursor() 
        c=self.change2UTF(c)
        c.execute("""SELECT DISTINCT uu.id_unitat, uu.nom_cat, uu.nom_esp, uu.nom_ing , uu.sigles, CASE WHEN sut.id=2 AND sub.id=2 THEN 1 WHEN sut.id=2 AND sub.id=1 THEN 2 ELSE 99 END orden_tipus FROM upc_on_simparteix uos, upc_unitat uu LEFT JOIN scp_unitat_tipus sut ON uu.id_unitat=sut.id_unitat LEFT JOIN scp_unitat_basiques sub ON uu.id_unitat=sub.id_unitat WHERE uos.id_estudi=%s AND uos.id_unitat=uu.id_unitat ORDER BY orden_tipus, uu.nom_cat""", (id_estudi,))
        results = c.fetchall()

        dictKeys = ('uu.id_unitat', 'uu.nom_cat', 'uu.nom_esp', 'uu.nom_ing', 'uu.sigles','orden_tipus',)    
        _result = []
        j=0
        for i in results:
            _result.append(self.remapList2Dic(dictKeys,results[j]))
            j=j+1

        return _result

    def select_subTipus(self, id_unitat):

        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT sub.id FROM scp_unitat_basiques sub , scp_basiques sb WHERE sub.id_unitat=%s AND sub.id = sb.id""", (id_unitat,))
        results = c.fetchone()
        dictKeys = ('sub.id',)
           
        return self.remapList2Dic(dictKeys,results)

    def select_tipus(self, id_unitat):
        
        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT sut.id id, web FROM scp_unitat_tipus sut, upc_unitat uni WHERE sut.id_unitat=%s AND uni.id_unitat=%s""", (id_unitat,id_unitat,))
        results = c.fetchall()
        
        dictKeys = ('sut.id id', 'web',)           
        _result = []
        j=0
        for i in results:
            _result.append(self.remapList2Dic(dictKeys,results[j]))
            j=j+1

        return _result

    def select_ambit(self, id_tit):
        
        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT ua.nom_cat, ua.nom_esp, ua.nom_ing FROM upc_titulacio LEFT JOIN upc_ambits ua ON ua.id_ambit=upc_titulacio.id_ambit WHERE upc_titulacio.id_titulacio=%s""", (id_tit,))
        results = c.fetchone()
        dictKeys = ('ua.nom_cat', 
                    'ua.nom_esp',
                    'ua.nom_ing',)
           
        return self.remapList2Dic(dictKeys,results)

    def recuperaLinkUnitats(self, id_unitat, lang):
        
        tipus = self.select_tipus(id_unitat)
        urltemp = 'x'
        
        for ii in tipus:
            if ii['sut.id id'] == 2:
                subtipus = self.select_subTipus(id_unitat)
                if subtipus['sub.id'] == 1:
                    urltemp='21_12x'
                if subtipus['sub.id'] == 2:
                    urltemp='22'
                if subtipus['sub.id'] == 3:
                    urltemp='23'                    
            if ii['sut.id id'] == 6:
                urltemp='6'

            if ii['sut.id id'] == 9:
                urltemp='9x'

            if ii['sut.id id'] == 12:
                urltemp='21_12x'

            if ii['sut.id id'] == 15:
                urltemp='15x'
  
        idioma = self.cambiaPrefijo(lang)
        return 'http://www.upc.edu/unitat/fitxa_unitat.php?id_unitat=' + str(id_unitat) + '&tip=' + urltemp + '&lang=' + idioma

    def select_participants(self, id_estudi):

        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT uu.id_unitat, uu.nom_cat, uu.nom_esp, uu.nom_ing, uu.sigles FROM upc_unitat uu, upc_master_universitat umu WHERE umu.id_estudi=%s AND umu.id_unitat=uu.id_unitat""", (id_estudi,))
        results = c.fetchall()
        
        dictKeys = ('uu.id_unitat', 'uu.nom_cat', 'uu.nom_esp', 'uu.nom_ing', 'uu.sigles',)           
        _result = []
        j=0
        for i in results:
            _result.append(self.remapList2Dic(dictKeys,results[j]))
            j=j+1

        return _result        
        
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

    def select_plaEstudis(self, id_estudi):

        db = self.connectDatabase()
        c=db.cursor()     
        c=self.change2UTF(c)
        c.execute("""SELECT upc_estudi.m_pla_estudis_cat, upc_estudi.m_pla_estudis_esp, upc_estudi.m_pla_estudis_ing FROM upc_estudi WHERE upc_estudi.id_estudi=%s""", (id_estudi,))
        results = c.fetchone()
        dictKeys = ('upc_estudi.m_pla_estudis_cat', 
                    'upc_estudi.m_pla_estudis_esp',
                    'upc_estudi.m_pla_estudis_ing',)
           
        return self.remapList2Dic(dictKeys,results)       
    
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
        url = ''
        label = "(obriu en una finestra nova)"
        if idioma == 'ca':
            label = "(obriu en una finestra nova)"
        if idioma == 'es':
            label = "(abre en ventana nueva)"
        if idioma == 'en':
            label = "(open in new window)"      
        return label
