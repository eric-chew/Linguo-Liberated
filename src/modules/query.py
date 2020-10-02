from __future__ import annotations


class Query:
    means_like = ''
    sounds_like = ''
    spelled_like = ''

    def __init__(self, query_conditions: dict) -> None:
        incorrect_condition = False
        for key, value in query_conditions.items():
            if key in self.valid_input_keys():
                setattr(
                    self,
                    self.underscore_attribute(key),
                    self.sanitise_query(value)
                )
            else:
                incorrect_condition = True
                print(f'''"{key}" is not a valid search condition.
This condition will be ignored.
Please correct it and try again.''')
        if incorrect_condition:
            print('A reminder that the supported conditions are:')
            for key in self.valid_input_keys():
                print(f'- {key}')

    @classmethod
    def sanitise_query(cls, query_string: str) -> str:
        sanitised_string = ''
        for char in query_string:
            if char.isalpha() or char in cls.valid_query_chars():
                sanitised_string += char
        return sanitised_string

    @classmethod
    def underscore_attribute(cls, dict_key: str) -> str:
        underscored_key = dict_key.replace(' ', '_')
        return underscored_key

    @classmethod
    def valid_query_chars(cls) -> list:
        return ['*', '?', '#', '@', ' ']

    @classmethod
    def valid_input_keys(cls) -> list:
        return [
            'means like',
            'sounds like',
            'spelled like'
        ]

    @classmethod
    def query_from_cli(cls) -> 'Query':
        query_dict = {}
        query_dict['means like'] = input('What does your word mean?\n')
        query_dict['sounds like'] = input('What does your word sound like?\n')
        query_dict['spelled like'] = input('What is your word spelled like?\n')
        query = Query(query_dict)
        return query
