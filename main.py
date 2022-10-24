from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from configparser import ConfigParser
from pyowm.owm import OWM
import RPi.GPIO as GPIO
import time

#Globals
textColor = (255, 255, 255)
#currentTime = datetime.now().strftime("%H:%M")
#currentDate = datetime.now().strftime("%d-%m")
image = Image.open("res/black.png").convert("RGB")
image.thumbnail((64, 32), Image.Resampling.LANCZOS)
config = ConfigParser()
config.read('appsettings.ini')


screen_id = 0
screen_max = 3

btn_up = 10
btn_down = 8
btn_right = 32
btn_left = 33

brightness = 100
matrix = None

def on_pushup(channel):
	global screen_id
	if screen_id >= screen_max:
		screen_id = 0
	else:
		screen_id = screen_id + 1

def on_pushdown(channel):
	global screen_id
	if screen_id <= 0:
		screen_id = 3
	else:
		screen_id = screen_id - 1

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



def main():
	global matrix
	matrix = matrix_init(brightness)

	GPIO.cleanup
	GPIO.cleanup
	GPIO.cleanup
	GPIO.cleanup
	GPIO.cleanup
	print('GPIO.cleanup')

	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(btn_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(btn_left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	GPIO.add_event_detect(btn_up, GPIO.RISING, callback=on_pushup, bouncetime=100)
	GPIO.add_event_detect(btn_down, GPIO.RISING, callback=on_pushdown, bouncetime=100)
	GPIO.add_event_detect(btn_right, GPIO.RISING, callback=on_pushright, bouncetime=100)
	GPIO.add_event_detect(btn_left, GPIO.RISING, callback=on_pushleft, bouncetime=100)

	try:

		while True:  # Run forever
			currentTime = datetime.now()


			if screen_id == 0:
				frame = sakura_clock(matrix, currentTime)
			if screen_id == 1:
				frame = fuji_clock(matrix, currentTime)
			if screen_id == 2:
				frame = clock(matrix, currentTime)


			print(screen_id)
			time.sleep(0.1)


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
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((4, 8.5), currentTime.strftime("%H:%M"), textColor, font)
	return frame

def weather_clock(matrix, currentTime):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	font_small = ImageFont.truetype(font='fonts/tiny.otf', size=5)
	weather = get_weather()

	weather_icon = get_weather_icon(weather.weather_icon_name)
	weatherIcon = Image.open(weather_icon).convert("RGB")

	#Temperature Celcius
	celsius = weather.temperature('celsius')
	temperature = str(round(celsius['temp'])) + '°C'
	temperature_max = str(round(celsius['temp_max'])) + '°'
	temperature_min = str(round(celsius['temp_min'])) + '°'
	temperature_min_max = temperature_min + '|' + temperature_max
	print(temperature_min_max)

	image.paste(weatherIcon, (5,10))

	frame = image.copy()
	draw = ImageDraw.Draw(frame)

	draw.text((25, 10), temperature, textColor, font)
	draw.text((25, 22), temperature_min_max, textColor, font_small)

	#draw.text((0, 1), currentDate, textColor, font_small)
	draw.text((25, 1), currentTime.strftime("%H:%M"), textColor, font_small)
	draw.text((52, 1), get_weekday_short(), textColor, font_small)
	draw.line(((0,7), (64,7)), textColor, 1)

	return frame

def get_weather():
	owm = OWM(config.get('Open_weather_map', 'owm_api_key'))
	location = config.get('Open_weather_map', 'location')
	mgr = owm.weather_manager()
	weather = mgr.weather_at_place(location).weather
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
	if icon_name == '01d' or '01n':
		return "res/01d.png"
	if icon_name == '02d' or '02n':
		return "res/02d.png"
	if icon_name == '03d' or '03n':
		return "res/03d.png"
	if icon_name == '04d' or '04n':
		return "res/04d.png"
	if icon_name == '09d' or '09n':
		return "res/09d.png"
	if icon_name == '10d' or '10n':
		return "res/10d.png"
	if icon_name == '13d' or '13n':
		return "res/13d.png"
	if icon_name == '50d' or '50n':
		return "res/50d.png"

# Main function
if __name__== "__main__" :
	main()
