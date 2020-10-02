import os


class FileHandler:
    pwd = os.getcwd()

    @classmethod
    def verify_path_exists(cls, path: str) -> bool:
        return os.path.isfile(path)

    @classmethod
    def read_query(cls, path: str) -> str:
        try:
            with open(path, 'r') as file_handler:
                content = file_handler.read()
                return content
        except FileNotFoundError:
            print(f'File not found at {path}')
            return ''
        except PermissionError:
            print(f'You don\'t have rights to read file at {path}')
            return ''

    @classmethod
    def validate_query(cls, content: str) -> dict:
        valid_query = {}
        lines = content.splitlines()
        line_number = 1
        for line in lines:
            if line.strip():
                try:
                    key, value = line.split(':', 1)
                    valid_query[key] = value.strip()
                except ValueError:
                    print(f'Error on line number {line_number}: {line}')
                    print('Please ensure the line contains ":" and try again')
                    return {}
            line_number += 1
        return valid_query

    @classmethod
    def query_from_file(cls, user_path: str) -> dict:
        if not cls.verify_path_exists(user_path):
            print(f'File {cls.pwd}/{user_path} does not exist')
            return {}
        file_query = cls.read_query(user_path)
        validated_query = cls.validate_query(file_query)
        return validated_query
