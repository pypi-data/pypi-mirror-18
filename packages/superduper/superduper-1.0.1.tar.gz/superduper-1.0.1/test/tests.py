"""
    A test for my superduper function
"""
import unittest
from super_duper import superduper


class Foo(object):
    a = 5

    def get_a(self):
        return self.a


class Bar(Foo):
    def get_a(self):
        return 'you failed!'


class Dummy(Bar):
    def get_a(self):
        return superduper(Dummy, self).get_a()


class TestSuperDuper(unittest.TestCase):

    def test_super_duper(self):
        obj = Dummy()
        self.assertEqual(obj.get_a(), 5)

if __name__ == '__main__':
    unittest.main()