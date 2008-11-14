from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.content import DocumentActionsViewlet, DocumentBylineViewlet 
from plone.app.layout.viewlets.common import PathBarViewlet
from zope.component import getMultiAdapter
from Products.CMFPlone.utils import safe_unicode
from cgi import escape
from upc.genwebupctheme.browser import utils
from Products.CMFCore.utils import getToolByName

class DocumentActions(DocumentActionsViewlet):

    render = ViewPageTemplateFile("document_actions.pt")

class PathBar(PathBarViewlet):
    
    render = ViewPageTemplateFile('path_bar.pt')


class PathBarRoot(PathBarViewlet):
    
    render = ViewPageTemplateFile('null.pt')

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
            TITLE_GW= utils.getGWConfig().titolespai_ca
        if lang == 'es':
            TITLE_GW= utils.getGWConfig().titolespai_es
        if lang == 'en':
            TITLE_GW= utils.getGWConfig().titolespai_en
                                    
        if page_title == portal_title:
            return u"<title> %s &mdash; %s </title>" % (escape(safe_unicode(TITLE_GW)), escape(safe_unicode('Universitat Politècnica de Catalunya')))
        else:
            return u"<title> %s &mdash; %s &mdash; %s </title>" % (escape(safe_unicode(TITLE_GW)), escape(safe_unicode('Universitat Politècnica de Catalunya')), escape(safe_unicode(page_title)))


# Sample code for a basic viewlet (In order to use it, you'll have to):
# - Un-comment the following useable piece of code (viewlet python class).
# - Rename the vielwet template file ('browser/viewlet.pt') and edit the
#   following python code accordingly.
# - Edit the class and template to make them suit your needs.
# - Make sure your viewlet is correctly registered in 'browser/configure.zcml'.
# - If you need it to appear in a specific order inside its viewlet manager,
#   edit 'profiles/default/viewlets.xml' accordingly.
# - Restart Zope.
# - If you edited any file in 'profiles/default/', reinstall your package.
# - Once you're happy with your viewlet implementation, remove any related
#   (unwanted) inline documentation  ;-p

#class MyViewlet(ViewletBase):
#    render = ViewPageTemplateFile('viewlet.pt')
#
#    def update(self):
#        self.computed_value = 'any output'
