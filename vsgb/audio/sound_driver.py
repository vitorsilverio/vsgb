#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

# import simpleaudio as sa
import threading

class SoundDriver():

    TICKS_PER_SEC = 4194304
    BUFFER_SIZE = int(22050 * 0.4)
    #BUFFER_SIZE = 220

    def __init__(self):
        self.sample_rate = 22050
        self.buffer = bytearray([0]*(SoundDriver.BUFFER_SIZE))
        self.ticks = 0
        self.div = SoundDriver.TICKS_PER_SEC // (self.sample_rate )
        self.i = 0
        self.play_obj = None
        self.has_sound = False

    
    def play(self, left, right, ticks):
        
        self.ticks += ticks
        if self.ticks <= self.div:
            return
            
        self.ticks = 0

        if left:
            self.has_sound = True

        self.buffer[self.i] = left
        #self.buffer[self.i+1] = right
        #self.i += 2
        self.i += 1

        if self.i >= SoundDriver.BUFFER_SIZE:
            if self.has_sound:
               threading.Thread(target=self.play_sound, args=(self.buffer,)).start()
                
            self.i = 0
            self.has_sound = False

    def stop(self):
        self.buffer = [0]*SoundDriver.BUFFER_SIZE
        if self.play_obj is not None:
            try:
                self.play_obj.stop()
            except:
                pass

    def play_sound(self,wave):
        try:
            # wave_obj = sa.WaveObject(wave,1,1,self.sample_rate)
            while self.play_obj and self.play_obj.is_playing():
                pass
            # self.play_obj = wave_obj.play()
        except:
            pass
    