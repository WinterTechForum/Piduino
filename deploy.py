#!/usr/bin/env python3

'''
Description - An auto-generated stub description.
'''

import argparse
import logging
import os

from fabric.api import cd
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import sudo

logger = logging.getLogger(__name__)

DEPLOY_DIR = '/opt/Piduino'
ARDUINO_SUBDIR = 'arduino'
RASPI_SUBDIR = 'pi'

ARDUINO_INSTALL_DIR = '/opt/arduino/current/'


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'hostname',
        help='The hostname (or ip address) of the target Raspberry Pi')
    parser.add_argument(
        '--project_dir',
        required=False,
        default=os.getcwd(),
        help='The directory containing the required Python, ' \
             'Arduino, and requirements3.txt files')
    # parser.add_argument('--bar', required=False)

    # If `argv` is None, `parse_args` will default to using `sys.argv`
    return parser.parse_args(args=argv)


def main(argv=None):
    args = parse_args(argv)
    # do some work

    args.project_dir = os.path.abspath(args.project_dir)
    project_name = os.path.basename(args.project_dir)
    logger.info('Deploying project: %s', project_name)

    env.user = 'root'
    env.host_string = '{}:22'.format(args.hostname)

    run('mkdir -p {}'.format(DEPLOY_DIR))
    with cd(DEPLOY_DIR):
        run('rm -rf {}/{} | true'.format(DEPLOY_DIR, project_name))
        put(args.project_dir, DEPLOY_DIR)

    with cd(os.path.join(DEPLOY_DIR, project_name)):
        run('mkdir -p build')
        run('pwd; ~/Go/bin/arduino-builder ' \
                '--hardware {arduino_dir}/hardware '\
                '--tools {arduino_dir}/hardware/tools/ ' \
                '--tools {arduino_dir}/tools-builder/ ' \
                '--libraries {arduino_dir}/libraries/ ' \
                '-fqbn arduino:avr:nano:cpu=atmega328 ' \
                '--build-path $PWD/build/ ' \
                '--verbose arduino/arduino.ino'.format(
                    arduino_dir=ARDUINO_INSTALL_DIR))
        sudo('avrdude ' \
                '-p atmega328p ' \
                '-C ~/GitHub/Piduino/avrdude_gpio.conf ' \
                '-c pi_1 -v -U flash:w:build/arduino.ino.hex:i')
        # sudo('pip install -r py/requirements.txt')
        # sudo('pip3 install -r py/requirements.txt')
        run('chmod +x py/main.py')
        run('./py/main.py')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
