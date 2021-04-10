from matplotlib import pyplot as plt
import serial
from datetime import datetime as dt

dev = '/dev/ttyACM0'


def save_data_to_file(filename, data):
    with open("files/" + filename, 'w') as file:
        for key in data:
            file.write(str(key) + "|" + str(data[key]) + "\n")


if __name__ == '__main__':
    u_t = {}
    y_t = {}
    port = serial.Serial(dev, timeout=1, baudrate=115200)
    """
        Reading with frequency 100Hz.
        T = 10ms
    """
    t = 0
    y = None
    u = None
    try:
        while port.is_open:
            line = str(port.readline(), 'ascii')
            splitted_line = line.split('|')

            try:
                y = float(splitted_line[0])
                u = int(splitted_line[1])
            except ValueError:
                print("skip")
                continue

            u_t[t] = u
            y_t[t] = y
            t += 1
    except serial.SerialException:
        pass

    date = dt.now()
    name_y = "y_" + str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute)
    name_u = "u_" + str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute)

    save_data_to_file(name_y + '.txt', y_t)
    save_data_to_file(name_u + '.txt', u_t)

    fig, axs = plt.subplots(2)

    axs[0].plot([i for i in y_t.keys()], [i for i in y_t.values()], '--')
    axs[1].plot([i for i in u_t.keys()], [i for i in u_t.values()])
    plt.show()
