#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

import simpleaudio as sa

class SoundDriver():

    TICKS_PER_SEC = 4194304
    BUFFER_SIZE = int( 22050 * 0.2) 

    def __init__(self):
        self.sample_rate = 22050
        self.buffer = [0]*SoundDriver.BUFFER_SIZE
        self.ticks = 0
        self.div = int(SoundDriver.TICKS_PER_SEC / (self.sample_rate ))
        self.i = 0
        self.play_obj = None

    
    def play(self, left, right, ticks):
        
        self.ticks += ticks
        if self.ticks <= self.div:
            return
            
        self.ticks = 0

        self.buffer[self.i] = left
        self.buffer[self.i+1] = right
        self.i += 2

        if self.i >= SoundDriver.BUFFER_SIZE / 2:
            wave = bytes(self.buffer)
            wave_obj = sa.WaveObject(wave,2,1,self.sample_rate)
            try:
                self.play_obj.stop()
            except:
                pass
            self.play_obj = wave_obj.play()
            #self.play_obj.wait_done()
            self.i = 0

    def stop(self):
        self.buffer = [0]*SoundDriver.BUFFER_SIZE
        if self.play_obj is not None:
            self.play_obj.stop()
