# Content Routes

## Introduction

The Content blueprint is in charge of displaying blog articles. It consists of three endpoints.

## /blog

This endpoint displays a page with links to blog articles. 

This page does not use Python to display blog post information. Rather, it uses vanilla JavaScript and an API endpoint for dynamic lazy loading. Once the user scrolls over the "sentinel" div, an API call is made that requests 10 blog posts in JSON format. The process repeats, with the counter argument incrementing.

Once the blog posts are exhausted, a message will display saying there are no more posts to show.

## /blog/content/{slug}

This endpoint displays a specific article, based on its slug.

First, we query the database for a Content object where the slug attribute is equal to the slug argument. If this is not found, a 404 error is raised.

Second, we check the session for a variable called `cookie_uuid`. If this does not exist, we set this variable equal to a random UUID. We also make the session permanent so that the cookie persists after the browser closes. Since this application does not support user authentication, cookies are used as a way of tracking unique page views.

Third, a `Log` object is created that records the primary key of the Content object, the `cookie_uuid` value from the session, and the current date and time in UTC. The Log object is then committed to the database, and an attempt is made to render the template stored in `/app/templates/content/blog/` + the file name specified in `Content.file_name`. If this fails, it errors out with a 404.

## /_api/load/content

As previously discussed, this endpoint is used to lazily load blog content.

First, all Content objects are sorted by when they were modified in descending order (newest first), then loaded into memory.

This endpoint relies on a `?counter=` argument. If this argument is not specified, it will raise a 500 error with a description complaining that the counter argument is required.

The counter value is converted to an integer. If the counter is greater than or equal to the length of the list of Content objects, it will return an empty JSON array.

Otherwise, it will slice the list of Content objects from `counter` to `counter + 10`. (If `counter=15`, the list will be sliced from 15 to 25.) Each content will be converted into a dictionary and appended to a list. The list is then converted to a JSON array-of-objects, then returned with a 200 status code.

### Response Format

```
[
    {
        "image_url": "https://www.image.com/image.jpg",
        "tags": ["a", "list", "of", "tags"],
        "title": "My Title",
        "description": "A brief description of the article.",
        "author": "John Doe",
        "content_url": "www.example.com/blog/content/example-slug",
        "modified_time": "2021-10-19 13:10:34"
    }
]
```