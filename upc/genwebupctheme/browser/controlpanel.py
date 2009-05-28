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
    enllaslogotipdret = ProxyFieldProperty(IgenWebControlPanel['enllaslogotipdret'])
    enllaslogotipdretalt = ProxyFieldProperty(IgenWebControlPanel['enllaslogotipdretalt'])    
    contacteid = ProxyFieldProperty(IgenWebControlPanel['contacteid'])
    contactegmaps = ProxyFieldProperty(IgenWebControlPanel['contactegmaps'])
    boolmaps = ProxyFieldProperty(IgenWebControlPanel['boolmaps'])
    codigoogle = ProxyFieldProperty(IgenWebControlPanel['codigoogle'])
    
    
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

    label = _("Genweb settings")
    description = _("Settings that configures the behaviour of the genWeb.")
    form_name = _("Genweb settings")
