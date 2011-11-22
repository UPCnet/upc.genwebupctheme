# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


 
class AddthisViewlet(ViewletBase):

    render = ViewPageTemplateFile('addthis.pt')

    def isEnabledOnContent(self):
        """ retorna True si estem a una Noticia
        """
        context = self.context
        if context.portal_type == 'News Item' or context.portal_type == 'Document':
            return True
        return False

    def retIdiomaActual(self):
        """ retorna l'idioma actual (p.ex. 'ca')
        """
        return self.context.portal_languages.getPreferredLanguage()


    def retUrl(self):
        """ retorna la url que s'utilitzarà per mostrar a les xarxes socials
        """
        return self.context.absolute_url()
