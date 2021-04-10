import serial
from serial.tools import list_ports

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

dev = '/dev/ttyACM0'


class Port(QObject):
    port_closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._port = serial.Serial(None, timeout=1, baudrate=115200)
        self.__is_running = True

    def __del__(self):
        self.close()

    @pyqtSlot(str)
    def execute(self, command):
        print("execute: " + command)
        if command == "Connect":
            self.__open()
        elif command == "Disconnect":
            self.__close()
        else:
            print("Unknown command!")

    def __open(self):
        print(list_ports.comports())
        if dev in list_ports.comports():
            self._port.setPort(dev)
            self._port.open()
        else:
            self.port_closed_signal.emit()

    def __close(self):
        if self._port.isOpen():
            self.port_closed_signal.emit()
            self._port.close()
            self._port.setPort(None)

    @pyqtSlot(str)
    def send(self, data: str):
        print(data)
        if not self._port.isOpen():
            return

        if len(data) > 2 and data[:2] == "0x":
            data = data[2:]

        bytes_data = bytes.fromhex(data)
        print(bytes_data)
        # self._port.write(bytes_data)

    def run(self):
        while self.__is_running:
            if not self._port.isOpen():
                continue

            bytes_num = self._port.in_waiting()
            try:
                data = self._port.read(bytes_num)
            except:
                print("exception")

    def stop(self):
        self.__close()
        self.__is_running = False
