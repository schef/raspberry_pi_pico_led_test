from machine import Pin
from utime import sleep
from time import ticks_ms

LED_PINS = [22, 21, 20, 19, 18, 17, 16, 14, 15, 13, 12, 11, 10, 9, 8]
BUTTON_PIN = 3
SPEED = 20
PATTERNS = [
    [
        ["x--------------", 100],
        ["-x-------------", 100],
        ["--x------------", 100],
        ["---x-----------", 100],
        ["----x----------", 100],
        ["-----x---------", 100],
        ["------x--------", 100],
        ["-------x-------", 100],
        ["--------x------", 100],
        ["---------x-----", 100],
        ["----------x----", 100],
        ["-----------x---", 100],
        ["------------x--", 100],
        ["-------------x-", 100],
        ["--------------x", 100],
        ["-------------x-", 100],
        ["------------x--", 100],
        ["-----------x---", 100],
        ["----------x----", 100],
        ["---------x-----", 100],
        ["--------x------", 100],
        ["-------x-------", 100],
        ["------x--------", 100],
        ["-----x---------", 100],
        ["----x----------", 100],
        ["---x-----------", 100],
        ["--x------------", 100],
        ["-x-------------", 100],
    ],
    [
        ["x-------------x", 100],
        ["-x-----------x-", 100],
        ["--x---------x--", 100],
        ["---x-------x---", 100],
        ["----x-----x----", 100],
        ["-----x---x-----", 100],
        ["------x-x------", 100],
        ["-------x-------", 100],
        ["------x-x------", 100],
        ["-----x---x-----", 100],
        ["----x-----x----", 100],
        ["---x-------x---", 100],
        ["--x---------x--", 100],
        ["-x-----------x-", 100],
    ],
    [
        ["-x-x-x-x-x-x-x-", 500],
        ["x-x-x-x-x-x-x-x", 500],
    ],
    [
        ["x-------------x", 100],
        ["xx-----------xx", 100],
        ["xxx---------xxx", 100],
        ["-xxx-------xxx-", 100],
        ["--xxx-----xxx--", 100],
        ["---xxx---xxx---", 100],
        ["----xxx-xxx----", 100],
        ["-----xxxxx-----", 100],
        ["------xxx------", 100],
        ["-----xxxxx-----", 100],
        ["----xxx-xxx----", 100],
        ["---xxx---xxx---", 100],
        ["--xxx-----xxx--", 100],
        ["-xxx-------xxx-", 100],
        ["xxx---------xxx", 100],
        ["xx-----------xx", 100],
        ["x-------------x", 100],
    ],
    [
        ["x--------------", 100],
        ["xx-------------", 100],
        ["xxx------------", 100],
        ["xxxx-----------", 100],
        ["-xxxx----------", 100],
        ["--xxxx---------", 100],
        ["---xxxx--------", 100],
        ["----xxxx-------", 100],
        ["-----xxxx------", 100],
        ["------xxxx-----", 100],
        ["-------xxxx----", 100],
        ["--------xxxx---", 100],
        ["---------xxxx--", 100],
        ["----------xxxx-", 100],
        ["-----------xxxx", 100],
        ["------------xxx", 100],
        ["-------------xx", 100],
        ["--------------x", 100],
    ],
    [
        ["x--------------", 250],
        ["--x------------", 250],
        ["----x----------", 250],
        ["-------x-------", 250],
        ["---------x-----", 250],
        ["-----------x---", 250],
        ["-------------x-", 250],
        ["-x-------------", 250],
        ["---x-----------", 250],
        ["-----x---------", 250],
        ["--------x------", 250],
        ["----------x----", 250],
        ["------------x--", 250],
        ["--------------x", 250],
    ],
    [
        ["x--------------", SPEED * 1],
        ["-x-------------", SPEED * 2],
        ["--x------------", SPEED * 3],
        ["---x-----------", SPEED * 4],
        ["----x----------", SPEED * 5],
        ["-----x---------", SPEED * 6],
        ["------x--------", SPEED * 7],
        ["-------x-------", SPEED * 8],
        ["--------x------", SPEED * 9],
        ["---------x-----", SPEED * 10],
        ["----------x----", SPEED * 11],
        ["-----------x---", SPEED * 12],
        ["------------x--", SPEED * 13],
        ["-------------x-", SPEED * 14],
        ["--------------x", SPEED * 15],
        ["-------------x-", SPEED * 14],
        ["------------x--", SPEED * 13],
        ["-----------x---", SPEED * 12],
        ["----------x----", SPEED * 11],
        ["---------x-----", SPEED * 9],
        ["--------x------", SPEED * 8],
        ["-------x-------", SPEED * 7],
        ["------x--------", SPEED * 6],
        ["-----x---------", SPEED * 5],
        ["----x----------", SPEED * 4],
        ["---x-----------", SPEED * 3],
        ["--x------------", SPEED * 2],
        ["-x-------------", SPEED * 1],
    ],
]

leds = []

def get_millis():
    return ticks_ms()

def millis_passed(timestamp):
    return get_millis() - timestamp

def create_led(pin):
    return Pin(pin, Pin.OUT)

def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_UP)

for pin in LED_PINS:
    leds.append(create_led(pin))

button = create_button(BUTTON_PIN)
button_state = 1
current_pattern = 0
current_line = 0
pattern_timestamp = 0

def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if not state:
        return
    global current_pattern, current_line
    current_pattern += 1
    current_line = 0
    if current_pattern == len(PATTERNS):
        current_pattern = 0

def check_button():
    global button_state
    state = button.value()
    if state != button_state:
        button_state = state
        on_button_callback(not button_state)
        
def check_leds():
    global pattern_timestamp, current_line
    if millis_passed(pattern_timestamp) >= PATTERNS[current_pattern][current_line][1]:
        pattern_timestamp = get_millis()
        current_line += 1
        if current_line >= len(PATTERNS[current_pattern]):
            current_line = 0
        for i in range(len(leds)):
            if PATTERNS[current_pattern][current_line][0][i] == "-":
                leds[i].off()
            else:
                leds[i].on()


while True:
    check_button()
    check_leds()
    