import os, email, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

path = os.path.dirname(__file__)
TEMPLATE_DIR = '/templates/'


class EmailTemplate(object):

    def __init__(self, template_name='', values={}):
        self.template_name = template_name
        self.values        = values


    def render(self):
        content = open(path + TEMPLATE_DIR + self.template_name).read()

        for k,v in self.values.items():
            content = content.replace('[%s]' % k,v)

        return content


class MailMessage(object):

    def __init__(self, from_email='', to_emails=[], cc_emails=[], subject='', body='', template=None, attachments=[]):
        self.from_email       = from_email
        self.to_emails        = to_emails
        self.cc_emails        = cc_emails
        self.subject          = subject
        self.template         = template
        self.body             = body
        self.file_attachments = attachments


    def attach_file(self, path):
        self.file_attachments.append(path)


    def get_message(self):
        if isinstance(self.to_emails, str):
            self.to_emails = [self.to_emails]

        if isinstance(self.cc_emails, str):
            self.cc_emails = [self.cc_emails]

        if len(self.to_emails) == 0 or self.from_email == '':
            raise ValueError('Invalid From or To email address(es)')

        msg = MIMEMultipart('alternative')

        msg['To']      = ', '.join(self.to_emails)
        msg['Cc']      = ', '.join(self.cc_emails)
        msg['From']    = self.from_email
        msg['Subject'] = self.subject

        if self.template:
            msg.attach(MIMEText(self.body, 'plain'))
            msg.attach(MIMEText(self.template.render(),'html'))
        else:
            msg.attach(MIMEText(self.body, 'plain'))

        for attachment in self.file_attachments:
            with open(attachment, "rb") as f:
                filename = os.path.basename(attachment)
                part = MIMEApplication(f.read(), Name=filename)
                part['Content-Disposition'] = 'attachment; filename="' + str(filename) + '"'
                msg.attach(part)

        return msg


class MailServer(object):

    def __init__(self, username, password, server_name='smtp.gmail.com'):
        self.username    = username
        self.password    = password
        self.server_name = server_name


def send_email(mail_msg, mail_server=MailServer()):
    server = smtplib.SMTP_SSL(mail_server.server_name)
    # server.set_debuglevel(1)
    server.login(mail_server.username, mail_server.password)
    server.sendmail(mail_msg.from_email, (mail_msg.to_emails + mail_msg.cc_emails), mail_msg.get_message().as_string())
    server.close()
