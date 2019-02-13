#!/usr/bin/env python3
import os
import unittest
import tempfile
import api
import json


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db_fd, api.dbfile = tempfile.mkstemp()
        api.app.testing = True
        self.app = api.app.test_client()
        with api.app.app_context():
            con = api.get_db()
            cur = con.cursor()
            cur.execute('CREATE TABLE posts (post_id integer primary key asc autoincrement, title string, body string)')
            con.commit()

    @classmethod
    def tearDownClass(self):
        os.close(self.db_fd)
        os.unlink(api.dbfile)

    def test_wrong_url(self):
        result = self.app.get('/hello')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(json.loads(result.data)['error'], 'invalid url')

    def test_add_post(self):
        result = self.app.post('/post', content_type='application/json',
                data=json.dumps({'title': 'testpost1', 'body': 'testbody1'}))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data)['success'], 'true')

    def test_view_posts(self):
        result = self.app.get('/posts')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(b'testpost1' in result.data)

    def test_wrong_post(self):
        result = self.app.post('/post', content_type='application/json',
                data=json.dumps({'title': 'testpost2', 'body': 'testbody2', 'some': 'thing'}))
        self.assertEqual(result.status_code, 400)
        self.assertIn('request body should contain', json.loads(result.data)['message'])


if __name__ == '__main__':
    unittest.main()

