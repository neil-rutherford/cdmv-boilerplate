import json
from app import create_app, db
from app.models import Content
from config import Config
import unittest
import datetime
import time
import uuid

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ContentRoutesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.app.test_client().get(
            '/content/blog/doesnt-exist'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("404.html", response.get_data(as_text=True))
    
    def test_500(self):
        response = self.app.test_client().get(
            '/_api/load/content'
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("500.html", response.get_data(as_text=True))