from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import implements, alsoProvides
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from zope.deprecation.deprecation import deprecate
from plone.app.layout.globals.interfaces import IViewView 
from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from Products.CMFCore.utils import getToolByName
from cgi import escape
from urllib import quote_plus

class capsaleraSuperior(ViewletBase):
    render = ViewPageTemplateFile('capsaleraSuperior.pt')

    def update(self):
        
        super(capsaleraSuperior, self).update()  # nuevo de Plone 3.1.1
        
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        portal_url = context_state.current_base_url() # para q funcionen las urls /?

        self.site_actions = context_state.actions().get('site_actions', None)
        
        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = ""

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())

        
class logosSuperior(ViewletBase):
    render = ViewPageTemplateFile('logosSuperior.pt')        
        
class logoNeutre(ViewletBase):
    render = ViewPageTemplateFile('logoNeutre.pt')

class eines(ViewletBase):
    render = ViewPageTemplateFile('eines.pt')
    
    def update(self):
        super(eines, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        
        sm = getSecurityManager()

        self.user_actions = context_state.actions().get('user', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:
        
            member = self.portal_state.member()
            userid = member.getId()
            
            if sm.checkPermission('Portlets: Manage own portlets', self.context):
                self.homelink_url = self.site_url + '/dashboard'
            else:
                self.homelink_url = self.site_url + '/author/' + quote_plus(userid)
            
            member_info = tools.membership().getMemberInfo(member.getId())
            fullname = member_info.get('fullname', '')
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid
    
