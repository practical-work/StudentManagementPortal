from flask_mail import Message
from flask import render_template
from app.extensions import mail


class EmailService:

    @staticmethod
    def send_email(to, subject, template, **kwargs):

        msg = Message(
            subject=subject,
            recipients=[to]
        )

        msg.html = render_template(template, **kwargs)

        mail.send(msg)