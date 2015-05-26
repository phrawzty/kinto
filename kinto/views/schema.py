import colander
from cliquet import errors
from cornice import Service
from pyramid import httpexceptions
from pyramid.security import NO_PERMISSION_REQUIRED


schema = Service(name='schema',
                 description='Collection schema',
                 path="/buckets/{bucket}/collections/{collection}/schema",
                 error_handler=errors.json_error_handler)


@schema.get(permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_get(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue

    bucket_id = request.matchdict['bucket']
    collection_id = request.matchdict['collection']

    schema_key = 'schema:%s:%s' % (bucket_id, collection_id)
    schema = keyvalue.get(schema_key)

    if schema is None:
        raise httpexceptions.HTTPNotFound()

    return schema


class JSONSchema(colander.MappingSchema):
    def schema_type(self, **kw):
        return colander.Mapping(unknown='preserve')


@schema.put(schema=JSONSchema, permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_put(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue

    bucket_id = request.matchdict['bucket']
    collection_id = request.matchdict['collection']

    schema_key = 'schema:%s:%s' % (bucket_id, collection_id)
    schema = request.validated
    keyvalue.set(schema_key, schema)

    return schema


@schema.delete(permission=NO_PERMISSION_REQUIRED)  # XXX perms
def schema_delete(request):
    keyvalue = request.registry.cache  # XXX cache --> keyvalue

    bucket_id = request.matchdict['bucket']
    collection_id = request.matchdict['collection']

    schema_key = 'schema:%s:%s' % (bucket_id, collection_id)
    keyvalue.delete(schema_key)

    return {}
