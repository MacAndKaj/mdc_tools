

class Message:
    FRAME_CTRL_DATA = 0xF0

    def message_id(self):
        raise NotImplementedError("Should be implemented in derived class!")

    def get_data(self):
        raise NotImplementedError("Should be implemented in derived class!")

    def serialize(self):
        data = bytearray([self.FRAME_CTRL_DATA, self.message_id()])
        data.join(self.get_data())
        data.join([self.FRAME_CTRL_DATA.to_bytes(1, 'big')])
        return data


class PlatformSetMotorSpeedReq(Message):
    PLATFORM_SET_MOTOR_SPEED_REQ_ID = 0x01

    def __init__(self, motor, speedI, speedF):
        self._motor = motor
        self._speedI = speedI
        self._speedF = speedF

    def message_id(self):
        return self.PLATFORM_SET_MOTOR_SPEED_REQ_ID

    def get_data(self):
        return [self._motor.to_bytes(1, 'big'), self._speedI.to_bytes(1, 'big', signed=True),
                self._speedF.to_bytes(1, 'big')]
