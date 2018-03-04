# Piduino
The unholy matrimony of a Raspberry Pi and an Arduino

## Raspberry Pi Setup

The following steps must be performed on the Raspberry Pi when it is first
powered on:

Append the following lines to the end of your `~/.bashrc`:

```
export GOPATH=$HOME/Go/
export PATH=$PATH:$GOPATH/bin
```

Then run the setup script:

```
./raspi_setup.sh
```


## Flash the Arduino from Raspberry Pi

### Wiring
Connect the Raspberry Pi GPIO pins to the Arduino ISP, following the instructions here: [https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/configuration#wiring]

### Deploying the code
The deploy.py script will copy all source code to the Raspberry Pi, build the
Arduino code, flash the arduino, and then run the given python `main.py`.

```
pipenv run $PWD/deploy.py --project_dir ~/GitHub/WinterTechForum/pyduino-secret-number/ 192.168.43.167
```


### Manual flashing

The following command may be used to flash the Arduino manually, when SSH'd into
the Raspberry Pi:

```
sudo avrdude -p atmega328p -C ~/avrdude_gpio.conf -c pi_1 -v -U flash:w:Blink.ino.hex:i
```
