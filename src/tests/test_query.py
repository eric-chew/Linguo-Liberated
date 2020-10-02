import unittest
from unittest.mock import patch
from modules.query import Query


class TestQuery(unittest.TestCase):

    query_from_cli_test_inputs = [
        'special',
        '',
        'e*!l'
    ]

    def test_init(self):
        query_dict1 = {}
        query1 = Query(query_dict1)
        self.assertEqual(
            query1.means_like,
            '',
            msg='Empty condition was not empty in Query'
        )
        self.assertEqual(
            query1.sounds_like,
            '',
            msg='Empty condition was not empty in Query'
        )
        self.assertEqual(
            query1.spelled_like,
            '',
            msg='Empty condition was not empty in Query'
        )

        query_dict2 = {
            'what': 'what',
            'means like': 'special'
        }
        query2 = Query(query_dict2)
        self.assertEqual(
            query2.means_like,
            'special',
            msg='Condition was not correctly set'
        )
        self.assertEqual(
            hasattr(query2, 'what'),
            False,
            msg='Improper condition was inserted into Query'
        )

        query_dict3 = {
            'means like': 'special',
            'sounds like': 'sp8ia]l'
        }
        query3 = Query(query_dict3)
        self.assertEqual(
            query3.means_like,
            'special',
            msg='Condition was not correctly set'
        )
        self.assertEqual(
            query3.sounds_like,
            'spial',
            msg='Condition with invalid chars was not correctly set'
        )

    def test_sanitise_query(self):
        query_string1 = 'validstring'
        sanitised_query_string1 = Query.sanitise_query(query_string1)
        self.assertEqual(
            sanitised_query_string1,
            'validstring',
            msg='Valid string was incorrectly sanitised'
        )

        query_string2 = 'ex^^^tra++\n+*%ch%20a(!)(\t)(-))(rs'
        sanitised_query_string2 = Query.sanitise_query(query_string2)
        self.assertEqual(
            sanitised_query_string2,
            'extra*chars',
            msg='String extra chars was incorrectly sanitised'
        )

    def test_underscore_attribute(self):
        attribute1 = 'nospaces'
        u_attribute1 = Query.underscore_attribute(attribute1)
        self.assertEqual(
            u_attribute1,
            'nospaces',
            msg='Attribute with no spaces was incorrectly underscored'
        )

        attribute2 = 'has space'
        u_attribute2 = Query.underscore_attribute(attribute2)
        self.assertEqual(
            u_attribute2,
            'has_space',
            msg='Attribute with a space was incorrectly underscored'
        )

    @patch('builtins.input', side_effect=query_from_cli_test_inputs)
    def test_query_from_cli(self, mock_inputs):
        query = Query.query_from_cli()
        self.assertEqual(
            query.means_like,
            'special',
            msg='Normal condition in Query improperly read from CLI'
        )
        self.assertEqual(
            query.sounds_like,
            '',
            msg='Blank condition in Query improperly read from CLI'
        )
        self.assertEqual(
            query.spelled_like,
            'e*l',
            msg='Condition with special chars improperly read from CLI'
        )
