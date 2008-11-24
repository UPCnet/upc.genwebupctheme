from plone.theme.interfaces import IDefaultPloneLayer
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import Interface, Attribute
from plone.app.controlpanel.skins import ISkinsSchema
import zope.schema

class IThemeSpecificNeutre3(IDefaultPloneLayer):
    """Marker interface del sabor Neutre3
    """

class IThemeSpecificUnitat(IDefaultPloneLayer):
    """Marker interface del sabor Unitat
    """

class IThemeSpecificNeutre2(IDefaultPloneLayer):
    """Marker interface del sabor Neutre2
    """

class IThemeSpecificMaster(IDefaultPloneLayer):
    """Marker interface del sabor Master
    """

class IThemeSpecificPortal(IDefaultPloneLayer):
    """Marker interface del sabor Portal
    """

class IgenWebUtility(Interface):
    """Marker Interface de la utility del control panel del genWeb
    """    
    
class IgenWebControlPanelSchemaGeneral(Interface):

    columna1 = zope.schema.List(__name__='columna1', title=u"Columna 1",value_type=zope.schema.Choice(values=['Agenda', 'Noticies', 'Noticies_Actualitat']), default=[])
    columna2 = zope.schema.List(__name__='columna2', title=u"Columna 2",value_type=zope.schema.Choice(values=['Agenda_Calendari', 'Actualitat_Noticies','Actualitat','Noticies']), default=[])
    columna3 = zope.schema.List(__name__='columna3', title=u"Columna 3",value_type=zope.schema.Choice(values=['Agenda', 'Actualitat_Noticies','Banners', 'Enquesta']), default=[])
    constrains = zope.schema.List(__name__='constrains', title=u"Contingut del menu afegir", description=u"Els elements de la columna de la dreta apareixeran al desplegable principal", value_type=zope.schema.Choice(values=['Document', 'Event', 'Favorite', 'File', 'Folder', 'Image', 'Link', 'News Item', 'Topic', 'Collage', 'Survey', 'PlonePopoll', 'Ploneboard', 'PoiTracker', 'simpleTask', 'Meeting', 'Window', 'FormFolder']), default=[])

    
class IgenWebControlPanelSchemaEspecifics(Interface):
    """ Marker interface de la pestanya dels colors especifics i altres opcions        
    """
    especific1 = zope.schema.TextLine(title=_(u'Especific 1'),)
    especific2 = zope.schema.TextLine(title=_(u'Especific 2'),)
    especific3 = zope.schema.TextLine(title=_(u'Especific 3'),)
    especific4 = zope.schema.TextLine(title=_(u'Especific 4'),)
    especific5 = zope.schema.TextLine(title=_(u'Especific 5'),)
    especific6 = zope.schema.TextLine(title=_(u'Especific 6'),)
    
    imatgedefonsprops = zope.schema.TextLine(title=_(u'Repeat imatge de fons'),required=False)


class IgenWebControlPanelSchemaInformacio(Interface):
    """ Marker interface de la pestanya dels literals        
    """
    titolespai_ca = zope.schema.TextLine(title=_(u'Titol de l\'espai - [catala]'),required=False)
    titolespai_es = zope.schema.TextLine(title=_(u'Titol de l\'espai - [castella]'),required=False)
    titolespai_en = zope.schema.TextLine(title=_(u'Titol de l\'espai - [angles]'),required=False)    
    firmaunitat_ca = zope.schema.TextLine(title=_(u'Firma de la unitat - [catala]'),required=False)
    firmaunitat_es = zope.schema.TextLine(title=_(u'Firma de la unitat - [castella]'),required=False)
    firmaunitat_en = zope.schema.TextLine(title=_(u'Firma de la unitat - [angles]'),required=False)
    enllaslogotip = zope.schema.TextLine(title=_(u'Enllac logotip de la unitat'),required=False)
    contacteid = zope.schema.TextLine(title=_(u'Contacta [id unitat]'),required=False)
    contactegmaps = zope.schema.TextLine(title=_(u'Codi google maps'),required=False)
    boolmaps = zope.schema.Bool(title=_(u'per que aparegui o no el mapa del google maps'),required=False)

class IgenWebControlPanelSchemaSabors(Interface):
    """ Marker interface de la pestanya de la informació sobre els sabors        
    """
    tipusintranet = zope.schema.Choice(title=_(u'Tipus d\'intranet'), values=['Visible', 'Discreta'], required=False)
    tipusNeutre2 = zope.schema.Choice(title=_(u'Tipus Neutre2'), values=['Default', 'Recerca','Intranet'], required=False)
    titolcapsaleraMaster = zope.schema.TextLine(title=_(u'Curs del master [2008/2009]'),required=False)
    idestudiMaster = zope.schema.TextLine(title=_(u'id_estudi'),required=False)
    idtitulacioMaster = zope.schema.TextLine(title=_(u'id_titulacio'),required=False)
    masterdoctorado =  zope.schema.Choice(title=_(u'Master o PhD'), values=['Master', 'Doctorat', 'Master i Doctorat'], required=False)
    ambitdoctorat_ca = zope.schema.TextLine(title=_(u'Ambit doctorat - [catala]'),required=False)
    ambitdoctorat_es = zope.schema.TextLine(title=_(u'Ambit doctorat - [castella]'),required=False)
    ambitdoctorat_en = zope.schema.TextLine(title=_(u'Ambit doctorat - [angles]'),required=False)
    
class IgenWebControlPanel(IgenWebControlPanelSchemaGeneral, ISkinsSchema, IgenWebControlPanelSchemaEspecifics, IgenWebControlPanelSchemaInformacio, IgenWebControlPanelSchemaSabors):
    """ Marker interface de la unio del schema especific de genweb i el dels skins estandar
        de plone i segregat en la pestanya principal
    """  

class IFormularioContact(Interface):
    """Define the fields of our form
    """
    
    nombre = zope.schema.TextLine(title=_(u'Nom'),
                                        description=_(u"Inseriu el vostre nom complet"),
                                        required=True)
                              
    destinatario = zope.schema.TextLine(title=_(u'A/e'),
                                        description=_(u"Si us plau escriviu, la vostra adreça de correu  electrònic"),
                                        required=True)
 
    asunto = zope.schema.TextLine(title=_(u'Assumpte'),
                                        description=_(u"Si us plau, entreu l\'assumpte del missatge que voleu enviar"),
                                        required=True)

    mensaje = zope.schema.Text(title=_(u'Missatge'),
                                        description=_(u"Si us plau, escriviu el missatge que voleu enviar"),
                                        required=True)
