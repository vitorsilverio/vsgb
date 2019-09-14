#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from threading import Thread
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



from pygb.input import Input


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
        self.last = time.monotonic()
        self.input = _input
        self.window = None
        
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Window.WINDOW_WIDTH, Window.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        self.window = glutCreateWindow(b'pygb')
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
        t = time.monotonic()
        fps = 1.0 / (t - self.last)
        self.last = t
        if self.window is not None:
            glutSetWindowTitle('pygb ({} fps)'.format(str(int(fps))).encode())
        self.updated = False

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        if not self.updated:
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
                logging.debug("UP released")
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = False
                logging.debug("DOWN released")
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = False
                logging.debug("LEFT released")
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = False
                logging.debug("RIGHT released")
                self.request_input_interrupt()
        else:
            if c == GLUT_KEY_UP:
                self.input.buttons['UP'] = True
                logging.debug("UP pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = True
                logging.debug("DOWN pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = True
                logging.debug("LEFT pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = True
                logging.debug("RIGHT pressed")
                self.request_input_interrupt()

    def _glkeyboard(self, c, x, y, up):
        if up:
            if c == 'z':
                self.input.buttons['A'] = False
                logging.debug("A released")
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = False
                logging.debug("B released")
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = False
                logging.debug("START released")
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELECT'] = False
                logging.debug("SELECT released")
                self.request_input_interrupt()
        else:
            if c == 'z':
                self.input.buttons['A'] = True
                logging.debug("A pressed")
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = True
                logging.debug("B pressed")
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = True
                logging.debug("START pressed")
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELECT'] = True
                logging.debug("SELECT pressed")
                self.request_input_interrupt()


         