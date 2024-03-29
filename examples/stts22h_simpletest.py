# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import stts22h

i2c = board.I2C()  # uses board.SCL and board.SDA
stts = stts22h.STTS22H(i2c)

while True:
    print(f"Temperature: {stts.temperature}°C")
    print()
    time.sleep(0.5)
