from typing import List

from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QCheckBox, \
    QApplication
from PyQt6.QtCore import Qt, QThread
from rs3helper.plugins.croesus.croesus_helper import CroesusHelper
from rs3helper.plugins.plugin import Plugin
import time
import traceback
import sys


class Application(QThread):
    def __init__(self):
        super().__init__()
        self.plugins: List[Plugin] = []
        self.running: bool = False

    def load_plugin(self, plugin: Plugin):
        try:
            self.plugins.append(plugin)
            plugin.disable()  # Start with plugin disabled
            print(f"Loaded plugin: {plugin.__class__.__name__}")
        except Exception as e:
            print(f"Error occurred while loading plugin: {str(e)}")

    def run(self):
        self.running = True
        print("Starting application...")
        while self.running:
            for plugin in self.plugins:
                print("Checking if plugin is enabled: " + str(plugin.enabled))
                if plugin.enabled:
                    try:
                        print(f"Updating plugin: {plugin.__class__.__name__}")
                        plugin.update()
                    except Exception as e:
                        print(f"Exception occurred: {e}")
                        traceback.print_exc()
            time.sleep(0.1)


class ApplicationGUI(QMainWindow):
    def __init__(self, application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Rs3Helper")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.application = application

        # Set up the main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        # Set up the start/stop button
        self.start_stop_button = QPushButton("Start", self)
        self.start_stop_button.clicked.connect(self.toggle_application)
        self.layout.addWidget(self.start_stop_button)

        # Set up the list of plugins
        self.plugin_list = QListWidget(self)
        self.layout.addWidget(self.plugin_list)

        # Load the plugins
        self.load_plugins()

        self.plugin_list.itemChanged.connect(self.plugin_item_changed)

    def toggle_application(self):
        if self.application.isRunning():
            self.application.running = False
            self.start_stop_button.setText("Start")
            for plugin in self.application.plugins:
                plugin.gui.hide()  # Hide the GUI of each plugin when the application stops
        else:
            self.application.start()
            self.start_stop_button.setText("Stop")
            for plugin in self.application.plugins:
                if plugin.enabled:
                    plugin.gui.show()  # Show the GUI of each enabled plugin when the application starts

    def load_plugins(self):
        for plugin in self.application.plugins:
            # Create a list item for each plugin
            item = QListWidgetItem(f"{plugin.__class__.__name__}")
            item.setCheckState(Qt.CheckState.Checked if plugin.enabled else Qt.CheckState.Unchecked)
            self.plugin_list.addItem(item)

    def plugin_item_changed(self, item):
        for plugin in self.application.plugins:
            if f"{plugin.__class__.__name__}" == item.text():
                if item.checkState() == Qt.CheckState.Checked:
                    plugin.enable()
                    if self.application.isRunning():
                        plugin.gui.show()
                else:
                    plugin.disable()
                    plugin.gui.hide()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        application = Application()
        croesus_helper = CroesusHelper()
        application.load_plugin(croesus_helper)  # Here

        gui = ApplicationGUI(application)
        gui.show()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Error occurred while running application: {str(e)}")
        traceback.print_exc()
