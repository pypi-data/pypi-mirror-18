from unittest import TestCase

from os3.components.processes import Processes


class TestEntry(TestCase):
    def test_all(self):
        Processes().filter(username='nekmo')
