import jsonschema
from cliquet import resource, schema
from cliquet.errors import raise_invalid
from jsonschema import exceptions as jsonschema_exceptions
from pyramid.settings import asbool

from kinto.views import object_exists_or_404


class RecordSchema(schema.ResourceSchema):
    class Options:
        preserve_unknown = True


_parent_path = '/buckets/{{bucket_id}}/collections/{{collection_id}}'


@resource.register(name='record',
                   collection_path=_parent_path + '/records',
                   record_path=_parent_path + '/records/{{id}}')
class Record(resource.ProtectedResource):

    mapping = RecordSchema()
    schema_field = 'schema'

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)

        self.bucket_id = self.request.matchdict['bucket_id']
        self.collection_id = self.request.matchdict['collection_id']
        collection_parent_id = '/buckets/%s' % self.bucket_id
        self._collection = object_exists_or_404(self.request,
                                                collection_id='collection',
                                                parent_id=collection_parent_id,
                                                object_id=self.collection_id)

    def get_parent_id(self, request):
        bucket_id = request.matchdict['bucket_id']
        collection_id = request.matchdict['collection_id']
        return '/buckets/%s/collections/%s' % (bucket_id, collection_id)

    def is_known_field(self, field_name):
        """Without schema, any field is considered as known."""
        return True

    def process_record(self, new, old=None):
        """Validate records against collection schema, if any."""
        new = super(Record, self).process_record(new, old)

        schema = self._collection.get('schema')
        settings = self.request.registry.settings
        schema_validation = 'kinto.experimental_collection_schema_validation'
        if not schema or not asbool(settings.get(schema_validation)):
            return new

        collection_timestamp = self._collection[self.collection.modified_field]

        try:
            jsonschema.validate(new, schema)
            new[self.schema_field] = collection_timestamp
        except jsonschema_exceptions.ValidationError as e:
            field = e.path.pop() if e.path else e.validator_value.pop()
            raise_invalid(self.request, name=field, description=e.message)

        return new

    def collection_get(self):
        result = super(Record, self).collection_get()
        self._handle_cache_expires(self.request.response)
        return result

    def get(self):
        result = super(Record, self).get()
        self._handle_cache_expires(self.request.response)
        return result

    def _handle_cache_expires(self, response):
        """If the parent collection defines a ``cache_expires`` attribute,
        then cache-control response headers are sent.

        .. note::

            Those headers are also sent if the
            ``cliquet.record_cache_expires_seconds`` setting is defined.
        """
        cache_expires = self._collection.get('cache_expires')
        if cache_expires is None:
            by_bucket = 'cliquet.%s_record_cache_expires_seconds' % (
                self.bucket_id)
            by_collection = 'cliquet.%s_%s_record_cache_expires_seconds' % (
                self.bucket_id, self.collection_id)
            settings = self.request.registry.settings
            cache_expires = settings.get(by_collection,
                                         settings.get(by_bucket))

        if cache_expires is not None:
            response.cache_expires(seconds=cache_expires)
