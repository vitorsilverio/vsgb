#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CPU:

    def __init__(self,mmu):
        self.mmu = mmu
        print('CPU')

    def step(self):
        print('cpu step')