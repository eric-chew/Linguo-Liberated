import unittest
from modules.file_handler import FileHandler


class TestFileHander(unittest.TestCase):
    def test_verify_path_exists(self):
        b_path_1 = FileHandler.verify_path_exists('notexist.txt')
        self.assertFalse(
            b_path_1,
            msg='Non existant file path returned True')

        b_path_2 = FileHandler.verify_path_exists('tests/test_file_handler.py')
        self.assertTrue(
            b_path_2,
            msg='Existing file returned False'
        )

    def test_read_query(self):
        expected = """means like: special
sounds like: ecksepshunul
spelled like: e*l
"""
        file_contents = FileHandler.read_query('example_input.txt')
        self.assertEqual(
            file_contents,
            expected,
            msg='Contents of read file was not expected'
        )

    def test_validate_query(self):
        content1 = """means like: special
sounds like: ecksepshunul
spelled like: e*l
"""
        query1 = FileHandler.validate_query(content1)
        self.assertIn(
            'means like',
            query1,
            msg='Condition not properly added in query validation'
        )
        self.assertIn(
            'sounds like',
            query1,
            msg='Condition not properly added in query validation'
        )
        self.assertIn(
            'spelled like',
            query1,
            msg='Condition not properly added in query validation'
        )

        content2 = 'random string'
        query2 = FileHandler.validate_query(content2)
        self.assertFalse(
            query2,
            msg='Improper content did not return empty dict')
