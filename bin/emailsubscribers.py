#!/usr/bin/env python
import sys
import datetime
import os

from pathlib import Path

project_path = Path(__file__).parent
website_path = project_path.parent / 'website/'
sys.path.append(str(website_path))

from emails.mail import MailServer, MailMessage, EmailTemplate, send_email
from common.models.email import Emails, EmailLogs
from common.models.main import Article


def send_emails(link):
    article = Article.get_article(link)

    now = datetime.now()

    for subscriber in Emails.select():

        # Create template
        params = {
            'article_link': f'https://blog.justinduch.com/article/{link}',
            'article_title': article.title,
            'unsubscribe_link': f'https://blog.justinduch.com/emails/unsubscribe/{subscriber.unsubscribe}'
        }

        template = EmailTemplate(template_name='new_post_template.html', values=params)

        # Specify server
        server = MailServer(
            server_name='smtp.gmail.com',
            username=os.environ.get('EMAIL_USER'),
            password=os.environ.get('EMAIL_PASS')
        )

        # Create message
        msg = MailMessage(
            from_email='noreply@noreply.justinduch.com',
            to_emails=[subscriber.email],
            subject=f'New Article: {article.title}',
            template=template
        )

        try:
            send_email(mail_msg=msg, mail_server=server)
        except Exception as e:
            EmailLogs.create(
                error=e,
                email=subscriber.email,
                process='notification',
                date=now
            ).save()
