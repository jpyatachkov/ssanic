import os
from datetime import datetime

import pytest
from faker import Faker

from ssanic.parser.config import ConfigFileParser

f = Faker()


class TestConfigFileParser:
    CONFIG_FILE_NAME = str(datetime.now().timestamp())

    def teardown(self):
        try:
            os.remove(os.path.abspath(self.CONFIG_FILE_NAME))
        except FileNotFoundError:
            pass

    def _prepare_config_file(self, content):
        with open(self.CONFIG_FILE_NAME, 'w') as fp:
            fp.write(content)

    @pytest.mark.parametrize('content,expected', [
        (
                '''document_root /home
                cpu_limit 2
                host localhost
                port 8080
                ''',
                (2, '/home', 'localhost', 8080)
        ),
        (
                '''cpu_limit 2
                document_root /home host localhost
                port 8080''',
                (2, '/home', 'localhost', 8080)
        ),
        (
                '''cpu_limit 2 document_root /home host localhost
                port 8080
                ''',
                (2, '/home', 'localhost', 8080)
        ),
        (
                '''host localhost
                port 8080
                cpu_limit 2 document_root C:\\Users\\jpyatachkov\\Desktop''',
                (2, r'C:\Users\jpyatachkov\Desktop', 'localhost', 8080)
        ),
        (
                '''host localhost port 8080 cpu_limit 2 document_root /f-1---1/folder.2/my_foler/fooolder''',
                (2, '/f-1---1/folder.2/my_foler/fooolder', 'localhost', 8080)
        ),
    ])
    def test_correct_file_format(self, content, expected, mocker):
        num_workers, document_root, host, port = expected
        self._prepare_config_file(content)

        with mocker.patch('os.path.exists', return_value=True):
            parser = ConfigFileParser(self.CONFIG_FILE_NAME)

        assert num_workers == parser.num_workers
        assert document_root == parser.document_root
        assert host == parser.host
        assert port == parser.port

    @pytest.mark.parametrize('content', [
        '',
        'num_workers 10',
        'cpu_limit 2',
        'host localhost',
        'port 8080',
        'document_root /home/folder',
        'cpu_limit kfmg document_root /home host localhost port 80',
        'cpu_limit 10 document_root /home host localhost port skfg',
    ])
    def test_incorrect_file_format(self, content, mocker):
        self._prepare_config_file(content)

        with mocker.patch('os.path.exists', return_value=True):
            with pytest.raises(ValueError):
                ConfigFileParser(self.CONFIG_FILE_NAME)

    @pytest.mark.parametrize('content', [
        'cpu_limit 2 document_root /wrong',
    ])
    def test_document_root_does_not_exists(self, content):
        self._prepare_config_file(content)

        with pytest.raises(ValueError):
            ConfigFileParser(self.CONFIG_FILE_NAME)

    def test_config_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            ConfigFileParser(f.file_path())
