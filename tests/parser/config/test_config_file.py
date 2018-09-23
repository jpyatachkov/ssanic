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
        ('''document_root /home
        cpu_limit 2
        ''', (2, '/home')),
        ('''cpu_limit 2
        document_root /home''', (2, '/home')),
        ('''cpu_limit 2 document_root /home
        ''', (2, '/home')),
        ('''cpu_limit 2 document_root C:\\Users\\jpyatachkov\\Desktop''', (2, r'C:\Users\jpyatachkov\Desktop')),
        ('''cpu_limit 2 document_root /f-1---1/folder.2/my_foler/fooolder''',
         (2, '/f-1---1/folder.2/my_foler/fooolder')),
    ])
    def test_correct_file_format(self, content, expected, mocker):
        num_workers, document_root = expected
        self._prepare_config_file(content)

        with mocker.patch('os.path.exists', return_value=True):
            parser = ConfigFileParser(self.CONFIG_FILE_NAME)

        assert num_workers == parser.num_workers
        assert document_root == parser.document_root

    @pytest.mark.parametrize('content', [
        '',
        'num_workers 10',
        'cpu_limit 2',
        'document_root /home/folder',
        'cpu_limit kfmg document_root /home',
        'cpu_limit kfmg document_root 100',
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
