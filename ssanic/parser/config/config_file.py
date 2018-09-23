import os
import re

__all__ = (
    'ConfigFileParser',
)


class ConfigFileParser:
    NUM_WORKERS_REGEX_PATTERN = r'.*cpu_limit (?P<num_workers>\d+).*'
    DOCUMENT_ROOT_REGEX_PATTERN = r'.*document_root (?P<document_root>.+).*'

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self._num_workers_re = re.compile(self.NUM_WORKERS_REGEX_PATTERN)
        self._document_root_re = re.compile(self.DOCUMENT_ROOT_REGEX_PATTERN)

        self.num_workers = None
        self.document_root = None

        self._parse()

    def _parse(self):
        with open(self._config_file_path, 'r') as fp:
            data = fp.read()

            if not data:
                raise ValueError('Config file is empty')

            match = self._num_workers_re.search(data)

            if match:
                self.num_workers = int(match.group('num_workers'))
            else:
                raise ValueError('Incorrect config: num_workers missing. Add this field or ensure to use line breaks.')

            match = self._document_root_re.search(data)

            if match:
                document_root = match.group('document_root')

                if not os.path.exists(document_root):
                    raise ValueError(
                        'Document root {} does not exist. Add this field or ensure to use line breaks.'.format(
                            document_root
                        )
                    )

                self.document_root = document_root
            else:
                raise ValueError('Incorrect config: document_root missing')
