#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sdl2

class Screen:

    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 432

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144

    def __init__(self):
        sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_VIDEO)
        self.buffer = [0]*(Screen.SCREEN_WIDTH * Screen.SCREEN_HEIGHT)
        self.window = sdl2.SDL_CreateWindow('pygb'.encode(), 0, 0, Screen.WINDOW_WIDTH, Screen.WINDOW_HEIGHT, sdl2.SDL_WINDOW_RESIZABLE)
        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)
        sdl2.SDL_SetHint('SDL_HINT_RENDER_SCALE_QUALITY'.encode(),'2'.encode())
        sdl2.SDL_RenderSetLogicalSize(self.renderer, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT)
        self.texture = sdl2.SDL_CreateTexture(self.renderer, sdl2.SDL_PIXELFORMAT_ABGR8888,1, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT)

    def render(self, framebuffer):
        sdl2.SDL_UpdateTexture(self.texture, None, framebuffer, Screen.SCREEN_WIDTH * 4)
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)