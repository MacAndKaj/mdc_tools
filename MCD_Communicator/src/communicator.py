from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPlainTextEdit, QLineEdit, QWidget, QTabWidget, \
    QPushButton
from PyQt5 import QtCore
from PyQt5.QtCore import *

import sys
from datetime import datetime

from MCD_Communicator.src.modules import port, messages


class CommunicatorLog(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.NoFocus)

    @pyqtSlot(str)
    def on_new_tx_text(self, text):
        prefix = "[" + self.get_time() + "] "
        self.insertPlainText(prefix + text + '\n')

    def get_time(self) -> str:
        now = datetime.now()
        return now.strftime("%d/%m/%Y-%H:%M:%S.%f")


class CommunicatorInputLine(QLineEdit):
    text_signal = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._input_text = ""

        self.returnPressed.connect(self.on_return_pressed)
        self.textChanged.connect(self.on_text_changed)

    def on_return_pressed(self):
        self.text_signal.emit(self._input_text)
        self.clear()

    def on_text_changed(self, text):
        self._input_text = text


class ConnectionButton(QPushButton):
    connection_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__("Connect")
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        transitions_map = {
            "Connect": "Disconnect",
            "Disconnect": "Connect",
        }
        previous_text = self.text()
        self.setText(transitions_map[self.text()])
        self.connection_signal.emit(previous_text)

    @pyqtSlot()
    def on_port_closed(self):
        print("on_port_closed")
        self.setText("Connect")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self._communicator_log = None
        self._communicator_input_line = None

        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle("MCD Communicator")
        self._connection_button = ConnectionButton()
        window_layout = QVBoxLayout()
        window_layout.addWidget(self._connection_button)

        main_widget = QTabWidget()
        self._free_communicator_tab = self.configure_free_communicator()
        main_widget.addTab(self._free_communicator_tab, "Free Communicator")
        self._message_communicator = QWidget()
        main_widget.addTab(self._message_communicator, "Message Communicator")
        window_layout.addWidget(main_widget)

        layout_widget = QWidget()
        layout_widget.setLayout(window_layout)
        self.setCentralWidget(layout_widget)
        self.setFocus()
        self.show()

    def configure_free_communicator(self) -> QWidget:
        free_communicator = QWidget()
        layout = QVBoxLayout()

        self._communicator_log = CommunicatorLog()
        self._communicator_input_line = CommunicatorInputLine()
        self._communicator_input_line.text_signal.connect(self._communicator_log.on_new_tx_text)

        layout.addWidget(self._communicator_log)
        layout.addWidget(self._communicator_input_line)

        free_communicator.setLayout(layout)
        return free_communicator

    def connect_main_window_with_port(self, port_obj: port.Port):
        self._connection_button.connection_signal.connect(port_obj.execute)
        self._communicator_input_line.text_signal.connect(port_obj.send)
        port_obj.port_closed_signal.connect(self._connection_button.on_port_closed)


class AppCore:
    def __init__(self):
        self._window = Window()
        self._port = port.Port()
        self._window.connect_main_window_with_port(self._port)
        self._port_thread = QThread()

    def start(self):
        self._port.moveToThread(self._port_thread)
        self._port_thread.started.connect(self._port.run)
        self._port_thread.start()

    def stop(self):
        self._port.stop()


if __name__ == '__main__':
    req = messages.PlatformSetMotorSpeedReq(1, -1, 50)
    print(req.serialize())

    app = QApplication(sys.argv)
    app_core = AppCore()
    # app_core.start()

    status = app.exec_()
    # app_core.stop()
    sys.exit(status)
