# SPDX-FileCopyrightText: 2022 Jeff Epler
#
# SPDX-License-Identifier: Unlicense

import board
import rainbowio
import adafruit_ticks
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelMap
from adafruit_neopxl8 import NeoPxl8

# Customize for your strands here
num_strands = 8
strand_length = 20
first_led_pin = board.NEOPIXEL0

num_pixels = num_strands * strand_length

# Make the object to control the pixels
pixels = NeoPxl8(
    first_led_pin,
    num_pixels,
    num_strands=num_strands,
    auto_write=False,
    brightness=0.50,
)


def strand(n):
    return PixelMap(
        pixels,
        range(n * strand_length, (n + 1) * strand_length),
        individual_pixels=True,
    )


# Create the 8 virtual strands
strands = [strand(i) for i in range(num_strands)]

# For each strand, blink a color (as rgb tuple or hex code)
animations = [
    Pulse(strand, 0.15, (0, 200, 200))
    for i, strand in enumerate(strands)
]


# Advance the animations by varying amounts so that they become staggered
for i, animation in enumerate(animations):
    animation._tail_start = 30 * 5 * i // 8  # pylint: disable=protected-access

# Group them so we can run them all at once
animations = AnimationGroup(*animations)

# Run the animations and report on the speed in frame per secodn
t0 = adafruit_ticks.ticks_ms()
frame_count = 0
while True:
    animations.animate()

