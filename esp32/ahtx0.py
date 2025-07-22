import time
from micropython import const

AHTX0_I2CADDR = const(0x38)

AHTX0_CMD_INITIALIZE = const(0xE1)
AHTX0_CMD_TRIGGER = const(0xAC)
AHTX0_CMD_SOFTRESET = const(0xBA)

AHTX0_STATUS_BUSY = const(0x80)
AHTX0_STATUS_CALIBRATED = const(0x08)


class AHTx0:
    def __init__(self, i2c, address=AHTX0_I2CADDR):
        self.i2c_device = i2c
        self.address = address
        self.buf = bytearray(6)

        self.reset()
        time.sleep(0.02)
        self.initialize()
        time.sleep(0.02)

    def reset(self):
        try:
            self.i2c_device.writeto(self.address, bytearray([AHTX0_CMD_SOFTRESET]))
        except OSError:
            pass
        time.sleep(0.02)

    def initialize(self):
        try:
            self.i2c_device.writeto(self.address, bytearray([AHTX0_CMD_INITIALIZE, 0x08, 0x00]))
        except OSError:
            pass
        time.sleep(0.02)

    def _read_data(self):
        self.i2c_device.writeto(self.address, bytearray([AHTX0_CMD_TRIGGER, 0x33, 0x00]))
        time.sleep(0.075)

        self.buf = self.i2c_device.readfrom(self.address, 6)

        if self.buf[0] & AHTX0_STATUS_BUSY:
            raise RuntimeError("Sensor está ocupado")

        raw_humi = ((self.buf[1] << 16) | (self.buf[2] << 8) | self.buf[3]) >> 4
        raw_temp = ((self.buf[3] & 0x0F) << 16) | (self.buf[4] << 8) | self.buf[5]

        humidity = (raw_humi / 1048576.0) * 100
        temperature = (raw_temp / 1048576.0) * 200 - 50

        return temperature, humidity

    @property
    def temperature(self):
        temp, _ = self._read_data()
        return temp

    @property
    def relative_humidity(self):
        _, hum = self._read_data()
        return hum


# Alias para facilitar o uso com AHT10 ou AHT20
class AHT10(AHTx0):
    pass

class AHT20(AHTx0):
    pass
