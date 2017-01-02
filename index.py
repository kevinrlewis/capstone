import kivy
import kivy.input
import time
import os
import sys
sys.path.insert(0, '/home/kevin/Documents/COS397/project-crypto/capstone/Ciphers')
import caesar

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import Canvas
from kivy.vector import Vector


from collections import deque

kv = '''
<CircularButton>:
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size
'''

Builder.load_string(kv)
try:
    os.remove('log')
except OSError:
    print 'file does not exist'
f = open('log', 'a')

class MyApp(App):
    topbar = None
    current = None
    uptrail = []
    trail = []
    def build(self):
        f.write("starting app...\n")
        global root
        root = FloatLayout()

        #mainpage to start the app
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
        f.write('main page entered\n')
        MyApp.current = self
        MyApp.trail = []
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Welcome")
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
        f.write('junior code breakers button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(JCBPage().create())

    def pressed_mc(self, *args):
        f.write('main contents button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MC().create())

    def pressed_ts(self, *args):
        f.write('teachers section button pressed\n')

class JCBPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Junior Code Breakers entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create('Junior Codebreakers')
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
                            on_release=self.caesarpressed)
        self.pigpen = Button(text = 'Pigpen Cipher',
                            pos_hint = {'center_y':.5},
                            size_hint = (.9,.06))
        self.pigpengrave = Button(text = 'Pigpen Gravestone',
                            pos_hint = {'center_y':.375},
                            size_hint = (.9,.06))
        self.atbash = Button(text = 'Atbash Cipher',
                            pos_hint = {'center_y':.25},
                            size_hint = (.9,.06),
                            on_release=self.atbashpressed)
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
        f.write('caesar shift button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CaesarShiftPage().create())

    def atbashpressed(self, *args):
        f.write('atbash button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AtbashPage().create())

################################################################################
#Begin Atbash Cipher Page
################################################################################
class AtbashPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('atbash page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.stralpha = ''.join(self.alpha)
        self.newalpha = self.alpha[::-1]

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Atbash Cipher")
        self.active = RelativeLayout(pos_hint = {'bottom':1},
                                    size_hint = (1,.5))
        self.passive = RelativeLayout(pos_hint = {'top':1},
                                    size_hint = (1,.5))

        with open('texts/atbashciphertext.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.125, 'top':.35},
                            size_hint = (.5,.5),
                            font_size = 13)

        self.atbashimage = Image(source = 'pics/BABEL.bmp',
                                    pos_hint = {'x':.47, 'top':.75},
                                    size_hint = (.75,.75))

        self.imagetext = Label(text = 'The Little Tower of Babel\n' +
                                        ' Pieter Bruegal the Elder (1563)',
                                        pos_hint = {'x':.75, 'top':.1},
                                        size_hint = (.2,.2),
                                        font_size = 11)

        self.spacebox = CheckBox(pos_hint = {'x':.25, 'y':.3},
                                size_hint = (.05,.05))
        self.cboxlabel = Label(text = 'Keep Spaces\nBetween Words',
                                pos_hint = {'x':.1, 'y':.3},
                                size_hint = (.05,.05))

        self.alabel = Label(text = 'Plaintext Alphabet',
                            pos_hint = {'x':.7, 'top':.7},
                            size_hint = (.27,.1))
        self.alphabet = TextInput(text = self.stralpha,
                                    pos_hint = {'x':.7, 'top':.6},
                                    size_hint = (.27,.1),
                                    disabled = True)

        self.clabel = Label(text = 'Ciphertext Alphabet',
                            pos_hint = {'x':.7, 'top':.5},
                            size_hint = (.27,.1))

        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet = TextInput(text = self.strnewalpha,
                                    pos_hint = {'x':.7, 'top':.4},
                                    size_hint = (.27,.1),
                                    disabled = True)

        self.plaintextinput = TextInput(pos_hint = {'x':.2, 'top':.2},
                                    size_hint = (.35, .15))
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.275},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.2},
                                            size_hint = (.35, .15),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.275},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.025, 'top':.2},
                                        size_hint = (.15,.15),
                                        on_release = self.encipherPressed)


        self.passive.add_widget(self.text)
        self.passive.add_widget(self.atbashimage)
        self.passive.add_widget(self.imagetext)

        self.active.add_widget(self.spacebox)
        self.active.add_widget(self.cboxlabel)
        self.active.add_widget(self.alabel)
        self.active.add_widget(self.alphabet)
        self.active.add_widget(self.clabel)
        self.active.add_widget(self.cipheralphabet)
        self.active.add_widget(self.plaintextinput)
        self.active.add_widget(self.plaintextlabel)
        self.active.add_widget(self.ciphertextdisplay)
        self.active.add_widget(self.ciphertextlabel)
        self.active.add_widget(self.encipherbutton)

        self.r.add_widget(self.tb)
        self.r.add_widget(self.passive)
        self.r.add_widget(self.active)
        return self.r

    def atbashen(self, text, spaces, *args):
        enciphered = ""
        text = text.lower()

        for letter in text:
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    enciphered += self.newalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "

        return enciphered

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.atbashen(self.plaintextinput.text, self.spacebox.active)
        self.ciphertextdisplay.text = enciphered

################################################################################
#End Atbash Cipher Page
################################################################################


################################################################################
#Begin Caesar Shift Page
################################################################################
class CaesarShiftPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('caesar shift page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])


        self.stralpha = ''.join(self.alpha)
        #setup layouts
        self.r = RelativeLayout()
        self.active = RelativeLayout(pos_hint = {'bottom':1},
                                    size_hint = (1,.5))
        self.passive = RelativeLayout(pos_hint = {'top':1},
                                    size_hint = (1,.5))

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Caesar Shift Cipher")

        #elements of the page
        self.spacebox = CheckBox(pos_hint = {'x':.25, 'y':.5},
                                size_hint = (.05,.05))
        self.cboxlabel = Label(text = 'Keep Spaces Between Words',
                                pos_hint = {'x':.1, 'y':.5},
                                size_hint = (.05,.05))
        self.shiftlabel = Label(text = 'Use Arrows to Change Shift Amount',
                                pos_hint = {'x':.125, 'y':.7},
                                size_hint = (.05,.05))
        self.decrem = Button(text = '<', pos_hint = {'x':0, 'top':.65},
                            size_hint = (.05,.05),
                            on_release = self.decr)
        self.shiftnum = Label(text = '0', font_size = '20sp', pos_hint = {'x':.05, 'top':.65},
                            size_hint = (.05,.05))
        self.increm = Button(text = '>', pos_hint = {'x':.1, 'top':.65},
                            size_hint = (.05,.05),
                            on_release = self.incr)

        self.alabel = Label(text = 'Plaintext Alphabet',
                            pos_hint = {'x':.5, 'top':.9},
                            size_hint = (.27,.1))
        self.alphabet = TextInput(text = self.stralpha,
                                    pos_hint = {'x':.5, 'top':.8},
                                    size_hint = (.27,.1),
                                    disabled = True)

        self.clabel = Label(text = 'Ciphertext Alphabet',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = (.27,.1))

        self.newalpha.rotate(-(int(self.shiftnum.text)))
        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet = TextInput(text = self.strnewalpha,
                                    pos_hint = {'x':.5, 'top':.6},
                                    size_hint = (.27,.1),
                                    disabled = True)

        self.plaintextinput = TextInput(pos_hint = {'x':.2, 'top':.4},
                                    size_hint = (.35, .35))
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.475},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.4},
                                            size_hint = (.35, .35),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.475},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.025, 'top':.3},
                                        size_hint = (.15,.2),
                                        on_release = self.encipherPressed)

        with open('texts/caesarciphertext.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.2, 'top':.6},
                            size_hint = (.5,.5))

        self.caesarimage = Image(source = 'pics/caesar2.bmp',
                                    pos_hint = {'x':.52, 'top':.75},
                                    size_hint = (.75,.75))
        self.imagetext = Label(text = 'Bust of Julius Caesar, from The\n' +
                                        ' Art f the Romans by H. P. Walters\n' +
                                        '(1911), The British Museum',
                                        pos_hint = {'x':.8, 'top':.03},
                                        size_hint = (.2,.2),
                                        font_size = 11)

        self.active.add_widget(self.shiftlabel)
        self.active.add_widget(self.cboxlabel)
        self.active.add_widget(self.spacebox)
        self.active.add_widget(self.decrem)
        self.active.add_widget(self.shiftnum)
        self.active.add_widget(self.increm)
        self.active.add_widget(self.alabel)
        self.active.add_widget(self.alphabet)
        self.active.add_widget(self.clabel)
        self.active.add_widget(self.cipheralphabet)
        self.active.add_widget(self.plaintextinput)
        self.active.add_widget(self.plaintextlabel)
        self.active.add_widget(self.ciphertextdisplay)
        self.active.add_widget(self.ciphertextlabel)
        self.active.add_widget(self.encipherbutton)

        self.passive.add_widget(self.text)
        self.passive.add_widget(self.caesarimage)
        self.passive.add_widget(self.imagetext)

        self.r.add_widget(self.passive)
        self.r.add_widget(self.active)
        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.caesarEncrypt(self.shiftnum.text, self.plaintextinput.text, self.spacebox.active)
        self.ciphertextdisplay.text = enciphered


    #encrypts text by a given shift amount
    def caesarEncrypt(self, shift, text, spaces, *args):
        alpha = list(self.alphabet.text)

        newalpha = list(self.cipheralphabet.text)
        f.write('\n' + str(alpha))
        f.write('\n' + str(newalpha))
        text = text.lower()

        f.write('\nshift: ' + str(shift) + ' text: ' + str(text) + ' spaces: ' + str(spaces) + '\n')

        enciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if alpha[i] == letter:
                    enciphered += newalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "
        f.write('\nencipherd: ' + enciphered + '\n')
        return enciphered

    def incr(self, *args):
        self.newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])
        if(int(self.shiftnum.text) == 26):
            self.shiftnum.text = '0'
        else:
            temp = int(self.shiftnum.text) + 1
            self.shiftnum.text = str(temp)

        self.newalpha.rotate(-(int(self.shiftnum.text)))
        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet.text = self.strnewalpha

    def decr(self, *args):
        self.newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])
        if(int(self.shiftnum.text) == 0):
            pass
        else:
            temp = int(self.shiftnum.text) - 1
            self.shiftnum.text = str(temp)

        self.newalpha.rotate(-(int(self.shiftnum.text)))
        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet.text = self.strnewalpha

################################################################################
#End Caesar Shift Page
################################################################################

################################################################################
#Begin Main Contents Page
################################################################################
class MC(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('the code book description page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Code Book")

        with open('texts/thecodebook.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5))

        self.birthbutton = Button(text = "The Birth of\nCryptography",
                                        pos_hint = {'x':.68, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.birthPressed,
                                        font_size = 14)
        self.birthtext = Label(text = "The earliest codes and\nciphers from Ancient\n" +
                                        "Greece to the execution\nof Mary Queen of Scots",
                            pos_hint = {'x':.875, 'top':.9},
                            size_hint = (.1,.1),
                            font_size = 11)

        self.uncrackablebutton = Button(text = "The Uncrackable\nCode",
                                        pos_hint = {'x':.68, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.uncrackablePressed,
                                        font_size = 14)
        self.uncrackabletext = Label(text = "The invention of the\nVigenere cipher and its\n" +
                                        "decipherment by a\nVictorian genius",
                            pos_hint = {'x':.875, 'top':.725},
                            size_hint = (.1,.1),
                            font_size = 11)

        self.mechbutton = Button(text = "Mechanising\nSecrecy",
                                        pos_hint = {'x':.68, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.mechPressed,
                                        font_size = 14)
        self.mechtext = Label(text = "Cryptography in the\nGreat War, the invention\n" +
                                        "of the Enigma cipher\nmachine and the Second\nWorld War",
                            pos_hint = {'x':.875, 'top':.55},
                            size_hint = (.1,.1),
                            font_size = 11)

        self.agebutton = Button(text = "Age of the\nInternet",
                                        pos_hint = {'x':.68, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.agePressed,
                                        font_size = 14)
        self.agetext = Label(text = "Computer security and\nprivacy on-line,\n" +
                                        "including DES, the key\ndistribution problem and\n" +
                                        "public key cryptography",
                            pos_hint = {'x':.875, 'top':.375},
                            size_hint = (.1,.1),
                            font_size = 11)

        self.futurebutton = Button(text = "Future of\nCryptography",
                                        pos_hint = {'x':.68, 'top':.2},
                                        size_hint = (.15,.1),
                                        on_release = self.futurePressed,
                                        font_size = 14)
        self.futuretext = Label(text = "Will politicians restrcit\nencryption, will\n" +
                                        "steganography replace\ncryptography, and is\n" +
                                        "quantum cryptography\nuncrackable?",
                            pos_hint = {'x':.875, 'top':.2},
                            size_hint = (.1,.1),
                            font_size = 11)

        self.r.add_widget(self.birthbutton)
        self.r.add_widget(self.birthtext)
        self.r.add_widget(self.uncrackablebutton)
        self.r.add_widget(self.uncrackabletext)
        self.r.add_widget(self.mechbutton)
        self.r.add_widget(self.mechtext)
        self.r.add_widget(self.agebutton)
        self.r.add_widget(self.agetext)
        self.r.add_widget(self.futurebutton)
        self.r.add_widget(self.futuretext)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def birthPressed(self, *args):
        f.write("birth of Cryptography pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BOFC().create())

    def uncrackablePressed(self, *args):
        f.write('the uncrackable code pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(UncrackableCode().create())

    def mechPressed(self, *args):
        f.write('mechanising secrecy pressed\n')

    def agePressed(self, *args):
        f.write('age of the internet pressed\n')

    def futurePressed(self, *args):
        f.write('future of Cryptography pressed\n')

################################################################################
#End Main Contents Page
################################################################################

################################################################################
#Begin Birth of Cryptography Page
################################################################################
class BOFC(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('the birth of Cryptography page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Birth of Cryptography")

        with open('texts/birthofc.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Transposition",
                                        pos_hint = {'x':.68, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Substitution",
                                        pos_hint = {'x':.68, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Cracking the\nSubstitution\nCipher",
                                        pos_hint = {'x':.68, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Key Secrets",
                                        pos_hint = {'x':.68, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "The\nTragedy of\nMary Queen\nof Scots",
                                        pos_hint = {'x':.68, 'top':.2},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("Transposition pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(Transposition().create())

    def twoPressed(self, *args):
        f.write('Substitution pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(Substitution().create())

    def threePressed(self, *args):
        f.write('cracking the Substitution cipher pressed\n')

    def fourPressed(self, *args):
        f.write('key secrets pressed\n')

    def fivePressed(self, *args):
        f.write('tragedy of mary queen of scots pressed\n')

################################################################################
#End Birth of Cryptography Page
################################################################################

################################################################################
#Begin Transposition Page
################################################################################
class Transposition(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Transposition page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Transposition")

        with open('texts/transposition.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Railfence",
                                        pos_hint = {'x':.68, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Latin Square",
                                        pos_hint = {'x':.68, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Scytale",
                                        pos_hint = {'x':.68, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("railfence pressed\n")

    def twoPressed(self, *args):
        f.write('latin square pressed\n')

    def threePressed(self, *args):
        f.write('scytale pressed\n')

################################################################################
#End Transposition Page
################################################################################


################################################################################
#Begin Substitution Page
################################################################################
class Substitution(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Substitution page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Substitution")

        with open('texts/substitution.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Caesar\nCipher",
                                        pos_hint = {'x':.68, 'top':.875},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Kama-Sutra\nCipher",
                                        pos_hint = {'x':.68, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Pigpen\nCipher",
                                        pos_hint = {'x':.68, 'top':.625},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Atbash\nCipher",
                                        pos_hint = {'x':.68, 'top':.5},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "Affine\nCipher",
                                        pos_hint = {'x':.68, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.button6 = Button(text = "General\nMono-\nalphabetic\nCipher",
                                        pos_hint = {'x':.68, 'top':.25},
                                        size_hint = (.15,.1),
                                        on_release = self.sixPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.button6)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("caesar pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CaesarShiftPage().create())

    def twoPressed(self, *args):
        f.write('kamasutra pressed\n')

    def threePressed(self, *args):
        f.write('pigpen pressed\n')

    def fourPressed(self, *args):
        f.write('atbash pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AtbashPage().create())

    def fivePressed(self, *args):
        f.write('affine pressed\n')

    def sixPressed(self, *args):
        f.write('general Monoalphabetic pressed\n')

################################################################################
#End Birth of Cryptography Page
################################################################################

################################################################################
#Begin Uncrackable Code Page
################################################################################
class UncrackableCode(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('the uncrackable code page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Birth of Cryptography")

        with open('texts/birthofc.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Transposition",
                                        pos_hint = {'x':.68, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Substitution",
                                        pos_hint = {'x':.68, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Cracking the\nSubstitution\nCipher",
                                        pos_hint = {'x':.68, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Key Secrets",
                                        pos_hint = {'x':.68, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "The\nTragedy of\nMary Queen\nof Scots",
                                        pos_hint = {'x':.68, 'top':.2},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("Transposition pressed\n")

    def twoPressed(self, *args):
        f.write('Substitution pressed\n')

    def threePressed(self, *args):
        f.write('cracking the Substitution cipher pressed\n')

    def fourPressed(self, *args):
        f.write('key secrets pressed\n')

    def fivePressed(self, *args):
        f.write('tragedy of mary queen of scots pressed\n')

################################################################################
#End Uncrackable Code Page
################################################################################

class TopBar(ButtonBehavior):
    def __init__(self):
        pass

    def create(self, title):
        self.r = RelativeLayout(size_hint = (1,.5), pos_hint = {'y':.95})
        self.titlelabel = Label(text = title,
                                pos_hint = {'x':.5},
                                size_hint = (.05,.05),
                                font_size = '30sp')
        self.back = Button(text = '<', size_hint = (.05,.07), pos_hint = {'x':0},
                            on_release = MyApp.topbar.back_press)
        self.up = Button(text = 'up', size_hint = (.05,.07), pos_hint = {'x':.055},
                            on_release = self.up_press)
        self.home = Button(text = 'home', size_hint = (.06,.07), pos_hint = {'right':1},
                            on_release = self.home_press)
        self.index = Button(text = '?', size_hint = (.05,.07), pos_hint = {'right':.935},
                            on_release = self.index_press)

        if(MyApp.trail == []):
            self.back.disabled = True
        else:
            self.back.disabled = False

        if(MyApp.uptrail == []):
            self.up.disabled = True
        else:
            self.up.disabled = False

        self.r.add_widget(self.titlelabel)
        self.r.add_widget(self.back)
        self.r.add_widget(self.up)
        self.r.add_widget(self.home)
        self.r.add_widget(self.index)
        return self.r

    def back_press(self, *args):
        f.write('back pressed\n')
        f.write(str(MyApp.trail))
        f.write('\n')
        root.clear_widgets()
        page = MyApp.trail.pop()
        root.add_widget(page.create())

    def up_press(self, *args):
        f.write('up pressed\n')

    def home_press(self, *args):
        f.write('home pressed\n')
        root.clear_widgets()
        root.add_widget(MainPage().create())

    def index_press(self, *args):
        f.write('index pressed\n')

if __name__ == '__main__':
    f.write("-----------------------------------------------------\n")
    f.write(time.strftime("%d/%m/%Y %I:%M:%S"))
    f.write('\n')
    MyApp().run()
    f.write("-----------------------------------------------------\n")
