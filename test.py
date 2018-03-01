import unittest
import trelloreq

class TestRequest(unittest.TestCase):
    def test_base_get(self):
        r = trelloreq.trello_get("members/me/boards/")
        self.assertTrue(r.ok)

    def test_get_boards(self):
        r = trelloreq.trello_get("members/me/boards/")
        boards = r.json()
        self.assertIsNotNone(boards)

