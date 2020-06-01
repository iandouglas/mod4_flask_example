import unittest
import json
from application import create_app, db
from application.models.user import User


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_get_all_users(self):
        user = User(name='ian douglas')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        # create a user
        response = self.test_app.get(
            '/api/users',
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 1)
        self.assertEquals(payload['users'][0]['name'], 'ian douglas')

    def test_create_user(self):
        # create a user
        response = self.test_app.post(
            '/api/users',
            json={
                'name': 'ian'
            },
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['name'], "ian")
        self.assertEquals(payload['tasks'], [])

    def test_get_one_user(self):
        response = self.test_app.post(
            '/api/users',
            json={
                'name': 'ian'
            },
            follow_redirects=True
        )
        user = json.loads(response.data)

        # get a user
        response = self.test_app.get(
            '/api/users/{}'.format(user['id']),
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['name'], 'ian')
        self.assertEquals(payload['tasks'], [])



if __name__ == "__main__":
    unittest.main()