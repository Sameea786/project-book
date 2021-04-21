from unittest import TestCase
from server import app
from flask import json

class TestBooks(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['Testing'] = True

    def test_get_books_list(self):
        result = self.client.get("/")
        data = result.get_json()
        print(result) 


if __name__ == "__main__":
    import unittest

    unittest.main()


