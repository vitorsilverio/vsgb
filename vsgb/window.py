#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from threading import Thread
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vsgb.input import Input


class Window(Thread):

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144 
    SCALE = 3
    WINDOW_WIDTH = SCREEN_WIDTH * SCALE
    WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE

    def __init__(self, _input : Input):
        super(Window, self). __init__()
        self.framebuffer = [0xffffffff]*(Window.WINDOW_WIDTH * Window.WINDOW_HEIGHT)
        self.updated = False
        self.input = _input
        self.window = None
        
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Window.WINDOW_WIDTH, Window.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        self.window = glutCreateWindow(b'vsgb')
        glutKeyboardFunc(self._key)
        glutKeyboardUpFunc(self._keyUp)
        glutSpecialFunc(self._spec)
        glutSpecialUpFunc(self._specUp)
        glPixelZoom(Window.SCALE,Window.SCALE)
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()

    def render(self, framebuffer : list):
        self.framebuffer = framebuffer
        self.updated = False

    def draw(self):
        if not self.updated:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glDrawPixels(Window.SCREEN_WIDTH, Window.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, self.framebuffer)
            glFlush()
            glutSwapBuffers()
        self.updated = True

    def request_input_interrupt(self):
        self.input.request_interrupt()

    def _key(self, c, x, y):
        self._glkeyboard(c.decode("ascii"), x, y, False)

    def _keyUp(self, c, x, y):
        self._glkeyboard(c.decode("ascii"), x, y, True)

    def _spec(self, c, x, y):
        self._glkeyboardspecial(c, x, y, False)

    def _specUp(self, c, x, y):
        self._glkeyboardspecial(c, x, y, True)



    def _glkeyboardspecial(self, c, x, y, up):
        if up:
            if c == GLUT_KEY_UP:
                self.input.buttons['UP'] = False
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = False
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = False
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = False
                self.request_input_interrupt()
        else:
            if c == GLUT_KEY_UP:
                self.input.buttons['UP'] = True
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = True
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = True
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = True
                self.request_input_interrupt()

    def _glkeyboard(self, c, x, y, up):
        if up:
            if c == 'z':
                self.input.buttons['A'] = False
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = False
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = False
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELECT'] = False
                self.request_input_interrupt()
        else:
            if c == 'z':
                self.input.buttons['A'] = True
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = True
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = True
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELECT'] = True
                self.request_input_interrupt()


         
