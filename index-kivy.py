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

kv = '''
<CircularButton>:
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size
'''

Builder.load_string(kv)

f = open('log', 'r+')

class MyApp(App):
    def build(self):
        f.write("starting app...\n")
        root = FloatLayout()

        #topbar
        topbar = TopBar()
        tb = topbar.r


        #mainpage
        mainpage = MainPage()

        root.add_widget(tb)
        root.add_widget(mainpage.r)


        return root

class MainPage(ButtonBehavior):
    def __init__(self):
        self.r = RelativeLayout()
        self.jcb = Button(text = 'Junior Code Breakers',
                                    size_hint = (.2,.3),
                                    pos_hint = {'center_x': .25, 'center_y': .55},
                                    on_release=self.pressed_jcb)
        self.mc = Button(text = 'Main Contents',
                                    size_hint = (.2,.3),
                                    pos_hint = {'center_x': .5, 'center_y': .55},
                                    on_release=self.pressed_mc)
        self.ts = Button(text = 'Teachers Section',
                                    size_hint = (.2,.3),
                                    pos_hint = {'center_x': .75, 'center_y': .55},
                                    on_release=self.pressed_ts)

        self.r.add_widget(self.jcb)
        self.r.add_widget(self.mc)
        self.r.add_widget(self.ts)

    def pressed_jcb(self, *args):
        f.write('junior code breakers entered 2\n')

    def pressed_mc(self, *args):
        f.write('main contents entered 2\n')

    def pressed_ts(self, *args):
        f.write('teachers section entered 2\n')


class TopBar():
    def __init__(self):
        self.r = RelativeLayout(size_hint = (1,.5), pos_hint = {'y':.95})
        self.back = Button(text = '<', size_hint = (.05,.07), pos_hint = {'x':0},
                            on_release = self.back_press)
        self.forward = Button(text = '>', size_hint = (.05,.07), pos_hint = {'x':.055},
                            on_release = self.forward_press)
        self.up = Button(text = 'up', size_hint = (.05,.07), pos_hint = {'x':.11},
                            on_release = self.up_press)
        self.home = Button(text = 'home', size_hint = (.06,.07), pos_hint = {'right':1},
                            on_release = self.home_press)
        self.index = Button(text = '?', size_hint = (.05,.07), pos_hint = {'right':.935},
                            on_release = self.index_press)

        self.r.add_widget(self.back)
        self.r.add_widget(self.forward)
        self.r.add_widget(self.up)
        self.r.add_widget(self.home)
        self.r.add_widget(self.index)

    def back_press(self, *args):
        f.write('back pressed\n')

    def forward_press(self, *args):
        f.write('forward pressed\n')

    def up_press(self, *args):
        f.write('up pressed\n')

    def home_press(self, *args):
        f.write('home pressed\n')

    def index_press(self, *args):
        f.write('index pressed\n')

if __name__ == '__main__':
    MyApp().run()
