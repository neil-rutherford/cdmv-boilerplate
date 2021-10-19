# Models

## Lead

A Lead is an individual who is interested in your business's services. In other words, a Lead is a sign-up.

```
id              : int       : Primary key.
first_name      : str(35)   : Lead's first name.
last_name       : str(35)   : Lead's last name.
email           : str(254)  : Lead's email address. (Must be unique.)
phone_number    : str(15)   : Lead's phone number. (Must be unique.)
category        : int       : Arbitrary differentiator, used for audience segmentation (if applicable).
can_contact     : bool      : Can we contact this individual?
timestamp       : datetime  : When was this object made, in UTC?
```

## Content

Content is an object that represents educational content on the site, particularly blog posts. Content objects contain valuable metadata that are used for SEO and rendering.

```
id              : int       : Primary key.
file_name       : str(300)  : File location (app/templates/content/blog/~)
slug            : str(100)  : What is the content's slug? (Must be unique.)
author_name     : str(70)   : Author's first and last name.
author_handle   : str(70)   : Author's Twitter handle.
title           : str(70)   : Article title.
description     : str(155)  : Brief description of the article.
category        : int       : Arbitrary differentiator, used for audience segmentation (e.g. 1-buyers, 2-sellers).
section         : str(50)   : Section differentiator (e.g. "politics", "economy", "startups", "legal", etc.)
tags            : str(100)  : A comma-separated (", ") list of tags that describe the article.
image_url       : str(300)  : URL for the cover image.
published_time  : datetime  : When was the article published, in UTC?
modified_time   : datetime  : When was the article last modified, in UTC?
views           : rel       : Many-to-one relationship with Logs.
```

## Log

Logs provide traffic information about blog traffic. Because the application does not support user logins and authentication, session cookies are used to track unique pageviews.

```
id              : int       : Primary key.
content_id      : int       : Foreign key for Content.id.
cookie_uuid     : str(36)   : UUID stored as a session variable.
timestamp       : datetime  : When was this generated, in UTC?
```