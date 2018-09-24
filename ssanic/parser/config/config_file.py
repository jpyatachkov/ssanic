import os
import re

__all__ = (
    'ConfigFileParser',
)


def _prepare_error_message(message):
    return 'Incorrect httpd.conf: {}.'.format(message)


class ConfigFileParser:
    NUM_WORKERS_REGEX_PATTERN = r'cpu_limit (?P<num_workers>\d+)'
    DOCUMENT_ROOT_REGEX_PATTERN = r'document_root (?P<document_root>[^\s]+)'
    HOST_REGEX_PATTERN = r'host (?P<host>[^\s]+)'
    PORT_REGEX_PATTERN = r'port (?P<port>\d+)'

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self._num_workers_re = re.compile(self.NUM_WORKERS_REGEX_PATTERN)
        self._document_root_re = re.compile(self.DOCUMENT_ROOT_REGEX_PATTERN)
        self._host_re = re.compile(self.HOST_REGEX_PATTERN)
        self._port_re = re.compile(self.PORT_REGEX_PATTERN)

        self.num_workers = None
        self.document_root = None
        self.host = None
        self.port = None

        self._parse()

    def _parse(self):
        with open(self._config_file_path, 'r') as fp:
            data = fp.read()

            if not data:
                raise ValueError(_prepare_error_message('Config file is empty'))

            match = self._num_workers_re.search(data)

            if match:
                self.num_workers = int(match.group('num_workers'))
            else:
                raise ValueError(_prepare_error_message('Number of workers param (cpu_limit) missing'))

            match = self._document_root_re.search(data)

            if match:
                document_root = match.group('document_root')

                if not os.path.exists(document_root):
                    raise ValueError(_prepare_error_message('Document root {} does not exist.'.format(document_root)))

                self.document_root = document_root
            else:
                raise ValueError(_prepare_error_message('Document root param (document_root) missing'))

            match = self._host_re.search(data)

            if match:
                self.host = match.group('host')
            else:
                raise ValueError(_prepare_error_message('Host param (host) missing'))

            match = self._port_re.search(data)

            if match:
                self.port = int(match.group('port'))
            else:
                raise ValueError(_prepare_error_message('Port param (port) is missing'))
