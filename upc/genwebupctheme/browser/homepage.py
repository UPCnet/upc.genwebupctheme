from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from upc.genwebupctheme.browser import utils
from upc.genwebupctheme.browser.interfaces import IHomepage
from zope.interface import implements
from Products.CMFCore.utils import getToolByName


class HomePageView(BrowserView):
    implements(IHomepage)

    def manageUrl(self):
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        return '%s/@@manage-homeportlets' % context_state.view_url()

    def canManagePortlets(self):
        mt = getToolByName(self.context, 'portal_membership')
        return mt.checkPermission('Portlets: Manage portlets', self.context)

    def getFrontPage(self):
        """
        Funcio que retorna la pagina principal del espai. Te en compte els permissos de lusuari validat, amb un
        restrictedTraverse sobre lobjecte (tenint en compte lidioma)
        """
        page = {}
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal = portal_state.portal()

        FrontPageObj = portal.benvingut.getTranslation()
        idFrontPageObj = FrontPageObj.id
        traversal = portal.restrictedTraverse(idFrontPageObj)
        page['body'] = FrontPageObj.CookedBody()

        return page

    def getColumn1(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig(self)
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna1

    def getColumn2(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig(self)
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna2

    def getColumn3(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig(self)
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna3

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal = portal_state.portal()
        return getattr(portal, 'benvingut', False)

    def getSetupLink(self):
        """Funcio que dona l'enllas al formulari de creacio dels elements per defecte
        """
        return utils.portal_url(self) + "/setup-view"
