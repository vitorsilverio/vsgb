#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from threading import Thread
import time

from pygb.input import Input
from pygb.interrupt_manager import Interrupt, InterruptManager


class Screen(Thread):

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144 
    SCALE = 3
    WINDOW_WIDTH = SCREEN_WIDTH * SCALE
    WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE

    def __init__(self, _input : Input, interruptManager : InterruptManager):
        super(Screen, self). __init__()
        self.framebuffer = [0xffffffff]*(Screen.WINDOW_WIDTH * Screen.WINDOW_HEIGHT)
        self.updated = False
        self.last = time.monotonic()
        self.input = _input
        self.interruptManager = interruptManager
        self.window = None
        
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Screen.WINDOW_WIDTH, Screen.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        self.window = glutCreateWindow(b'pygb')
        glutKeyboardFunc(self._key)
        glutKeyboardUpFunc(self._keyUp)
        glutSpecialFunc(self._spec)
        glutSpecialUpFunc(self._specUp)
        glPixelZoom(Screen.SCALE,Screen.SCALE)
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
            glDrawPixels(Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, self.framebuffer)
            glFlush()
            glutSwapBuffers()
        self.updated = True

    def request_input_interrupt(self):
        self.interruptManager.request_interrupt(Interrupt.INTERRUPT_JOYPAD)

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
                logging.warning("UP released")
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = False
                logging.warning("DOWN released")
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = False
                logging.warning("LEFT released")
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = False
                logging.warning("RIGHT released")
                self.request_input_interrupt()
        else:
            if c == GLUT_KEY_UP:
                self.input.buttons['UP'] = True
                logging.warning("UP pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_DOWN:
                self.input.buttons['DOWN'] = True
                logging.warning("DOWN pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_LEFT:
                self.input.buttons['LEFT'] = True
                logging.warning("LEFT pressed")
                self.request_input_interrupt()
            if c == GLUT_KEY_RIGHT:
                self.input.buttons['RIGHT'] = True
                logging.warning("RIGHT pressed")
                self.request_input_interrupt()

    def _glkeyboard(self, c, x, y, up):
        if up:
            if c == 'z':
                self.input.buttons['A'] = False
                logging.warning("A released")
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = False
                logging.warning("B released")
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = False
                logging.warning("START released")
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELCT'] = False
                logging.warning("SELECT released")
                self.request_input_interrupt()
        else:
            if c == 'z':
                self.input.buttons['A'] = True
                logging.warning("A pressed")
                self.request_input_interrupt()
            elif c == 'x':
                self.input.buttons['B'] = True
                logging.warning("B pressed")
                self.request_input_interrupt()
            elif c == chr(13):
                self.input.buttons['START'] = True
                logging.warning("START pressed")
                self.request_input_interrupt()
            elif c == chr(8):
                self.input.buttons['SELCT'] = True
                logging.warning("SELECT pressed")
                self.request_input_interrupt()


         