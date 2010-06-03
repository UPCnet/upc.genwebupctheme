# -*- coding: utf-8 -*-
import re
import z3c.form.validator
import upc.genweb.recaptcha

from zope.interface import Interface
from zope import schema
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from upc.genweb.recaptcha.widget import ReCaptchaFieldWidget
from Products.statusmessages.interfaces import IStatusMessage
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform.templates import ZopeTwoFormTemplateFactory
from Products.CMFPlone import PloneMessageFactory as _ 
from Products.CMFPlone.utils import safe_unicode
from cgi import escape
from zope.component import getMultiAdapter


# Define a valiation method for email addresses
class NotAnEmailAddress(schema.ValidationError):
    __doc__ = _(u"Invalid email address")

check_email = re.compile(r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}").match
def validate_email(value):
    if not check_email(value):
        raise NotAnEmailAddress(value)
    return True
    
MESSAGE_TEMPLATE = """\
Enquiry from: %(name)s <%(email_address)s>

%(message)s
"""

class IContactForm(Interface):
    """Define the fields of our form
    """
    
    nombre = schema.TextLine(title=_('label_sender_fullname', default=u"Name"),
                                        description=_("help_sender_fullname", default="Please enter your full name."),
                                        required=True)
                              
    destinatario = schema.TextLine(title=_('label_sender_from_address',default=u"E-Mail"),
                                        description=_("help_sender_from_address", default="Please enter your e-mail address."),
                                        required=True,
                                        constraint=validate_email)
 
    asunto = schema.TextLine(title=_('label_subject', default="Subject"),
                                        description=_("help_subject", default="Please enter the subject of the message you want to send."),
                                        required=True)

    mensaje = schema.Text(title=_('label_message', default="Message"),
                                        description=_("help_message", default="Please enter the message you want to send."),
                                        required=True)

    captcha = schema.TextLine(title=_(u'Type the code'),
                      description=_(u'Type the code from the picture shown below'), required=True)

z3c.form.validator.WidgetValidatorDiscriminators(upc.genweb.recaptcha.validator.ReCaptchaValidator, field=IContactForm['captcha'])

class Contact(object):
    nombre = u""
    destinatario = u""
    asunto = u""
    mensaje = u""
    captcha = u""
    def __init__(self, context):
        self.context = context


class ContactBaseForm(form.Form):
    fields = field.Fields(IContactForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget

    # This trick hides the editable border and tabs in Plone
    def __call__(self):
        self.request.set('disable_border', True)
        return super(ContactForm, self).__call__()


    def get_email_from_name(self):
        return getUtility(ISiteRoot).email_from_name

    destinatario = property(get_email_from_name)

    
    @button.buttonAndHandler(_(u"Send"))
    def action_send(self, action):
        """Send the email to the configured mail address in properties and redirect to the
        front page, showing a status message to say the message was received.
        """
        data, errors = self.extractData()
        if 'recaptcha_response_field' in self.request.keys():
            # Verify the user input against the captcha
            if self.context.restrictedTraverse('@@recaptcha').verify():
                pass
            else:
                return
        else: 
            return

        if not data.has_key('asunto') or not data.has_key('destinatario') or not data.has_key('mensaje') or not data.has_key('nombre'):
            return

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
        
        self.request.response.redirect('contact_feedback')
 
        return ''


ContactForm = wrap_form(ContactBaseForm, index=ViewPageTemplateFile('contact-info.pt'))
