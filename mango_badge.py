# Mango badge code - images should be 288 x 130

from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import jpegdec
import qrcode
import _thread

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)


WIDTH, HEIGHT = display.get_bounds()

LIGHTEST = display.create_pen(255, 255, 255)
LIGHT = display.create_pen(255, 182, 80)
DARK = display.create_pen(255, 156, 81)
DARKEST = display.create_pen(0, 0, 0)

# Constants for states
NAME = "Mango-Birb"
QR_TEXT = "https://t.me/Mangobirb"
badge_mode = "photo"
IMAGE_NAME = "watermango.jpg"

current_image = 1
total_images = 5

# Some constants for drawing
BORDER_SIZE = 4
PADDING = 10


def draw_badge():
    # draw border
    display.set_pen(LIGHT)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw name text
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING, WIDTH, 6)
    
    # Draw button labels
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("Info", 48, 215, 160, 2)
    display.text("Slideshow", 120, 215, 160, 2)
    display.text("QR", 240, 215, 160, 2)
    
def draw_transition():
    # draw border
    display.set_pen(LIGHT)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw name text
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text("Slideshow starting...", BORDER_SIZE + PADDING, HEIGHT - 130 , WIDTH, 3)
    


def show_photo():
    j = jpegdec.JPEG(display)
    
    # Open the JPEG file
    j.open_file(IMAGE_NAME)

    # Draws a box around the image
    display.set_pen(LIGHT)
    display.rectangle(PADDING , HEIGHT - ((BORDER_SIZE * 2) + PADDING) - 153, 292 + (BORDER_SIZE * 2), 130 + (BORDER_SIZE * 2))

    # Decode the JPEG
    j.decode(BORDER_SIZE + PADDING + 2, HEIGHT - (BORDER_SIZE + PADDING) - 153)


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(LIGHTEST)
    display.rectangle(ox, oy, size, size)
    display.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def show_qr():
    display.set_pen(DARK)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(QR_TEXT)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)

def image_rotate(current_image, total_images):
    if current_image == 1:
        IMAGE_NAME = "watermango.jpg"
    if current_image == 2:
        IMAGE_NAME = "pinkmango.jpg"
    if current_image == 3:
        IMAGE_NAME = "yellowmango.jpg"
    if current_image == 4:
        IMAGE_NAME = "sofamango.jpg"
    if current_image == 5:
        IMAGE_NAME = "realisticmango.jpg"
    return IMAGE_NAME

def core0_thread():
    while True:
        global badge_mode
        if button_c.is_pressed:
            if badge_mode == "photo":
                badge_mode = "qr"
                show_qr()
                display.update()
            else:
                badge_mode = "photo"
                draw_badge()
                show_photo()
                display.update()
            time.sleep(1)
            
        if button_a.is_pressed:
            if badge_mode == "photo":
                badge_mode = "info"
                draw_badge()
                display.update()
            else:
                badge_mode = "info"
                draw_badge()
                show_photo()
                display.update()
            time.sleep(1)
            
        if button_b.is_pressed:
            if badge_mode == "photo":
                badge_mode = "slide"
                draw_transition()
                display.update()
                time.sleep(2)
                draw_badge()
                show_photo()
                display.update()
            else:
                badge_mode = "photo"
                draw_badge()
                show_photo()
                display.update()
            time.sleep(1)
 
 
def core1_thread():
    while True:
        while badge_mode == "slide":
            global IMAGE_NAME, current_image, total_images
            time.sleep(5)
            IMAGE_NAME = image_rotate(current_image, total_images)
            if current_image == total_images:
                current_image = 0
            current_image += 1
            draw_badge()
            show_photo()
            display.update()
 

# draw the badge for the first time
draw_badge()
show_photo()
display.update()

second_thread = _thread.start_new_thread(core1_thread, ())

core0_thread()
