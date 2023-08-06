# encoding: utf-8
from flask.ext.mail import Message
from ..extensions import mail 



def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)