from zope.publisher.browser import BrowserPage
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _

class Logout(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        logout(self.context, self.request)

def logout(context, request):
    mt = getToolByName(context, 'portal_membership')
    mt.logoutUser(REQUEST=request)
    IStatusMessage(request).addStatusMessage(_('heading_signed_out'), type='info')
    portal = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
    return request.RESPONSE.redirect(portal)
