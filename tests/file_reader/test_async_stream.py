import os
from datetime import datetime

import pytest
from faker import Faker

from ssanic.file_reader import AsyncStreamFileReader

f = Faker()


class TestAsyncFileReader:
    TMP_FILE_NAME = str(datetime.now().timestamp())

    def teardown(self):
        try:
            os.remove(self.TMP_FILE_NAME)
        except FileNotFoundError:
            pass

    def _prepare_file(self, content=b''):
        with open(self.TMP_FILE_NAME, 'wb') as fp:
            fp.write(content)

    def test_init_correct_file(self):
        self._prepare_file()
        AsyncStreamFileReader(self.TMP_FILE_NAME)

    def test_init_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            AsyncStreamFileReader(f.file_path())

    @pytest.mark.parametrize('content,size', (
            (b'aaaaaaaaaa', 1),
            (b'aaaaaaaaaa', 5),
            (b'aa', 4),
            (b'', 1),
    ))
    @pytest.mark.asyncio
    async def test_async_read(self, content, size):
        self._prepare_file(content)

        reader = AsyncStreamFileReader(self.TMP_FILE_NAME)

        line_num = 0
        async for line in reader.read(size):
            expected = content[(line_num * size):((line_num + 1) * size)]
            assert expected == line
            line_num += 1
