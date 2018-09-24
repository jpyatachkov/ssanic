from multiprocessing import Process

from ssanic.parser.config import (
    construct_cli_parser,
    ConfigFileParser
)
from ssanic.worker import (
    create_sock_connection,
    SsanicWorker
)


# noinspection PyShadowingNames
def _create_worker(sock, document_root):
    worker = SsanicWorker(sock, document_root)
    worker.idle()


def _main():
    cli_parser = construct_cli_parser()
    args = cli_parser.parse_args()

    processes = []

    if args.config_file:
        c = ConfigFileParser(args.config_file)
        num_workers, host, port, document_root = c.num_workers, c.host, c.port, c.document_root
    else:
        num_workers, host, port, document_root = args.num_workers, args.host, args.port, args.document_root

    print('SERVER START')
    print('host: {}'.format(host))
    print('port: {}'.format(port))
    print('document_root: {}'.format(document_root))
    print('num_workers: {}'.format(num_workers))

    sock = create_sock_connection(host, port)

    try:
        for process_num in range(num_workers):
            print('WORKER {} START'.format(process_num))
            process = Process(target=_create_worker, args=(sock, document_root))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process_num, process in enumerate(processes):
            print('WORKER {} STOP'.format(process_num))
            process.terminate()
        sock.close()
        print('SERVER STOP')


if __name__ == '__main__':
    _main()
