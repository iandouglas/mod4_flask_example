import unittest
import json
from application import create_app, db
from application.models.user import User
from application.models.task import Task


class TestTasks(unittest.TestCase):
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

    def test_get_all_tasks(self):
        user = User(name='ian douglas')
        task1 = Task(name='make an app', description='make a little restful api app', user_id=1)
        task2 = Task(name='make another app', description='make another little restful api app', user_id=1)
        with self.app.app_context():
            db.session.add(user)
            db.session.add(task1)
            db.session.add(task2)
            db.session.commit()

        # create a user
        response = self.test_app.get(
            '/api/tasks',
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['count'], 2)
        self.assertEquals(payload['tasks'][0]['name'], 'make an app')
        self.assertEquals(payload['tasks'][1]['name'], 'make another app')

    def test_create_task(self):
        response = self.test_app.post(
            '/api/users',
            json={
                'name': 'ian'
            },
            follow_redirects=True
        )
        user = json.loads(response.data)

        response = self.test_app.post(
            '/api/tasks',
            json={
                'name': 'test app',
                'description': 'whatever',
                'user_id': user['id']
            },
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['name'], "test app")
        self.assertEquals(payload['description'], 'whatever')
        self.assertEquals(payload['user_id'], user['id'])

        response = self.test_app.get(
            '/api/users/{}'.format(user['id']),
            follow_redirects=True
        )

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        payload = json.loads(response.data)
        self.assertEquals(payload['name'], 'ian')
        self.assertEquals(payload['tasks'][0]['name'], 'test app')
        self.assertEquals(payload['tasks'][0]['description'], 'whatever')



if __name__ == "__main__":
    unittest.main()