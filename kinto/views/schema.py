from cliquet import errors
from cornice import Service
import jsonschema
from jsonschema import exceptions as jsonschema_exceptions
from pyramid import httpexceptions
from pyramid.security import NO_PERMISSION_REQUIRED


schema = Service(name='schema',
                 description='Collection schema',
                 path=('/buckets/{bucket_id}'
                       '/collections/{collection_id}/schema'),
                 error_handler=errors.json_error_handler)


def _schema_key(request):
    bucket_id = request.matchdict['bucket_id']
    collection_id = request.matchdict['collection_id']
    schema_key = 'schema:%s:%s' % (bucket_id, collection_id)
    return schema_key


def get_collection_schema(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue
    schema = keyvalue.get(_schema_key(request))
    return schema


@schema.get(permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_get(request):
    schema = request.get_collection_schema()
    if schema is None:
        raise httpexceptions.HTTPNotFound()

    return schema


def validate_jsonschema(request):
    try:
        schema = request.json_body
        assert schema, 'Schema is empty'
        jsonschema.Draft4Validator.check_schema(schema)
        request.validated = schema
    except jsonschema_exceptions.SchemaError as e:
        request.errors.add('body', e.path.pop(), e.message)
    except (ValueError, AssertionError) as e:
        request.errors.add('body', '', e.message)


@schema.put(validators=(validate_jsonschema,),
            permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_put(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue
    schema = request.validated
    keyvalue.set(_schema_key(request), schema)
    return schema


@schema.delete(permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_delete(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue
    keyvalue.delete(_schema_key(request))
    return {}
