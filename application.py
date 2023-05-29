import time
from typing import List

from plugins.croesus.croesus_helper import CroesusHelper
from plugins.plugin import Plugin



class Application:
    def __init__(self):
        self.plugins: List[Plugin] = []
        self.running: bool = False

    def load_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)

    def start(self):
        self.running = True
        while self.running:
            for plugin in self.plugins:
                if plugin.enabled:
                    print('Updating')
                    plugin.update()
            time.sleep(0.1)

    def stop(self):
        self.running = False


if __name__ == '__main__':
    app = Application()
    croesus_helper = CroesusHelper()
    app.load_plugin(croesus_helper)
    app.start()
