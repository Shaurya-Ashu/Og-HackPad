import board
import time
import neopixel

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()

# -------------------------
# LED SETUP (4x4 MATRIX)
# -------------------------
PIXEL_PIN = board.GP26
NUM_PIXELS = 16

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.4,
    auto_write=False
)

# -------------------------
# SIMPLE VISUALIZER ENGINE
# -------------------------
hue = 0

def rainbow_cycle(step=5):
    global hue
    for i in range(NUM_PIXELS):
        pixels[i] = (
            (hue + i * 10) % 255,
            255 - ((hue + i * 10) % 255),
            (hue * 2) % 255
        )
    pixels.show()
    hue = (hue + step) % 255

# -------------------------
# MEDIA KEYS
# -------------------------
keyboard.extensions.append(MediaKeys())

# -------------------------
# ROTARY ENCODER
# -------------------------
encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.GP27, board.GP28),  # Encoder A/B
)

encoder.map = [
    (
        KC.VOLU,  # clockwise
        KC.VOLD   # counter-clockwise
    )
]

# -------------------------
# BUTTON MATRIX (3 KEYS)
# -------------------------
keyboard.col_pins = (board.GP1, board.GP2, board.GP3)
keyboard.row_pins = ()
keyboard.diode_orientation = None

keyboard.keymap = [
    [
        KC.MPLY,   # SW1 → Play / Pause
        KC.MNXT,   # SW2 → Next Track
        KC.MPRV,   # SW3 → Previous Track
    ]
]

# -------------------------
# MAIN LOOP HOOK
# -------------------------
def before_matrix_scan():
    rainbow_cycle()

keyboard.before_matrix_scan = before_matrix_scan

keyboard.go()
