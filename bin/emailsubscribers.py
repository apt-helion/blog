#!/usr/bin/env python
import sys

from os.path import isfile, join
from pathlib import Path

project_path = Path(__file__).parent
website_path = project_path.parent / 'website/'
sys.path.append(str(website_path))

import datetime

from emails.mail import *
from common.models.email import *
from common.models.main import *
from config import Config


def send_emails(link):
    article = Article.get_article(link)

    now = datetime.now()

    for subscriber in Emails.select():

        # Create template
        params = {
            'article_link'     : f'https://blog.justinduch.com/article/{link}',
            'article_title'    : article.title,
            'unsubscribe_link' : f'https://blog.justinduch.com/emails/unsubscribe/{subscriber.unsubscribe}'
        }

        template = EmailTemplate(template_name='new_post_template.html', values=params)

        # Specify server
        server = MailServer(
            server_name = 'smtp.gmail.com',
            username = Config.EMAIL['username'],
            password = Config.EMAIL['password']
        )

        # Create message
        msg = MailMessage(
            from_email = 'noreply@noreply.justinduch.com',
            to_emails = [subscriber.email],
            subject = f'New Article: {article.title}',
            template = template
        )

        try:
            send_email(mail_msg=msg, mail_server=server)
        except Exception as e:
            EmailLogs.create(
                error = e,
                email = email,
                process = 'notification',
                date = now
            ).save()
