from .support import BaseWebTest, unittest


SCHEMA_URL = '/buckets/blog/collections/articles/schema'
RECORDS_URL = '/collections/articles/records'


SCHEMA = {
    "title": "Blog post schema",
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["title"]
}


class MissingSchemaTest(BaseWebTest, unittest.TestCase):
    def test_returns_404_if_no_schema_defined(self):
        self.app.get(SCHEMA_URL,
                     headers=self.headers,
                     status=404)

    def test_accepts_any_kind_of_record(self):
        self.app.post_json(RECORDS_URL,
                           {'title': 'Troll'},
                           headers=self.headers,
                           status=201)
        self.app.post_json(RECORDS_URL,
                           {'author': {'age': 32, 'status': 'captain'}},
                           headers=self.headers,
                           status=201)


class MethodsTest(BaseWebTest, unittest.TestCase):
    def setUp(self):
        super(MethodsTest, self).setUp()
        resp = self.app.put_json(SCHEMA_URL,
                                 SCHEMA,
                                 headers=self.headers)
        self.schema = resp.json
        self.assertEqual(self.schema, SCHEMA)

    def test_get_retrieves_current_schema(self):
        resp = self.app.get(SCHEMA_URL, headers=self.headers)
        self.assertEqual(resp.json, self.schema)

    def test_put_replaces_current_schema(self):
        newschema = SCHEMA.copy()
        newschema['properties']['category'] = {"type": "string"}
        resp = self.app.put_json(SCHEMA_URL,
                                 newschema,
                                 headers=self.headers)
        resp = self.app.get(SCHEMA_URL, headers=self.headers)
        self.assertEqual(resp.json, newschema)

    def test_post_is_not_allowed(self):
        self.app.post(SCHEMA_URL, status=405)

    def test_patch_is_not_allowed(self):
        self.app.patch(SCHEMA_URL, status=405)

    def test_delete_removes_schema(self):
        self.app.delete(SCHEMA_URL, headers=self.headers)
        self.app.get(SCHEMA_URL,
                     headers=self.headers,
                     status=404)


class InvalidSchemaTest(BaseWebTest, unittest.TestCase):
    def test_empty_schema_is_invalid(self):
        pass

    def test_schema_should_be_json_schema(self):
        pass


class RecordsValidationTest(BaseWebTest, unittest.TestCase):
    def setUp(self):
        super(MethodsTest, self).setUp()
        self.app.put_json(SCHEMA_URL,
                          SCHEMA,
                          headers=self.headers)

    def test_records_are_invalid_if_do_match_schema(self):
        pass

    def test_validation_error_response_provides_details(self):
        pass
