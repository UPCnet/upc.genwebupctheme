from zope.formlib import form
from upc.genwebupctheme.browser.interfaces import IFormularioContact

from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.formlib import formbase
from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFPlone import PloneMessageFactory as _ 

class ContactForm(formbase.PageForm):
    form_fields = form.FormFields(IFormularioContact)
#    label = _(u"Active zone for reporters")
#    description = _(u"Ask us for some media material.")
    
    template = ViewPageTemplateFile('contact-info.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        return super(ContactForm, self).__call__()
    
    @form.action("Send")
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

        # Construct and send a message
        to_address = proptool.saladepremsa_properties.getProperty('mail_subscriute')
#        source = "%s <%s>" % (data['name'], data['email_address'])
        subject = "[Sala de Premsa] Formulari Subscriu-te"
        message="a"
#        message = "Nom: %s\nCognoms: %s\nMitjà de comunicació: %s\nTelèfon: %s\nAdreça electrònica: %s\nPetició: %s\n" % (data['name'], data['sirname'], data['media'], data['phone'], data['email_address'], data['message'])

        mailhost.secureSend(message, to_address, to_address,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=False,
                            From=to_address)
        
        # Issue a status message
        confirm = _(u"Thank you! Your request has been sent successfully.")
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        
        # Redirect to the portal front page. Return an empty string as the
        # page body - we are redirecting anyway!
        self.request.response.redirect(portal.absolute_url())
        return ''
