from flask import Flask, render_template, request
import time
import board
import neopixel
import random
import soco
from multiprocessing import Process, Value, active_children
from PIL import ImageColor

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

app = Flask(__name__)

p = None
active_mode = None
brightness = 50
speed = 50
color="#FFFFFF"
sonos = None
def_volume = 0


def init_sonos():
    try:
        print("init sonos")
        global def_volume
        devices = soco.discover()
        device = devices.pop()
        def_volume = device.volume
    except:
        device = None
    return device

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

def set_brightness(b):
    global active_mode, speed
    pixels.brightness = int(b)/100
    set_to_mode(active_mode)
    pixels.show()

def set_color(c):
    pixels.fill(ImageColor.getcolor(c, "RGB"))
    pixels.show()

def rainbow_cycle_random(wait):
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i*(i+20)) +j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

def party(wait):
    while True:
        for i in range(num_pixels):
            pixels[i] = (random.randint(0, 220),random.randint(0, 220),random.randint(0, 220))
            pixels.show()
        time.sleep(wait)

def random_loop(wait):
    while True:
        for i in range(num_pixels):
            pixels[i] = (random.randint(0, 220),random.randint(0, 220),random.randint(0, 220))
            pixels.show()
            time.sleep(wait)

def jelly_fish_dance(wait):
    global sonos
    if not sonos:
        sonos = init_sonos()
    try:
        sonos.partymode()
    except:
        sonos.unjoin()
        sonos.partymode()
    try:
        sonos.play_uri('https://www.televisiontunes.com/uploads/audio/SpongeBob%20SquarePants%20-%20Stadium%20Rave%20A.mp3')
        group = sonos.group
        group.volume += 20 
    except:
        print("sonos not found")
    
    while True:
        for i in range(3):
            pixels.fill((255,0,0))
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0,255,0))
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0,0,255))
            pixels.show()
            time.sleep(0.5)
        for x in range(2):
            for j in range(1,4):
                for x in range(2):
                    for i in range(num_pixels):
                            if (i+x) % 2 == 1:
                                pixels[i] = (0,0,255)
                            else:
                                pixels[i] = (255,0,0)
                    pixels.show()
                    time.sleep(0.1)
            time.sleep(0.5)
        for j in range(1,7):
            for i in range(num_pixels):
                if j % 3 == 1:
                    pixels[i] = (255,0,0)
                if j % 3 == 2:
                    pixels[i] = (0,255,0)
                if j % 3 == 0:
                    pixels[i] = (0,0,255)
                pixels.show()
                time.sleep(0.008)
        for j in range(1,6):
            for x in range(2):
                for i in range(num_pixels):
                        if (i+x) % 2 == 1:
                            pixels[i] = (255,0,0)
                        else:
                            pixels[i] = (0,255,0)
                pixels.show()
                time.sleep(0.5)
        for j in range(1,6):
            for x in range(2):
                for i in range(num_pixels):
                        if (i+x) % 2 == 1:
                            pixels[i] = (0,0,255)
                        else:
                            pixels[i] = (255,0,0)
                pixels.show()
                time.sleep(0.5)

def jelly_fish_static(wait):
    silver = [1,5,8,14,17,19,28,31,35,38,46]
    blue = [2,10,16,24,25,26,29,32,33,40,42,44]
    purple = [4,12,21,27,45]
    red = [6,30,37]
    green=[23,41,47]
    empty = [3,7,9,11,13,15,18,20,22,34,36,39,43,48]

    sdict = {}
    while True:
        for i in range(num_pixels):
            x = i+1
            if x in silver:
                try:
                    if sdict[x]["add"]:
                        sdict[x]["v"]=sdict[x]["v"]+1
                        if sdict[x]["v"] == 255:
                            sdict[x]["add"] = 0
                    else:
                        sdict[x]["v"]=sdict[x]["v"]-1
                        if sdict[x]["v"] <= 70:
                            sdict[x]["add"] = 1
                except:
                    sdict[x]= {
                        "v" : random.randint(70,254),
                        "add" : 1
                    }
                pixels[i] = (sdict[x]["v"],sdict[x]["v"],sdict[x]["v"])

            if x in blue:
                pixels[i] = (0,0,255)
            if x in purple:
                pixels[i] = (255,0,255)
            if x in red:
                pixels[i] = (255,0,0)
            if x in green:
                pixels[i] = (0,255,0)
            if x in empty:
                pixels[i] = (0,0,0)
        pixels.show()
        time.sleep(wait)

def set_to_mode(mode):
    global active_mode, p, speed
    try:
        p.terminate()
    except:
        pass
    calc_speed = (100-speed)/1000
    if mode == "party":
        if not active_mode == mode:
            speed = 50
            calc_speed = (100-speed)/1000
        active_mode = "party"
        p = Process(target=party, args=(calc_speed/10,))
        p.start()
    elif mode == "rainbow_cycle":
        if not active_mode == mode:
            speed = 95
            calc_speed = (100-speed)/1000
        active_mode = "rainbow_cycle"
        p = Process(target=rainbow_cycle, args=(calc_speed,))
        p.start()
    elif mode == "random_loop":
        if not active_mode == mode:
            speed = 50
            calc_speed = (100-speed)/1000
        active_mode = "random_loop"
        p = Process(target=random_loop, args=(calc_speed,))
        p.start()
    elif mode == "rainbow_cycle_random":
        if not active_mode == mode:
            speed = 95
            calc_speed = (100-speed)/1000
        active_mode = "rainbow_cycle_random"
        p = Process(target=rainbow_cycle_random, args=(calc_speed,))
        p.start()
    elif mode == "jelly_fish_dance":
        active_mode = "jelly_fish_dance"
        p = Process(target=jelly_fish_dance, args=(calc_speed,))
        p.start()
    elif mode == "jelly_fish_static":
        if not active_mode == mode:
            speed = 100
            calc_speed = (100-speed)/1000
        active_mode = "jelly_fish_static"
        p = Process(target=jelly_fish_static, args=(calc_speed,))
        p.start()

@app.before_first_request
def initial_mode():
    set_to_mode("jelly_fish_static")

@app.route('/', methods=['GET'])
def get_index():
    global sonos
    if not sonos:
        sonos = init_sonos()
    return render_template('index.html', brightness=brightness, speed=speed, color=color)

@app.route('/leds', methods=['GET'])
def set_function():
    pixels.fill((0,0,0))
    pixels.show()
    mode = request.args.get("mode")
    set_to_mode(mode)
    return render_template('index.html', brightness=brightness, speed=speed, color=color)


@app.route('/stop', methods=['GET'])
def stop():
    global sonos, def_volume, active_mode
    if active_mode == "jelly_fish_dance":
        try:
            group = sonos.group
            group.coordinator.stop()
            group.volume = def_volume
        except:
            print("sonos not running")
    active = active_children()
    try:
        for child in active:
            child.terminate()
    except:
        print("already terminated")
    pixels.fill((0,0,0))
    pixels.show()
    active_mode = None
    return render_template('index.html', brightness=brightness, speed=speed, color=color)

@app.route('/set-controls', methods=['GET'])
def set_controls():
    global brightness, speed, color
    brightness = request.args.get("bright")
    speed = int(request.args.get("speed"))
    set_brightness(brightness)
    if color != request.args.get("color"):
        color = request.args.get("color")
        set_color(color)
    return render_template('index.html', brightness=brightness, speed=speed, color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
