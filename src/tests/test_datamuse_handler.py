import unittest
from modules.datamuse_handler import DatamuseHandler
from modules.query import Query


class TestDatamuseHandler(unittest.TestCase):
    def test_query_string_generator(self):
        query_dict1 = {
            'means like': '',
            'sounds like': '',
            'spelled like': '',
        }
        query1 = Query(query_dict1)
        query_string1 = DatamuseHandler.query_string_generator(query1)
        self.assertEqual(
            query_string1,
            'https://api.datamuse.com/words?',
            msg='Empty Query incorrectly generated'
        )

        query_dict2 = {
            'means like': 'special',
            'sounds like': 'ecksepshunul',
            'spelled like': '',
        }
        query2 = Query(query_dict2)
        query_string2 = DatamuseHandler.query_string_generator(query2)
        self.assertEqual(
            query_string2,
            'https://api.datamuse.com/words?' +
            'ml=special&sl=ecksepshunul&max=5&md=d',
            msg='Query with 1 empty condition was incorrectly generated'
        )

        query_dict3 = {
            'means like': 'special',
            'sounds like': 'ecksepshunul',
            'spelled like': 'e*l',
        }
        query3 = Query(query_dict3)
        query_string3 = DatamuseHandler.query_string_generator(query3)
        self.assertEqual(
            query_string3,
            'https://api.datamuse.com/words?' +
            'ml=special&sl=ecksepshunul&sp=e%2Al&max=5&md=d',
            msg='Query with wildcards was incorrectly generated'
        )

    def test_response_from_api(self):
        response1 = DatamuseHandler.response_from_api(
            'https://api.datamuse.com/words?'
        )
        self.assertEqual(
            response1,
            [],
            msg='Empty query did not return empty list from API'
        )

        response2 = DatamuseHandler.response_from_api(
            'https://api.datamuse.com/words?' +
            'ml=special&sl=ecksepshunul&max=5&md=d'
        )
        self.assertIn(
            'exceptional',
            response2[0]['word'],
            msg='API response did not include expected word with 2 conditions'
        )

        response3 = DatamuseHandler.response_from_api(
            'https://api.datamuse.com/words?' +
            'ml=special&sl=ecksepshunul&sp=e%2Al&max=5&md=d'
        )
        self.assertIn(
            'exceptional',
            response3[0]['word'],
            msg='API response did not include expected word' +
            'with wildcard condition'
        )

    def test_call_datamuse(self):
        query_dict1 = {
            'means like': '',
            'sounds like': '',
            'spelled like': '',
        }
        query1 = Query(query_dict1)
        call1 = DatamuseHandler.call_datamuse(query1)
        self.assertEqual(
            call1,
            [],
            msg='Empty query did not return empty list from API'
        )

        query_dict2 = {
            'means like': 'special',
            'sounds like': 'ecksepshunul',
            'spelled like': '',
        }
        query2 = Query(query_dict2)
        call2 = DatamuseHandler.call_datamuse(query2)
        self.assertIn(
            'exceptional',
            call2[0]['word'],
            msg='API response did not include expected word with 2 conditions'
        )

        query_dict3 = {
            'means like': 'special',
            'sounds like': 'ecksepshunul',
            'spelled like': 'e*l',
        }
        query3 = Query(query_dict3)
        call3 = DatamuseHandler.call_datamuse(query3)
        self.assertIn(
            'exceptional',
            call3[0]['word'],
            msg='API response did not include expected word' +
            'with wildcard condition'
        )
