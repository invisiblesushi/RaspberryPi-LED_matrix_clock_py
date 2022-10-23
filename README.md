# RPI-led-matrix-clock-py

# Setup Python 3
```shell
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd /bindings/python/
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

Make sure rgbmatrix folder exist in /usr/local/lib/python3.9/dist-packages/rgbmatrix


```

# Requirement
Pillow or PIL

|LED matrix pin| Pin | Pin |LED matrix pin
|-------------:|:---:|:---:|:-----------
|         -    |   1 |   2 | -
|         -    |   3 |   4 | -
|         -    |   5 |   6 | **GND**
|**strobe**    |   7 |   8 |
|         -    |   9 |  10 |    
|**clock**     |  11 |  12 | **OE-**  
|       **G1** |  13 |  14 | -
|        **A** |  15 |  16 | **B**    
|         -    |  17 |  18 | **C**    
|       **B2** |  19 |  20 | -
|       **G2** |  21 |  22 | **D**    
|       **R1** |  23 |  24 | **R2**
|         -    |  25 |  26 | **B1**
|         -    |  27 |  28 | -
|         -    |  29 |  30 | -
|         -    |  31 |  32 | -
|         -    |  33 |  34 | -
|         -    |  35 |  36 | -
|         -    |  37 |  38 | -
|         -    |  39 |  40 | -
