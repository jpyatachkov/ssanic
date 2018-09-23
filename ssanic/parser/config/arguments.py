import argparse as ap


def construct_cli_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('document_root',
                        type=str,
                        default='',
                        help='Directory to serve static files')
    parser.add_argument('host',
                        type=str,
                        default='localhost',
                        help='Host to bind to')
    parser.add_argument('port',
                        type=str,
                        default='80',
                        help='Port to listen to')
    parser.add_argument('--workers',
                        type=int,
                        dest='num_workers',
                        default=1,
                        help='Number of workers')
    parser.add_argument('--config-file',
                        type=str,
                        dest='config_file',
                        default='',
                        help='Path to config file (if provided, all CLI args will be ignored)')

    return parser
