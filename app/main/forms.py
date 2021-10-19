from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LeadCaptureForm(FlaskForm):
    first_name = StringField('First name', validators=[
        DataRequired(),
        Length(max=35)
    ])
    last_name = StringField('Last name', validators=[
        DataRequired(),
        Length(max=35)
    ])
    email = StringField('Email address', validators=[
        DataRequired(),
        Length(max=254),
        Email()
    ])
    phone_number = StringField('Phone number', validators=[
        DataRequired(),
        Length(max=15)
    ])
    category = SelectField('Which best describes you?', choices=[
        (1, 'I want to buy.'),
        (2, 'I want to sell.'),
        (3, "I'm not sure yet.")
    ], validators=[
        DataRequired()
    ])
    submit = SubmitField('Submit')