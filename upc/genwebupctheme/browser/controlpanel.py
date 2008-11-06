from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import DropdownChoiceWidget

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from plone.fieldsets.fieldsets import FormFieldsets

from persistent import Persistent

from upc.genwebupctheme.browser.interfaces import *
from upc.genwebupctheme.browser.utils import getGWConfig
from plone.app.controlpanel.skins import ISkinsSchema 

class GenWebControlPanelUtility(Persistent):
    """Clase que implementa la utilitat i la fa persistent
    """
    implements(IgenWebUtility)
    
    # de la pestanya general
    columna1 = []
    columna2 = []
    columna3 = []
    constrains = ['Document', 'Event', 'File', 'Folder', 'Image', 'Link', 'News Item', 'Topic', 'Collage']

    # de la pestanya d'especifics
    especific1='#007dcc'
    especific2='#006DA3'
    especific3='#557c95'
    especific4='#aeb4b8'
    especific5='#e6e6e6'
    especific6='#f3f3f3'

    imatgedefonsprops='repeat-y'

    barraidiomesbool = False
    
    # de la pestanya d'informació
    titolespai_ca = 'Titol de lespai en catala'
    titolespai_es ='Titol de lespai en castella'
    titolespai_en = 'Titol de lespai en angles'
    firmaunitat_ca = 'Firma de la unitat en catala'
    firmaunitat_es = 'Firma de la unitat en castella'
    firmaunitat_en = 'Firma de la unitat en angles'
    edicio_ca = 'curs 2008/2009'
    edicio_es = 'curso 2008/2009'
    edicio_en = ' 2008/2009 Edition'
    enllaslogotip = 'http://www.upc.edu'
    contacteid = '200'
    contactegmaps = '<iframe width="640" height="480" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/?ie=UTF8&amp;s=AARTsJqzARj-Z8VnW5pkPMLMmZbqrJcYpw&amp;ll=41.390075,2.115383&amp;spn=0.007727,0.013733&amp;z=16&amp;output=embed"></iframe>'
    boolmaps = True
    
    # de la pestanya de sabors
    tipusintranet = 'Visible'
    titolcapsaleraMaster = 'Titol de capsalera del master'
    idestudiMaster = ''
    idtitulacioMaster = ''
    masterdoctorado = 'Master'
    
class GenWebControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IgenWebControlPanel)

    def __init__(self, context):
        super(GenWebControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(context, 'portal_skins')
        self.jstool = getToolByName(context, 'portal_javascripts')
        ptool = getToolByName(context, 'portal_properties')
        self.props = ptool.site_properties

    def get_theme(self):
        return self.context.getDefaultSkin()

    def set_theme(self, value):
        self.context.default_skin = value

    theme = property(get_theme, set_theme)

    @apply
    def columna1():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna1 = value
        return property(get, set)

    @apply    
    def columna2():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna2
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna2 = value
        return property(get, set)

    @apply
    def columna3():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna3
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna3 = value
        return property(get, set)
        
    @apply
    def constrains():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.constrains
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.constrains = value
        return property(get, set)        

    @apply
    def especific1():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def especific2():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific2
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific2 = value
        return property(get, set)

    @apply
    def especific3():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific3
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific3 = value
        return property(get, set)

    @apply
    def especific4():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific4
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific4 = value
        return property(get, set)

    @apply
    def especific5():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific5
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific5 = value
        return property(get, set)            

    @apply
    def especific6():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific6
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific6 = value
        return property(get, set)

    @apply
    def imatgedefonsprops():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.imatgedefonsprops
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.imatgedefonsprops = value
        return property(get, set)

    @apply
    def barraidiomesbool():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.barraidiomesbool
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.barraidiomesbool = value
        return property(get, set)

    @apply
    def titolespai_ca():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_ca
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_ca = value
        return property(get, set)

    @apply
    def titolespai_en():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_en
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_en = value
        return property(get, set)

    @apply
    def titolespai_es():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_es
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_es = value
        return property(get, set)
            
    @apply
    def firmaunitat_ca():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_ca
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_ca = value
        return property(get, set)

    @apply
    def firmaunitat_en():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_en
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_en = value
        return property(get, set)

    @apply
    def firmaunitat_es():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_es
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_es = value
        return property(get, set)

    @apply
    def edicio_ca():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.edicio_ca
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_es = value
        return property(get, set)
    
    @apply
    def edicio_en():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.edicio_en
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_es = value
        return property(get, set)
    
    @apply
    def edicio_es():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.edicio_es
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_es = value
        return property(get, set)
    
    @apply
    def enllaslogotip():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.enllaslogotip
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.enllaslogotip = value
        return property(get, set)

    @apply
    def contacteid():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.contacteid
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.contacteid = value
        return property(get, set)

    @apply
    def contactegmaps():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.contactegmaps
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.contactegmaps = value
        return property(get, set)

    @apply
    def boolmaps():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.boolmaps
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.boolmaps = value
        return property(get, set)

    @apply
    def tipusintranet():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.tipusintranet
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.tipusintranet = value
        return property(get, set)

    @apply
    def titolcapsaleraMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolcapsaleraMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolcapsaleraMaster = value
        return property(get, set)

    @apply
    def idestudiMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.idestudiMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.idestudiMaster = value
        return property(get, set)

    @apply
    def idtitulacioMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.idtitulacioMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.idtitulacioMaster = value
        return property(get, set)                    
    
    @apply
    def masterdoctorado():
        def get(self):
            return getGWConfig().masterdoctorado
        def set(self, value):
            getGWConfig().masterdoctorado = value
        return property(get, set)

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
