from RPi import GPIO
from time import sleep
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import threading
import time

COUNTS_PER_ROTATION = 531.0 * (406.78 / 360.0) * (340.0 / 360.0)

lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

clk = 17
dt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

degrees_per_count = 360.0 / COUNTS_PER_ROTATION
counter = 0.0
prev = 0.0

def refresh():
	global counter
	lcd.color=[255,255,255]
	msg = "%07.2f\n" % (counter)
	lcd.message = msg

def read_enc():
	return GPIO.input(clk), GPIO.input(dt)

def check_cmds():
	global counter
	while True:
		refresh()
		if lcd.select_button:
			counter = 0.0
			time.sleep(3)
		if lcd.left_button:
			lcd.clear()
			time.sleep(3)
		time.sleep(0.5)

prev_a, _ = read_enc()

t = threading.Timer(1, check_cmds)
t.daemon = True
t.start()

lcd.clear()
lcd.message = "0000.00"
try:
	while True:
		curr_a, curr_b = read_enc()
		if curr_a != prev_a:
			if curr_b != curr_a:
                		counter += degrees_per_count
			else:
                		counter -= degrees_per_count
			prev_a = curr_a
finally:
	GPIO.cleanup()

