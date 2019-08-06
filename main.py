#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

from pygb.emulator import Emulator

def main():
    parser = argparse.ArgumentParser(description='PyGB: A simple gameboy emulator', usage='%(prog)s [options] -r rom')
    parser.add_argument('-r', '--rom', metavar='path', nargs='?', help='gameboy rom file path', required=True)
    parser.add_argument('-s', '--skip', help='Skip boot rom', action='store_true')
    parser.add_argument('-d', '--debug', help='Debug mode', action='store_true')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, filename='pygb.log', filemode='w', format='%(levelname)s: %(message)s')
    emulator = Emulator(args.rom)
    if args.skip:
        emulator.skip_boot_rom()
    emulator.run()
  

if __name__ == '__main__':
    main()
