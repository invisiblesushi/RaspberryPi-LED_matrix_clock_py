from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image , ImageDraw, ImageFont
from datetime import datetime
import time
import sys

def main():
        print("Hello, World!")

        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'regular'

        matrix = RGBMatrix(options = options)

        image = Image.open("res/bg.png").convert("RGB")

        image.thumbnail((64, 32), Image.ANTIALIAS)

        #font = graphics.Font()
        #font.LoadFont("fonts/7x13.bdf")

        font = ImageFont.load_default()

        textColor = graphics.Color(255, 255, 255)
        myText = "Hello world"



        white_screen = Image.new("RGB", (options.cols, options.rows), (255,255,255))


        light_pink = (255,219,218)


        while(True):
                currentTime = datetime.now()
                hours = str(currentTime.hour)
                minutes = str(currentTime.minute)
                seconds = str(currentTime.second)

                frame = image.copy()
                draw = ImageDraw.Draw(frame)
                draw.text((0,-2), hours + ":" + minutes + ":" + seconds, light_pink, font)
                matrix.SetImage(frame)
