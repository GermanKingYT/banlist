import threading
import time


class Bfbc2:
    """
    BFBC2 plugin
    """

    def __init__(self, logging):
        self.logging = logging
        self.clients = {}

        self.thread = None
        self.run_loop = True

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()

    def stop_thread(self):
        self.run_loop = False
        self.logging.info('BFBC2: got signal to stop thread')

    def relay(self):
        while self.run_loop:
            time.sleep(1)
        self.logging.info('BFBC2: stopped thread')

    @classmethod
    def create_from_config(cls, logging, relay_config):
        return cls(
            logging=logging
        )
