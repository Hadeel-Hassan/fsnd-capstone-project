from app import create_app
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import setup_db, db, Drink, Donut, Combo
from unittest.mock import patch

'''
Below "mock_decorator" is to mimic a fake JWT token to
bybass the @requires_auth decorator in order to test the
endpoints without having to go through the
authentication process. To test the authentication with
associated roles please use Postman and import the file:
"fsnd-capstone-prod.postman_collection.json" to test the
roles in production or
"fsnd-capstone-dev.postman_collection.json" to test the
roles in development.
'''


def mock_decorator(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = 'fake'
            try:
                payload = 'fake'
            except:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description':
                    'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            # check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


patch('app.requires_auth', mock_decorator).start()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'hade','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test each endpoint.
    """

    def test_01_add_drink(self):
        '''
        Successfuly adding a drink with the
        following attributes:
        "title": "coffee"
        '''
        res = self.client().post('/drink',
                                 json={'drink_title': 'coffee'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_02_422_add_drink(self):
        '''
        Attempting to add a drink without the title attribute
        which should return a 422 error since
        the column "title" is not nullable.
        '''
        res = self.client().post('/drink',
                                 json={})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_03_add_donut(self):
        '''
        Successfuly adding a donut with the
        following attributes:
        "title": "sugar"
        '''
        res = self.client().post('/donut',
                                 json={'donut_title': 'sugar'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_04_add_another_donut(self):
        '''
        Successfuly adding another donut with the
        following attributes:
        "title": "chocolate", this was for the next patch request
        '''
        res = self.client().post('/donut',
                                 json={'donut_title': 'chocolate'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_05_add_combo(self):
        '''
        Successfuly adding a combo with the
        following attributes:
        "drink_id": 1,
        "donut_id": 1
        '''
        res = self.client().post('/combo',
                                 json={'drink_id': 1, 'donut_id': 1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_06_patch_combo(self):
        '''
        Successfuly updating the "donut_id" of the
        combo with "id": 1 from
        1 to 2
        '''
        res = self.client().patch('/combo/1',
                                  json={'donut_id': 2})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        

    def test_07_422_patch_combo(self):
        '''
        Attempting to update the "donut_id" of the
        combo with "id": 1 from
        1 to None in which it should return a
        422 error since "donut_id" is not nullable
        '''
        res = self.client().patch('/combo/1',
                                  json={'donut_id': None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)


    def test_08_delete_combo(self):
        '''
        Successfuly deleting a combo with ID: 1
        '''
        res = self.client().delete('/combo/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_09_404_delete_combo(self):
        '''
        Attempting to delete a combo ID: 5 
        in which it should return a 404 error 
        since the combo does
        not exist in the database
        '''
        res = self.client().delete('/combo/5')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
