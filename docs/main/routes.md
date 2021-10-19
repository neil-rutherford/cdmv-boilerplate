# Main

## Introduction

The purpose of this portion of the application is to provide context about who you are as an organization and an opportunity to sign up. It consists of two pages, an about/manifesto page and an index page.

## /

If we think of this website as a sort of funnel where content draws people in, this page is the focal point where they are being directed to. This is the main page and where users have the opportunity to sign up.

The sign-up form is rendered and validated on the page using Flask-WTForms. On user submit, the information from the `LeadCaptureForm` is used to create a `Lead` object. If all goes well, the Lead will be committed to the database, a success message will be flashed, and an email will be sent to the email address specified in the config variables. If the email or phone number are already in use, however, the Lead will not be committed to the database.

The user will be redirected back to this page once the form is submitted. On success, a success message will be flashed. On failure, a failure message will be flashed.

## /about

The about page is a static page that contains the organization's manifesto. The manifesto should answer the following questions:

- Who is your target market?
- What is your idea? How will it change the current status quo?
- Where do you plan to offer your services?
- Why are you doing this? Why should people care?

## /unsubscribe/{email}

This unsubscribes a user from your email list by setting their `User.can_contact` variable to False. To comply with CAN-SPAM requirements, a link to this endpoint should be included on all email correspondence.