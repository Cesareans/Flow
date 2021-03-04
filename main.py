import common.logging_config as logging_config
from network.game_server import Server
from registor import Registor
from watch.watcher import Watcher

if __name__ == '__main__':
    logging_config.init()
    Registor.register()
    server = Server()
    Watcher(server).start()
    server.start()
