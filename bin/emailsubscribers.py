#!/usr/bin/env python
import sys
import datetime

from pathlib import Path

project_path = Path(__file__).parent
website_path = project_path.parent / 'website/'
sys.path.append(str(website_path))

from emails.mail import EmailTemplate, send_mail # noqa
from common.models.email import Emails, EmailLogs  # noqa
from common.models.main import Article  # noqa


def send_emails(link):
    article = Article.get_article(link)

    for subscriber in Emails.select():
        # Create template
        params = {
            'article_link': f'https://blog.justinduch.com/article/{link}',
            'article_title': article.title,
            'unsubscribe_link': f'https://blog.justinduch.com/emails/unsubscribe/{subscriber.unsubscribe}'
        }

        html_template = EmailTemplate(template_name='new_post_template.html', values=params).render()

        try:
            send_mail(
                to_email=subscriber.email,
                subject=f'New Article: {article.title}',
                content=html_template
            )
        except Exception as e:
            EmailLogs.create(
                error=e,
                email=subscriber.email,
                process='notification',
            ).save()
