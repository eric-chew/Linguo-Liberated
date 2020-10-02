from modules.query import Query
from modules.datamuse_handler import DatamuseHandler
from modules.file_handler import FileHandler


valid_user_inputs = ('1', '2', '8', '9')

help_message = """
Welcome to Linguo Liberated, your brain extension for the words at the tip of
your tongue.
Linguo Liberated uses the Datamuse API to retrieve words and their definitions
based on your descriptions of them.
Datamuse API: https://www.datamuse.com/api/

Currently, three search conditions are supported:
1. 'means like': search based on semantics
2. 'sounds like': search based on phonetics
3. 'spelled like': search based on orthography

When filling in these conditions, it is okay to leave one blank if you want.

You can also use the following wildcards to enhance your search:
* : Matches any number of characters
? : Matches exactly one character
# : Matches exactly one consonant
@ : Matches exactly one vowel

Linguo Liberated currently supports two modes of searching:
1. Manually inputting search conditions from the menu
2. Uploading a query from a file
"""

print('Welcome to Linguo Liberated')
while True:
    user_choice = input('''
What would you like to do?
1. Query from command line prompts
2. Query from file
8. Open Help
9. Exit
''').strip()
    if user_choice in valid_user_inputs:
        if user_choice == '1':
            query = Query.query_from_cli()
            api_response = DatamuseHandler.call_datamuse(query)
            DatamuseHandler.print_formatted_response(api_response)
        if user_choice == '2':
            user_path = input(f'''Please enter a file to read
Relative to {FileHandler.pwd}: ''').strip()
            validated_query = FileHandler.query_from_file(user_path)
            if validated_query:
                query = Query(validated_query)
                api_response = DatamuseHandler.call_datamuse(query)
                DatamuseHandler.print_formatted_response(api_response)
        if user_choice == '8':
            print(help_message)
            input('Press ENTER to return to the main menu\n')
        if user_choice == '9':
            print('Hope to see you again!')
            exit()
    else:
        print('Sorry, I didn\'t understand that.')
