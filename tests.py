import os
import key_value_store
import unittest
import tempfile
import json
import urllib.parse


class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, key_value_store.app.config['DATABASE'] = tempfile.mkstemp()
        key_value_store.app.testing = True
        self.app = key_value_store.app.test_client()
        with key_value_store.app.app_context():
            key_value_store.db.create_all()
        self.Entry = key_value_store.Entry
        self.db = key_value_store.db

    def tearDown(self):
        self.db.drop_all()
        os.close(self.db_fd)
        os.unlink(key_value_store.app.config['DATABASE'])


class TestGets(TestCase):
    def _create_entry(self, key, value):
        """Create a DB entry with the supplied key and value"""
        new_entry = self.Entry(key=key, value=value)
        self.db.session.add(new_entry)
        self.db.session.commit()

    def _test_get(self, key, value):
        """
        Create a DB entry with the supplied key and value, then assert
        we can make an API request to get the value from the key.
        """
        self._create_entry(key, value)

        url_key = urllib.parse.quote_plus(key)
        rv = self.app.get('/api/entry/{}'.format(url_key))

        self.assertEqual(rv.status_code, 200)
        self.assertDictEqual(json.loads(rv.data), {
            'key': key,
            'value': value
        })

    def test_404(self):
        """Test getting a key that is not there."""
        rv = self.app.get('/api/entry/some_key')
        self.assertEqual(rv.status_code, 404)

    def test_get_integers(self):
        """Test getting where key and values are integer strings"""
        self._test_get('1', '2')

    def test_get_ascii(self):
        """Test getting where key and values are ascii strings"""
        self._test_get('123!@#', '456$%^')

    def test_get_unicode(self):
        """Test getting where key and values are unicode strings"""
        self._test_get('😀', '😟')


class TestSets(TestCase):
    def _post_request_create_entry(self, key, value):
        """Send post request to create Entry, and return the response"""
        return self.app.post('/api/entry', data=json.dumps({
            'key': key,
            'value': value
        }), headers={'Content-Type': 'application/json'})

    def _test_set(self, key, value):
        """
        Send POST request creating the entry with the key and value. Verify response. Verify 
        entry is in DB.
        """
        rv = self._post_request_create_entry(key, value)

        # verify response
        self.assertEqual(rv.status_code, 201)
        self.assertDictEqual(json.loads(rv.data),
                             {
                                 'key': key,
                                 'value': value
                             })

        # verify the entry is in the DB
        entry = self.Entry.query.filter_by(key=key).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.key, key)
        self.assertEqual(entry.value, value)

    def test_set_integers(self):
        """Test setting key and value integer strings"""
        self._test_set('1', '2')

    def test_set_ascii(self):
        """Test setting key and value ascii strings"""
        self._test_set('123!@#', '456$%^')

    def test_set_unicode(self):
        """Test setting key and value unicode strings"""
        self._test_set('😀', '😟')

    def test_set_duplicate_value(self):
        """Test setting a duplicate value is ok"""
        self._post_request_create_entry('1', '3')
        self._test_set('2', '3')

    def test_set_duplicate_key(self):
        """Test attempting to set a duplicate key results in a validation error"""
        self._post_request_create_entry('1', '3')
        rv = self._post_request_create_entry('1', '2')
        self.assertEqual(rv.status_code, 400)
        # TODO give more informative validation error
        self.assertEqual(json.loads(rv.data).get('validation_errors'),
                         'Could not determine specific validation errors')

if __name__ == '__main__':
    unittest.main()
