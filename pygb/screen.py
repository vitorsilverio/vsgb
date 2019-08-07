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


class Screen(Thread):

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144 
    SCALE = 3
    WINDOW_WIDTH = SCREEN_WIDTH * SCALE
    WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE

    def __init__(self, _input : Input):
        super(Screen, self). __init__()
        self.framebuffer = [0xffffffff]*(Screen.WINDOW_WIDTH * Screen.WINDOW_HEIGHT)
        self.updated = False
        self.last = time.monotonic()
        self.input = _input
        self.window = None
        
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Screen.WINDOW_WIDTH, Screen.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        self.window = glutCreateWindow(b'pygb')
        glPixelZoom(Screen.SCALE,Screen.SCALE)
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutKeyboardFunc(self.keyboard)
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

    def keyboard(self, key, x : int, y : int):
        for button in self.input.buttons:
            self.input.buttons[button] = False

        if key == GLUT_KEY_UP:
            self.input.buttons['UP'] = True
        elif key == GLUT_KEY_DOWN:
            self.input.buttons['DOWN'] = True
        elif key == GLUT_KEY_LEFT:
            self.input.buttons['LEFT'] = True
        elif key == GLUT_KEY_RIGHT:
            self.input.buttons['RIGHT'] = True
        elif key == 'x':
            self.input.buttons['A'] = True
        elif key == 'z':
            self.input.buttons['B'] = True
        elif key == 'v':
            self.input.buttons['START'] = True
        elif key == 'c':
            self.input.buttons['SELCT'] = True


         