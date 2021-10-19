# Configuration Variables

It is imperative that you set environmental variables before deploying this application to a production environment. If unset, these variables will default to unsecure values.

This application is designed to be deployed on Heroku, and some of the config variables reflect this, specifically `DATABASE_URL` and `LOG_TO_STDOUT`.

```
COMPANY_NAME                    : str   : What is your company name? 
GOAL                            : int   : How many leads are you hoping to get?

SECRET_KEY                      : str   : Random string used to keep client-side sessions secure.
PUBLISHER_KEY                   : str   : Random string used to grant users access to the Content API.
ADMIN_KEY                       : str   : Random string used to grant users access to the Lead API.

DATABASE_URL                    : str   : Where is the SQL database being hosted?
SQLALCHEMY_TRACK_MODIFICATIONS  : bool  : Set this to False ;)

MAIL_SERVER                     : str   : Outgoing SMTP server for your email provider (e.g. "smtp.gmail.com")
MAIL_PORT                       : int   : Outgoing mail port for your email provider (e.g. 587)
MAIL_USE_TLS                    : bool  : Do you want to use TLS? (e.g. True)
MAIL_USERNAME                   : str   : What is the email address? (e.g. "myemail@gmail.com")
MAIL_PASSWORD                   : str   : What is the email password? (e.g. "password123")

LOG_TO_STDOUT                   : bool  : Do you want it logged to stdout or to a specified logger? (Used for Heroku deployment.)
```