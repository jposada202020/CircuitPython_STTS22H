# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`stts22h`
================================================================================

CircuitPython Driver for the STTS22H Temperature Sensor


* Author(s): Jose D. Montoya


"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

try:
    from busio import I2C
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_STTS22H.git"

_REG_WHOAMI = const(0x01)
_CTRL = const(0x04)


ODR_25_HZ = const(0b00)
ODR_50_HZ = const(0b01)
ODR_100_HZ = const(0b10)
ODR_200_HZ = const(0b11)
output_data_rate_values = (ODR_25_HZ, ODR_50_HZ, ODR_100_HZ, ODR_200_HZ)


class STTS22H:
    """Driver for the STTS22H Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the STTS22H is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x3C`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`STTS22H` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import stts22h

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        stts = stts22h.STTS22H(i2c)

    Now you have access to the attributes

    .. code-block:: python

        temp = stts.temperature

    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")

    _temperature_high_limit = UnaryStruct(0x02, "B")
    _temperature_low_limit = UnaryStruct(0x03, "B")

    _freerun = RWBit(_CTRL, 2)
    _output_data_rate = RWBits(2, _CTRL, 4)

    _temperature_LSB = ROUnaryStruct(0x06, "B")
    _temperature_MSB = ROUnaryStruct(0x07, "B")

    _high_limit = ROBit(0x05, 1)
    _low_limit = ROBit(0x05, 2)

    def __init__(self, i2c_bus: I2C, address: int = 0x3C) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0xA0:
            raise RuntimeError("Failed to find STTS22H")

        self._freerun = True

    @property
    def temperature(self) -> float:
        """
        The temperature sensor in Celsius
        :return: Temperature
        """

        return (self._temperature_MSB * 256 + self._temperature_LSB) / 100

    @property
    def temperature_high_limit(self) -> float:
        """
        Temperature High Limit
        """
        return self._temperature_high_limit

    @temperature_high_limit.setter
    def temperature_high_limit(self, value):
        self._temperature_high_limit = value

    @property
    def temperature_low_limit(self) -> float:
        """
        Temperature Low limit
        """
        return self._temperature_low_limit

    @temperature_low_limit.setter
    def temperature_low_limit(self, value: float):
        self._temperature_low_limit = value

    @property
    def high_limit(self) -> bool:
        """
        The bit is automatically reset to '0' upon reading the STATUS register.
        :return: value if the temperature exceeds the high limit
        """
        value = (False, True)
        return value[self._high_limit]

    @property
    def low_limit(self) -> bool:
        """
        The bit is automatically reset to '0' upon reading the STATUS register.
        :return: value if the temperature went under the low limit
        """
        value = (False, True)
        return value[self._low_limit]

    @property
    def output_data_rate(self) -> str:
        """
        Sensor output_data_rate

        +--------------------------------+------------------+
        | Mode                           | Value            |
        +================================+==================+
        | :py:const:`stts22h.ODR_25_HZ`  | :py:const:`0b00` |
        +--------------------------------+------------------+
        | :py:const:`stts22h.ODR_50_HZ`  | :py:const:`0b01` |
        +--------------------------------+------------------+
        | :py:const:`stts22h.ODR_100_HZ` | :py:const:`0b10` |
        +--------------------------------+------------------+
        | :py:const:`stts22h.ODR_200_HZ` | :py:const:`0b11` |
        +--------------------------------+------------------+
        """
        values = (
            "ODR_25_HZ",
            "ODR_50_HZ",
            "ODR_100_HZ",
            "ODR_200_HZ",
        )
        return values[self._output_data_rate]

    @output_data_rate.setter
    def output_data_rate(self, value: int) -> None:
        if value not in output_data_rate_values:
            raise ValueError("Value must be a valid output_data_rate setting")
        self._output_data_rate = value
