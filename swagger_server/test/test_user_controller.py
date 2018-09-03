# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO
import urllib2
import logging
import sys
from swagger_server import util
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase
from flask_testing import LiveServerTestCase
from swagger_server.models import orm
import requests
from swagger_server import globals
from swagger_server.test import *

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

login_creds={"username":"login","password":"login"}
def getcookie(payload):
    return util.encode_password_token(payload)


class TestUserController(BaseTestCase,LiveServerTestCase):
    """UserController integration test stubs"""


    def setUp(self):

        global db_session
        globals.db_session=orm.init_db('sqlite://')

    def tearuser(self):
        user = {"dao_username": "login", "dao_firstname": "login",
                "dao_lastname": "login", "dao_email": "login",
                "dao_password": util.generate_hash("login"), "id": "7"}
        globals.db_session.delete(user)
        globals.db_session.commit()

    def test_login(self):
        hashed_token=util.generate_hash("login")
        user = {"dao_username": "login", "dao_firstname": "login",
                "dao_lastname": "login", "dao_email": "login",
                "dao_password":hashed_token ,"id":"7"}
        globals.db_session.add(orm.Userinfo(**user))
        globals.db_session.commit()
        logging.info("login")
        logging.info(globals.db_session.query(orm.Userinfo).all())
        response = self.client.open(
            '/v1/login',
            method='POST',
            data=json.dumps(login_creds),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



    def test_create_user(self):
        """Test case for create_user

        Create user
        """
        body = User(id=1, username="user1", first_name="user1", last_name="user1", email="user1", password="user1")
        response = self.client.open(
            '/v1/user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',headers={'Cookie': 'Autorization='+getcookie(login_creds)})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        logging.info("create")
        logging.info("create" + str(globals.db_session.query(orm.Userinfo).all()[0].dao_username))




    def test_delete_user(self):
        """Test case for delete_user

        Delete user
        """
        self.test_create_user()
        response = self.client.open(
            '/v1/user/{username}'.format(username='user1'),
            method='DELETE',headers={'Cookie': 'Autorization='+getcookie(login_creds)})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_by_name(self):
        """Test case for get_user_by_name

        Get user by user name
        """
        self.test_create_user()
        response = self.client.open(
            '/v1/user/{username}'.format(username='user1'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Updated user
        """
        self.test_create_user()
        body = User(id=1, username="user1", first_name="user1", last_name="user1", email="user_update", password="user1")
        response = self.client.open(
            '/v1/user/{username}'.format(username='user1'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',headers={'Cookie': 'Autorization='+getcookie(login_creds)})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))





if __name__ == '__main__':
    import unittest
    unittest.main()

