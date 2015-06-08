import jsonschema
import six
from cliquet import resource
from jsonschema import exceptions as jsonschema_exceptions


def validate_jsonschema(request):
    """Validate a JSON Schema definition.

    It relies on version 4. See http://json-schema.org.
    """
    try:
        schema = request.json_body
        assert schema, 'Schema is empty'
        jsonschema.Draft4Validator.check_schema(schema)
        request.validated = schema
    except jsonschema_exceptions.SchemaError as e:
        request.errors.add('body', e.path.pop(), e.message)
    except (ValueError, AssertionError) as e:
        request.errors.add('body', '', six.text_type(e))


class NoopGenerator(object):
    def match(self, record_id):
        return True


@resource.register(name='schema',
                   collection_methods=tuple(),  # disabled.
                   validate_schema_for=tuple(),  # disabled.
                   record_methods=('GET', 'PUT', 'DELETE'),
                   record_path=('/buckets/{{bucket_id}}'
                                '/collections/{{collection_id}}/schema'),
                   record_put_arguments={'validators': validate_jsonschema})
class Schema(resource.BaseResource):
    def __init__(self, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)
        self.collection.id_generator = NoopGenerator()

        bucket_id = self.request.matchdict['bucket_id']
        collection_id = self.request.matchdict['collection_id']
        parent_id = '/buckets/%s/collections/%s' % (bucket_id, collection_id)
        self.collection.parent_id = parent_id

        # There is only one record.
        self.record_id = '__entry__'

    def _remove_resource_fields(self, record):
        # Remove resource fields from schema.
        record.pop(self.collection.id_field)
        record.pop(self.collection.modified_field)
        return record

    def get(self):
        result = super(Schema, self).get()
        self._remove_resource_fields(result)
        return result

    def put(self):
        result = super(Schema, self).put()
        self._remove_resource_fields(result)
        return result

    def delete(self):
        result = super(Schema, self).delete()
        self._remove_resource_fields(result)
        return result
