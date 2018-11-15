#!/usr/bin/env python
import sys
sys.path.append('./website/')

import datetime

from website.emails.mail import *
from website.config import Config
from website.common.models.email import *
from website.common.models.main import *


def send_emails(link):
    article = Article.get_article(link)

    now = datetime.datetime.now()

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
            print(f'Sent {subscriber.email}')
        except Exception as e:
            EmailLogs.create(
                error = e,
                email = email,
                process = 'notification',
                date = now
            ).save()

            print(f'{subscriber.email} Error: {e}')



if __name__ == '__main__':
    send_emails(sys.argv[1])
