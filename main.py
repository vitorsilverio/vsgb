#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

def main():
    parser = argparse.ArgumentParser(description='PyGB: A simple gameboy emulator', usage='%(prog)s [options] -r rom')
    parser.add_argument('-r', '--rom', metavar='path', nargs='?', help='gameboy rom file path', required=True)
    args = parser.parse_args()
    

if __name__ == '__main__':
    main()
