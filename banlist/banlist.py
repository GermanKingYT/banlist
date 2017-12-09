import logging
import sys

import yaml

from .bfbc2 import Bfbc2


def main():
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
    numeric_level = getattr(logging, config['system']['logLevel'].upper(), None)
    if numeric_level is None:
        raise ValueError('Invalid log level: %s' % config['system']['logLevel'])
    logging.basicConfig(
        level=numeric_level,
        format='[%(asctime)s] %(message)s',
        handlers=[
            logging.FileHandler("system.log"),
            logging.StreamHandler()
        ]
    )

    services = []

    if config['bfbc2']['enabled']:
        inst_bfbc2 = Bfbc2.create_from_config(logging, config['bfbc2'])
        inst_bfbc2.start_thread()
        services.append(inst_bfbc2)
        logging.info('BFBC2: started plugin')

    try:
        # now all services are started
        # wait for threads to stop or for keyboard interrupt
        for service in services:
            service.thread.join()
    except KeyboardInterrupt:
        logging.info('received KeyboardInterrupt, stopping threads')
        for service in services:
            service.stop_thread()
        logging.info('closed sockets, waiting for threads to stop')
        for service in services:
            service.thread.join()
        logging.info('threads stopped')
