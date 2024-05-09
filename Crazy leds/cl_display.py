from machine import Pin, SoftI2C, I2S, SPI, freq, RTC

import gc

###  hardware initialization

from lib.st7735r import ST7735R as TFT


#LCD TFT display configuration
dc = Pin(2, Pin.OUT, value=1)  # Arbitrary pins
cs = Pin(5, Pin.OUT, value=1)
rst = Pin(4, Pin.OUT, value=1)
# Hardware SPI on native pins for performance. Check DRIVERS.md for optimum baudrate.
spi = SPI(2, 60_000_000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
gc.collect()
gc.mem_free()
tft = TFT(spi, cs, dc, rst)
# On st7735r 1.8 inch display can exchange height and width for portrait mode. See docs.
# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2020 Peter Hinch



