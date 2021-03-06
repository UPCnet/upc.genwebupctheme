from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from urllib import quote_plus

from upc.genwebupctheme.browser.utils import havePermissionAtRoot


class capsaleraSuperior(ViewletBase):
    render = ViewPageTemplateFile('capsaleraSuperior.pt')

    def update(self):

        super(capsaleraSuperior, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        self.site_actions = context_state.actions('site_actions')

        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = ""

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())


class titolsMaster(ViewletBase):
    render = ViewPageTemplateFile('master/titolsMaster.pt')


class titolsNeutre2(ViewletBase):
    render = ViewPageTemplateFile('neutre2/titolsNeutre2.pt')


class titols(ViewletBase):
    render = ViewPageTemplateFile('titols.pt')


class logoNeutre3(ViewletBase):
    render = ViewPageTemplateFile('neutre3/logoNeutre3.pt')


class barraSuperior (ViewletBase):
    render = ViewPageTemplateFile('neutre3/barraSuperior.pt')


class logoNeutre2(ViewletBase):
    render = ViewPageTemplateFile('neutre2/logoNeutre2.pt')


class logoMaster(ViewletBase):
    render = ViewPageTemplateFile('master/logoMaster.pt')


class barraColor (ViewletBase):
    render = ViewPageTemplateFile('barra.pt')


class eines(ViewletBase):
    render = ViewPageTemplateFile('eines.pt')

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
        page = self.request.get('URL', '').split('/')[-3]
        return page not in ('login_form', 'join_form')

    @property
    def available(self):
        return self.auth() is not None and self.show()

    def login_form(self):
        url = self.portal_state.portal_url()
        url_split = url.split(":")
        if len(url_split) > 0:
            if url_split[0] == 'http':
                url = url.replace('http', 'https')
        return '%s/login_form' % url

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

    def came_from(self):
        current_page = self.context_state.current_page_url()
        current_page_split = current_page.split(":")
        if len(current_page_split) > 0:
            if current_page_split[0] == 'http':
                current_page = current_page.replace('http', 'https')
        return current_page

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

# Lo del personal_bar
    def update(self):
        super(eines, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')

        sm = getSecurityManager()

        self.user_actions = context_state.actions('user')

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

            member_info = tools.membership().getMemberInfo()

            fullname = member_info.get('fullname', '')
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid

    def canSeeToolLink(self):
        """Torna la funcio dels utils"""
        return havePermissionAtRoot(self)
