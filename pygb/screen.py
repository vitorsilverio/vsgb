#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from threading import Thread



class Screen(Thread):

    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 144 

    SCALE = 3

    WINDOW_WIDTH = SCREEN_WIDTH * SCALE
    WINDOW_HEIGHT = SCREEN_HEIGHT * SCALE

     

    def __init__(self):
        super(Screen, self). __init__()
        self.framebuffer = [0xffffffff]*(Screen.WINDOW_WIDTH * Screen.WINDOW_HEIGHT)
        self.updated = False
        

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Screen.WINDOW_WIDTH, Screen.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        window = glutCreateWindow(b'pygb')
        glPixelZoom(Screen.SCALE,Screen.SCALE)
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()

    def render(self, framebuffer):
        for x in range(0, Screen.SCREEN_WIDTH):
            for y in range(0, Screen.SCREEN_HEIGHT):
                self.framebuffer[x + Screen.SCREEN_WIDTH * y] = framebuffer[x + Screen.SCREEN_WIDTH * (Screen.SCREEN_HEIGHT - y -1)]

        self.updated = False

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        if not self.updated:
            glDrawPixels(Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8, self.framebuffer)
            glFlush()
            glutSwapBuffers()
        self.updated = True


         