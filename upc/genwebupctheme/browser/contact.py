# -*- coding: utf-8 -*-
from zope.formlib import form
from upc.genwebupctheme.browser.interfaces import IFormularioContact

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFPlone import PloneMessageFactory as _ 

from Products.CMFPlone.utils import safe_unicode
from cgi import escape


class ContactForm(formbase.PageForm):
    form_fields = form.FormFields(IFormularioContact)
    
    template = ViewPageTemplateFile('contact-info.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        return super(ContactForm, self).__call__()


    def get_email_from_name(self):
        return getUtility(ISiteRoot).email_from_name

    destinatario = property(get_email_from_name)

    
    @form.action(_(u"label_send"))
    def action_send(self, action, data):
        """Send the email to the configured mail address in properties and redirect to the
        front page, showing a status message to say the message was received.
        """
        
        context = aq_inner(self.context)
        
        mailhost = getToolByName(context, 'MailHost')
        urltool = getToolByName(context, 'portal_url')
        proptool = getToolByName(context, 'portal_properties')
        
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        
        to_address = portal.getProperty('email_from_address')
        from_name = portal.getProperty('email_from_name')
        titulo_web = portal.getProperty('title')

        str = "Heu rebut aquest correu perquè en/na"
        str1 = "l'espai"
        source = "%s <%s>" % (escape(safe_unicode(data['nombre'])), escape(safe_unicode(data['destinatario'])))
        subject = "[Formulari Contacte] %s" % (escape(safe_unicode(data['asunto'])))
        message = "%s %s %s ha\nenviat comentaris sobre %s Genweb que administreu a\n%s.\n\nEl missatge es:\n\n%s\n--\n%s" % (escape(safe_unicode(str)), escape(safe_unicode(data['nombre'])), escape(safe_unicode(data['destinatario'])),escape(safe_unicode(str1)), portal.absolute_url(),escape(safe_unicode(data['mensaje'])),from_name)

        mailhost.secureSend(message, to_address, to_address,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=False,
                            From=source)

        confirm = _(u"Mail sent.")
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        
#        self.request.response.redirect(portal.absolute_url())
        self.request.response.redirect('contact_feedback')
 
        return ''
