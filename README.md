# Piduino
The unholy matrimony of a Raspberry Pi and an Arduino

## Raspberry Pi Setup

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

SCP the `*.hex` file from your machine to the Raspberry Pi. `Blink.ino.hex` is used in the example below.

Connect the Raspberry Pi GPIO pins to the Arduino ISP, following the instructions here: [https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/configuration#wiring]

```
sudo avrdude -p atmega328p -C ~/avrdude_gpio.conf -c pi_1 -v -U flash:w:Blink.ino.hex:i
```
