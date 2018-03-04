#! /usr/bin/env bash

set -euo pipefail
set -x

# Install apt-get packages
sudo apt-get -y install arduino-core avrdude git golang python2.7 python3

# Install arduino-builder and deps
echo 'Installing Go dependencies for arduino-builder'
mkdir -p $GOPATH
go get github.com/go-errors/errors
go get github.com/stretchr/testify
go get github.com/jstemmer/go-junit-report
go get github.com/arduino/go-properties-map
go get github.com/arduino/go-timeutils
go get github.com/arduino/arduino-builder

echo 'Build and install the Go arduino-builder'
go install github.com/arduino/arduino-builder/arduino-builder

# Install an even more recent version of Arduino
arduino_version=arduino-1.8.5
arduino_build=$arduino_version-linuxarm
arduino_tar=$arduino_build.tar.xz
arduino_install_dir=/opt/arduino/

wget https://downloads.arduino.cc/$arduino_tar -P /tmp/
sudo mkdir -p $arduino_install_dir
sudo chmod 775 $arduino_install_dir
sudo chown $USER $arduino_install_dir
(
  cd $arduino_install_dir
  tar xf /tmp/$arduino_tar
  cd $arduino_version
  ln -s $arduino_install_dir/$arduino_version $arduino_install_dir/current
  sudo cp -ru lib /usr/share/arduino
  sudo cp -ru libraries /usr/share/arduino
  sudo cp -ru tools /usr/share/arduino
  sudo cp -ru hardware /usr/share/arduino
  sudo cp -ru examples /usr/share/doc/arduino-core
  sudo cp -ru reference /usr/share/doc/arduino-core
)


# Build the example sketch
arduino_dir=$arduino_install_dir/current/
arduino-builder --hardware $arduino_dir/hardware --tools $arduino_dir/hardware/tools/ --tools $arduino_dir/tools-builder/ -fqbn arduino:avr:nano:cpu=atmega328 --build-path $PWD/build/ --verbose examples/blink.ino
