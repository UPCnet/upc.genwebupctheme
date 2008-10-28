from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter, getUtility
from upc.genwebupctheme.browser.utils import utilitats
from upc.genwebupctheme.browser import utils


class HomePageView(BrowserView):
    __call__=ViewPageTemplateFile('homepage.pt')

    def getFrontPage(self):
        page = {}
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')

        frontpageobj=portal_state.portal()['front-page']
        page['title']=frontpageobj.Title()
        page['body']=frontpageobj.CookedBody()

        return page

    def getColumn1(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig()
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna1
        
    def getColumn2(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig()
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna2
                
    def getColumn3(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = utils.getGWConfig()
        #gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna3
