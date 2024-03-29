#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from threading import Thread
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from vsgb.input import Input


class Window(Thread):

    SCREEN_WIDTH: int = 160
    SCREEN_HEIGHT: int = 144 
    V_SCALE: int = 4
    H_SCALE: int = 4
    WINDOW_WIDTH: int = SCREEN_WIDTH * H_SCALE
    WINDOW_HEIGHT: int = SCREEN_HEIGHT * V_SCALE
    framebuffer: list = [0xffffffff]*(WINDOW_WIDTH * WINDOW_HEIGHT)
    refresh: bool = False

    def __init__(self):
        super(Window, self). __init__()
        
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Window.WINDOW_WIDTH, Window.WINDOW_HEIGHT)
        glutInitWindowPosition(200, 200)
        glutCreateWindow(b'vsgb')
        glutKeyboardFunc(self._key)
        glutKeyboardUpFunc(self._keyUp)
        glutSpecialFunc(self._spec)
        glutSpecialUpFunc(self._specUp)
        glPixelZoom(Window.H_SCALE,Window.V_SCALE)
        glutReshapeFunc(self.resize)
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()

    def draw(self):
        if Window.refresh:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glDrawPixels(Window.SCREEN_WIDTH, Window.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_SHORT_1_5_5_5_REV, Window.framebuffer)
            glFlush()
            glutSwapBuffers()
            Window.refresh = False
        

    def resize(self, width, height):
        new_h_scale = (width / Window.SCREEN_WIDTH)
        new_v_scale = (height / Window.SCREEN_HEIGHT)
        glPixelZoom(new_h_scale, new_v_scale)

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
                Input.BUTTON_UP = False  
            elif c == GLUT_KEY_DOWN:
                Input.BUTTON_DOWN = False
            elif c == GLUT_KEY_LEFT:
                Input.BUTTON_LEFT = False
            elif c == GLUT_KEY_RIGHT:
                Input.BUTTON_RIGHT = False
            elif c == GLUT_KEY_F4:
                #self.parent.save_state()
                print('TODO bind savestate')
            elif c == GLUT_KEY_F5:
                #self.parent.load_state()    
                print('TODO bind savestate')
                
        else:
            if c == GLUT_KEY_UP:
                Input.BUTTON_UP = True
            elif c == GLUT_KEY_DOWN:
                Input.BUTTON_DOWN = True
            elif c == GLUT_KEY_LEFT:
                Input.BUTTON_LEFT = True
            elif c == GLUT_KEY_RIGHT:
                Input.BUTTON_RIGHT = True 

    def _glkeyboard(self, c, x, y, up):
        if up:
            if c == 'z':
                Input.BUTTON_A = False
            elif c == 'x':
                Input.BUTTON_B = False
            elif c == chr(13):
                Input.BUTTON_START = False
            elif c == chr(8):
                Input.BUTTON_SELECT = False
                
        else:
            if c == 'z':
                Input.BUTTON_A = True  
            elif c == 'x':
                Input.BUTTON_B = True  
            elif c == chr(13):
                Input.BUTTON_START = True
            elif c == chr(8):
                Input.BUTTON_SELECT = True
                


         
