import naivedb
import unittest
from unittest import TestCase

class Dummy(TestCase):
    @classmethod
    def setUpClass(cls):
        naivedb.create_db("test_db","tests")
        cls.db=naivedb.NaiveDB("tests")

    def test_NaiveDB(self):
        self.assertIsInstance(Dummy.db,naivedb.NaiveDB)

    def tearDown(self):
        Dummy.db.tear_down()
if __name__ == "__main__":
    unittest.main()