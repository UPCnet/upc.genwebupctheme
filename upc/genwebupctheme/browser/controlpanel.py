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
    titolespai_ca = escape(safe_unicode('Títol de l\'espai en català'))
    titolespai_es = escape(safe_unicode('Títol de l\'espai en castellà'))
    titolespai_en = escape(safe_unicode('Títol de l\'espai en anglés'))
    firmaunitat_ca = escape(safe_unicode('Firma de la unitat en català'))
    firmaunitat_es = escape(safe_unicode('Firma de la unitat en castellà'))
    firmaunitat_en = escape(safe_unicode('Firma de la unitat en anglés'))
    edicio_ca = 'curs 2008/2009'
    edicio_es = 'curso 2008/2009'
    edicio_en = ' 2008/2009 Edition'
    enllaslogotip = 'http://www.upc.edu'
    contacteid = '200'
    contactegmaps = '<iframe width="640" height="480" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/?ie=UTF8&amp;s=AARTsJqzARj-Z8VnW5pkPMLMmZbqrJcYpw&amp;ll=41.390075,2.115383&amp;spn=0.007727,0.013733&amp;z=16&amp;output=embed"></iframe>'
    boolmaps = True
    
    # de la pestanya de sabors
    tipusintranet = 'Visible'
    tipusNeutre2 = 'Default'
    titolcapsaleraMaster = '2008/2009'
    idestudiMaster = '50'
    idtitulacioMaster = '114'
    masterdoctorado = 'Master'
    ambitdoctorat_ca = escape(safe_unicode('Àmbit doctorat - [català]'))
    ambitdoctorat_es = escape(safe_unicode('Àmbit doctorat - [castellà]'))
    ambitdoctorat_en = escape(safe_unicode('Àmbit doctorat - [english]'))
    
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
            return getGWConfig().columna1
        def set(self, value):
            getGWConfig().columna1 = value
        return property(get, set)

    @apply    
    def columna2():
        def get(self):
            return getGWConfig().columna2
        def set(self, value):
            getGWConfig().columna2 = value
        return property(get, set)

    @apply
    def columna3():
        def get(self):
            return getGWConfig().columna3
        def set(self, value):
            getGWConfig().columna3 = value
        return property(get, set)
        
    @apply
    def constrains():
        def get(self):
            return getGWConfig().constrains
        def set(self, value):
            getGWConfig().constrains = value
        return property(get, set)        

    @apply
    def especific1():
        def get(self):
            return getGWConfig().especific1
        def set(self, value):
            getGWConfig().especific1 = value
        return property(get, set)

    @apply
    def especific2():
        def get(self):
            return getGWConfig().especific2
        def set(self, value):
            getGWConfig().especific2 = value
        return property(get, set)

    @apply
    def especific3():
        def get(self):
            return getGWConfig().especific3
        def set(self, value):
            getGWConfig().especific3 = value
        return property(get, set)

    @apply
    def especific4():
        def get(self):
            return getGWConfig().especific4
        def set(self, value):
            getGWConfig().especific4 = value
        return property(get, set)

    @apply
    def especific5():
        def get(self):
            return getGWConfig().especific5
        def set(self, value):
            getGWConfig().especific5 = value
        return property(get, set)            

    @apply
    def especific6():
        def get(self):
            return getGWConfig().especific6
        def set(self, value):
            getGWConfig().especific6 = value
        return property(get, set)

    @apply
    def imatgedefonsprops():
        def get(self):
            return getGWConfig().imatgedefonsprops
        def set(self, value):
            getGWConfig().imatgedefonsprops = value
        return property(get, set)

    @apply
    def barraidiomesbool():
        def get(self):
            return getGWConfig().barraidiomesbool
        def set(self, value):
            getGWConfig().barraidiomesbool = value
        return property(get, set)

    @apply
    def titolespai_ca():
        
        def get(self):
            return getGWConfig().titolespai_ca
        def set(self, value):
            getGWConfig().titolespai_ca = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def titolespai_en():
        def get(self):
            return getGWConfig().titolespai_en
        def set(self, value):
            getGWConfig().titolespai_en = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def titolespai_es():
        def get(self):
            return getGWConfig().titolespai_es
        def set(self, value):
            getGWConfig().titolespai_es = escape(safe_unicode(value))
        return property(get, set)
            
    @apply
    def firmaunitat_ca():
        def get(self):
            return getGWConfig().firmaunitat_ca
        def set(self, value):
            getGWConfig().firmaunitat_ca = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def firmaunitat_en():
        def get(self):
            return getGWConfig().firmaunitat_en
        def set(self, value):
            getGWConfig().firmaunitat_en = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def firmaunitat_es():
        def get(self):
            return getGWConfig().firmaunitat_es
        def set(self, value):
            getGWConfig().firmaunitat_es = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def edicio_ca():
        def get(self):
            return getGWConfig().edicio_ca
        def set(self, value):
            getGWConfig().firmaunitat_es = escape(safe_unicode(value))
        return property(get, set)
    
    @apply
    def edicio_en():
        def get(self):
            return getGWConfig().edicio_en
        def set(self, value):
            getGWConfig().firmaunitat_es = escape(safe_unicode(value))
        return property(get, set)
    
    @apply
    def edicio_es():
        def get(self):
            return getGWConfig().edicio_es
        def set(self, value):
            getGWConfig().firmaunitat_es = escape(safe_unicode(value))
        return property(get, set)
    
    @apply
    def enllaslogotip():
        def get(self):
            return getGWConfig().enllaslogotip
        def set(self, value):
            getGWConfig().enllaslogotip = value
        return property(get, set)

    @apply
    def contacteid():
        def get(self):
            return getGWConfig().contacteid
        def set(self, value):
            getGWConfig().contacteid = value
        return property(get, set)

    @apply
    def contactegmaps():
        def get(self):
            return getGWConfig().contactegmaps
        def set(self, value):
            getGWConfig().contactegmaps = value
        return property(get, set)

    @apply
    def boolmaps():
        def get(self):
            return getGWConfig().boolmaps
        def set(self, value):
            getGWConfig().boolmaps = value
        return property(get, set)

    @apply
    def tipusintranet():
        def get(self):
            return getGWConfig().tipusintranet
        def set(self, value):
            getGWConfig().tipusintranet = value
        return property(get, set)

    @apply
    def tipusNeutre2():
        def get(self):
            return getGWConfig().tipusNeutre2
        def set(self, value):
            getGWConfig().tipusNeutre2 = value
        return property(get, set)


    @apply
    def titolcapsaleraMaster():
        def get(self):
            return getGWConfig().titolcapsaleraMaster
        def set(self, value):
            getGWConfig().titolcapsaleraMaster = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def idestudiMaster():
        def get(self):
            return getGWConfig().idestudiMaster
        def set(self, value):
            getGWConfig().idestudiMaster = value
        return property(get, set)

    @apply
    def idtitulacioMaster():
        def get(self):
            return getGWConfig().idtitulacioMaster
        def set(self, value):
            getGWConfig().idtitulacioMaster = value
        return property(get, set)                    
    
    @apply
    def masterdoctorado():
        def get(self):
            return getGWConfig().masterdoctorado
        def set(self, value):
            getGWConfig().masterdoctorado = value
        return property(get, set)

    @apply
    def ambitdoctorat_ca():
        def get(self):
            return getGWConfig().ambitdoctorat_ca
        def set(self, value):
            getGWConfig().ambitdoctorat_ca = escape(safe_unicode(value))
        return property(get, set)

    @apply
    def ambitdoctorat_es():
        def get(self):
            return getGWConfig().ambitdoctorat_es
        def set(self, value):
            getGWConfig().ambitdoctorat_es = escape(safe_unicode(value))
        return property(get, set)
    
    @apply
    def ambitdoctorat_en():
        def get(self):
            return getGWConfig().ambitdoctorat_en
        def set(self, value):
            getGWConfig().ambitdoctorat_en = escape(safe_unicode(value))
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
