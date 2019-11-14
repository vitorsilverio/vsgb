#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

from vsgb.emulator import Emulator

def main():
    parser = argparse.ArgumentParser(description='VSGB: A simple gameboy emulator', usage='%(prog)s [options] -r rom')
    parser.add_argument('-r', '--rom', metavar='path', nargs='?', help='gameboy rom file path', required=True)
    parser.add_argument('-s', '--skip', help='Skip boot rom', action='store_true')
    parser.add_argument('-c', '--cgb', help='CGB MODE', action='store_true')
    parser.add_argument('-d', '--debug', help='Debug mode', action='store_true')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, filename='vsgb.log', filemode='w', format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    print(args.cgb)
    emulator = Emulator(args.rom, args.cgb)
    if args.skip:
        emulator.skip_boot_rom()
    emulator.run()
  

if __name__ == '__main__':
    main()
