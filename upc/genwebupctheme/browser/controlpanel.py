# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import DropdownChoiceWidget

from zope.app.form.browser import RadioWidget as _RadioWidget

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from plone.fieldsets.fieldsets import FormFieldsets

from persistent import Persistent

from upc.genwebupctheme.browser.interfaces import *
from upc.genwebupctheme.browser.utils import getGWConfig
from plone.app.controlpanel.skins import ISkinsSchema

from Products.CMFPlone.utils import safe_unicode
from cgi import escape

class GenWebControlPanelUtility(object):
    """Clase que implementa la utilitat i la fa persistent
    """
    implements(IgenWebUtility)

    
class GenWebControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IgenWebControlPanel)

    def __init__(self, context):
        super(GenWebControlPanelAdapter, self).__init__(context)
        self.contextps = getToolByName(context, 'portal_skins')
        self.jstool = getToolByName(context, 'portal_javascripts')
        ptool = getToolByName(context, 'portal_properties')
        self.props = ptool.site_properties
        self.context = ptool.genwebupc_properties

    def get_theme(self):
        return self.contextps.getDefaultSkin()
    def set_theme(self, value):
        self.contextps.default_skin = value
    theme = property(get_theme, set_theme)

    columna1 = ProxyFieldProperty(IgenWebControlPanel['columna1'])
    columna2 = ProxyFieldProperty(IgenWebControlPanel['columna2'])
    columna3 = ProxyFieldProperty(IgenWebControlPanel['columna3'])

    constrains = ProxyFieldProperty(IgenWebControlPanel['constrains'])
    
    especific1 = ProxyFieldProperty(IgenWebControlPanel['especific1'])
    especific2 = ProxyFieldProperty(IgenWebControlPanel['especific2'])
    especific3 = ProxyFieldProperty(IgenWebControlPanel['especific3'])
    especific4 = ProxyFieldProperty(IgenWebControlPanel['especific4'])
    especific5 = ProxyFieldProperty(IgenWebControlPanel['especific5'])
    especific6 = ProxyFieldProperty(IgenWebControlPanel['especific6'])
    
    imatgedefonsprops = ProxyFieldProperty(IgenWebControlPanel['imatgedefonsprops'])

    titolespai_ca = ProxyFieldProperty(IgenWebControlPanel['titolespai_ca'])
    titolespai_es = ProxyFieldProperty(IgenWebControlPanel['titolespai_es'])
    titolespai_en = ProxyFieldProperty(IgenWebControlPanel['titolespai_en'])
    firmaunitat_ca = ProxyFieldProperty(IgenWebControlPanel['firmaunitat_ca'])
    firmaunitat_es = ProxyFieldProperty(IgenWebControlPanel['firmaunitat_es'])
    firmaunitat_en = ProxyFieldProperty(IgenWebControlPanel['firmaunitat_en'])
    enllaslogotip = ProxyFieldProperty(IgenWebControlPanel['enllaslogotip'])
    contacteid = ProxyFieldProperty(IgenWebControlPanel['contacteid'])
    contactegmaps = ProxyFieldProperty(IgenWebControlPanel['contactegmaps'])
    boolmaps = ProxyFieldProperty(IgenWebControlPanel['boolmaps'])
    
    
    tipusintranet = ProxyFieldProperty(IgenWebControlPanel['tipusintranet'])
    tipusNeutre2 = ProxyFieldProperty(IgenWebControlPanel['tipusNeutre2'])
    titolcapsaleraMaster = ProxyFieldProperty(IgenWebControlPanel['titolcapsaleraMaster'])    
    idestudiMaster = ProxyFieldProperty(IgenWebControlPanel['idestudiMaster'])    
    idtitulacioMaster = ProxyFieldProperty(IgenWebControlPanel['idtitulacioMaster'])    
    masterdoctorado = ProxyFieldProperty(IgenWebControlPanel['masterdoctorado'])
    ambitdoctorat_ca = ProxyFieldProperty(IgenWebControlPanel['ambitdoctorat_ca'])
    ambitdoctorat_es = ProxyFieldProperty(IgenWebControlPanel['ambitdoctorat_es'])
    ambitdoctorat_en = ProxyFieldProperty(IgenWebControlPanel['ambitdoctorat_en'])
    
#    @apply
#    def columna1():
#        def get(self):
#            return getGWConfig().columna1
#        def set(self, value):
#            getGWConfig().columna1 = value
#        return property(get, set)
#
#    @apply    
#    def columna2():
#        def get(self):
#            return getGWConfig().columna2
#        def set(self, value):
#            getGWConfig().columna2 = value
#        return property(get, set)
#
#    @apply
#    def columna3():
#        def get(self):
#            return getGWConfig().columna3
#        def set(self, value):
#            getGWConfig().columna3 = value
#        return property(get, set)
#        
#    @apply
#    def constrains():
#        def get(self):
#            return getGWConfig().constrains
#        def set(self, value):
#            getGWConfig().constrains = value
#        return property(get, set)        
#
#    @apply
#    def especific1():
#        def get(self):
#            return getGWConfig().especific1
#        def set(self, value):
#            getGWConfig().especific1 = value
#        return property(get, set)
#
#    @apply
#    def especific2():
#        def get(self):
#            return getGWConfig().especific2
#        def set(self, value):
#            getGWConfig().especific2 = value
#        return property(get, set)
#
#    @apply
#    def especific3():
#        def get(self):
#            return getGWConfig().especific3
#        def set(self, value):
#            getGWConfig().especific3 = value
#        return property(get, set)
#
#    @apply
#    def especific4():
#        def get(self):
#            return getGWConfig().especific4
#        def set(self, value):
#            getGWConfig().especific4 = value
#        return property(get, set)
#
#    @apply
#    def especific5():
#        def get(self):
#            return getGWConfig().especific5
#        def set(self, value):
#            getGWConfig().especific5 = value
#        return property(get, set)            
#
#    @apply
#    def especific6():
#        def get(self):
#            return getGWConfig().especific6
#        def set(self, value):
#            getGWConfig().especific6 = value
#        return property(get, set)
#
#    @apply
#    def imatgedefonsprops():
#        def get(self):
#            return getGWConfig().imatgedefonsprops
#        def set(self, value):
#            getGWConfig().imatgedefonsprops = value
#        return property(get, set)
#
#    @apply
#    def barraidiomesbool():
#        def get(self):
#            return getGWConfig().barraidiomesbool
#        def set(self, value):
#            getGWConfig().barraidiomesbool = value
#        return property(get, set)
#
#    @apply
#    def titolespai_ca():
#        
#        def get(self):
#            return getGWConfig().titolespai_ca
#        def set(self, value):
#            getGWConfig().titolespai_ca = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def titolespai_en():
#        def get(self):
#            return getGWConfig().titolespai_en
#        def set(self, value):
#            getGWConfig().titolespai_en = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def titolespai_es():
#        def get(self):
#            return getGWConfig().titolespai_es
#        def set(self, value):
#            getGWConfig().titolespai_es = safe_unicode(value)
#        return property(get, set)
#            
#    @apply
#    def firmaunitat_ca():
#        def get(self):
#            return getGWConfig().firmaunitat_ca
#        def set(self, value):
#            getGWConfig().firmaunitat_ca = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def firmaunitat_en():
#        def get(self):
#            return getGWConfig().firmaunitat_en
#        def set(self, value):
#            getGWConfig().firmaunitat_en = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def firmaunitat_es():
#        def get(self):
#            return getGWConfig().firmaunitat_es
#        def set(self, value):
#            getGWConfig().firmaunitat_es = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def enllaslogotip():
#        def get(self):
#            return getGWConfig().enllaslogotip
#        def set(self, value):
#            getGWConfig().enllaslogotip = value
#        return property(get, set)
#
#    @apply
#    def contacteid():
#        def get(self):
#            return getGWConfig().contacteid
#        def set(self, value):
#            getGWConfig().contacteid = value
#        return property(get, set)
#
#    @apply
#    def contactegmaps():
#        def get(self):
#            return getGWConfig().contactegmaps
#        def set(self, value):
#            getGWConfig().contactegmaps = value
#        return property(get, set)
#
#    @apply
#    def boolmaps():
#        def get(self):
#            return getGWConfig().boolmaps
#        def set(self, value):
#            getGWConfig().boolmaps = value
#        return property(get, set)
#
#    @apply
#    def tipusintranet():
#        def get(self):
#            return getGWConfig().tipusintranet
#        def set(self, value):
#            getGWConfig().tipusintranet = value
#        return property(get, set)
#
#    @apply
#    def tipusNeutre2():
#        def get(self):
#            return getGWConfig().tipusNeutre2
#        def set(self, value):
#            getGWConfig().tipusNeutre2 = value
#        return property(get, set)
#
#
#    @apply
#    def titolcapsaleraMaster():
#        def get(self):
#            return getGWConfig().titolcapsaleraMaster
#        def set(self, value):
#            getGWConfig().titolcapsaleraMaster = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def idestudiMaster():
#        def get(self):
#            return getGWConfig().idestudiMaster
#        def set(self, value):
#            getGWConfig().idestudiMaster = value
#        return property(get, set)
#
#    @apply
#    def idtitulacioMaster():
#        def get(self):
#            return getGWConfig().idtitulacioMaster
#        def set(self, value):
#            getGWConfig().idtitulacioMaster = value
#        return property(get, set)                    
#    
#    @apply
#    def masterdoctorado():
#        def get(self):
#            return getGWConfig().masterdoctorado
#        def set(self, value):
#            getGWConfig().masterdoctorado = value
#        return property(get, set)
#
#    @apply
#    def ambitdoctorat_ca():
#        def get(self):
#            return getGWConfig().ambitdoctorat_ca
#        def set(self, value):
#            getGWConfig().ambitdoctorat_ca = safe_unicode(value)
#        return property(get, set)
#
#    @apply
#    def ambitdoctorat_es():
#        def get(self):
#            return getGWConfig().ambitdoctorat_es
#        def set(self, value):
#            getGWConfig().ambitdoctorat_es = safe_unicode(value)
#        return property(get, set)
#    
#    @apply
#    def ambitdoctorat_en():
#        def get(self):
#            return getGWConfig().ambitdoctorat_en
#        def set(self, value):
#            getGWConfig().ambitdoctorat_en = safe_unicode(value)
#        return property(get, set)
            
general = FormFieldsets(ISkinsSchema['theme'], IgenWebControlPanelSchemaGeneral)
general.id = 'genWebControlPanelgeneral'
general.label = _(u'label_gwcp_general', default=u'General')
general['theme'].custom_widget = DropdownChoiceWidget

especifics = FormFieldsets(IgenWebControlPanelSchemaEspecifics)
especifics.id = 'genWebControlPanelespecifics'
especifics.label = _(u'label_gwcp_especifics', default=u'Especific')

informacio = FormFieldsets(IgenWebControlPanelSchemaInformacio)
informacio.id = 'genWebControlPanelinformacio'
informacio.label = _(u'label_gwcp_informacio', default=u'Informacio')

sabors = FormFieldsets(IgenWebControlPanelSchemaSabors)
sabors.id = 'genWebControlPanelsabors'
sabors.label = _(u'label_gwcp_sabors', default=u'Sabors')
sabors['tipusintranet'].custom_widget = DropdownChoiceWidget

class GenWebControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(general, informacio, especifics, sabors)

    #form_fields = form_fields.select('theme','especial','columna1','columna2','columna3')
    #form_fields.fieldsets[0] = form_fields.fieldsets[0].select('theme','especial','columna1','columna2','columna3')

    label = _("genWeb settings")
    description = _("Settings that configures the behaviour of the genWeb.")
    form_name = _("genWeb settings")
