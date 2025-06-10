from flask_mail import Message
from flask import current_app
from api import mail

def send_email(subject, recipients, body, html=None):
    msg = Message(subject, recipients=recipients, body=body, html=html)
    mail.send(msg)

def send_account_creation_email(user):
    subject = "Welcome to MyWatchList!"
    body = f"Hello {user.name or user.username},\n\nYour account was created successfully."
    send_email(subject, [user.email], body)

def send_password_change_email(user):
    subject = "Your MyWatchList password was changed"
    body = f"Hello {user.name or user.username},\n\nYour password has been changed."
    send_email(subject, [user.email], body)

def send_email_change_email(user, old_email, new_email):
    subject = "Your MyWatchList email was changed"
    body = f"Hello {user.name or user.username},\n\nYour email was changed from {old_email} to {new_email}."
    send_email(subject, [new_email], body)

def send_account_deletion_email(user, email=None):
    subject = "Your MyWatchList account was deleted"
    recipient = email or user.email
    body = f"Hello {user.name or user.username},\n\nYour account has been deleted from MyWatchList. If this was not intended, please contact support."
    send_email(subject, [recipient], body)

