#!/usr/bin/env python
# -*- coding: utf-8 -*-

def signed_value(byte):
    return (byte & 0x7F) - 0x80 if byte > 127 else byte