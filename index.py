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
import jcbpages

kv = '''
<CircularButton>:
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size
'''

Builder.load_string(kv)
f = open('log', 'a')

class MyApp(App):
    def build(self):
        f.write("starting app...\n")
        global root
        root = FloatLayout()

        #mainpage
        mainpage = MainPage()

        #jcb
        #jcb = JCBPage()

        #root.add_widget(jcb.create())
        root.add_widget(mainpage.create())


        return root

class MainPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        self.tb = TopBar().create("")
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

        self.r.add_widget(self.tb)
        self.r.add_widget(self.jcb)
        self.r.add_widget(self.mc)
        self.r.add_widget(self.ts)
        return self.r

    def pressed_jcb(self, *args):
        f.write('junior code breakers entered 2\n')
        root.clear_widgets()
        root.add_widget(JCBPage().create())

    def pressed_mc(self, *args):
        f.write('main contents entered 2\n')

    def pressed_ts(self, *args):
        f.write('teachers section entered 2\n')

class JCBPage():
    def __init__(self):
        pass

    def create(self):
        #root layout of the instance
        self.r = RelativeLayout()
        self.tb = TopBar().create('Junior Codebreakers')
        self.leftc = RelativeLayout(size_hint = (.5,.6),
                                    pos_hint = {'left':1})
        self.rightc = RelativeLayout(size_hint = (.5,.6),
                                    pos_hint = {'right':1})
        self.buttonlay = RelativeLayout(pos_hint = {'center_x':.5, 'center_y':.65},
                                        size_hint = (.6,1))

        #column 1
        self.railfence = Button(text = 'Transposition - Railfence',
                            pos_hint = {'center_y':1},
                            size_hint = (.9,.06))
        self.latin = Button(text = 'Transposition - Latin Square',
                            pos_hint = {'center_y':.875},
                            size_hint = (.9,.06))
        self.scytale = Button(text = 'Transposition - Scytale',
                            pos_hint = {'center_y':.75},
                            size_hint = (.9,.06))
        self.caesar = Button(text = 'Caesar Cipher',
                            pos_hint = {'center_y':.625},
                            size_hint = (.9,.06),
                            on_release = self.caesarpressed)
        self.pigpen = Button(text = 'Pigpen Cipher',
                            pos_hint = {'center_y':.5},
                            size_hint = (.9,.06))
        self.pigpengrave = Button(text = 'Pigpen Gravestone',
                            pos_hint = {'center_y':.375},
                            size_hint = (.9,.06))
        self.atbash = Button(text = 'Atbash Cipher',
                            pos_hint = {'center_y':.25},
                            size_hint = (.9,.06))
        self.mono = Button(text = 'General Monoalphabetic',
                            pos_hint = {'center_y':.125},
                            size_hint = (.9,.06))
        self.leftc.add_widget(self.railfence)
        self.leftc.add_widget(self.latin)
        self.leftc.add_widget(self.scytale)
        self.leftc.add_widget(self.caesar)
        self.leftc.add_widget(self.pigpen)
        self.leftc.add_widget(self.pigpengrave)
        self.leftc.add_widget(self.atbash)
        self.leftc.add_widget(self.mono)

        #column 2
        self.howfreq = Button(text = 'How Frequency Analysis Works',
                            pos_hint = {'center_y':1},
                            size_hint = (.9,.06))
        self.digraph = Button(text = 'Digraph Substitution',
                            pos_hint = {'center_y':.875},
                            size_hint = (.9,.06))
        self.playfair = Button(text = 'Playfair Cipher',
                            pos_hint = {'center_y':.75},
                            size_hint = (.9,.06))
        self.homo = Button(text = 'Homophonic Cipher',
                            pos_hint = {'center_y':.625},
                            size_hint = (.9,.06))
        self.morse = Button(text = 'Morse Code',
                            pos_hint = {'center_y':.5},
                            size_hint = (.9,.06))
        self.dancing = Button(text = 'Dancing Men Cipher',
                            pos_hint = {'center_y':.375},
                            size_hint = (.9,.06))
        self.meetenigma = Button(text = 'Meet the Enigma Machine',
                            pos_hint = {'center_y':.25},
                            size_hint = (.9,.06))
        self.codetalkers = Button(text = 'Codetalkers',
                            pos_hint = {'center_y':.125},
                            size_hint = (.9,.06))
        self.rightc.add_widget(self.howfreq)
        self.rightc.add_widget(self.digraph)
        self.rightc.add_widget(self.playfair)
        self.rightc.add_widget(self.homo)
        self.rightc.add_widget(self.morse)
        self.rightc.add_widget(self.dancing)
        self.rightc.add_widget(self.meetenigma)
        self.rightc.add_widget(self.codetalkers)


        self.buttonlay.add_widget(self.leftc)
        self.buttonlay.add_widget(self.rightc)
        self.r.add_widget(self.tb)
        self.r.add_widget(self.buttonlay)
        return self.r

    def caesarpressed(self, *args):
        f.write('caesar shift page entered\n')
        root.clear_widgets()
        root.add_widget(jcbpages.CaesarShiftPage().create())

class TopBar():
    def __init__(self):
        pass

    def create(self, title):
        self.r = RelativeLayout(size_hint = (1,.5), pos_hint = {'y':.95})
        self.titlelabel = Label(text = title,
                                pos_hint = {'x':.5},
                                size_hint = (.05,.05))
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

        self.r.add_widget(self.titlelabel)
        self.r.add_widget(self.back)
        self.r.add_widget(self.forward)
        self.r.add_widget(self.up)
        self.r.add_widget(self.home)
        self.r.add_widget(self.index)
        return self.r


    def back_press(self, *args):
        f.write('back pressed: \n')
        f.write(str(self))

    def forward_press(self, *args):
        f.write('forward pressed\n')

    def up_press(self, *args):
        f.write('up pressed\n')

    def home_press(self, *args):
        f.write('home pressed\n')

    def index_press(self, *args):
        f.write('index pressed\n')

if __name__ == '__main__':
    f.write("-----------------------------------------------------\n")
    f.write(time.strftime("%d/%m/%Y %I:%M:%S"))
    f.write('\n')
    MyApp().run()
    f.write("-----------------------------------------------------\n")
