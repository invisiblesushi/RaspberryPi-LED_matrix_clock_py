from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from configparser import ConfigParser
from pyowm.owm import OWM
import RPi.GPIO as GPIO
import time
import os

#Globals
textColor = (255, 255, 255)
textColor_blue = (0, 0, 255)
textColor_red = (255, 0, 0)

matrix = None
weather = None
last_weather_time = datetime.min

image = Image.open("res/black.png").convert("RGB")
image.thumbnail((64, 32), Image.Resampling.LANCZOS)
config = ConfigParser()
config.read('appsettings.ini')

#GPIO pin config
screen_id = 0
screen_max = 3
btn_up = 10
btn_down = 8
btn_right = 32
btn_left = 33
btn_rst = 31
brightness = 100

def main():
	global matrix
	global weather
	weather = get_weather()
	matrix = matrix_init(brightness)
	gpio_init()

	print('screen_id = ' + str(screen_id))

	try:
		while True:  # Run forever
			currentTime = datetime.now()

			if screen_id == 0:
				frame = sakura_clock(matrix, currentTime)
			if screen_id == 1:
				frame = fuji_clock(matrix, currentTime)
			if screen_id == 2:
				frame = clock(matrix, currentTime)
			if screen_id == 3:
				frame = weather_clock(matrix, currentTime)

			time.sleep(0.1)

			# Print image on LED matrix
			matrix.SetImage(frame)

	finally:
		GPIO.cleanup
		print('GPIO.cleanup')


def matrix_init(brightness):
	options = RGBMatrixOptions()
	options.rows = 32
	options.cols = 64
	options.chain_length = 1
	options.parallel = 1
	options.hardware_mapping = 'regular'
	options.brightness = brightness
	options.gpio_slowdown = 0
	options.pwm_lsb_nanoseconds = 80
	options.limit_refresh_rate_hz = 150
	options.drop_privileges = False
	return RGBMatrix(options = options)

def gpio_init():
	GPIO.cleanup
	print('GPIO.cleanup')

	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	# Configure gpio buttons
	GPIO.setup(btn_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_rst, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	# Set button event detection
	GPIO.add_event_detect(btn_up, GPIO.RISING, callback=on_pushup, bouncetime=200)
	GPIO.add_event_detect(btn_down, GPIO.RISING, callback=on_pushdown, bouncetime=200)
	GPIO.add_event_detect(btn_right, GPIO.RISING, callback=on_pushright, bouncetime=200)
	GPIO.add_event_detect(btn_left, GPIO.RISING, callback=on_pushleft, bouncetime=200)
	GPIO.add_event_detect(btn_rst, GPIO.RISING, callback=on_pushrst, bouncetime=200)

def on_pushup(channel):
	global screen_id
	if screen_id >= screen_max:
		screen_id = 0
	else:
		screen_id = screen_id + 1
	print('screen_id = ' + str(screen_id))

def on_pushdown(channel):
	global screen_id
	if screen_id <= 0:
		screen_id = 3
	else:
		screen_id = screen_id - 1
	print('screen_id = ' + str(screen_id))

def on_pushright(channel):
	global matrix
	global brightness
	if (brightness <= 100) & (brightness > 10):
		brightness = brightness - 10
	print(brightness)
	matrix.brightness = brightness

def on_pushleft(channel):
	global matrix
	global brightness
	if (brightness >= 10) & (brightness < 100):
		brightness = brightness + 10
	print(brightness)
	matrix.brightness = brightness

def on_pushrst(channel):
	print("Shutting down")
	os.system("shutdown now -h")

def sakura_clock(matrix, currentTime):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	image = Image.open("res/sakura.png").convert("RGB")
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((1, 1), currentTime.strftime("%H:%M"), textColor, font)
	return frame

def fuji_clock(matrix, currentTime):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	image = Image.open("res/fuji.png").convert("RGB")
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((13, 1), currentTime.strftime("%H:%M"), textColor, font)
	return frame

def clock(matrix, currentTime):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=15)
	image = Image.open("res/black.png").convert("RGB")
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((4, 8.5), currentTime.strftime("%H:%M"), textColor, font)
	return frame

def weather_clock(matrix, currentTime):
	global weather
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	font_small = ImageFont.truetype(font='fonts/tiny.otf', size=5)
	weather = get_weather()

	weather_icon = get_weather_icon(weather.weather_icon_name)
	weatherIcon = Image.open(weather_icon).convert("RGB")
	image.paste(weatherIcon, (5,10))

	#Temperature Celcius
	celsius = weather.temperature('celsius')
	temperature = str(round(celsius['temp'])) + '°C'
	temperature_max = str(round(celsius['temp_max'])) + '°'
	temperature_min = str(round(celsius['temp_min'])) + '°'

	frame = image.copy()
	draw = ImageDraw.Draw(frame)

	# low high temp
	draw.text((25, 10), temperature, textColor, font)
	draw.text((25, 22), temperature_min, textColor_blue, font_small)
	draw.text((35, 22), '|', textColor, font_small)
	draw.text((39, 22), temperature_max, textColor_red, font_small)

	# Date
	draw.text((1, 1), currentTime.strftime('%d'), textColor, font_small)
	draw.line(((9, 5), (9, 5)), textColor, 1)
	draw.text((11, 1), currentTime.strftime('%m'), textColor, font_small)

	# Time
	draw.text((25, 1), currentTime.strftime('%H'), textColor, font_small)
	draw.text((32, 1), currentTime.strftime(':'), textColor, font_small)
	draw.text((35, 1), currentTime.strftime('%M'), textColor, font_small)

	# Weekday
	draw.text((52, 1), get_weekday_short(), textColor, font_small)

	# Divider line
	draw.line(((0,7), (64,7)), textColor, 1)

	return frame

def get_weather():
	global weather
	global last_weather_time
	last_weather_diff_min = (datetime.now() - last_weather_time).total_seconds() / 60

	# get weather every 10m
	if last_weather_diff_min > 10:
		owm = OWM(config.get('Open_weather_map', 'owm_api_key'))
		location = config.get('Open_weather_map', 'location')
		mgr = owm.weather_manager()
		weather = mgr.weather_at_place(location).weather
		last_weather_time = datetime.now();
		print('Weather = ' + str(weather))

	return weather

def get_weekday_short():
	weekday = datetime.now().weekday()
	if weekday == 1:
		return 'MON'
	if weekday == 2:
		return 'TUE'
	if weekday == 3:
		return 'WED'
	if weekday == 4:
		return 'THU'
	if weekday == 5:
		return 'FRI'
	if weekday == 6:
		return 'SAT'
	if weekday == 7:
		return 'SUN'

def get_weather_icon(icon_name):
	if icon_name == '01d' or icon_name == '01n':
		return "res/01d.png"
	elif icon_name == '02d' or icon_name == '02n':
		return "res/02d.png"
	elif icon_name == '03d' or icon_name == '03n':
		return "res/03d.png"
	elif icon_name == '04d' or icon_name == '04n':
		return "res/04d.png"
	elif icon_name == '09d' or icon_name == '09n':
		return "res/09d.png"
	elif icon_name == '10d' or icon_name == '10n':
		return "res/10d.png"
	elif icon_name == '13d' or icon_name == '13n':
		return "res/13d.png"
	elif icon_name == '50d' or icon_name == '50n':
		return "res/50d.png"


# Main function
if __name__== "__main__" :
	main()
