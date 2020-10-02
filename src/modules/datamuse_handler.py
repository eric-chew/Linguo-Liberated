import requests
import json
from modules.query import Query


class DatamuseHandler:
    max_returned = 5
    api_timeout = 3
    definitions_on = True

    @classmethod
    def prefix(cls) -> str:
        return 'https://api.datamuse.com/words?'

    @classmethod
    def wildcards_percent_encoding(cls) -> dict:
        return {
            '*': '%2A',
            '?': '%3F',
            '#': '%23',
            '@': '%40',
            ' ': '%20'
        }

    @classmethod
    def query_string_generator(cls, query: Query) -> str:
        to_append = ''
        if query.means_like:
            query_ml = query.means_like
            for key, value in cls.wildcards_percent_encoding().items():
                query_ml = query_ml.replace(key, value)
            to_append += f'&ml={query_ml}'
        if query.sounds_like:
            query_sl = query.sounds_like
            for key, value in cls.wildcards_percent_encoding().items():
                query_sl = query_sl.replace(key, value)
            to_append += f'&sl={query_sl}'
        if query.spelled_like:
            query_sp = query.spelled_like
            for key, value in cls.wildcards_percent_encoding().items():
                query_sp = query_sp.replace(key, value)
            to_append += f'&sp={query_sp}'
        if to_append:
            to_append = f'{to_append}&max={cls.max_returned}'
            to_append = to_append[1:]
            if cls.definitions_on:
                to_append = f'{to_append}&md=d'
        to_send = cls.prefix() + to_append
        return to_send

    @classmethod
    def response_from_api(cls, query_string: str) -> list:
        try:
            response = requests.get(query_string, timeout=cls.api_timeout)
            if response.status_code not in range(200, 300):
                print('''There was a problem retrieving your query
Please try again.''')
                return []
            else:
                return json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            print(f'''The API did not respond within {cls.api_timeout} seconds.
Please try again later.''')
            return []

    @classmethod
    def call_datamuse(cls, query: Query) -> list:
        query_url = cls.query_string_generator(query)
        content = cls.response_from_api(query_url)
        if not content:
            print('Nothing was returned from the API')
        return content

    @classmethod
    def definition_parser(cls, definition: str) -> str:
        new_definition = definition.split('\t')[1]
        return new_definition

    @classmethod
    def print_formatted_response(cls, response: list) -> None:
        for word in response:
            print(f'\nWord: {word["word"]}')
            if cls.definitions_on:
                try:
                    for definition in word['defs']:
                        print(
                            '  - Definition: ',
                            f'{cls.definition_parser(definition)}'
                        )
                except KeyError:
                    pass
