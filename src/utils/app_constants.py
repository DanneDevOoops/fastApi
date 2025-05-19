"""
Module: app_constants

This module defines constants used for configuring Cross-Origin Resource
Sharing (CORS) and HTTP request handling in the application.

Constants:
----------

1. REQUEST_HEADERS:
    - Description: A list of HTTP headers allowed for CORS requests.
    - Values:
        - "Accept": Specifies the media types acceptable for the response.
        - "Accept-Language": Indicates the preferred language for the
            response.
        - "Content-Type": Specifies the media type of the request body.
        - "Authorization": Used for passing authentication credentials.
        - "X-Requested-With": Commonly used for identifying AJAX requests.
        - "X-API-Key": Custom header for API key authentication.

2. REQUEST_METHODS:
    - Description: A list of HTTP methods allowed for CORS requests.
    - Values:
        - "GET": Retrieve data from the server.
        - "POST": Submit data to the server.
        - "PUT": Update existing data on the server.
        - "PATCH": Partially update data on the server.
        - "DELETE": Remove data from the server.
        - "OPTIONS": Used for preflight requests in CORS.

3. REQUEST_ORIGINS:
    - Description: A list of origins allowed to access the application.
    - Values:
        - "*": Allows requests from any origin.
"""

REQUEST_HEADERS = [
    "Accept",
    "Accept-Language",
    "Authorization",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Origin",
    "Access-Control-Expose-Headers",
    "Access-Control-Max-Age",
    "Cache-Control",
    "Content-Type",
    # "ETag",
    # "If-Modified-Since",
    "X-Requested-With",
    "X-API-Key"
]

REQUEST_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

REQUEST_ORIGINS = ["*"]
