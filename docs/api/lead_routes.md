# Lead API

## Introduction

The Lead API is an easy way to generate a mailing list of leads who have demonstrated interest in the product.

## Read Leads

To generate a list of all leads, a `POST` request must be made to the `/_api/read/leads` endpoint. The request must be form-encoded in the following format:

```
{
    admin_key   : str(100)  : Administrator credentials, stored in config file.
}
```

### Response Codes
- `200 OK`
    - Meaning: Successfully retrieved list of leads
    - Returns: JSON list of objects
- `403 FORBIDDEN`
    - Meaning: Wrong admin_key
    - Returns: "Incorrect admin_key"
- `405 METHOD NOT ALLOWED`
    - Meaning: It needs to be a POST request.
- `500 INTERNAL SERVER ERROR`
    - Meaning: Error in retrieving list of leads
    - Returns: String with a description of the error