#!/usr/bin/python3.6
import uuid
import datetime

from simplerr.web import web, GET, POST
from emails.mail import *
from config import Config
from common.models.main import *
from common.models.email import *


@web('/emails')
def redirect(request): return web.redirect('/')


@web('/emails/subscribe', '/emails/templates/subscribe.html', POST)
def subscribe(request):
    email = request.form.get('email')
    if not email: return web.redirect('/')
    exists = Emails.get_or_none(Emails.email == email)
    if exists: return { 'success': False, 'error': 'already_exists' }

    verify = EmailVerifications.create_verification(email)

    params = { 'verify_link' : f'https://blog.justinduch.com/emails/verify/{verify.code}' }
    template = EmailTemplate(template_name='verify_email_template.html', values=params)

    server = MailServer(
        server_name = 'smtp.gmail.com',
        username = Config.EMAIL['username'],
        password = Config.EMAIL['password']
    )

    msg = MailMessage(
        from_email = 'noreply@noreply.justinduch.com',
        to_emails = [email],
        subject = 'Verify Your Email',
        template = template
    )

    try:
        send_email(mail_msg=msg, mail_server=server)
    except Exception as e:
        EmailLogs.create(
            error = e,
            email = email,
            process = 'verification',
            date = now
        ).save()

        return { 'success': False, 'error': 'whodunit' }

    return { 'success': True, 'email': email }


@web('/emails/verify/<code>', '/emails/templates/verify.html')
def verify(request, code):
    if not code: return web.redirect('/')

    verify = EmailVerifications.get_or_none(EmailVerifications.id == code)
    if not verify: return { 'success': False, 'error': 'invalid_code' }

    now = datetime.datetime.now()
    expiry_threshold = now - datetime.timedelta(minutes = 30)

    if verify.expiry < expiry_threshold: return { 'success': False, 'error': 'code_expired' }

    new_subscriber = Emails.create(
        email = verify.email,
        unsubscribe = uuid.uuid4().hex,
        created = now
    )

    new_subscriber.save()
    verify.delete_instance()

    return { 'success': True }


@web('/emails/unsubscribe/<code>', '/emails/templates/unsubscribe.html')
def unsubscribe(request, code):
    if not code: return web.redirect('/')

    unsub = Emails.get_or_none(Emails.unsubscribe == code)
    if not unsub: return { 'success': False, 'error': 'invalid_code' }
    unsub.delete_instance()

    return { 'success': True }
