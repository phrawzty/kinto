from .support import BaseWebTest, unittest


SCHEMA_URL = '/buckets/blog/collections/articles/schema'
RECORDS_URL = '/buckets/blog/collections/articles/records'


SCHEMA = {
    "title": "Blog post schema",
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["title"]
}

VALID_RECORD = {'title': 'About us', 'body': '<h1>About</h1>'}


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
    def test_empty_body_is_invalid(self):
        resp = self.app.put_json(SCHEMA_URL,
                                 headers=self.headers,
                                 status=400)
        self.assertEqual(resp.json['message'],
                         'No JSON object could be decoded')

    def test_empty_schema_is_invalid(self):
        resp = self.app.put_json(SCHEMA_URL,
                                 {},
                                 headers=self.headers,
                                 status=400)
        self.assertEqual(resp.json['message'],
                         'Schema is empty')

    def test_schema_should_be_json_schema(self):
        newschema = SCHEMA.copy()
        newschema['type'] = 'Washmachine'
        resp = self.app.put_json(SCHEMA_URL,
                                 newschema,
                                 headers=self.headers,
                                 status=400)
        error_msg = "'Washmachine' is not valid under any of the given schemas"
        self.assertIn(error_msg, resp.json['message'])


class RecordsValidationTest(BaseWebTest, unittest.TestCase):
    def setUp(self):
        super(RecordsValidationTest, self).setUp()
        self.app.put_json(SCHEMA_URL,
                          SCHEMA,
                          headers=self.headers)

    def test_records_are_valid_if_match_schema(self):
        self.app.post_json(RECORDS_URL,
                           VALID_RECORD,
                           headers=self.headers,
                           status=201)

    def test_records_are_invalid_if_do_not_match_schema(self):
        self.app.post_json(RECORDS_URL,
                           {'body': '<h1>About</h1>'},
                           headers=self.headers,
                           status=400)

    def test_records_are_validated_on_patch(self):
        resp = self.app.post_json(RECORDS_URL,
                                  VALID_RECORD,
                                  headers=self.headers,
                                  status=201)
        record_id = resp.json['id']
        self.app.patch_json('%s/%s' % (RECORDS_URL, record_id),
                            {'title': 3.14},
                            headers=self.headers,
                            status=400)

    def test_records_are_validated_on_put(self):
        resp = self.app.post_json(RECORDS_URL,
                                  VALID_RECORD,
                                  headers=self.headers,
                                  status=201)
        record_id = resp.json['id']
        self.app.put_json('%s/%s' % (RECORDS_URL, record_id),
                          {'body': '<h1>About</h1>'},
                          headers=self.headers,
                          status=400)

    def test_validation_error_response_provides_details(self):
        resp = self.app.post_json(RECORDS_URL,
                                  {'body': '<h1>About</h1>'},
                                  headers=self.headers,
                                  status=400)
        self.assertIn("'title' is a required property", resp.json['message'])
        self.assertEqual(resp.json['details'][0]['name'], 'title')

    def test_records_of_other_bucket_are_not_impacted(self):
        pass
