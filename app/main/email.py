from flask import render_template, current_app
from app.email import send_email
from app.models import Lead

def send_alert_email(lead):
    send_email(
        'New lead!', 
        sender=Config.MAIL_USERNAME, 
        recipients=[Config.MAIL_USERNAME], 
        text_body=render_template('email/alert.txt', lead=lead, leads=len(Lead.query.all()), goal=Config.GOAL)
    )