from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from configparser import ConfigParser
from pyowm.owm import OWM
from pyowm.utils import config

#Globals
textColor = (255, 255, 255)
currentTime = datetime.now().strftime("%H:%M")
image = Image.open("res/black.png").convert("RGB")
image.thumbnail((64, 32), Image.Resampling.LANCZOS)

def main():
	config = ConfigParser()
	config.read('appsettings.ini')
	print(config.get('config', 'test'))

	matrix = matrix_init()



	while(True):
		sakura_clock(matrix)

def matrix_init():
	options = RGBMatrixOptions()
	options.rows = 32
	options.cols = 64
	options.chain_length = 1
	options.parallel = 1
	options.hardware_mapping = 'regular'
	options.brightness = 100
	return RGBMatrix(options = options)

def sakura_clock(matrix):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	image = Image.open("res/sakura.png").convert("RGB")
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((1, 1), currentTime, textColor, font)
	matrix.SetImage(frame)

def fuji_clock(matrix):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=10)
	image = Image.open("res/fuji.png").convert("RGB")
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((13, 1), currentTime, textColor, font)
	matrix.SetImage(frame)

def clock(matrix):
	font = ImageFont.truetype(font='fonts/tiny.otf', size=15)
	frame = image.copy()
	draw = ImageDraw.Draw(frame)
	draw.text((4, 8.5), currentTime, textColor, font)
	matrix.SetImage(frame)




# Main function
if __name__== "__main__" :
	main()



