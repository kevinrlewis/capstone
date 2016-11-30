from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
import kivy
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import Canvas
from kivy.uix.behaviors import ButtonBehavior
from kivy.vector import Vector
from kivy.uix.widget import Widget
import kivy.input
import time
import index

class CaesarShiftPage():
    def __init__(self):
        pass


    def create(self):
        self.r = RelativeLayout()
        self.tb = index.TopBar().create('Caesar Shift Cipher')


        self.r.add_widget(self.tb)
        return self.r
