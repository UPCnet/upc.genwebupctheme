# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getUtility, getMultiAdapter


 
class AddthisViewlet(ViewletBase):

    render = ViewPageTemplateFile('addthis.pt')

    def isEnabledOnContent(self):
        """ retorna True si estem a una Noticia
        """
        context = self.context
        request = self.request
        utils = getMultiAdapter((self.context, self.request),name=u'upc.genweb.utils')

        #Si esta instalat el Genweb UPC llavors fem la comprovacio de si es una Intranet o no
        #per no mostrar les icones del "Comparteix" en el cas de que sigui una Intranet.
        if utils.getGWConfig() is not None:
            if utils.getGWConfig().tipusNeutre2!=('Intranet'):
                return True
            else:
                return False
        else:
            return True
    
    def retIdiomaActual(self):
        """ retorna l'idioma actual (p.ex. 'ca')
        """
        return self.context.portal_languages.getPreferredLanguage()


    def retUrl(self):
        """ retorna la url que s'utilitzarà per mostrar a les xarxes socials
        """
        return self.context.absolute_url()
