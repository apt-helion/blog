#!/usr/bin/env python

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

path = os.path.dirname(__file__)
TEMPLATE_DIR = '/templates/'


class EmailTemplate(object):

    def __init__(self, template_name='', values={}):
        self.template_name = template_name
        self.values = values

    def render(self):
        content = open(path + TEMPLATE_DIR + self.template_name).read()

        for k, v in self.values.items():
            content = content.replace('[%s]' % k, v)

        return content


def send_mail(to_email, subject, content, process='notification'):
    message = Mail(
        from_email='Justin Duch <noreply@justinduch.com>',
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
    return sg.send(message)


if __name__ == '__main__':
    import sys
    from pathlib import Path

    current_path = Path(__file__).parent
    website_path = str(Path(current_path / '../').resolve())

    sys.path.append(website_path)

    from common.loadenv import LoadEnv
    LoadEnv.load_dot_env()

    res = send_mail('justin@justinduch.com', 'test', EmailTemplate(template_name='new_post_template.html').render())
    print(res.status_code)
    print(res.body)
    print(res.headers)
