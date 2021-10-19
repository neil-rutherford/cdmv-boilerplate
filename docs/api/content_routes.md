# Content API

## Introduction

Uploading content to the website is a two-part process. 

The HTML file (and accompanying static files) must first be Git pushed to the source code. The blog files live in the `app/templates/content/blog` folder, while the static files live in the `app/static` folder. An API call must then be made to the website to create a Content object. 

A Git push without an API call means that the file is undiscoverable. An API call without a Git push will result in a broken link.

## Creating Content

To create a Content object, a `POST` request must be made to the `/_api/create/resource` endpoint. The request must be form encoded in the following format:

```
{
    publisher_key   : str(100)  : Publisher credentials, stored in config file.
    file_name       : str(300)  : The location of the file ("app/templates/content/blog/~")
    slug            : str(100)  : Unique slug for the content.
    author_name     : str(70)   : Who wrote the content?
    author_handle   : str(70)   : What is the author's Twitter handle?
    title           : str(70)   : Title of the content
    description     : str(155)  : Description of the content
    category        : int       : What audience segment is this content for (e.g. buyers? sellers? undecideds?)
    section         : str(50)   : What section is this content? (e.g. "marketing", "sales", "politics", etc.)
    tags            : str(100)  : Comma-separated (", ") list of tags used to group content 
    image_url       : str(300)  : URL for the cover image
}
```

### Response Codes
- `201 CREATED`
    - Meaning: The Content object was successfully created
    - Returns: JSON object
- `403 FORBIDDEN`
    - Meaning: Wrong publisher_key.
    - Returns: "Incorrect publisher_key."
- `405 METHOD NOT ALLOWED`
    - Meaning: It needs to be a POST request.
- `500 INTERNAL SERVER ERROR`
    - Meaning: Error in creating the object. (Check the variable lengths?)
    - Returns: String describing the error.

## Viewing Content

To view an existing Content object, a `GET` request must be made to the `/_api/read/content/<slug>` endpoint, where `<slug>` is the Content object's slug.

### Response Codes
- `200 OK`
    - Meaning: Content object found and returned
    - Returns: JSON object
- `404 NOT FOUND`
    - Meaning: Cannot find the Content object (is the slug correct?)
- `405 METHOD NOT ALLOWED`
    - Meaning: It needs to be a GET request.

## Updating Content

To edit an existing Content object, a `POST` request must be made to the `/_api/update/content/<slug>` endpoint, where `<slug>` is the Content object's slug. Regardless of the attribute you intend to edit, all fields must be filled out. The request must be form-encoded in the following format:

```
{
    publisher_key   : str(100)  : Publisher credentials, stored in config file.
    file_name       : str(300)  : The location of the file ("app/templates/content/blog/~")
    author_name     : str(70)   : Who wrote the content?
    author_handle   : str(70)   : What is the author's Twitter handle?
    title           : str(70)   : Title of the content
    description     : str(155)  : Description of the content
    category        : int       : What audience segment is this content for (e.g. buyers? sellers? undecideds?)
    section         : str(50)   : What section is this content? (e.g. "marketing", "sales", "politics", etc.)
    tags            : str(100)  : Comma-separated (", ") list of tags used to group content 
    image_url       : str(300)  : URL for the cover image
}
```

### Response Codes
- `200 OK`
    - Meaning: The object has been successfully edited.
    - Returns: JSON object
- `403 FORBIDDEN`
    - Meaning: Wrong publisher_key.
    - Returns: "Incorrect publisher_key."
- `405 METHOD NOT ALLOWED`
    - Meaning: It needs to be a POST request.
- `500 INTERNAL SERVER ERROR`
    - Meaning: Some error occurred while updating the object. (Check the variable lengths?)
    - Returns: String describing the error.

## Deleting Content

To delete an existing Content object, a `POST` request must be made to the `/_api/delete/content/<slug>` endpoint, where `<slug>` is the Content object's slug. The request must be form-encoded in the following format:

```
{
    publisher_key   : str(100)  : Publisher credentials, stored in config file.
}
```

### Response Codes
- `204 NO CONTENT`
    - Meaning: The object has been successfully deleted.
    - Response: "Content with slug {slug} successfully deleted."
- `403 FORBIDDEN`
    - Meaning: Wrong publisher_key.
    - Response: "Incorrect publisher_key."
- `405 METHOD NOT ALLOWED`
    - Meaning: It needs to be a POST request.
- `500 INTERNAL SERVER ERROR`
    - Meaning: Some error occurred while deleting the object.
    - Returns: String describing the error.