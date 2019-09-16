#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pygb.byte_operations import signed_value, set_bit, bit_mask
from pygb.io_registers import IO_Registers
from pygb.registers import Registers

DAATable = [
    0x0080, 0x0100, 0x0200, 0x0300, 0x0400, 0x0500, 0x0600, 0x0700,
    0x0800, 0x0900, 0x1000, 0x1100, 0x1200, 0x1300, 0x1400, 0x1500,
    0x1000, 0x1100, 0x1200, 0x1300, 0x1400, 0x1500, 0x1600, 0x1700,
    0x1800, 0x1900, 0x2000, 0x2100, 0x2200, 0x2300, 0x2400, 0x2500,
    0x2000, 0x2100, 0x2200, 0x2300, 0x2400, 0x2500, 0x2600, 0x2700,
    0x2800, 0x2900, 0x3000, 0x3100, 0x3200, 0x3300, 0x3400, 0x3500,
    0x3000, 0x3100, 0x3200, 0x3300, 0x3400, 0x3500, 0x3600, 0x3700,
    0x3800, 0x3900, 0x4000, 0x4100, 0x4200, 0x4300, 0x4400, 0x4500,
    0x4000, 0x4100, 0x4200, 0x4300, 0x4400, 0x4500, 0x4600, 0x4700,
    0x4800, 0x4900, 0x5000, 0x5100, 0x5200, 0x5300, 0x5400, 0x5500,
    0x5000, 0x5100, 0x5200, 0x5300, 0x5400, 0x5500, 0x5600, 0x5700,
    0x5800, 0x5900, 0x6000, 0x6100, 0x6200, 0x6300, 0x6400, 0x6500,
    0x6000, 0x6100, 0x6200, 0x6300, 0x6400, 0x6500, 0x6600, 0x6700,
    0x6800, 0x6900, 0x7000, 0x7100, 0x7200, 0x7300, 0x7400, 0x7500,
    0x7000, 0x7100, 0x7200, 0x7300, 0x7400, 0x7500, 0x7600, 0x7700,
    0x7800, 0x7900, 0x8000, 0x8100, 0x8200, 0x8300, 0x8400, 0x8500,
    0x8000, 0x8100, 0x8200, 0x8300, 0x8400, 0x8500, 0x8600, 0x8700,
    0x8800, 0x8900, 0x9000, 0x9100, 0x9200, 0x9300, 0x9400, 0x9500,
    0x9000, 0x9100, 0x9200, 0x9300, 0x9400, 0x9500, 0x9600, 0x9700,
    0x9800, 0x9900, 0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510,
    0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510, 0x0610, 0x0710,
    0x0810, 0x0910, 0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510,
    0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510, 0x1610, 0x1710,
    0x1810, 0x1910, 0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510,
    0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510, 0x2610, 0x2710,
    0x2810, 0x2910, 0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510,
    0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510, 0x3610, 0x3710,
    0x3810, 0x3910, 0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510,
    0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510, 0x4610, 0x4710,
    0x4810, 0x4910, 0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510,
    0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510, 0x5610, 0x5710,
    0x5810, 0x5910, 0x6010, 0x6110, 0x6210, 0x6310, 0x6410, 0x6510,
    0x6010, 0x6110, 0x6210, 0x6310, 0x6410, 0x6510, 0x6610, 0x6710,
    0x6810, 0x6910, 0x7010, 0x7110, 0x7210, 0x7310, 0x7410, 0x7510,
    0x7010, 0x7110, 0x7210, 0x7310, 0x7410, 0x7510, 0x7610, 0x7710,
    0x7810, 0x7910, 0x8010, 0x8110, 0x8210, 0x8310, 0x8410, 0x8510,
    0x8010, 0x8110, 0x8210, 0x8310, 0x8410, 0x8510, 0x8610, 0x8710,
    0x8810, 0x8910, 0x9010, 0x9110, 0x9210, 0x9310, 0x9410, 0x9510,
    0x9010, 0x9110, 0x9210, 0x9310, 0x9410, 0x9510, 0x9610, 0x9710,
    0x9810, 0x9910, 0xA010, 0xA110, 0xA210, 0xA310, 0xA410, 0xA510,
    0xA010, 0xA110, 0xA210, 0xA310, 0xA410, 0xA510, 0xA610, 0xA710,
    0xA810, 0xA910, 0xB010, 0xB110, 0xB210, 0xB310, 0xB410, 0xB510,
    0xB010, 0xB110, 0xB210, 0xB310, 0xB410, 0xB510, 0xB610, 0xB710,
    0xB810, 0xB910, 0xC010, 0xC110, 0xC210, 0xC310, 0xC410, 0xC510,
    0xC010, 0xC110, 0xC210, 0xC310, 0xC410, 0xC510, 0xC610, 0xC710,
    0xC810, 0xC910, 0xD010, 0xD110, 0xD210, 0xD310, 0xD410, 0xD510,
    0xD010, 0xD110, 0xD210, 0xD310, 0xD410, 0xD510, 0xD610, 0xD710,
    0xD810, 0xD910, 0xE010, 0xE110, 0xE210, 0xE310, 0xE410, 0xE510,
    0xE010, 0xE110, 0xE210, 0xE310, 0xE410, 0xE510, 0xE610, 0xE710,
    0xE810, 0xE910, 0xF010, 0xF110, 0xF210, 0xF310, 0xF410, 0xF510,
    0xF010, 0xF110, 0xF210, 0xF310, 0xF410, 0xF510, 0xF610, 0xF710,
    0xF810, 0xF910, 0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510,
    0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510, 0x0610, 0x0710,
    0x0810, 0x0910, 0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510,
    0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510, 0x1610, 0x1710,
    0x1810, 0x1910, 0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510,
    0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510, 0x2610, 0x2710,
    0x2810, 0x2910, 0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510,
    0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510, 0x3610, 0x3710,
    0x3810, 0x3910, 0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510,
    0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510, 0x4610, 0x4710,
    0x4810, 0x4910, 0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510,
    0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510, 0x5610, 0x5710,
    0x5810, 0x5910, 0x6010, 0x6110, 0x6210, 0x6310, 0x6410, 0x6510,
    0x0600, 0x0700, 0x0800, 0x0900, 0x0A00, 0x0B00, 0x0C00, 0x0D00,
    0x0E00, 0x0F00, 0x1000, 0x1100, 0x1200, 0x1300, 0x1400, 0x1500,
    0x1600, 0x1700, 0x1800, 0x1900, 0x1A00, 0x1B00, 0x1C00, 0x1D00,
    0x1E00, 0x1F00, 0x2000, 0x2100, 0x2200, 0x2300, 0x2400, 0x2500,
    0x2600, 0x2700, 0x2800, 0x2900, 0x2A00, 0x2B00, 0x2C00, 0x2D00,
    0x2E00, 0x2F00, 0x3000, 0x3100, 0x3200, 0x3300, 0x3400, 0x3500,
    0x3600, 0x3700, 0x3800, 0x3900, 0x3A00, 0x3B00, 0x3C00, 0x3D00,
    0x3E00, 0x3F00, 0x4000, 0x4100, 0x4200, 0x4300, 0x4400, 0x4500,
    0x4600, 0x4700, 0x4800, 0x4900, 0x4A00, 0x4B00, 0x4C00, 0x4D00,
    0x4E00, 0x4F00, 0x5000, 0x5100, 0x5200, 0x5300, 0x5400, 0x5500,
    0x5600, 0x5700, 0x5800, 0x5900, 0x5A00, 0x5B00, 0x5C00, 0x5D00,
    0x5E00, 0x5F00, 0x6000, 0x6100, 0x6200, 0x6300, 0x6400, 0x6500,
    0x6600, 0x6700, 0x6800, 0x6900, 0x6A00, 0x6B00, 0x6C00, 0x6D00,
    0x6E00, 0x6F00, 0x7000, 0x7100, 0x7200, 0x7300, 0x7400, 0x7500,
    0x7600, 0x7700, 0x7800, 0x7900, 0x7A00, 0x7B00, 0x7C00, 0x7D00,
    0x7E00, 0x7F00, 0x8000, 0x8100, 0x8200, 0x8300, 0x8400, 0x8500,
    0x8600, 0x8700, 0x8800, 0x8900, 0x8A00, 0x8B00, 0x8C00, 0x8D00,
    0x8E00, 0x8F00, 0x9000, 0x9100, 0x9200, 0x9300, 0x9400, 0x9500,
    0x9600, 0x9700, 0x9800, 0x9900, 0x9A00, 0x9B00, 0x9C00, 0x9D00,
    0x9E00, 0x9F00, 0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510,
    0x0610, 0x0710, 0x0810, 0x0910, 0x0A10, 0x0B10, 0x0C10, 0x0D10,
    0x0E10, 0x0F10, 0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510,
    0x1610, 0x1710, 0x1810, 0x1910, 0x1A10, 0x1B10, 0x1C10, 0x1D10,
    0x1E10, 0x1F10, 0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510,
    0x2610, 0x2710, 0x2810, 0x2910, 0x2A10, 0x2B10, 0x2C10, 0x2D10,
    0x2E10, 0x2F10, 0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510,
    0x3610, 0x3710, 0x3810, 0x3910, 0x3A10, 0x3B10, 0x3C10, 0x3D10,
    0x3E10, 0x3F10, 0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510,
    0x4610, 0x4710, 0x4810, 0x4910, 0x4A10, 0x4B10, 0x4C10, 0x4D10,
    0x4E10, 0x4F10, 0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510,
    0x5610, 0x5710, 0x5810, 0x5910, 0x5A10, 0x5B10, 0x5C10, 0x5D10,
    0x5E10, 0x5F10, 0x6010, 0x6110, 0x6210, 0x6310, 0x6410, 0x6510,
    0x6610, 0x6710, 0x6810, 0x6910, 0x6A10, 0x6B10, 0x6C10, 0x6D10,
    0x6E10, 0x6F10, 0x7010, 0x7110, 0x7210, 0x7310, 0x7410, 0x7510,
    0x7610, 0x7710, 0x7810, 0x7910, 0x7A10, 0x7B10, 0x7C10, 0x7D10,
    0x7E10, 0x7F10, 0x8010, 0x8110, 0x8210, 0x8310, 0x8410, 0x8510,
    0x8610, 0x8710, 0x8810, 0x8910, 0x8A10, 0x8B10, 0x8C10, 0x8D10,
    0x8E10, 0x8F10, 0x9010, 0x9110, 0x9210, 0x9310, 0x9410, 0x9510,
    0x9610, 0x9710, 0x9810, 0x9910, 0x9A10, 0x9B10, 0x9C10, 0x9D10,
    0x9E10, 0x9F10, 0xA010, 0xA110, 0xA210, 0xA310, 0xA410, 0xA510,
    0xA610, 0xA710, 0xA810, 0xA910, 0xAA10, 0xAB10, 0xAC10, 0xAD10,
    0xAE10, 0xAF10, 0xB010, 0xB110, 0xB210, 0xB310, 0xB410, 0xB510,
    0xB610, 0xB710, 0xB810, 0xB910, 0xBA10, 0xBB10, 0xBC10, 0xBD10,
    0xBE10, 0xBF10, 0xC010, 0xC110, 0xC210, 0xC310, 0xC410, 0xC510,
    0xC610, 0xC710, 0xC810, 0xC910, 0xCA10, 0xCB10, 0xCC10, 0xCD10,
    0xCE10, 0xCF10, 0xD010, 0xD110, 0xD210, 0xD310, 0xD410, 0xD510,
    0xD610, 0xD710, 0xD810, 0xD910, 0xDA10, 0xDB10, 0xDC10, 0xDD10,
    0xDE10, 0xDF10, 0xE010, 0xE110, 0xE210, 0xE310, 0xE410, 0xE510,
    0xE610, 0xE710, 0xE810, 0xE910, 0xEA10, 0xEB10, 0xEC10, 0xED10,
    0xEE10, 0xEF10, 0xF010, 0xF110, 0xF210, 0xF310, 0xF410, 0xF510,
    0xF610, 0xF710, 0xF810, 0xF910, 0xFA10, 0xFB10, 0xFC10, 0xFD10,
    0xFE10, 0xFF10, 0x0090, 0x0110, 0x0210, 0x0310, 0x0410, 0x0510,
    0x0610, 0x0710, 0x0810, 0x0910, 0x0A10, 0x0B10, 0x0C10, 0x0D10,
    0x0E10, 0x0F10, 0x1010, 0x1110, 0x1210, 0x1310, 0x1410, 0x1510,
    0x1610, 0x1710, 0x1810, 0x1910, 0x1A10, 0x1B10, 0x1C10, 0x1D10,
    0x1E10, 0x1F10, 0x2010, 0x2110, 0x2210, 0x2310, 0x2410, 0x2510,
    0x2610, 0x2710, 0x2810, 0x2910, 0x2A10, 0x2B10, 0x2C10, 0x2D10,
    0x2E10, 0x2F10, 0x3010, 0x3110, 0x3210, 0x3310, 0x3410, 0x3510,
    0x3610, 0x3710, 0x3810, 0x3910, 0x3A10, 0x3B10, 0x3C10, 0x3D10,
    0x3E10, 0x3F10, 0x4010, 0x4110, 0x4210, 0x4310, 0x4410, 0x4510,
    0x4610, 0x4710, 0x4810, 0x4910, 0x4A10, 0x4B10, 0x4C10, 0x4D10,
    0x4E10, 0x4F10, 0x5010, 0x5110, 0x5210, 0x5310, 0x5410, 0x5510,
    0x5610, 0x5710, 0x5810, 0x5910, 0x5A10, 0x5B10, 0x5C10, 0x5D10,
    0x5E10, 0x5F10, 0x6010, 0x6110, 0x6210, 0x6310, 0x6410, 0x6510,
    0x00C0, 0x0140, 0x0240, 0x0340, 0x0440, 0x0540, 0x0640, 0x0740,
    0x0840, 0x0940, 0x0A40, 0x0B40, 0x0C40, 0x0D40, 0x0E40, 0x0F40,
    0x1040, 0x1140, 0x1240, 0x1340, 0x1440, 0x1540, 0x1640, 0x1740,
    0x1840, 0x1940, 0x1A40, 0x1B40, 0x1C40, 0x1D40, 0x1E40, 0x1F40,
    0x2040, 0x2140, 0x2240, 0x2340, 0x2440, 0x2540, 0x2640, 0x2740,
    0x2840, 0x2940, 0x2A40, 0x2B40, 0x2C40, 0x2D40, 0x2E40, 0x2F40,
    0x3040, 0x3140, 0x3240, 0x3340, 0x3440, 0x3540, 0x3640, 0x3740,
    0x3840, 0x3940, 0x3A40, 0x3B40, 0x3C40, 0x3D40, 0x3E40, 0x3F40,
    0x4040, 0x4140, 0x4240, 0x4340, 0x4440, 0x4540, 0x4640, 0x4740,
    0x4840, 0x4940, 0x4A40, 0x4B40, 0x4C40, 0x4D40, 0x4E40, 0x4F40,
    0x5040, 0x5140, 0x5240, 0x5340, 0x5440, 0x5540, 0x5640, 0x5740,
    0x5840, 0x5940, 0x5A40, 0x5B40, 0x5C40, 0x5D40, 0x5E40, 0x5F40,
    0x6040, 0x6140, 0x6240, 0x6340, 0x6440, 0x6540, 0x6640, 0x6740,
    0x6840, 0x6940, 0x6A40, 0x6B40, 0x6C40, 0x6D40, 0x6E40, 0x6F40,
    0x7040, 0x7140, 0x7240, 0x7340, 0x7440, 0x7540, 0x7640, 0x7740,
    0x7840, 0x7940, 0x7A40, 0x7B40, 0x7C40, 0x7D40, 0x7E40, 0x7F40,
    0x8040, 0x8140, 0x8240, 0x8340, 0x8440, 0x8540, 0x8640, 0x8740,
    0x8840, 0x8940, 0x8A40, 0x8B40, 0x8C40, 0x8D40, 0x8E40, 0x8F40,
    0x9040, 0x9140, 0x9240, 0x9340, 0x9440, 0x9540, 0x9640, 0x9740,
    0x9840, 0x9940, 0x9A40, 0x9B40, 0x9C40, 0x9D40, 0x9E40, 0x9F40,
    0xA040, 0xA140, 0xA240, 0xA340, 0xA440, 0xA540, 0xA640, 0xA740,
    0xA840, 0xA940, 0xAA40, 0xAB40, 0xAC40, 0xAD40, 0xAE40, 0xAF40,
    0xB040, 0xB140, 0xB240, 0xB340, 0xB440, 0xB540, 0xB640, 0xB740,
    0xB840, 0xB940, 0xBA40, 0xBB40, 0xBC40, 0xBD40, 0xBE40, 0xBF40,
    0xC040, 0xC140, 0xC240, 0xC340, 0xC440, 0xC540, 0xC640, 0xC740,
    0xC840, 0xC940, 0xCA40, 0xCB40, 0xCC40, 0xCD40, 0xCE40, 0xCF40,
    0xD040, 0xD140, 0xD240, 0xD340, 0xD440, 0xD540, 0xD640, 0xD740,
    0xD840, 0xD940, 0xDA40, 0xDB40, 0xDC40, 0xDD40, 0xDE40, 0xDF40,
    0xE040, 0xE140, 0xE240, 0xE340, 0xE440, 0xE540, 0xE640, 0xE740,
    0xE840, 0xE940, 0xEA40, 0xEB40, 0xEC40, 0xED40, 0xEE40, 0xEF40,
    0xF040, 0xF140, 0xF240, 0xF340, 0xF440, 0xF540, 0xF640, 0xF740,
    0xF840, 0xF940, 0xFA40, 0xFB40, 0xFC40, 0xFD40, 0xFE40, 0xFF40,
    0xA050, 0xA150, 0xA250, 0xA350, 0xA450, 0xA550, 0xA650, 0xA750,
    0xA850, 0xA950, 0xAA50, 0xAB50, 0xAC50, 0xAD50, 0xAE50, 0xAF50,
    0xB050, 0xB150, 0xB250, 0xB350, 0xB450, 0xB550, 0xB650, 0xB750,
    0xB850, 0xB950, 0xBA50, 0xBB50, 0xBC50, 0xBD50, 0xBE50, 0xBF50,
    0xC050, 0xC150, 0xC250, 0xC350, 0xC450, 0xC550, 0xC650, 0xC750,
    0xC850, 0xC950, 0xCA50, 0xCB50, 0xCC50, 0xCD50, 0xCE50, 0xCF50,
    0xD050, 0xD150, 0xD250, 0xD350, 0xD450, 0xD550, 0xD650, 0xD750,
    0xD850, 0xD950, 0xDA50, 0xDB50, 0xDC50, 0xDD50, 0xDE50, 0xDF50,
    0xE050, 0xE150, 0xE250, 0xE350, 0xE450, 0xE550, 0xE650, 0xE750,
    0xE850, 0xE950, 0xEA50, 0xEB50, 0xEC50, 0xED50, 0xEE50, 0xEF50,
    0xF050, 0xF150, 0xF250, 0xF350, 0xF450, 0xF550, 0xF650, 0xF750,
    0xF850, 0xF950, 0xFA50, 0xFB50, 0xFC50, 0xFD50, 0xFE50, 0xFF50,
    0x00D0, 0x0150, 0x0250, 0x0350, 0x0450, 0x0550, 0x0650, 0x0750,
    0x0850, 0x0950, 0x0A50, 0x0B50, 0x0C50, 0x0D50, 0x0E50, 0x0F50,
    0x1050, 0x1150, 0x1250, 0x1350, 0x1450, 0x1550, 0x1650, 0x1750,
    0x1850, 0x1950, 0x1A50, 0x1B50, 0x1C50, 0x1D50, 0x1E50, 0x1F50,
    0x2050, 0x2150, 0x2250, 0x2350, 0x2450, 0x2550, 0x2650, 0x2750,
    0x2850, 0x2950, 0x2A50, 0x2B50, 0x2C50, 0x2D50, 0x2E50, 0x2F50,
    0x3050, 0x3150, 0x3250, 0x3350, 0x3450, 0x3550, 0x3650, 0x3750,
    0x3850, 0x3950, 0x3A50, 0x3B50, 0x3C50, 0x3D50, 0x3E50, 0x3F50,
    0x4050, 0x4150, 0x4250, 0x4350, 0x4450, 0x4550, 0x4650, 0x4750,
    0x4850, 0x4950, 0x4A50, 0x4B50, 0x4C50, 0x4D50, 0x4E50, 0x4F50,
    0x5050, 0x5150, 0x5250, 0x5350, 0x5450, 0x5550, 0x5650, 0x5750,
    0x5850, 0x5950, 0x5A50, 0x5B50, 0x5C50, 0x5D50, 0x5E50, 0x5F50,
    0x6050, 0x6150, 0x6250, 0x6350, 0x6450, 0x6550, 0x6650, 0x6750,
    0x6850, 0x6950, 0x6A50, 0x6B50, 0x6C50, 0x6D50, 0x6E50, 0x6F50,
    0x7050, 0x7150, 0x7250, 0x7350, 0x7450, 0x7550, 0x7650, 0x7750,
    0x7850, 0x7950, 0x7A50, 0x7B50, 0x7C50, 0x7D50, 0x7E50, 0x7F50,
    0x8050, 0x8150, 0x8250, 0x8350, 0x8450, 0x8550, 0x8650, 0x8750,
    0x8850, 0x8950, 0x8A50, 0x8B50, 0x8C50, 0x8D50, 0x8E50, 0x8F50,
    0x9050, 0x9150, 0x9250, 0x9350, 0x9450, 0x9550, 0x9650, 0x9750,
    0x9850, 0x9950, 0x9A50, 0x9B50, 0x9C50, 0x9D50, 0x9E50, 0x9F50,
    0xFA40, 0xFB40, 0xFC40, 0xFD40, 0xFE40, 0xFF40, 0x00C0, 0x0140,
    0x0240, 0x0340, 0x0440, 0x0540, 0x0640, 0x0740, 0x0840, 0x0940,
    0x0A40, 0x0B40, 0x0C40, 0x0D40, 0x0E40, 0x0F40, 0x1040, 0x1140,
    0x1240, 0x1340, 0x1440, 0x1540, 0x1640, 0x1740, 0x1840, 0x1940,
    0x1A40, 0x1B40, 0x1C40, 0x1D40, 0x1E40, 0x1F40, 0x2040, 0x2140,
    0x2240, 0x2340, 0x2440, 0x2540, 0x2640, 0x2740, 0x2840, 0x2940,
    0x2A40, 0x2B40, 0x2C40, 0x2D40, 0x2E40, 0x2F40, 0x3040, 0x3140,
    0x3240, 0x3340, 0x3440, 0x3540, 0x3640, 0x3740, 0x3840, 0x3940,
    0x3A40, 0x3B40, 0x3C40, 0x3D40, 0x3E40, 0x3F40, 0x4040, 0x4140,
    0x4240, 0x4340, 0x4440, 0x4540, 0x4640, 0x4740, 0x4840, 0x4940,
    0x4A40, 0x4B40, 0x4C40, 0x4D40, 0x4E40, 0x4F40, 0x5040, 0x5140,
    0x5240, 0x5340, 0x5440, 0x5540, 0x5640, 0x5740, 0x5840, 0x5940,
    0x5A40, 0x5B40, 0x5C40, 0x5D40, 0x5E40, 0x5F40, 0x6040, 0x6140,
    0x6240, 0x6340, 0x6440, 0x6540, 0x6640, 0x6740, 0x6840, 0x6940,
    0x6A40, 0x6B40, 0x6C40, 0x6D40, 0x6E40, 0x6F40, 0x7040, 0x7140,
    0x7240, 0x7340, 0x7440, 0x7540, 0x7640, 0x7740, 0x7840, 0x7940,
    0x7A40, 0x7B40, 0x7C40, 0x7D40, 0x7E40, 0x7F40, 0x8040, 0x8140,
    0x8240, 0x8340, 0x8440, 0x8540, 0x8640, 0x8740, 0x8840, 0x8940,
    0x8A40, 0x8B40, 0x8C40, 0x8D40, 0x8E40, 0x8F40, 0x9040, 0x9140,
    0x9240, 0x9340, 0x9440, 0x9540, 0x9640, 0x9740, 0x9840, 0x9940,
    0x9A40, 0x9B40, 0x9C40, 0x9D40, 0x9E40, 0x9F40, 0xA040, 0xA140,
    0xA240, 0xA340, 0xA440, 0xA540, 0xA640, 0xA740, 0xA840, 0xA940,
    0xAA40, 0xAB40, 0xAC40, 0xAD40, 0xAE40, 0xAF40, 0xB040, 0xB140,
    0xB240, 0xB340, 0xB440, 0xB540, 0xB640, 0xB740, 0xB840, 0xB940,
    0xBA40, 0xBB40, 0xBC40, 0xBD40, 0xBE40, 0xBF40, 0xC040, 0xC140,
    0xC240, 0xC340, 0xC440, 0xC540, 0xC640, 0xC740, 0xC840, 0xC940,
    0xCA40, 0xCB40, 0xCC40, 0xCD40, 0xCE40, 0xCF40, 0xD040, 0xD140,
    0xD240, 0xD340, 0xD440, 0xD540, 0xD640, 0xD740, 0xD840, 0xD940,
    0xDA40, 0xDB40, 0xDC40, 0xDD40, 0xDE40, 0xDF40, 0xE040, 0xE140,
    0xE240, 0xE340, 0xE440, 0xE540, 0xE640, 0xE740, 0xE840, 0xE940,
    0xEA40, 0xEB40, 0xEC40, 0xED40, 0xEE40, 0xEF40, 0xF040, 0xF140,
    0xF240, 0xF340, 0xF440, 0xF540, 0xF640, 0xF740, 0xF840, 0xF940,
    0x9A50, 0x9B50, 0x9C50, 0x9D50, 0x9E50, 0x9F50, 0xA050, 0xA150,
    0xA250, 0xA350, 0xA450, 0xA550, 0xA650, 0xA750, 0xA850, 0xA950,
    0xAA50, 0xAB50, 0xAC50, 0xAD50, 0xAE50, 0xAF50, 0xB050, 0xB150,
    0xB250, 0xB350, 0xB450, 0xB550, 0xB650, 0xB750, 0xB850, 0xB950,
    0xBA50, 0xBB50, 0xBC50, 0xBD50, 0xBE50, 0xBF50, 0xC050, 0xC150,
    0xC250, 0xC350, 0xC450, 0xC550, 0xC650, 0xC750, 0xC850, 0xC950,
    0xCA50, 0xCB50, 0xCC50, 0xCD50, 0xCE50, 0xCF50, 0xD050, 0xD150,
    0xD250, 0xD350, 0xD450, 0xD550, 0xD650, 0xD750, 0xD850, 0xD950,
    0xDA50, 0xDB50, 0xDC50, 0xDD50, 0xDE50, 0xDF50, 0xE050, 0xE150,
    0xE250, 0xE350, 0xE450, 0xE550, 0xE650, 0xE750, 0xE850, 0xE950,
    0xEA50, 0xEB50, 0xEC50, 0xED50, 0xEE50, 0xEF50, 0xF050, 0xF150,
    0xF250, 0xF350, 0xF450, 0xF550, 0xF650, 0xF750, 0xF850, 0xF950,
    0xFA50, 0xFB50, 0xFC50, 0xFD50, 0xFE50, 0xFF50, 0x00D0, 0x0150,
    0x0250, 0x0350, 0x0450, 0x0550, 0x0650, 0x0750, 0x0850, 0x0950,
    0x0A50, 0x0B50, 0x0C50, 0x0D50, 0x0E50, 0x0F50, 0x1050, 0x1150,
    0x1250, 0x1350, 0x1450, 0x1550, 0x1650, 0x1750, 0x1850, 0x1950,
    0x1A50, 0x1B50, 0x1C50, 0x1D50, 0x1E50, 0x1F50, 0x2050, 0x2150,
    0x2250, 0x2350, 0x2450, 0x2550, 0x2650, 0x2750, 0x2850, 0x2950,
    0x2A50, 0x2B50, 0x2C50, 0x2D50, 0x2E50, 0x2F50, 0x3050, 0x3150,
    0x3250, 0x3350, 0x3450, 0x3550, 0x3650, 0x3750, 0x3850, 0x3950,
    0x3A50, 0x3B50, 0x3C50, 0x3D50, 0x3E50, 0x3F50, 0x4050, 0x4150,
    0x4250, 0x4350, 0x4450, 0x4550, 0x4650, 0x4750, 0x4850, 0x4950,
    0x4A50, 0x4B50, 0x4C50, 0x4D50, 0x4E50, 0x4F50, 0x5050, 0x5150,
    0x5250, 0x5350, 0x5450, 0x5550, 0x5650, 0x5750, 0x5850, 0x5950,
    0x5A50, 0x5B50, 0x5C50, 0x5D50, 0x5E50, 0x5F50, 0x6050, 0x6150,
    0x6250, 0x6350, 0x6450, 0x6550, 0x6650, 0x6750, 0x6850, 0x6950,
    0x6A50, 0x6B50, 0x6C50, 0x6D50, 0x6E50, 0x6F50, 0x7050, 0x7150,
    0x7250, 0x7350, 0x7450, 0x7550, 0x7650, 0x7750, 0x7850, 0x7950,
    0x7A50, 0x7B50, 0x7C50, 0x7D50, 0x7E50, 0x7F50, 0x8050, 0x8150,
    0x8250, 0x8350, 0x8450, 0x8550, 0x8650, 0x8750, 0x8850, 0x8950,
    0x8A50, 0x8B50, 0x8C50, 0x8D50, 0x8E50, 0x8F50, 0x9050, 0x9150,
    0x9250, 0x9350, 0x9450, 0x9550, 0x9650, 0x9750, 0x9850, 0x9950,
]

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = cpu.mmu
        self.registers = cpu.registers
        self.stackManager = cpu.stackManager

    def perform_instruction(self, opcode: int) -> int:
        try:
            instruction = getattr(self, 'inst' + hex(opcode))
            return instruction()
        except AttributeError:
            return self.unimplemented(opcode)

    
    def inst0x0(self) -> int:
        self.debug('{}: NOP'.format(hex(self.registers.pc -1)))
        return 4
    
    def inst0x1(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_bc(word) 
        self.debug('{}: LD BC, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def inst0x2(self) -> int:
        self.mmu.write_byte(self.registers.get_bc(), self.registers.a)
        self.debug('{}: LD (BC), A'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x3(self) -> int:
        self.registers.set_bc((self.registers.get_bc() + 1) & 0xffff )
        self.debug('{}: INC BC'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x4(self) -> int:
        self.registers.b = self.inc_byte(self.registers.b)
        self.debug('{}: INC B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x5(self) -> int:
        self.registers.b = self.dec_byte(self.registers.b)
        self.debug('{}: DEC B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.b = byte 
        self.debug('{}: LD B, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0x7(self) -> int:
        self.registers.a = self.rlc(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: RLCA'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_word(word, self.registers.sp)
        self.debug('{}: LD ({}), SP'.format(hex(self.registers.pc-3), hex(word)))
        return 20

    def inst0x9(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_bc()))
        self.debug('{}: ADD HL, BC'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0xa(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_bc())
        self.debug('{}: LD A, (BC)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xb(self) -> int:
        self.registers.set_bc((self.registers.get_bc() - 1) & 0xffff )
        self.debug('{}: DEC BC'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xc(self) -> int:
        self.registers.c = self.inc_byte(self.registers.c)
        self.debug('{}: INC C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xd(self) -> int:
        self.registers.c = self.dec_byte(self.registers.c)
        self.debug('{}: DEC C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0xe(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.c = byte 
        self.debug('{}: LD C, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xf(self) -> int:
        self.registers.a = self.rrc(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        self.debug('{}: RRCA'.format(hex(self.registers.pc-1)))
        return 4  

    def inst0x10(self) -> int:
        self.cpu.stop = True
        self.registers.pc += 1
        self.debug('{}: STOP 0'.format(hex(self.registers.pc-2)))
        return 4       
    
    def inst0x11(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_de(word) 
        self.debug('{}: LD DE, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def inst0x12(self) -> int:
        self.mmu.write_byte(self.registers.get_de(), self.registers.a)
        self.debug('{}: LD (DE), A'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x13(self) -> int:
        self.registers.set_de((self.registers.get_de() + 1) & 0xffff )
        self.debug('{}: INC DE'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x14(self) -> int:
        self.registers.d = self.inc_byte(self.registers.d)
        self.debug('{}: INC D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x15(self) -> int:
        self.registers.d = self.dec_byte(self.registers.d)
        self.debug('{}: DEC D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x16(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.d = byte 
        self.debug('{}: LD D, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0x17(self) -> int:
        self.registers.a = self.rl(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: RLA'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x18(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR {}'.format(hex(self.registers.pc-2), hex(byte)))
        self.registers.pc += signed_value(byte)
        return 12

    def inst0x19(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_de()))
        self.debug('{}: ADD HL, DE'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x1a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_de())
        self.debug('{}: LD A, (DE)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x1b(self) -> int:
        self.registers.set_de((self.registers.get_de() - 1) & 0xffff )
        self.debug('{}: DEC DE'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x1c(self) -> int:
        self.registers.e = self.inc_byte(self.registers.e)
        self.debug('{}: INC E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x1d(self) -> int:
        self.registers.e = self.dec_byte(self.registers.e)
        self.debug('{}: DEC E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x1e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.e = byte 
        self.debug('{}: LD E, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0x1f(self) -> int:
        self.registers.a = self.rr(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        self.debug('{}: RRA'.format(hex(self.registers.pc-1)))
        return 4  

    def inst0x20(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR NZ, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if not self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8
    
    def inst0x21(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_hl(word) 
        self.debug('{}: LD HL, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def inst0x22(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()+1)
        self.debug('{}: LD (HL+), A'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x23(self) -> int:
        self.registers.set_hl((self.registers.get_hl() + 1) & 0xffff )
        self.debug('{}: INC HL'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x24(self) -> int:
        self.registers.h = self.inc_byte(self.registers.h)
        self.debug('{}: INC H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x25(self) -> int:
        self.registers.h = self.dec_byte(self.registers.h)
        self.debug('{}: DEC H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x26(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.h = byte 
        self.debug('{}: LD H, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0x27(self) -> int:
        #From visualboyadvance-m
        #tempRegister.W = AF.B.B1;
        #tempRegister.W |= (AF.B.B0 & (GB_C_FLAG | GB_H_FLAG | GB_N_FLAG)) << 4;
        #AF.W = DAATable[tempRegister.W];
        temp = self.registers.f
        temp |= (self.registers.a & (Registers.C_FLAG | Registers.H_FLAG | Registers.N_FLAG)) << 4
        self.registers.set_af(DAATable[temp & 0xffff])
        self.debug('{}: DAA'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x28(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR Z, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8

    def inst0x29(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_hl()))
        self.debug('{}: ADD HL, HL'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x2a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()+1)
        self.debug('{}: LD A, (HL+)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x2b(self) -> int:
        self.registers.set_hl((self.registers.get_hl() - 1) & 0xffff )
        self.debug('{}: DEC HL'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x2c(self) -> int:
        self.registers.l = self.inc_byte(self.registers.l)
        self.debug('{}: INC L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x2d(self) -> int:
        self.registers.l = self.dec_byte(self.registers.l)
        self.debug('{}: DEC L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x2e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.l = byte 
        self.debug('{}: LD L, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0x2f(self) -> int:
        self.registers.a = self.registers.a ^ 0xff
        self.registers.set_n_flag()
        self.registers.set_h_flag()
        self.debug('{}: CPL'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x30(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR NC, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if not self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8
    
    def inst0x31(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.sp = word
        self.debug('{}: LD SP, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def inst0x32(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()-1)
        self.debug('{}: LD (HL-), A'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x33(self) -> int:
        self.registers.sp = ((self.registers.sp + 1) & 0xffff )
        self.debug('{}: INC SP'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x34(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.inc_byte(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: INC C'.format(hex(self.registers.pc-1)))
        return 12

    def inst0x35(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.dec_byte(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: DEC (HL)'.format(hex(self.registers.pc-1)))
        return 12
    
    def inst0x36(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte(self.registers.get_hl(),byte)
        self.debug('{}: LD (HL), {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 12

    def inst0x37(self) -> int:
        self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: SCF'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x38(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR C, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8

    def inst0x39(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.sp))
        self.debug('{}: ADD HL, SP'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x3a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()-1)
        self.debug('{}: LD A, (HL-)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x3b(self) -> int:
        self.registers.sp = ((self.registers.sp - 1) & 0xffff )
        self.debug('{}: DEC SP'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x3c(self) -> int:
        self.registers.a = self.inc_byte(self.registers.a)
        self.debug('{}: INC A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x3d(self) -> int:
        self.registers.a = self.dec_byte(self.registers.a)
        self.debug('{}: DEC A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x3e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = byte
        self.debug('{}: LD A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8

    def inst0x3f(self) -> int:
        if self.registers.is_c_flag():
            self.registers.reset_c_flag()
        else:
            self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: CCF'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x40(self) -> int:
        self.debug('{}: LD B, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x41(self) -> int:
        self.registers.b = self.registers.c
        self.debug('{}: LD B, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x42(self) -> int:
        self.registers.b = self.registers.d
        self.debug('{}: LD B, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x43(self) -> int:
        self.registers.b = self.registers.e
        self.debug('{}: LD B, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x44(self) -> int:
        self.registers.b = self.registers.h
        self.debug('{}: LD B, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x45(self) -> int:
        self.registers.b = self.registers.l
        self.debug('{}: LD B, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x46(self) -> int:
        self.registers.b = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD B, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x47(self) -> int:
        self.registers.b = self.registers.a
        self.debug('{}: LD B, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x48(self) -> int:
        self.registers.c = self.registers.b
        self.debug('{}: LD C, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x49(self) -> int:
        self.debug('{}: LD C, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x4a(self) -> int:
        self.registers.c = self.registers.d
        self.debug('{}: LD C, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x4b(self) -> int:
        self.registers.c = self.registers.e
        self.debug('{}: LD C, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x4c(self) -> int:
        self.registers.c = self.registers.h
        self.debug('{}: LD C, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x4d(self) -> int:
        self.registers.c = self.registers.l
        self.debug('{}: LD C, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x4e(self) -> int:
        self.registers.c = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD C, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x4f(self) -> int:
        self.registers.c = self.registers.a
        self.debug('{}: LD C, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x50(self) -> int:
        self.registers.d = self.registers.b
        self.debug('{}: LD D, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x51(self) -> int:
        self.registers.d = self.registers.c
        self.debug('{}: LD D, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x52(self) -> int:
        self.debug('{}: LD D, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x53(self) -> int:
        self.registers.d = self.registers.e
        self.debug('{}: LD D, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x54(self) -> int:
        self.registers.d = self.registers.h
        self.debug('{}: LD D, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x55(self) -> int:
        self.registers.d = self.registers.l
        self.debug('{}: LD D, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x56(self) -> int:
        self.registers.d = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD D, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x57(self) -> int:
        self.registers.d = self.registers.a
        self.debug('{}: LD D, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x58(self) -> int:
        self.registers.e = self.registers.b
        self.debug('{}: LD E, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x59(self) -> int:
        self.registers.e = self.registers.c
        self.debug('{}: LD E, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x5a(self) -> int:
        self.registers.e = self.registers.d
        self.debug('{}: LD E, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x5b(self) -> int:
        self.debug('{}: LD E, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x5c(self) -> int:
        self.registers.e = self.registers.h
        self.debug('{}: LD E, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x5d(self) -> int:
        self.registers.e = self.registers.l
        self.debug('{}: LD E, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x5e(self) -> int:
        self.registers.e = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD E, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x5f(self) -> int:
        self.registers.e = self.registers.a
        self.debug('{}: LD E, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x60(self) -> int:
        self.registers.h = self.registers.b
        self.debug('{}: LD H, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x61(self) -> int:
        self.registers.h = self.registers.c
        self.debug('{}: LD H, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x62(self) -> int:
        self.registers.h = self.registers.d
        self.debug('{}: LD H, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x63(self) -> int:
        self.registers.h = self.registers.e
        self.debug('{}: LD H, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x64(self) -> int:
        self.debug('{}: LD H, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x65(self) -> int:
        self.registers.h = self.registers.l
        self.debug('{}: LD H, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x66(self) -> int:
        self.registers.h = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD H, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x67(self) -> int:
        self.registers.h = self.registers.a
        self.debug('{}: LD H, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x68(self) -> int:
        self.registers.l = self.registers.b
        self.debug('{}: LD L, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x69(self) -> int:
        self.registers.l = self.registers.c
        self.debug('{}: LD L, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6a(self) -> int:
        self.registers.l = self.registers.d
        self.debug('{}: LD L, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6b(self) -> int:
        self.registers.l = self.registers.e
        self.debug('{}: LD L, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6c(self) -> int:
        self.registers.l = self.registers.h
        self.debug('{}: LD L, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6d(self) -> int:
        self.debug('{}: LD L, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x6e(self) -> int:
        self.registers.l = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD L, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x6f(self) -> int:
        self.registers.l = self.registers.a
        self.debug('{}: LD L, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x70(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.b)
        self.debug('{}: LD (HL), B'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x71(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.c)
        self.debug('{}: LD (HL), C'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x72(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.d)
        self.debug('{}: LD (HL), D'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x73(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.e)
        self.debug('{}: LD (HL), E'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x74(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.h)
        self.debug('{}: LD (HL), H'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x75(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.l)
        self.debug('{}: LD (HL), L'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x76(self) -> int:
        self.cpu.pre_halt_interrupt = self.mmu.read_byte(IO_Registers.IF)
        self.cpu.halted = True
        self.debug('{}: HALT'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x77(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.debug('{}: LD (HL), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x78(self) -> int:
        self.registers.a = self.registers.b
        self.debug('{}: LD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x79(self) -> int:
        self.registers.a = self.registers.c
        self.debug('{}: LD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x7a(self) -> int:
        self.registers.a = self.registers.d
        self.debug('{}: LD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x7b(self) -> int:
        self.registers.a = self.registers.e
        self.debug('{}: LD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x7c(self) -> int:
        self.registers.a = self.registers.h
        self.debug('{}: LD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x7d(self) -> int:
        self.registers.a = self.registers.l
        self.debug('{}: LD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x7e(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x7f(self) -> int:
        self.debug('{}: LD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x80(self) -> int:
        self.add_byte(self.registers.b)
        self.debug('{}: ADD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x81(self) -> int:
        self.add_byte(self.registers.c)
        self.debug('{}: ADD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x82(self) -> int:
        self.add_byte(self.registers.d)
        self.debug('{}: ADD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x83(self) -> int:
        self.add_byte(self.registers.e)
        self.debug('{}: ADD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x84(self) -> int:
        self.add_byte(self.registers.h)
        self.debug('{}: ADD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x85(self) -> int:
        self.add_byte(self.registers.l)
        self.debug('{}: ADD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x86(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.add_byte(byte)
        self.debug('{}: ADD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x87(self) -> int:
        self.add_byte(self.registers.a)
        self.debug('{}: ADD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x88(self) -> int:
        self.adc(self.registers.b)
        self.debug('{}: ADC A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x89(self) -> int:
        self.adc(self.registers.c)
        self.debug('{}: ADC A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8a(self) -> int:
        self.adc(self.registers.d)
        self.debug('{}: ADC A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8b(self) -> int:
        self.adc(self.registers.e)
        self.debug('{}: ADC A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8c(self) -> int:
        self.adc(self.registers.h)
        self.debug('{}: ADC A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8d(self) -> int:
        self.adc(self.registers.l)
        self.debug('{}: ADC A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0x8e(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.adc(byte)
        self.debug('{}: ADC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0x8f(self) -> int:
        self.adc(self.registers.a)
        self.debug('{}: ADC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x90(self) -> int:
        self.sub(self.registers.b)
        self.debug('{}: SUB A, B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x91(self) -> int:
        self.sub(self.registers.c)
        self.debug('{}: SUB A, C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x92(self) -> int:
        self.sub(self.registers.d)
        self.debug('{}: SUB A, D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x93(self) -> int:
        self.sub(self.registers.e)
        self.debug('{}: SUB A, E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x94(self) -> int:
        self.sub(self.registers.h)
        self.debug('{}: SUB A, H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x95(self) -> int:
        self.sub(self.registers.l)
        self.debug('{}: SUB A, L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x96(self) -> int:
        self.sub(self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: SUB A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x97(self) -> int:
        self.sub(self.registers.a)
        self.debug('{}: SUB A, A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x98(self) -> int:
        self.sbc(self.registers.b)
        self.debug('{}: SBC A, B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x99(self) -> int:
        self.sbc(self.registers.c)
        self.debug('{}: SBC A, C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x9a(self) -> int:
        self.sbc(self.registers.d)
        self.debug('{}: SBC A, D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x9b(self) -> int:
        self.sbc(self.registers.e)
        self.debug('{}: SBC A, E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x9c(self) -> int:
        self.sbc(self.registers.h)
        self.debug('{}: SBC A, H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x9d(self) -> int:
        self.sbc(self.registers.l)
        self.debug('{}: SBC A, L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0x9e(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.sbc(byte)
        self.debug('{}: SBC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0x9f(self) -> int:
        self.sbc(self.registers.a)
        self.debug('{}: SBC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa0(self) -> int:
        self._and(self.registers.b)
        self.debug('{}: AND B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa1(self) -> int:
        self._and(self.registers.c)
        self.debug('{}: AND C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa2(self) -> int:
        self._and(self.registers.d)
        self.debug('{}: AND D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa3(self) -> int:
        self._and(self.registers.e)
        self.debug('{}: AND E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa4(self) -> int:
        self._and(self.registers.h)
        self.debug('{}: AND H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa5(self) -> int:
        self._and(self.registers.l)
        self.debug('{}: AND L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa6(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._and(byte)
        self.debug('{}: AND (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xa7(self) -> int:
        self._and(self.registers.a)
        self.debug('{}: AND A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa8(self) -> int:
        self.xor(self.registers.b)
        self.debug('{}: XOR B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xa9(self) -> int:
        self.xor(self.registers.c)
        self.debug('{}: XOR C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xaa(self) -> int:
        self.xor(self.registers.d)
        self.debug('{}: XOR D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xab(self) -> int:
        self.xor(self.registers.e)
        self.debug('{}: XOR E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xac(self) -> int:
        self.xor(self.registers.h)
        self.debug('{}: XOR H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xad(self) -> int:
        self.xor(self.registers.l)
        self.debug('{}: XOR L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xae(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.xor(byte)
        self.debug('{}: XOR (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xaf(self) -> int:
        self.xor(self.registers.a)
        self.debug('{}: XOR A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb0(self) -> int:
        self._or(self.registers.b)
        self.debug('{}: OR B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb1(self) -> int:
        self._or(self.registers.c)
        self.debug('{}: OR C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb2(self) -> int:
        self._or(self.registers.d)
        self.debug('{}: OR D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb3(self) -> int:
        self._or(self.registers.e)
        self.debug('{}: OR E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb4(self) -> int:
        self._or(self.registers.h)
        self.debug('{}: OR H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb5(self) -> int:
        self._or(self.registers.l)
        self.debug('{}: OR L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb6(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._or(byte)
        self.debug('{}: OR (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xb7(self) -> int:
        self._or(self.registers.a)
        self.debug('{}: OR A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb8(self) -> int:
        self.cp(self.registers.b)
        self.debug('{}: CP B'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xb9(self) -> int:
        self.cp(self.registers.c)
        self.debug('{}: CP C'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xba(self) -> int:
        self.cp(self.registers.d)
        self.debug('{}: CP D'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xbb(self) -> int:
        self.cp(self.registers.e)
        self.debug('{}: CP E'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xbc(self) -> int:
        self.cp(self.registers.h)
        self.debug('{}: CP H'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xbd(self) -> int:
        self.cp(self.registers.l)
        self.debug('{}: CP L'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xbe(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.cp(byte)
        self.debug('{}: CP (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xbf(self) -> int:
        self.cp(self.registers.a)
        self.debug('{}: CP A'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xc0(self) -> int:
        self.debug('{}: RET NZ'.format(hex(self.registers.pc-1)))
        if not self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def inst0xc1(self) -> int:
        self.registers.set_bc(self.stackManager.pop_word())
        self.debug('{}: POP BC'.format(hex(self.registers.pc-1)))
        return 12

    def inst0xc2(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP NZ, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def inst0xc3(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc = word
        self.debug('{}: JP {}'.format(hex(self.registers.pc-3), hex(word)))
        return 16

    def inst0xc4(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL NZ, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12
    
    def inst0xc5(self) -> int:
        self.stackManager.push_word(self.registers.get_bc())
        self.debug('{}: PUSH BC'.format(hex(self.registers.pc-1)))
        return 16
    
    def inst0xc6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.add_byte(byte)
        self.debug('{}: ADD A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xc7(self) -> int:
        self.debug('{}: RST 0x00'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x00
        return 16

    def inst0xc8(self) -> int:
        self.debug('{}: RET Z'.format(hex(self.registers.pc-1)))
        if self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def inst0xc9(self) -> int:
        self.debug('{}: RET'.format(hex(self.registers.pc-1)))
        self.registers.pc = self.stackManager.pop_word()
        return 16

    def inst0xca(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP Z, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def inst0xcc(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL Z, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12

    def inst0xcd(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL {}'.format(hex(self.registers.pc-3), hex(word)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = word
        return 12
    
    def inst0xce(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.adc(byte)
        self.debug('{}: ADC A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xcf(self) -> int:
        self.debug('{}: RST 0x08'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x08
        return 16

    def inst0xd0(self) -> int:
        self.debug('{}: RET NC'.format(hex(self.registers.pc-1)))
        if not self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def inst0xd1(self) -> int:
        self.registers.set_de(self.stackManager.pop_word())
        self.debug('{}: POP DE'.format(hex(self.registers.pc-1)))
        return 12

    def inst0xd2(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP NC, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def inst0xd4(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL NC, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12
    
    def inst0xd5(self) -> int:
        self.stackManager.push_word(self.registers.get_de())
        self.debug('{}: PUSH DE'.format(hex(self.registers.pc-1)))
        return 16

    def inst0xd6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sub(byte)
        self.debug('{}: SUB A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8

    def inst0xd7(self) -> int:
        self.debug('{}: RST 0x10'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x10
        return 16

    def inst0xd8(self) -> int:
        self.debug('{}: RET C'.format(hex(self.registers.pc-1)))
        if self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def inst0xd9(self) -> int:
        self.debug('{}: RETI'.format(hex(self.registers.pc-1)))
        self.registers.pc = self.stackManager.pop_word()
        self.cpu.ime = True
        return 16

    def inst0xda(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP C, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def inst0xdc(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL C, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12

    def inst0xde(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sbc(byte)
        self.debug('{}: SBC A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xdf(self) -> int:
        self.debug('{}: RST 0x18'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x18
        return 16

    def inst0xe0(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte((byte + 0xff00), self.registers.a)
        self.debug('{}: LDH ({}), A'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def inst0xe1(self) -> int:
        self.registers.set_hl(self.stackManager.pop_word())
        self.debug('{}: POP HL'.format(hex(self.registers.pc-1)))
        return 12

    def inst0xe2(self) -> int:
        self.mmu.write_byte((self.registers.c + 0xff00), self.registers.a)
        self.debug('{}: LD (0xff00+C), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0xe5(self) -> int:
        self.stackManager.push_word(self.registers.get_hl())
        self.debug('{}: PUSH HL'.format(hex(self.registers.pc-1)))
        return 16

    def inst0xe6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._and(byte)
        self.debug('{}: AND {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xe7(self) -> int:
        self.debug('{}: RST 0x20'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x20
        return 16

    def inst0xe8(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        if self.registers.sp ^ byte ^ ((self.registers.sp + signed_value(byte)) & 0xffff) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else:
            self.registers.reset_c_flag()
        if self.registers.sp ^ byte ^ ((self.registers.sp + signed_value(byte)) & 0xffff) & 0x10 == 0x10:
            self.registers.set_h_flag()
        else:
            self.registers.reset_h_flag()
        self.registers.sp += signed_value(byte)
        self.debug('{}: ADD SP, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 16

    def inst0xe9(self) -> int:
        self.debug('{}: JP HL'.format(hex(self.registers.pc-1)))
        word = self.registers.get_hl()
        self.registers.pc = word
        return 4
    
    def inst0xea(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_byte(word, self.registers.a)
        self.debug('{}: LD ({}), A'.format(hex(self.registers.pc-3),hex(word)))
        return 16

    def inst0xee(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.xor(byte)
        self.debug('{}: XOR {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xef(self) -> int:
        self.debug('{}: RST 0x28'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x28
        return 16
    
    def inst0xf0(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = self.mmu.read_byte((byte + 0xff00))
        self.debug('{}: LDH A, ({})'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def inst0xf1(self) -> int:
        self.registers.set_af(self.stackManager.pop_word())
        self.debug('{}: POP AF'.format(hex(self.registers.pc-1)))
        return 12
    
    def inst0xf2(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.c + 0xff00)
        self.debug('{}: LD A, (0xff00+C)'.format(hex(self.registers.pc-1)))
        return 8

    def inst0xf3(self) -> int:
        self.cpu.ime = False
        self.debug('{}: DI'.format(hex(self.registers.pc-1)))
        return 4
    
    def inst0xf5(self) -> int:
        self.stackManager.push_word(self.registers.get_af())
        self.debug('{}: PUSH AF'.format(hex(self.registers.pc-1)))
        return 16

    def inst0xf6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._or(byte)
        self.debug('{}: OR {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xf7(self) -> int:
        self.debug('{}: RST 0x30'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x30
        return 16
    
    def inst0xf8(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        hl = self.registers.sp + signed_value(byte)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x10 == 0x10:
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.set_hl(hl)
        self.debug('{}: LDHL SP, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 12
    
    def inst0xf9(self) -> int:
        self.registers.sp = self.registers.get_hl()
        self.debug('{}: LD SP, HL'.format(hex(self.registers.pc-1)))
        return 8
    
    def inst0xfa(self) -> int:
        byte = self.mmu.read_byte(self.mmu.read_word(self.registers.pc))
        self.registers.pc += 2
        self.registers.a = byte
        self.debug('{}: LD A, ({})'.format(hex(self.registers.pc-3),hex(byte)))
        return 16

    def inst0xfb(self) -> int:
        self.cpu.ime = True
        self.debug('{}: EI'.format(hex(self.registers.pc-1)))
        return 4

    def inst0xfe(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.cp(byte)
        self.debug('{}: CP {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def inst0xff(self) -> int:
        self.debug('{}: RST 0x38'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x38
        return 16

    def inst0xcb00(self) -> int:
        self.registers.b = self.rlc(self.registers.b)
        self.debug('{}: RLC B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb01(self) -> int:
        self.registers.c = self.rlc(self.registers.c)
        self.debug('{}: RLC C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb02(self) -> int:
        self.registers.d = self.rlc(self.registers.d)
        self.debug('{}: RLC D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb03(self) -> int:
        self.registers.e = self.rlc(self.registers.e)
        self.debug('{}: RLC E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb04(self) -> int:
        self.registers.h = self.rlc(self.registers.h)
        self.debug('{}: RLC H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb05(self) -> int:
        self.registers.l = self.rlc(self.registers.l)
        self.debug('{}: RLC L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb06(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rlc(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RLC (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb07(self) -> int:
        self.registers.a = self.rlc(self.registers.a)
        self.debug('{}: RLC A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb08(self) -> int:
        self.registers.b = self.rrc(self.registers.b)
        self.debug('{}: RRC B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb09(self) -> int:
        self.registers.c = self.rrc(self.registers.c)
        self.debug('{}: RRC C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb0a(self) -> int:
        self.registers.d = self.rrc(self.registers.d)
        self.debug('{}: RRC D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb0b(self) -> int:
        self.registers.e = self.rrc(self.registers.e)
        self.debug('{}: RRC E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb0c(self) -> int:
        self.registers.h = self.rrc(self.registers.h)
        self.debug('{}: RRC H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb0d(self) -> int:
        self.registers.l = self.rrc(self.registers.l)
        self.debug('{}: RRC L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb0e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rrc(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RRC (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb0f(self) -> int:
        self.registers.a = self.rrc(self.registers.a)
        self.debug('{}: RRC A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb10(self) -> int:
        self.registers.b = self.rl(self.registers.b)
        self.debug('{}: RL B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb11(self) -> int:
        self.registers.c = self.rl(self.registers.c)
        self.debug('{}: RL C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb12(self) -> int:
        self.registers.d = self.rl(self.registers.d)
        self.debug('{}: RL D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb13(self) -> int:
        self.registers.e = self.rl(self.registers.e)
        self.debug('{}: RL E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb14(self) -> int:
        self.registers.h = self.rl(self.registers.h)
        self.debug('{}: RL H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb15(self) -> int:
        self.registers.l = self.rl(self.registers.l)
        self.debug('{}: RL L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb16(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rl(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RL (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb17(self) -> int:
        self.registers.a = self.rl(self.registers.a)
        self.debug('{}: RL A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb18(self) -> int:
        self.registers.b = self.rr(self.registers.b)
        self.debug('{}: RR B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb19(self) -> int:
        self.registers.c = self.rr(self.registers.c)
        self.debug('{}: RR C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb1a(self) -> int:
        self.registers.d = self.rr(self.registers.d)
        self.debug('{}: RR D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb1b(self) -> int:
        self.registers.e = self.rr(self.registers.e)
        self.debug('{}: RR E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb1c(self) -> int:
        self.registers.h = self.rr(self.registers.h)
        self.debug('{}: RR H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb1d(self) -> int:
        self.registers.l = self.rr(self.registers.l)
        self.debug('{}: RR L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb1e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rr(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RR (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb1f(self) -> int:
        self.registers.a = self.rr(self.registers.a)
        self.debug('{}: RR A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb20(self) -> int:
        self.registers.b = self.rlc(self.registers.b)
        self.registers.reset_c_flag()
        self.debug('{}: SLA B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb21(self) -> int:
        self.registers.c = self.rlc(self.registers.c)
        self.registers.reset_c_flag()
        self.debug('{}: SLA C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb22(self) -> int:
        self.registers.d = self.rlc(self.registers.d)
        self.registers.reset_c_flag()
        self.debug('{}: SLA D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb23(self) -> int:
        self.registers.e = self.rlc(self.registers.e)
        self.registers.reset_c_flag()
        self.debug('{}: SLA E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb24(self) -> int:
        self.registers.h = self.rlc(self.registers.h)
        self.registers.reset_c_flag()
        self.debug('{}: SLA H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb25(self) -> int:
        self.registers.l = self.rlc(self.registers.l)
        self.registers.reset_c_flag()
        self.debug('{}: SLA L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb26(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rlc(self.mmu.read_byte(self.registers.get_hl())))
        self.registers.reset_c_flag()
        self.debug('{}: SLA (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb27(self) -> int:
        self.registers.a = self.rlc(self.registers.a)
        self.registers.reset_c_flag()
        self.debug('{}: SLA A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb28(self) -> int:
        self.registers.b = self.rr(self.registers.b)
        self.registers.reset_c_flag()
        self.debug('{}: SRA B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb29(self) -> int:
        self.registers.c = self.rr(self.registers.c)
        self.registers.reset_c_flag()
        self.debug('{}: SRA C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb2a(self) -> int:
        self.registers.d = self.rr(self.registers.d)
        self.registers.reset_c_flag()
        self.debug('{}: SRA D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb2b(self) -> int:
        self.registers.e = self.rr(self.registers.e)
        self.registers.reset_c_flag()
        self.debug('{}: SRA E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb2c(self) -> int:
        self.registers.h = self.rr(self.registers.h)
        self.registers.reset_c_flag()
        self.debug('{}: SRA H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb2d(self) -> int:
        self.registers.l = self.rr(self.registers.l)
        self.registers.reset_c_flag()
        self.debug('{}: SRA L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb2e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rr(self.mmu.read_byte(self.registers.get_hl())))
        self.registers.reset_c_flag()
        self.debug('{}: SRA (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb2f(self) -> int:
        self.registers.a = self.rr(self.registers.a)
        self.registers.reset_c_flag()
        self.debug('{}: SRA A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb30(self) -> int:
        self.registers.b = self.swap(self.registers.b)
        self.debug('{}: SWAP B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb31(self) -> int:
        self.registers.c = self.swap(self.registers.c)
        self.debug('{}: SWAP C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb32(self) -> int:
        self.registers.d = self.swap(self.registers.d)
        self.debug('{}: SWAP D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb33(self) -> int:
        self.registers.e = self.swap(self.registers.e)
        self.debug('{}: SWAP E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb34(self) -> int:
        self.registers.h = self.swap(self.registers.h)
        self.debug('{}: SWAP H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb35(self) -> int:
        self.registers.l = self.swap(self.registers.l)
        self.debug('{}: SWAP L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb36(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.swap(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SWAP (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb37(self) -> int:
        self.registers.a = self.swap(self.registers.a)
        self.debug('{}: SWAP A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb38(self) -> int:
        self.registers.b = self.rrc(self.registers.b)
        self.registers.reset_c_flag()
        self.debug('{}: SRL B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb39(self) -> int:
        self.registers.c = self.rrc(self.registers.c)
        self.registers.reset_c_flag()
        self.debug('{}: SRL C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb3a(self) -> int:
        self.registers.d = self.rrc(self.registers.d)
        self.registers.reset_c_flag()
        self.debug('{}: SRL D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb3b(self) -> int:
        self.registers.e = self.rrc(self.registers.e)
        self.registers.reset_c_flag()
        self.debug('{}: SRL E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb3c(self) -> int:
        self.registers.h = self.rrc(self.registers.h)
        self.registers.reset_c_flag()
        self.debug('{}: SRL H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb3d(self) -> int:
        self.registers.l = self.rrc(self.registers.l)
        self.registers.reset_c_flag()
        self.debug('{}: SRL L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb3e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rrc(self.mmu.read_byte(self.registers.get_hl())))
        self.registers.reset_c_flag()
        self.debug('{}: SRL (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb3f(self) -> int:
        self.registers.a = self.rrc(self.registers.a)
        self.registers.reset_c_flag()
        self.debug('{}: SRL A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb40(self) -> int:
        self.bit(0, self.registers.b)
        self.debug('{}: BIT 0, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb41(self) -> int:
        self.bit(0, self.registers.c)
        self.debug('{}: BIT 0, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb42(self) -> int:
        self.bit(0, self.registers.d)
        self.debug('{}: BIT 0, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb43(self) -> int:
        self.bit(0, self.registers.e)
        self.debug('{}: BIT 0, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb44(self) -> int:
        self.bit(0, self.registers.h)
        self.debug('{}: BIT 0, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb45(self) -> int:
        self.bit(0, self.registers.l)
        self.debug('{}: BIT 0, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb46(self) -> int:
        self.bit(0, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 0, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb47(self) -> int:
        self.bit(0, self.registers.a)
        self.debug('{}: BIT 0, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb48(self) -> int:
        self.bit(1, self.registers.b)
        self.debug('{}: BIT 1, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb49(self) -> int:
        self.bit(1, self.registers.c)
        self.debug('{}: BIT 1, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb4a(self) -> int:
        self.bit(1, self.registers.d)
        self.debug('{}: BIT 1, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb4b(self) -> int:
        self.bit(1, self.registers.e)
        self.debug('{}: BIT 1, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb4c(self) -> int:
        self.bit(1, self.registers.h)
        self.debug('{}: BIT 1, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb4d(self) -> int:
        self.bit(1, self.registers.l)
        self.debug('{}: BIT 1, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb4e(self) -> int:
        self.bit(1, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 1, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb4f(self) -> int:
        self.bit(1, self.registers.a)
        self.debug('{}: BIT 1, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb50(self) -> int:
        self.bit(2, self.registers.b)
        self.debug('{}: BIT 2, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb51(self) -> int:
        self.bit(2, self.registers.c)
        self.debug('{}: BIT 2, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb52(self) -> int:
        self.bit(2, self.registers.d)
        self.debug('{}: BIT 2, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb53(self) -> int:
        self.bit(2, self.registers.e)
        self.debug('{}: BIT 2, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb54(self) -> int:
        self.bit(2, self.registers.h)
        self.debug('{}: BIT 2, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb55(self) -> int:
        self.bit(2, self.registers.l)
        self.debug('{}: BIT 2, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb56(self) -> int:
        self.bit(2, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 2, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb57(self) -> int:
        self.bit(2, self.registers.a)
        self.debug('{}: BIT 2, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb58(self) -> int:
        self.bit(3, self.registers.b)
        self.debug('{}: BIT 3, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb59(self) -> int:
        self.bit(3, self.registers.c)
        self.debug('{}: BIT 3, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb5a(self) -> int:
        self.bit(3, self.registers.d)
        self.debug('{}: BIT 3, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb5b(self) -> int:
        self.bit(3, self.registers.e)
        self.debug('{}: BIT 3, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb5c(self) -> int:
        self.bit(3, self.registers.h)
        self.debug('{}: BIT 3, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb5d(self) -> int:
        self.bit(3, self.registers.l)
        self.debug('{}: BIT 3, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb5e(self) -> int:
        self.bit(3, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 3, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb5f(self) -> int:
        self.bit(3, self.registers.a)
        self.debug('{}: BIT 3, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb60(self) -> int:
        self.bit(4, self.registers.b)
        self.debug('{}: BIT 4, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb61(self) -> int:
        self.bit(4, self.registers.c)
        self.debug('{}: BIT 4, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb62(self) -> int:
        self.bit(4, self.registers.d)
        self.debug('{}: BIT 4, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb63(self) -> int:
        self.bit(4, self.registers.e)
        self.debug('{}: BIT 4, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb64(self) -> int:
        self.bit(4, self.registers.h)
        self.debug('{}: BIT 4, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb65(self) -> int:
        self.bit(4, self.registers.l)
        self.debug('{}: BIT 4, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb66(self) -> int:
        self.bit(4, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 4, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb67(self) -> int:
        self.bit(4, self.registers.a)
        self.debug('{}: BIT 4, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb68(self) -> int:
        self.bit(5, self.registers.b)
        self.debug('{}: BIT 5, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb69(self) -> int:
        self.bit(5, self.registers.c)
        self.debug('{}: BIT 5, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb6a(self) -> int:
        self.bit(5, self.registers.d)
        self.debug('{}: BIT 5, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb6b(self) -> int:
        self.bit(5, self.registers.e)
        self.debug('{}: BIT 5, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb6c(self) -> int:
        self.bit(5, self.registers.h)
        self.debug('{}: BIT 5, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb6d(self) -> int:
        self.bit(5, self.registers.l)
        self.debug('{}: BIT 5, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb6e(self) -> int:
        self.bit(5, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 5, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb6f(self) -> int:
        self.bit(5, self.registers.a)
        self.debug('{}: BIT 5, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb70(self) -> int:
        self.bit(6, self.registers.b)
        self.debug('{}: BIT 6, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb71(self) -> int:
        self.bit(6, self.registers.c)
        self.debug('{}: BIT 6, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb72(self) -> int:
        self.bit(6, self.registers.d)
        self.debug('{}: BIT 6, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb73(self) -> int:
        self.bit(6, self.registers.e)
        self.debug('{}: BIT 6, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb74(self) -> int:
        self.bit(6, self.registers.h)
        self.debug('{}: BIT 6, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb75(self) -> int:
        self.bit(6, self.registers.l)
        self.debug('{}: BIT 6, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb76(self) -> int:
        self.bit(6, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 6, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb77(self) -> int:
        self.bit(6, self.registers.a)
        self.debug('{}: BIT 6, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb78(self) -> int:
        self.bit(7, self.registers.b)
        self.debug('{}: BIT 7, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb79(self) -> int:
        self.bit(7, self.registers.c)
        self.debug('{}: BIT 7, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb7a(self) -> int:
        self.bit(7, self.registers.d)
        self.debug('{}: BIT 7, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb7b(self) -> int:
        self.bit(7, self.registers.e)
        self.debug('{}: BIT 7, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb7c(self) -> int:
        self.bit(7, self.registers.h)
        self.debug('{}: BIT 7, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb7d(self) -> int:
        self.bit(7, self.registers.l)
        self.debug('{}: BIT 7, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb7e(self) -> int:
        self.bit(7, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 7, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb7f(self) -> int:
        self.bit(7, self.registers.a)
        self.debug('{}: BIT 7, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb80(self) -> int:
        self.registers.b = self.res(0, self.registers.b)
        self.debug('{}: RES 0, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb81(self) -> int:
        self.registers.c = self.res(0, self.registers.c)
        self.debug('{}: RES 0, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb82(self) -> int:
        self.registers.d = self.res(0, self.registers.d)
        self.debug('{}: RES 0, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb83(self) -> int:
        self.registers.e = self.res(0, self.registers.e)
        self.debug('{}: RES 0, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb84(self) -> int:
        self.registers.h = self.res(0, self.registers.h)
        self.debug('{}: RES 0, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb85(self) -> int:
        self.registers.l = self.res(0, self.registers.l)
        self.debug('{}: RES 0, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb86(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(0, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 0, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb87(self) -> int:
        self.registers.a = self.res(0, self.registers.a)
        self.debug('{}: RES 0, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb88(self) -> int:
        self.registers.b = self.res(1, self.registers.b)
        self.debug('{}: RES 1, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb89(self) -> int:
        self.registers.c = self.res(1, self.registers.c)
        self.debug('{}: RES 1, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb8a(self) -> int:
        self.registers.d = self.res(1, self.registers.d)
        self.debug('{}: RES 1, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb8b(self) -> int:
        self.registers.e = self.res(1, self.registers.e)
        self.debug('{}: RES 1, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb8c(self) -> int:
        self.registers.h = self.res(1, self.registers.h)
        self.debug('{}: RES 1, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb8d(self) -> int:
        self.registers.l = self.res(1, self.registers.l)
        self.debug('{}: RES 1, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb8e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(1, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 1, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb8f(self) -> int:
        self.registers.a = self.res(1, self.registers.a)
        self.debug('{}: RES 1, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb90(self) -> int:
        self.registers.b = self.res(2, self.registers.b)
        self.debug('{}: RES 2, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb91(self) -> int:
        self.registers.c = self.res(2, self.registers.c)
        self.debug('{}: RES 2, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb92(self) -> int:
        self.registers.d = self.res(2, self.registers.d)
        self.debug('{}: RES 2, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb93(self) -> int:
        self.registers.e = self.res(2, self.registers.e)
        self.debug('{}: RES 2, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb94(self) -> int:
        self.registers.h = self.res(2, self.registers.h)
        self.debug('{}: RES 2, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb95(self) -> int:
        self.registers.l = self.res(2, self.registers.l)
        self.debug('{}: RES 2, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb96(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(2, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 2, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb97(self) -> int:
        self.registers.a = self.res(2, self.registers.a)
        self.debug('{}: RES 2, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb98(self) -> int:
        self.registers.b = self.res(3, self.registers.b)
        self.debug('{}: RES 3, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb99(self) -> int:
        self.registers.c = self.res(3, self.registers.c)
        self.debug('{}: RES 3, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb9a(self) -> int:
        self.registers.d = self.res(3, self.registers.d)
        self.debug('{}: RES 3, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb9b(self) -> int:
        self.registers.e = self.res(3, self.registers.e)
        self.debug('{}: RES 3, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb9c(self) -> int:
        self.registers.h = self.res(3, self.registers.h)
        self.debug('{}: RES 3, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb9d(self) -> int:
        self.registers.l = self.res(3, self.registers.l)
        self.debug('{}: RES 3, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcb9e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(3, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 3, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcb9f(self) -> int:
        self.registers.a = self.res(3, self.registers.a)
        self.debug('{}: RES 3, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba0(self) -> int:
        self.registers.b = self.res(4, self.registers.b)
        self.debug('{}: RES 4, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba1(self) -> int:
        self.registers.c = self.res(4, self.registers.c)
        self.debug('{}: RES 4, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba2(self) -> int:
        self.registers.d = self.res(4, self.registers.d)
        self.debug('{}: RES 4, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba3(self) -> int:
        self.registers.e = self.res(4, self.registers.e)
        self.debug('{}: RES 4, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba4(self) -> int:
        self.registers.h = self.res(4, self.registers.h)
        self.debug('{}: RES 4, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba5(self) -> int:
        self.registers.l = self.res(4, self.registers.l)
        self.debug('{}: RES 4, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(4, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 4, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcba7(self) -> int:
        self.registers.a = self.res(4, self.registers.a)
        self.debug('{}: RES 4, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba8(self) -> int:
        self.registers.b = self.res(5, self.registers.b)
        self.debug('{}: RES 5, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcba9(self) -> int:
        self.registers.c = self.res(5, self.registers.c)
        self.debug('{}: RES 5, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbaa(self) -> int:
        self.registers.d = self.res(5, self.registers.d)
        self.debug('{}: RES 5, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbab(self) -> int:
        self.registers.e = self.res(5, self.registers.e)
        self.debug('{}: RES 5, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbac(self) -> int:
        self.registers.h = self.res(5, self.registers.h)
        self.debug('{}: RES 5, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbad(self) -> int:
        self.registers.l = self.res(5, self.registers.l)
        self.debug('{}: RES 5, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbae(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(5, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 5, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbaf(self) -> int:
        self.registers.a = self.res(5, self.registers.a)
        self.debug('{}: RES 5, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb0(self) -> int:
        self.registers.b = self.res(6, self.registers.b)
        self.debug('{}: RES 6, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb1(self) -> int:
        self.registers.c = self.res(6, self.registers.c)
        self.debug('{}: RES 6, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb2(self) -> int:
        self.registers.d = self.res(6, self.registers.d)
        self.debug('{}: RES 6, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb3(self) -> int:
        self.registers.e = self.res(6, self.registers.e)
        self.debug('{}: RES 6, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb4(self) -> int:
        self.registers.h = self.res(6, self.registers.h)
        self.debug('{}: RES 6, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb5(self) -> int:
        self.registers.l = self.res(6, self.registers.l)
        self.debug('{}: RES 6, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(6, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 6, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbb7(self) -> int:
        self.registers.a = self.res(6, self.registers.a)
        self.debug('{}: RES 6, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb8(self) -> int:
        self.registers.b = self.res(7, self.registers.b)
        self.debug('{}: RES 7, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbb9(self) -> int:
        self.registers.c = self.res(7, self.registers.c)
        self.debug('{}: RES 7, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbba(self) -> int:
        self.registers.d = self.res(7, self.registers.d)
        self.debug('{}: RES 7, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbbb(self) -> int:
        self.registers.e = self.res(7, self.registers.e)
        self.debug('{}: RES 7, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbbc(self) -> int:
        self.registers.h = self.res(7, self.registers.h)
        self.debug('{}: RES 7, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbbd(self) -> int:
        self.registers.l = self.res(7, self.registers.l)
        self.debug('{}: RES 7, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbbe(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(7, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: RES 7, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbbf(self) -> int:
        self.registers.a = self.res(7, self.registers.a)
        self.debug('{}: RES 7, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc0(self) -> int:
        self.registers.b = set_bit(0, self.registers.b)
        self.debug('{}: SET 0, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc1(self) -> int:
        self.registers.c = set_bit(0, self.registers.c)
        self.debug('{}: SET 0, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc2(self) -> int:
        self.registers.d = set_bit(0, self.registers.d)
        self.debug('{}: SET 0, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc3(self) -> int:
        self.registers.e = set_bit(0, self.registers.e)
        self.debug('{}: SET 0, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc4(self) -> int:
        self.registers.h = set_bit(0, self.registers.h)
        self.debug('{}: SET 0, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc5(self) -> int:
        self.registers.l = set_bit(0, self.registers.l)
        self.debug('{}: SET 0, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(0, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 0, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbc7(self) -> int:
        self.registers.a = set_bit(0, self.registers.a)
        self.debug('{}: SET 0, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc8(self) -> int:
        self.registers.b = set_bit(1, self.registers.b)
        self.debug('{}: SET 1, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbc9(self) -> int:
        self.registers.c = set_bit(1, self.registers.c)
        self.debug('{}: SET 1, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbca(self) -> int:
        self.registers.d = set_bit(1, self.registers.d)
        self.debug('{}: SET 1, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbcb(self) -> int:
        self.registers.e = set_bit(1, self.registers.e)
        self.debug('{}: SET 1, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbcc(self) -> int:
        self.registers.h = set_bit(1, self.registers.h)
        self.debug('{}: SET 1, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbcd(self) -> int:
        self.registers.l = set_bit(1, self.registers.l)
        self.debug('{}: SET 1, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbce(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(1, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 1, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbcf(self) -> int:
        self.registers.a = set_bit(1, self.registers.a)
        self.debug('{}: SET 1, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd0(self) -> int:
        self.registers.b = set_bit(2, self.registers.b)
        self.debug('{}: SET 2, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd1(self) -> int:
        self.registers.c = set_bit(2, self.registers.c)
        self.debug('{}: SET 2, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd2(self) -> int:
        self.registers.d = set_bit(2, self.registers.d)
        self.debug('{}: SET 2, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd3(self) -> int:
        self.registers.e = set_bit(2, self.registers.e)
        self.debug('{}: SET 2, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd4(self) -> int:
        self.registers.h = set_bit(2, self.registers.h)
        self.debug('{}: SET 2, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd5(self) -> int:
        self.registers.l = set_bit(2, self.registers.l)
        self.debug('{}: SET 2, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(2, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 2, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbd7(self) -> int:
        self.registers.a = set_bit(2, self.registers.a)
        self.debug('{}: SET 2, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd8(self) -> int:
        self.registers.b = set_bit(3, self.registers.b)
        self.debug('{}: SET 3, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbd9(self) -> int:
        self.registers.c = set_bit(3, self.registers.c)
        self.debug('{}: SET 3, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbda(self) -> int:
        self.registers.d = set_bit(3, self.registers.d)
        self.debug('{}: SET 3, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbdb(self) -> int:
        self.registers.e = set_bit(3, self.registers.e)
        self.debug('{}: SET 3, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbdc(self) -> int:
        self.registers.h = set_bit(3, self.registers.h)
        self.debug('{}: SET 3, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbdd(self) -> int:
        self.registers.l = set_bit(3, self.registers.l)
        self.debug('{}: SET 3, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbde(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(3, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 3, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbdf(self) -> int:
        self.registers.a = set_bit(3, self.registers.a)
        self.debug('{}: SET 3, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe0(self) -> int:
        self.registers.b = set_bit(4, self.registers.b)
        self.debug('{}: SET 4, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe1(self) -> int:
        self.registers.c = set_bit(4, self.registers.c)
        self.debug('{}: SET 4, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe2(self) -> int:
        self.registers.d = set_bit(4, self.registers.d)
        self.debug('{}: SET 4, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe3(self) -> int:
        self.registers.e = set_bit(4, self.registers.e)
        self.debug('{}: SET 4, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe4(self) -> int:
        self.registers.h = set_bit(4, self.registers.h)
        self.debug('{}: SET 4, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe5(self) -> int:
        self.registers.l = set_bit(4, self.registers.l)
        self.debug('{}: SET 4, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(4, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 4, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbe7(self) -> int:
        self.registers.a = set_bit(4, self.registers.a)
        self.debug('{}: SET 4, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe8(self) -> int:
        self.registers.b = set_bit(5, self.registers.b)
        self.debug('{}: SET 5, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbe9(self) -> int:
        self.registers.c = set_bit(5, self.registers.c)
        self.debug('{}: SET 5, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbea(self) -> int:
        self.registers.d = set_bit(5, self.registers.d)
        self.debug('{}: SET 5, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbeb(self) -> int:
        self.registers.e = set_bit(5, self.registers.e)
        self.debug('{}: SET 5, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbec(self) -> int:
        self.registers.h = set_bit(5, self.registers.h)
        self.debug('{}: SET 5, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbed(self) -> int:
        self.registers.l = set_bit(5, self.registers.l)
        self.debug('{}: SET 5, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbee(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(5, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 5, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbef(self) -> int:
        self.registers.a = set_bit(5, self.registers.a)
        self.debug('{}: SET 5, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf0(self) -> int:
        self.registers.b = set_bit(6, self.registers.b)
        self.debug('{}: SET 6, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf1(self) -> int:
        self.registers.c = set_bit(6, self.registers.c)
        self.debug('{}: SET 6, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf2(self) -> int:
        self.registers.d = set_bit(6, self.registers.d)
        self.debug('{}: SET 6, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf3(self) -> int:
        self.registers.e = set_bit(6, self.registers.e)
        self.debug('{}: SET 6, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf4(self) -> int:
        self.registers.h = set_bit(6, self.registers.h)
        self.debug('{}: SET 6, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf5(self) -> int:
        self.registers.l = set_bit(6, self.registers.l)
        self.debug('{}: SET 6, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(6, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 6, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbf7(self) -> int:
        self.registers.a = set_bit(6, self.registers.a)
        self.debug('{}: SET 6, A'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf8(self) -> int:
        self.registers.b = set_bit(7, self.registers.b)
        self.debug('{}: SET 7, B'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbf9(self) -> int:
        self.registers.c = set_bit(7, self.registers.c)
        self.debug('{}: SET 7, C'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbfa(self) -> int:
        self.registers.d = set_bit(7, self.registers.d)
        self.debug('{}: SET 7, D'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbfb(self) -> int:
        self.registers.e = set_bit(7, self.registers.e)
        self.debug('{}: SET 7, E'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbfc(self) -> int:
        self.registers.h = set_bit(7, self.registers.h)
        self.debug('{}: SET 7, H'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbfd(self) -> int:
        self.registers.l = set_bit(7, self.registers.l)
        self.debug('{}: SET 7, L'.format(hex(self.registers.pc-2)))
        return 8

    def inst0xcbfe(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(7, self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SET 7, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def inst0xcbff(self) -> int:
        self.registers.a = set_bit(7, self.registers.a)
        self.debug('{}: SET 7, A'.format(hex(self.registers.pc-2)))
        return 8
    
    def unimplemented(self, opcode : int) -> int:
        logging.error('{}: Unknow Opcode {}'.format(hex(self.registers.pc-1), hex(opcode)))
        raise NotImplementedError()

    def add_byte(self, value : int) -> int:
        byte = self.registers.a + value
        if (byte & 0xff) == 0x00:
            self.registers.set_z_flag()
        else:
                self.registers.reset_z_flag()
        if (self.registers.a ^ value ^ byte) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a ^ value ^ byte) & 0x10 == 0x10: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.a = byte & 0xff

    def add_word(self, value1 : int, value2 : int) -> int:
        result = value1 + value2

        self.registers.reset_n_flag()
        if result & 0x10000 == 0x10000: 
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (value1 ^ value2 ^ (result & 0xFFFF)) & 0x1000 == 0x1000: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()

        return result & 0xFFFF

    def adc(self, value : int) -> int:
        carry = 1 if self.registers.is_c_flag() else 0
        result = self.registers.a + value + carry
        if result & 0xff == 0x0: 
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if result > 0xff: 
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a & 0xf) + (value & 0xf) + carry > 0xf: 
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.a = result & 0xff
        
    def sub(self, value : int) -> int:
        result = self.registers.a - value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if (self.registers.a ^ value ^ result) & 0x100 == 0x100:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a ^ value ^ result) & 0x10 == 0x10:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        self.registers.a = result & 0xff

    def sbc(self, value : int) -> int:
        carry = 1 if self.registers.is_c_flag() else 0
        result = self.registers.a - value - carry
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result < 0x0:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a & 0xF) - (value & 0xF) - carry < 0: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        self.registers.a = result & 0xff

    def _and(self, value: int) -> int:
        result = self.registers.a & value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()
        self.registers.a = result & 0xff

    def _or(self, value : int) -> int:
        result = self.registers.a | value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def xor(self, value: int) -> int:
        result = self.registers.a ^ value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def cp(self, value: int):
        result = self.registers.a - value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if self.registers.a < value:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (result & 0xf) > (self.registers.a & 0xf):
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()

    def bit(self, pos : int, value : int) -> int:
        bit = 1 if value & bit_mask[pos] == bit_mask[pos] else 0
        if bit & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()

    def res(self, pos : int, value : int) -> int:
        return value & (bit_mask[pos] ^ 0xff)

    def swap(self, value : int) -> int:
        value = ((value << 4) & 0xff) | (value >> 4)
        if value & 0xff == 0x00:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.reset_c_flag()
        return value


    def inc_byte(self, value : int) -> int:
        result = value + 1
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result & 0xf == 0x0:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        return result & 0xff

    def dec_byte(self, value : int) -> int:
        result = value - 1
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result & 0xf == 0x0:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        return result & 0xff

    def rl(self, value : int) -> int:
        carry = 1 if self.registers.is_c_flag() else 0
        if value & 0x80 == 0x80:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        result = ((value << 1) & 0xff) + carry
        if result & 0xFF == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return result

    def rlc(self, value : int) -> int:
        bit_out = 0x1 if value & 0x80 == 0x80 else 0x0
        if bit_out == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if ((value << 1) & 0xff) + bit_out == 0x00:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return ((value << 1) & 0xff) + bit_out

    def rr(self, value : int) -> int:
        carry = 0x80 if self.registers.is_c_flag() else 0x0
        if value & 0x1 == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        if (value >> 1) + carry == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        return (value >> 1) + carry

    def rrc(self, value : int) -> int:
        bit_out = 0x80 if value & 0x1 == 0x1 else 0x0
        if bit_out == 0x80:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        if (value >> 1) + bit_out == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        return (value >> 1) + bit_out

    def debug(self, text : str):
        logging.debug('{} [{}]'.format(text,self.registers.__str__()))
