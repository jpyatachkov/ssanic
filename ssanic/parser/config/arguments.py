import argparse as ap


def construct_cli_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--workers', type=int, dest='num_workers', default=1)
    parser.add_argument('--document-root', type=str, dest='document_root', default='')
    parser.add_argument('--config-file', type=str, dest='config_file', default='')

    return parser
