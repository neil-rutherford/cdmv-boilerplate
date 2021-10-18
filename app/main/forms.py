from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LeadCaptureForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=35)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=35)
    ])
    email = StringField('Email Address', validators=[
        DataRequired(),
        Length(max=254),
        Email()
    ])
    category = SelectField('Which best describes you?', choices=[
        ('BUYER', 'I want to buy.'),
        ('SELLER', 'I want to sell.'),
        ('NOT SURE', "I'm not sure yet.")
    ], validators=[
        DataRequired()
    ])
    submit = SubmitField('Submit')