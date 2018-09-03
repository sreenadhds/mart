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

class Testserver(BaseTestCase,LiveServerTestCase):
    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url() + "/v1/ui/")
        self.assertEqual(response.code, 200)