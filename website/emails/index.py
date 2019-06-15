#!/usr/bin/python3.6
from simplerr.web import web, POST
from common.models.email import Emails


@web('/emails')
def redirect(request):
    return web.redirect('/')


@web('/emails/subscribe', '/emails/templates/subscribe.html', POST)
def subscribe(request):
    email = request.form.get('email')

    if not email:
        return web.redirect('/')

    Emails.create(email=email).save()

    return { 'success': True, 'email': email }


@web('/emails/unsubscribe/<code>', '/emails/templates/unsubscribe.html')
def unsubscribe(request, code):
    if not code:
        return web.redirect('/')

    unsub = Emails.get_or_none(Emails.unsubscribe == code)

    if unsub is None:
        return { 'success': False, 'error': 'invalid_code' }

    unsub.delete_instance()

    return { 'success': True }
