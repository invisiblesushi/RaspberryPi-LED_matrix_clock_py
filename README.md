# RaspberryPi-LED_matrix_clock_py
<img src="/Image/Sakura_clock.png" width="600" />
<img src="/Image/Weather.png" width="600" />
<img src="/Image/Back2.jpg" width="600" />

# Setup Python 3
```shell
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd /bindings/python/
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

Make sure rgbmatrix folder exist in /usr/local/lib/python3.9/dist-packages/rgbmatrix
```

# Requirement
- PIL
- pyowm
- https://github.com/hzeller/rpi-rgb-led-matrix libary

# Part list
- Raspberry pi zero W
- HCW-P715 Buck Converter
- P3 RGB 64x32 dot panel
- Five Direction Navigation Button Module

# GPIO conncetion
|       LED matrix pin | Pin | Pin |LED matrix pin
|---------------------:|:---:|:---:|:-----------
| btn_com + [resistor] |   1 |   2 | -
|                    - |   3 |   4 | -
|                    - |   5 |   6 | **GND**
|     **strobe/latch** |   7 |   8 |  btn_down [screen - 1]
|                    - |   9 |  10 |  btn_up   [screen + 1]
|            **clock** |  11 |  12 | **OE-**  
|               **G1** |  13 |  14 | -
|                **A** |  15 |  16 | **B**    
|                    - |  17 |  18 | **C**    
|               **B2** |  19 |  20 | -
|               **G2** |  21 |  22 | **D**    
|               **R1** |  23 |  24 | **R2**
|                    - |  25 |  26 | **B1**
|                    - |  27 |  28 | -
|                    - |  29 |  30 | -
|   btn_rst [Shutdown] |  31 |  32 | btn_right  [brightness - 1]
|   btn_left   [brightness + 1] |  33 |  34 | 
|                    - |  35 |  36 | -
|                    - |  37 |  38 | -
|                    - |  39 |  40 | -

# Run
```shell
// Disclamer it has to run as sudo, cause it's reqired by the libary used
sudo python main.py --led-no-hardware-pulse
```

# Autostart on startup
```shell
sudo nano .bashrc

Add line:
sudo /usr/bin/python /home/pi/RPI-led-matrix-clock-py/main.py >> /home/pi/log.txt
```

# Source
- sakura.png https://github.com/allenslab/matrix-dashboard/blob/master/impl/apps_v2/res/main_screen/sakura-bg.png
- tiny.otf https://github.com/allenslab/matrix-dashboard/blob/master/impl/fonts/tiny.otf

# Custom raspberry pi hat
<img src="/Image/PCB.png" width="300" />
<img src="/Image/PCB3.jpg" width="300" />

# Schematics
<img src="/Image/Schematic_Led%20Matrix%20RPI.png" width="600" />
