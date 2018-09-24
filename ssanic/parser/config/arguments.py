import argparse as ap


def construct_cli_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--document_root',
                        type=str,
                        default='',
                        help='directory to serve static files from')
    parser.add_argument('--host',
                        type=str,
                        default='localhost',
                        help='host to bind to')
    parser.add_argument('--port',
                        type=str,
                        default='80',
                        help='port to listen to')
    parser.add_argument('--num-workers',
                        type=int,
                        dest='num_workers',
                        default=1,
                        help='number of workers')
    parser.add_argument('--config-file',
                        type=str,
                        dest='config_file',
                        default='',
                        help='path to config file (if provided, all other CLI args will be ignored - their values would be obtained from config file)')

    return parser
