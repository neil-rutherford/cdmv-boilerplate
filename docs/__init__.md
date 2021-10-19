# The Application

## Application Factory

This application uses an application factory pattern. It first creates a Flask object, then initializes the following imports as plugins:

- Flask-SQLAlchemy for SQL database operations;
- Flask-Migrate for database migrations;
- Flask-Mail for email functionality;
- Flask-Moment for datetime localization.

Blueprints are used to better organize content. The application then registers three blueprints:

- the API Blueprint, which is concerned with REST API routes for CRUD'ing Content objects, generating email lists, and accessing logs;
- the Content Blueprint, which is concerned with loading and displaying blog content;
- the Main Blueprint, which is concerned with miscellaneous client-facing pages (in this case, "/" and "/about").