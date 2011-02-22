# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.content import DocumentActionsViewlet, DocumentBylineViewlet 
from plone.app.layout.viewlets.common import PathBarViewlet
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from zope.component import getMultiAdapter
from Products.CMFPlone.utils import safe_unicode
from cgi import escape
from upc.genwebupctheme.browser import utils
from Products.CMFCore.utils import getToolByName

from upc.genwebupctheme.browser.master.information import IinfoGeneral, Icompetencies, Irequisits, Ipreinscripcio

class DocumentActions(DocumentActionsViewlet):

    render = ViewPageTemplateFile("document_actions.pt")

class PathBar(PathBarViewlet):
    
    render = ViewPageTemplateFile('path_bar.pt')
    
    def eliminaBRs(self, crumb):
        title = crumb['Title']
        if isinstance(title, str):
            title = title.decode('utf-8')
        return title.replace(u'<br/>','').replace(u'<br>','').replace(u'<br />','').replace(u'&nbsp;','')
    
class GlobalSections(GlobalSectionsViewlet):
    
    render = ViewPageTemplateFile('global_sections.pt')    

class PathBarRoot(PathBarViewlet):
    index = ViewPageTemplateFile('null.pt')
    # GW4 Superseeded afegint directives al overrides.zcml (previament, posat a la nevera)
    # def __init__(self, context, request, view, manager=None):
    #     super(PathBarViewlet, self).__init__(context,request,view, manager)
    # 
    #     if IinfoGeneral.providedBy(self.view):
    #         self.index = ViewPageTemplateFile('bGeneral_inf.pt')
    #     elif Icompetencies.providedBy(self.view):
    #         self.index = ViewPageTemplateFile('bCompetencies.pt')
    #     elif Irequisits.providedBy(self.view):
    #         self.index = ViewPageTemplateFile('bRequisits.pt')
    #     elif Ipreinscripcio.providedBy(self.view):
    #         self.index = ViewPageTemplateFile('bPreinscripcio.pt')
    #     else:
    #         self.index = ViewPageTemplateFile('null.pt')

class DarreraModificacio(ViewletBase):
    
    render = ViewPageTemplateFile('darreramodificacio.pt')

class DocumentByLine(DocumentBylineViewlet):
    
    render = ViewPageTemplateFile('documentbyline.pt')


class TitleViewlet(ViewletBase):

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.page_title = self.context_state.object_title
        self.portal_title = self.portal_state.portal_title

    def index(self):
        portal_title = safe_unicode(self.portal_title())
        page_title = safe_unicode(self.page_title())
        
        lang= getToolByName(self, 'portal_languages').getPreferredLanguage()
        
        if lang == 'ca':
          TITLE_GW= utils.getGWConfig(self.context).titolespai_ca
        elif lang == 'es':
          TITLE_GW= utils.getGWConfig(self.context).titolespai_es
        elif lang == 'en':
          TITLE_GW= utils.getGWConfig(self.context).titolespai_en
        elif lang == 'zh':
          TITLE_GW= utils.getGWConfig(self.context).titolespai_zh
        else:
            TITLE_GW = "Genweb UPC"
                                    
        if page_title == portal_title:
            return u"<title> %s &mdash; %s </title>" % (escape(safe_unicode(TITLE_GW)), escape(safe_unicode('UPC. Universitat Politècnica de Catalunya BarcelonaTech.')))
        else:
            return u"<title> %s &mdash; %s &mdash; %s </title>" % (escape(safe_unicode(page_title)), escape(safe_unicode(TITLE_GW)), escape(safe_unicode('UPC. Universitat Politècnica de Catalunya BarcelonaTech.')))
