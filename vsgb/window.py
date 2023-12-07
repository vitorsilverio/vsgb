#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import numpy as np
import sdl2
import sdl2.ext
import sdl2.ext.renderer
import ctypes


class Window(Thread):
    SCREEN_WIDTH: int = 160
    SCREEN_HEIGHT: int = 144
    V_SCALE: int = 1
    H_SCALE: int = 1
    WINDOW_WIDTH: int = SCREEN_WIDTH * H_SCALE
    WINDOW_HEIGHT: int = SCREEN_HEIGHT * V_SCALE
    framebuffer = np.array([0xffff] * (WINDOW_WIDTH * WINDOW_HEIGHT), dtype=ctypes.c_uint16)
    refresh: bool = False

    def __init__(self):
        super(Window, self).__init__()

    def run(self):
        # Initialize the SDL2 library
        sdl2.ext.init()

        # Create a window and renderer
        window =  sdl2.ext.Window("VSGB", (Window.WINDOW_WIDTH, Window.WINDOW_HEIGHT), flags=sdl2.SDL_WINDOW_SHOWN)
        self.renderer = sdl2.ext.renderer.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED)

        # Create a texture to hold the framebuffer data
        self.texture = sdl2.SDL_CreateTexture(self.renderer.sdlrenderer, sdl2.SDL_PIXELFORMAT_ARGB1555,
                                                sdl2.SDL_TEXTUREACCESS_STREAMING, Window.WINDOW_WIDTH,
                                                Window.SCREEN_HEIGHT)
        
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

        sdl2.ext.quit()

    def draw(self):
        if Window.refresh:
            # Update the texture with the framebuffer data
            sdl2.SDL_UpdateTexture(self.texture, None, self.framebuffer, 640 * 2)

            # Clear the renderer
            self.renderer.clear()

            # Copy the texture to the renderer
            self.render.copy(self.texture)

            # Present the rendered image
            self.render.present()
            Window.refresh = False




