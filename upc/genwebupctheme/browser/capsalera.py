from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common

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

class portletLogin(ViewletBase):

    def __init__(self, context, request, view, manager):
        ViewletBase.__init__(self, context, request, view, manager)
        
        self.membership = getToolByName(self.context, 'portal_membership')
        
        self.context_state = getMultiAdapter((context, request), name=u'plone_context_state')
        self.portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        self.pas_info = getMultiAdapter((context, request), name=u'pas_info')

    def show(self):
        if not self.portal_state.anonymous():
            return False
        if not self.pas_info.hasLoginPasswordExtractor():
            return False
        page = self.request.get('URL', '').split('/')[-1]
        return page not in ('login_form', 'join_form')

    @property
    def available(self):
        return self.auth() is not None and self.show()

    def login_form(self):
        return '%s/login_form' % self.portal_state.portal_url()

    def mail_password_form(self):
        return '%s/mail_password_form' % self.portal_state.portal_url()

    def login_name(self):
        auth = self.auth()
        name = None
        if auth is not None:
            name = getattr(auth, 'name_cookie', None)
        if not name:
            name = '__ac_name'
        return name

    def login_password(self):
        auth = self.auth()
        passwd = None
        if auth is not None:
            passwd = getattr(auth, 'pw_cookie', None)
        if not passwd:
            passwd = '__ac_password'
        return passwd

    def join_action(self):
        userActions = self.context_state.actions()['user']
        joinAction = [a['url'] for a in userActions if a['id'] == 'join']
        if len(joinAction) > 0:
            return joinAction.pop()
        else:
            return None

    def can_register(self):
        if getToolByName(self.context, 'portal_registration', None) is None:
            return False
        return self.membership.checkPermission('Add portal member', self.context)

    def can_request_password(self):
        return self.membership.checkPermission('Mail forgotten password', self.context)

    @memoize
    def auth(self, _marker=[]):
        acl_users = getToolByName(self.context, 'acl_users')
        return getattr(acl_users, 'credentials_cookie_auth', None)

    def update(self):
        pass

    render = ViewPageTemplateFile('portletLogin.pt')
    
