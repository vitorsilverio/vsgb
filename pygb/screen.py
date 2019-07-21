#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdl2 import *
from PIL import Image


class Screen():

    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 432

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144  

    def __init__(self):
        SDL_InitSubSystem(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(b'pygb', 0, 0, Screen.WINDOW_WIDTH, Screen.WINDOW_HEIGHT, SDL_WINDOW_RESIZABLE)
        self.renderer = SDL_CreateRenderer(self.window, -1, 0)
        SDL_SetHint(b'SDL_HINT_RENDER_SCALE_QUALITY',b'2')
        SDL_RenderSetLogicalSize(self.renderer, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT)
        self.texture = SDL_CreateTexture(self.renderer, SDL_PIXELFORMAT_ABGR8888, 1, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT)  

    def render(self, framebuffer):
        SDL_UpdateTexture(self.texture, None, None, Screen.SCREEN_WIDTH * 4)
        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)

    def dump_frame(self, framebuffer):
        frame = Image.new('RGB',(Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT),0)
        pixels = frame.load()
        for x in range(0,Screen.SCREEN_WIDTH):
            for y in range(0,Screen.SCREEN_HEIGHT):
                pixels[x,y] = framebuffer[y*Screen.SCREEN_WIDTH + x]
        frame.show()

