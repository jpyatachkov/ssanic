from ssanic.parser.http import RequestParser


class SsanicWorker:

    def __init__(self, document_root):
        self.document_root = document_root
        self.request_parser = RequestParser()

    def idle(self):
        pass

    def _handle_request(self):
        pass
