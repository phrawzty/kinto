.. _schemas:

Schemas
#######

A JSON schema can optionally be associated to a collection.

Once a schema is set, records will be validated during creation or update.
If the validation fails, a ``400 Bad Request`` error response will be
returned.


GET /buckets/<bucket_id>/collections/<collection_id>/schema
===========================================================

**Requires authentication**

Returns the schema of the collection in this bucket.

If no schema was defined, a ``404 Not Found`` error response is returned.

.. code-block:: http

    $ http GET http://localhost:8888/v1/buckets/blog/collections/articles/schema --auth "admin:"
    HTTP/1.1 200 OK
    Access-Control-Expose-Headers: Backoff, Retry-After, Alert, Last-Modified
    Content-Length: 131
    Content-Type: application/json; charset=UTF-8
    Date: Wed, 10 Jun 2015 10:06:28 GMT
    Last-Modified: 1433930788461
    Server: waitress

    {
        "title": "Blog post schema",
        "type": "object",
        "properties": {
            "body": {
                "type": "string"
            },
            "title": {
                "type": "string"
            }
        },
        "required": [
            "title"
        ]
    }


PUT /buckets/<bucket_id>/collections/<collection_id>/schema
===========================================================

**Requires authentication**

Associates a JSON schema to the collection in this bucket.
The schema itself is validated against the `JSON Schema specification version 4
<http://json-schema.org/>`_.

If a schema was already defined, it will be replaced.

.. note::

    Existing records are left intact. If some records do not match the new
    schema, they will be validated only when updated.


.. code-block:: http

    $ echo '{
        "title": "Blog post schema",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["title"]
    }' | http PUT http://localhost:8888/v1/buckets/blog/collections/articles/schema --auth "admin:"
    HTTP/1.1 200 OK
    Access-Control-Expose-Headers: Backoff, Retry-After, Alert
    Content-Length: 131
    Content-Type: application/json; charset=UTF-8
    Date: Wed, 10 Jun 2015 10:05:56 GMT
    Server: waitress

    {
        "title": "Blog post schema",
        "type": "object",
        "properties": {
            "body": {
                "type": "string"
            },
            "title": {
                "type": "string"
            }
        },
        "required": [
            "title"
        ]
    }


Now that a schema has been defined, the posted records must match it:

.. code-block:: http

    $ echo '{
        "body": "Fails if no title"
    }' | http POST http://localhost:8888/v1/buckets/blog/collections/articles/records --auth "admin:"
    HTTP/1.1 400 Bad Request
    Access-Control-Expose-Headers: Backoff, Retry-After, Alert
    Content-Length: 192
    Content-Type: application/json; charset=UTF-8
    Date: Wed, 10 Jun 2015 10:17:01 GMT
    Server: waitress

    {
        "code": 400,
        "details": [
            {
                "description": "u'title' is a required property",
                "location": "body",
                "name": "title"
            }
        ],
        "errno": 107,
        "error": "Invalid parameters",
        "message": "u'title' is a required property"
    }



DELETE /buckets/<bucket_id>/collections/<collection_id>/schema
==============================================================

**Requires authentication**

Removes the schema from the collection in this bucket.

If no schema was defined, a ``404 Not Found`` error response is returned.

.. code-block:: http

    $ http DELETE http://localhost:8888/v1/buckets/blog/collections/articles/schema --auth "admin:"
    HTTP/1.1 200 OK
    Access-Control-Expose-Headers: Backoff, Retry-After, Alert
    Content-Length: 16
    Content-Type: application/json; charset=UTF-8
    Date: Wed, 10 Jun 2015 10:11:21 GMT
    Server: waitress

    {
        "deleted": true
    }
