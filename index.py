#author: Kevin Lewis
#images, videos, and text by Simon Singh: http://simonsingh.net/

#imports
################################################################################
import kivy
from kivy.config import Config
Config.set('graphics','resizable',0)
import kivy.input
import time
import os
import sys
import webbrowser
import binascii
import math
import base64
import hashlib
import blake2

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
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import Canvas, InstructionGroup
from kivy.vector import Vector
from kivy.utils import escape_markup
from kivy.core.window import Window


from collections import deque
from random import shuffle
from random import randint
from random import choice
from fractions import gcd
from Crypto.Cipher import AES, Blowfish
from Crypto import Random
from struct import pack
from flask import Flask, render_template

################################################################################
################################################################################
#log file
try:
    os.remove('log')
except OSError:
    print 'file does not exist'
f = open('log', 'a')
################################################################################



################################################################################
#Builds the App
################################################################################
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

        #testing
        test = SymmetricPage()

        #production
        root.add_widget(mainpage.create())

        #testing
        #root.add_widget(test.create())

        return root
################################################################################

################################################################################
#Begin Home Page
################################################################################
class MainPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('main page entered\n')
        MyApp.current = self
        #creates a trail of how the user got to a certain Page
        #used for the back button in the top bar
        MyApp.trail = []
        self.btrowtop = .4

        #initialize the topbar
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("")

        #setup layouts
        self.r = RelativeLayout()
        self.title = RelativeLayout()

        #button to get to the junior codebreakers section
        self.jcb = Button(text = 'Junior Code Breakers',
                                    size_hint = (.3,.2),
                                    pos_hint = {'x': .05, 'top': .75},
                                    on_release=self.pressed_jcb)
        #button to get to the main contents section
        self.mc = Button(text = 'Main Contents',
                                    size_hint = (.3,.2),
                                    pos_hint = {'x': .415, 'top': .75},
                                    on_release=self.pressed_mc)

        #button to get to the highlights section of the application
        self.highlightsbutton = Button(text = '[b][color=ff6600]Highlights[/color][/b]',
                                    size_hint = (.15,.1),
                                    pos_hint = {'x': .215, 'top':self.btrowtop},
                                    on_release=self.pressed_highlights,
                                    markup = True)

        self.extra = Button(text = "Extras",
                                    size_hint = (.15,.1),
                                    pos_hint = {'x': .415, 'top':self.btrowtop},
                                    on_release = self.pressed_extra)

        self.simonbutton = Button(text = "Simon Singh",
                                    size_hint = (.15,.1),
                                    pos_hint = {'x': .415, 'top':self.btrowtop})

        self.codebook = Button(text = "The Code\nBook",
                                    size_hint = (.15,.1),
                                    pos_hint = {'x': .215, 'top':self.btrowtop},
                                    halign = 'center')

        self.simonpic = Image(source = 'pics/simong2.png',
                                    size_hint = (.8,.8),
                                    pos_hint = {'x': .5, 'top': 1})

        self.link = Label(text = '[ref=simon][color=ffff00]simonsingh.net[/color][/ref]',
                                    size_hint = (.2,.2),
                                    pos_hint = {'x':.01, 'top': 1},
                                    markup = True,
                                    on_ref_press = self.linkpress)

        #set the image title
        titlestr = 'THE CODE BOOK'

        x = -.045
        top = .2
        #loop through the letters to append images to the title layout
        for letter in titlestr:
            tempimage = Image()
            if letter == ' ':
                x += .035
            else:
                tempimage.source = 'pics/title/TYPE' + letter + '2.png'
                tempimage.pos_hint = {'x': x, 'top': top}
                tempimage.size_hint = (.2,.2)
                x += .08
                self.title.add_widget(tempimage)

        #add widgets to the main layout
        self.r.add_widget(self.highlightsbutton)
        self.r.add_widget(self.link)
        self.r.add_widget(self.simonpic)
        self.r.add_widget(self.extra)
        self.r.add_widget(self.title)
        self.r.add_widget(self.tb)
        self.r.add_widget(self.jcb)
        self.r.add_widget(self.mc)
        return self.r

    #function is called when the highlights button is pressed
    #adds page to the trail
    #clears all of the widgets from the root
    #adds the new page to the root
    def pressed_highlights(self, *args):
        f.write('highlights button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HighlightsPage().create())

    #function is called when the junior codebreakers button is pressed
    #adds page to the trail
    #clears all of the widgets from the root
    #adds the new page to the root
    def pressed_jcb(self, *args):
        f.write('junior code breakers button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(JCBPage().create())

    #function is called when the main contents button is pressed
    #adds page to the trail
    #clears all of the widgets from the root
    #adds the new page to the root
    def pressed_mc(self, *args):
        f.write('main contents button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MC().create())

    def linkpress(self, *args):
        f.write('opening simonsingh.net...\n')
        webbrowser.open("http://simonsingh.net/")

    def pressed_extra(self, *args):
        f.write('extra stuff pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CurrentCryptographyPage().create())

################################################################################
#End Home Page
################################################################################

################################################################################
#Begin Current Cryptography Page
#-Symmetric
#   -AES - block
#-Asymmetric
#   -SSH - protocol
#-Hash
#   -MD5
#   -SHA1
#   -SHA256
#   -BLAKE2
################################################################################
class CurrentCryptographyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Current Cryptography page entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('Current Cryptography')
        self.x = .75
        self.btnsize = (.2,.1)

        with open('texts/currentcryptography.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.425, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/hacker.jpg',
                            pos_hint = {'x':.05, 'top':.7},
                            size_hint = (.6,.6))

        #buttons
        self.symmetric = Button(text = 'Symmetric\nAlgorithms',
                            pos_hint = {'x':self.x, 'top':.65},
                            size_hint = self.btnsize,
                            on_release = self.symmetricpressed)
        self.asymmetric = Button(text = 'Asymmetric\nAlgorithms',
                            pos_hint = {'x':self.x, 'top':.45},
                            size_hint = self.btnsize,
                            on_release = self.asymmetricpressed)
        self.hash = Button(text = 'Hash\nEncryption',
                            pos_hint = {'x':self.x, 'top':.25},
                            size_hint = self.btnsize,
                            on_release = self.hashingpressed)

        #add widgets to the main layout
        self.r.add_widget(self.image)
        self.r.add_widget(self.text)
        self.r.add_widget(self.symmetric)
        self.r.add_widget(self.asymmetric)
        self.r.add_widget(self.hash)
        self.r.add_widget(self.tb)
        return self.r

    def symmetricpressed(self, *args):
        f.write('symmetric button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SymmetricPage().create())

    def asymmetricpressed(self, *args):
        f.write('asymmetric button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AsymmetricPage().create())

    def hashingpressed(self, *args):
        f.write('hashing button pressed\n')
        #md5, sha1, sha256 interactive
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HashingPage().create())
################################################################################
#End Current Cryptography Page
################################################################################

################################################################################
#Begin Symmetric Page
################################################################################
class SymmetricPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Symmetric page entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('Symmetric Algorithms')
        self.x = .75
        self.btnsize = (.2,.1)

        with open('texts/symmetric.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/symmetric.png',
                            pos_hint = {'x':-.075, 'top':1.05},
                            size_hint = (.9,.9))

        #buttons
        self.aes = Button(text = 'AES',
                            pos_hint = {'x':self.x, 'top':.65},
                            size_hint = self.btnsize,
                            on_release = self.aespressed)

        self.link = Label(text = 'Image from: [color=ffff00][ref=pk]http://ccm.net/contents/130-private-key-or-secret-key-cryptography[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)

        self.linkinfo = Label(text = 'Information from: [color=ffff00][ref=pk]https://en.wikipedia.org/wiki/Symmetric-key_algorithm[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.12},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)



        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.link)
        self.r.add_widget(self.linkinfo)
        self.r.add_widget(self.image)
        self.r.add_widget(self.aes)
        self.r.add_widget(self.tb)
        return self.r

    def aespressed(self, *args):
        f.write('aes button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AESPage().create())

    def link1(self, *args):
        f.write('opening http://ccm.net/contents/130-private-key-or-secret-key-cryptography ...\n')
        webbrowser.open("http://ccm.net/contents/130-private-key-or-secret-key-cryptography")

    def link2(self, *args):
        f.write('opening https://en.wikipedia.org/wiki/Symmetric-key_algorithm ...\n')
        webbrowser.open("https://en.wikipedia.org/wiki/Symmetric-key_algorithm")
################################################################################
#End Symmetric Page
################################################################################

################################################################################
#Begin AES Page
################################################################################
class AESPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('aes page entered\n')
        MyApp.current = self
        self.cipher = ''
        self.secret = ''
        self.encoded = ''

        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('AES')
        self.x = .75
        self.btnsize = (.2,.1)
        self.txtinsz = (.475,.2)

        with open('texts/aes.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True)

        self.link1 = Label(text = 'Information from: [color=ffff00][ref=aes]http://aesencryption.net/[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)
        self.link2 = Label(text = 'Algorithm from: [color=ffff00][ref=aesalg]http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)

        self.plaintextlabel = Label(text = "Plaintext",
                            pos_hint = {'x':.4375, 'top':.825},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.plaintextinput = maxinput(text = '',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = self.txtinsz)
        self.plaintextinput.max_chars = 32

        self.ciphertextlabel = Label(text = "Ciphertext",
                            pos_hint = {'x':.4375, 'top':.525},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.ciphertextdisplay = Label(text = '',
                            pos_hint = {'x':0, 'top':.65},
                            size_hint = (1,1),
                            markup = True,
                            font_size = 24)

        self.encryptbutton = Button(text = 'Encrypt',
                            pos_hint = {'x':.5, 'top':.495},
                            size_hint = (.475,.05),
                            on_release = self.encryptpressed)

        self.decryptbutton = Button(text = 'Decrypt',
                            pos_hint = {'x':.5, 'top':.425},
                            size_hint = (.475,.05),
                            on_release = self.decryptpressed,
                            disabled = True)

        self.decryptdisplay = Label(text = '',
                            pos_hint = {'x':0, 'top':.6},
                            size_hint = (1,1),
                            markup = True,
                            font_size = 24)

        self.instructions = Label(text = 'Type your message into the plaintext box\n' +
                                        'and press the encrypt button. The AES encrypted\n' +
                                        'message will display at the bottom of the page.\n' +
                                        'Pressing the decrypt button will decrypt the AES\n' +
                                        'encrypted message and display it at the bottom of\n' +
                                        'the screen.',
                            pos_hint = {'x':.135, 'top':.725},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/first_round_process.jpg',
                            pos_hint = {'x':.025, 'top':.5},
                            size_hint = (.3,.3))

        self.imagelabel = Label(text = 'TutorialsPoint',
                            pos_hint = {'x':0, 'top':.285},
                            size_hint = (.2,.2),
                            font_size = 10)

        #add widgets to the main layout
        self.r.add_widget(self.image)
        self.r.add_widget(self.imagelabel)
        self.r.add_widget(self.text)
        self.r.add_widget(self.link1)
        self.r.add_widget(self.link2)
        self.r.add_widget(self.plaintextlabel)
        #self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.encryptbutton)
        self.r.add_widget(self.decryptbutton)
        self.r.add_widget(self.decryptdisplay)
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.tb)
        return self.r

    def encryptpressed(self, *args):
        f.write('encrypt button pressed\n')
        text = self.plaintextinput.text
        self.encoded = self.encrypt(text)
        self.ciphertextdisplay.text = '[color=ff0000][b]' + self.encoded + '[/b][/color]'
        self.decryptbutton.disabled = False
        self.decryptdisplay.text = ''

    def decryptpressed(self, *args):
        f.write('decrypt button pressed\n')
        decoded = self.decrypt(self.encoded)
        self.decryptbutton.disabled = True
        if decoded == 'hello':
            self.decryptdisplay.font_size = 500
            self.decryptdisplay.pos_hint = {'x':0, 'top':1}
        else:
            self.decryptdisplay.font_size = 18
            self.decryptdisplay.pos_hint = {'x':0, 'top':.6}
        self.decryptdisplay.text = '[color=ff0000][b]' + decoded + '[/b][/color]'


    def encrypt(self, text, *args):
        #http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/
        # the block size for the cipher object; must be 16 per FIPS-197
        BLOCK_SIZE = 16

        # the character used for padding--with a block cipher such as AES, the value
        # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'

        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        # one-liners to encrypt/encode a string
        # encrypt with AES, encode with base64
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        # generate a random secret key
        self.secret = os.urandom(BLOCK_SIZE)

        # create a cipher object using the random secret
        self.cipher = AES.new(self.secret)

        # encode a string
        encoded = EncodeAES(self.cipher, text)
        f.write('Encrypted string:' + encoded + '\n')
        return encoded

    def decrypt(self, encoded, *args):
        f.write('decrypting aes...\n')
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        # decode the encoded string
        decoded = DecodeAES(self.cipher, encoded)
        f.write('Decrypted string:' + decoded + '\n')
        return decoded

    def link1(self, *args):
        f.write('opening http://aesencryption.net/ ...\n')
        webbrowser.open("http://aesencryption.net/")

    def link2(self, *args):
        f.write('opening http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/ ...\n')
        webbrowser.open("http://www.codekoala.com/posts/aes-encryption-python-using-pycrypto/")
################################################################################
#End AES Page
################################################################################

################################################################################
#Begin Asymmetric Page - SSH - Bitcoin/LiteCoin
################################################################################
class AsymmetricPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Asymmetric page entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('Asymmetric Algorithms')
        self.x = .75
        self.btnsize = (.2,.1)

        with open('texts/asymmetric.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.875},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/asymmetric.png',
                            pos_hint = {'x':.2, 'top':.65},
                            size_hint = (.5,.5))

        #buttons
        self.ssh = Button(text = 'SSH',
                            pos_hint = {'x':self.x, 'top':.65},
                            size_hint = self.btnsize,
                            on_release = self.sshpressed)

        self.link = Label(text = 'Information from: [color=ffff00][ref=pk]https://en.wikipedia.org/wiki/Public-key_cryptography[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)

        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.link)
        self.r.add_widget(self.image)
        self.r.add_widget(self.ssh)
        self.r.add_widget(self.tb)
        return self.r

    def sshpressed(self, *args):
        f.write('ssh button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SSHPage().create())

    def link1(self, *args):
        f.write('opening https://en.wikipedia.org/wiki/Public-key_cryptography ...\n')
        webbrowser.open("https://en.wikipedia.org/wiki/Public-key_cryptography")
################################################################################
#End Asymmetric Page
################################################################################

################################################################################
#Begin SSH Page
################################################################################
class SSHPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('SSH page entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('SSH Protocol')
        self.x = .75
        self.btnsize = (.2,.1)

        with open('texts/ssh.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.875},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/ssh.jpg',
                            pos_hint = {'x':.15, 'top':.75},
                            size_hint = (.7,.7))


        self.link = Label(text = 'Information and image from: [color=ffff00][ref=ssh]https://www.ssh.com/ssh/protocol/[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)

        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.link)
        self.r.add_widget(self.image)
        self.r.add_widget(self.tb)
        return self.r

    def link1(self, *args):
        f.write('opening https://www.ssh.com/ssh/protocol/ ...\n')
        webbrowser.open("https://www.ssh.com/ssh/protocol/")
################################################################################
#End SSH Page
################################################################################

################################################################################
#Begin Hashing Page - MD5 - SHA1 - SHA256 - BLAKE2
################################################################################
class HashingPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Hashing page entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('Cryptographic Hash Functions')
        self.x = .75
        self.btnsize = (.2,.1)

        with open('texts/hashing.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/crypthash.png',
                            pos_hint = {'x':-.05, 'top':.9},
                            size_hint = (1,1))

        #buttons
        self.md5 = Button(text = 'MD5',
                            pos_hint = {'x':self.x, 'top':.65},
                            size_hint = self.btnsize,
                            on_release = self.md5pressed)

        self.sha1 = Button(text = 'SHA-1 and SHA-256',
                            pos_hint = {'x':self.x, 'top':.45},
                            size_hint = self.btnsize,
                            on_release = self.sha1pressed)

        self.blake2 = Button(text = 'BLAKE2',
                            pos_hint = {'x':self.x, 'top':.25},
                            size_hint = self.btnsize,
                            on_release = self.blake2pressed)

        self.linkinfo = Label(text = 'Information and image from: [color=ffff00][ref=pk]https://en.wikipedia.org/wiki/Cryptographic_hash_function[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.12},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)



        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.linkinfo)
        self.r.add_widget(self.image)
        self.r.add_widget(self.md5)
        self.r.add_widget(self.sha1)
        self.r.add_widget(self.blake2)
        self.r.add_widget(self.tb)
        return self.r

    def md5pressed(self, *args):
        f.write('aes button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MD5Page().create())

    def sha1pressed(self, *args):
        f.write('sha1 button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SHA1Page().create())

    def blake2pressed(self, *args):
        f.write('blake2 button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BLAKE2Page().create())

    def link2(self, *args):
        f.write('opening https://en.wikipedia.org/wiki/Cryptographic_hash_function ...\n')
        webbrowser.open("https://en.wikipedia.org/wiki/Cryptographic_hash_function")
################################################################################
#End Hashing Page
################################################################################

################################################################################
#Begin MD5 Page
################################################################################
class MD5Page(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('MD5 page entered\n')
        MyApp.current = self
        self.cipher = ''
        self.secret = ''
        self.encoded = ''

        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('MD5')
        self.x = .75
        self.btnsize = (.2,.1)
        self.txtinsz = (.475,.2)

        with open('texts/md5.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.91},
                            size_hint = (.2,.2),
                            markup = True)

        self.linkinfo = Label(text = 'Information from: [color=ffff00][ref=md5]https://en.wikipedia.org/wiki/MD5[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)
        self.linkalg = Label(text = 'Algorithm from: [color=ffff00][ref=md5alg]https://docs.python.org/2/library/hashlib.html[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)

        self.plaintextlabel = Label(text = "Plaintext",
                            pos_hint = {'x':.4375, 'top':.825},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.plaintextinput = maxinput(text = '',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = self.txtinsz)
        self.plaintextinput.max_chars = 32

        self.ciphertextlabel = Label(text = "Ciphertext",
                            pos_hint = {'x':.4375, 'top':.525},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.ciphertextdisplay = Label(text = '',
                            pos_hint = {'x':0, 'top':.65},
                            size_hint = (1,1),
                            markup = True,
                            font_size = 24)

        self.encryptbutton = Button(text = 'Encrypt',
                            pos_hint = {'x':.5, 'top':.495},
                            size_hint = (.475,.05),
                            on_release = self.encryptpressed)

        self.instructions = Label(text = 'Type your message into the plaintext box\n' +
                                        'and press the encrypt button. The MD5 encrypted\n' +
                                        'message will display at the bottom of the page.',
                            pos_hint = {'x':.135, 'top':.725},
                            size_hint = (.2,.2))

        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.linkalg)
        self.r.add_widget(self.linkinfo)
        self.r.add_widget(self.plaintextlabel)
        #self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.encryptbutton)
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.tb)
        return self.r

    def encryptpressed(self, *args):
        f.write('encrypt button pressed\n')
        text = self.plaintextinput.text
        self.encoded = self.encrypt(text)
        self.ciphertextdisplay.text = '[color=ff0000][b]' + self.encoded + '[/b][/color]'


    def encrypt(self, text, *args):
        return hashlib.md5(text).hexdigest()

    def link1(self, *args):
        f.write('opening https://en.wikipedia.org/wiki/MD5 ...\n')
        webbrowser.open("https://en.wikipedia.org/wiki/MD5")

    def link2(self, *args):
        f.write('opening https://docs.python.org/2/library/hashlib.html ...\n')
        webbrowser.open("https://docs.python.org/2/library/hashlib.html")
################################################################################
#End MD5 Page
################################################################################

################################################################################
#Begin SHA-1 Page
################################################################################
class SHA1Page(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('SHA-1 page entered\n')
        MyApp.current = self
        self.cipher = ''
        self.secret = ''
        self.encoded = ''

        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('SHA-1 and SHA-256')
        self.x = .75
        self.btnsize = (.2,.1)
        self.txtinsz = (.475,.2)

        with open('texts/sha1.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.91},
                            size_hint = (.2,.2),
                            markup = True)

        self.linkinfo = Label(text = 'Information from: [color=ffff00][ref=md5]https://en.wikipedia.org/wiki/SHA-1[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)
        self.linkalg = Label(text = 'Algorithm from: [color=ffff00][ref=md5alg]https://docs.python.org/2/library/hashlib.html[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)

        self.plaintextlabel = Label(text = "Plaintext",
                            pos_hint = {'x':.4375, 'top':.825},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.plaintextinput = maxinput(text = '',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = self.txtinsz)
        self.plaintextinput.max_chars = 32

        self.plaintextlabel2 = Label(text = "Plaintext",
                            pos_hint = {'x':.4375, 'top':.525},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.plaintextinput2 = maxinput(text = '',
                            pos_hint = {'x':.5, 'top':.4},
                            size_hint = self.txtinsz)
        self.plaintextinput2.max_chars = 32

        self.ciphertextlabel = Label(text = "Ciphertext",
                            pos_hint = {'x':.4375, 'top':.525},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.ciphertextdisplay = Label(text = '',
                            pos_hint = {'x':0, 'top':.6},
                            size_hint = (1,1),
                            markup = True,
                            font_size = 24)

        self.encryptbutton = Button(text = 'Encrypt SHA-1',
                            pos_hint = {'x':.5, 'top':.495},
                            size_hint = (.475,.05),
                            on_release = self.encryptpressed)
        self.encryptbutton2 = Button(text = 'Encrypt SHA-256',
                            pos_hint = {'x':.5, 'top':.195},
                            size_hint = (.475,.05),
                            on_release = self.encryptpressed2)

        self.instructions = Label(text = 'Type your message into the plaintext box\n' +
                                        'and press the encrypt button. The SHA-1 or SHA-256\n' +
                                        'encrypted message will display at the bottom of\n' +
                                        'the page.',
                            pos_hint = {'x':.135, 'top':.525},
                            size_hint = (.2,.2))

        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.linkalg)
        self.r.add_widget(self.linkinfo)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel2)
        self.r.add_widget(self.plaintextinput2)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.encryptbutton)
        self.r.add_widget(self.encryptbutton2)
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.tb)
        return self.r

    def encryptpressed(self, *args):
        f.write('encrypt button pressed\n')
        text = self.plaintextinput.text
        self.encoded = self.encrypt(text)
        self.ciphertextdisplay.text = '[color=ff0000][b]' + self.encoded + '[/b][/color]'
        self.ciphertextdisplay.font_size = 24
        self.plaintextinput.text = ''
        self.plaintextinput2.text = ''

    def encryptpressed2(self, *args):
        f.write('encrypt2 button pressed\n')
        text = self.plaintextinput.text
        self.encoded = self.encrypt2(text)
        self.ciphertextdisplay.text = '[color=ff0000][b]' + self.encoded + '[/b][/color]'
        self.ciphertextdisplay.font_size = 20
        self.plaintextinput.text = ''
        self.plaintextinput2.text = ''

    def encrypt2(self, text, *args):
        return hashlib.sha256(text).hexdigest()

    def encrypt(self, text, *args):
        return hashlib.sha1(text).hexdigest()

    def link1(self, *args):
        f.write('opening https://en.wikipedia.org/wiki/SHA-1 ...\n')
        webbrowser.open("https://en.wikipedia.org/wiki/SHA-1")

    def link2(self, *args):
        f.write('opening https://docs.python.org/2/library/hashlib.html ...\n')
        webbrowser.open("https://docs.python.org/2/library/hashlib.html")
################################################################################
#End SHA-1 Page
################################################################################

################################################################################
#Begin BLAKE2 Page
################################################################################
class BLAKE2Page(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('BLAKE2 page entered\n')
        MyApp.current = self
        self.cipher = ''
        self.secret = ''
        self.encoded = ''

        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('BLAKE2')
        self.x = .75
        self.btnsize = (.2,.1)
        self.txtinsz = (.475,.2)

        with open('texts/blake2.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.4, 'top':.91},
                            size_hint = (.2,.2),
                            markup = True)

        self.linkinfo = Label(text = 'Information from: [color=ffff00][ref=md5]https://blake2.net/[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link1)
        self.linkalg = Label(text = 'Algorithm from: [color=ffff00][ref=md5alg]https://github.com/buggywhip/blake2_py[/ref][/color]',
                            pos_hint = {'x':.4, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.link2)

        self.plaintextlabel = Label(text = "Plaintext",
                            pos_hint = {'x':.4375, 'top':.825},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.plaintextinput = maxinput(text = '',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = self.txtinsz)
        self.plaintextinput.max_chars = 32

        self.ciphertextlabel = Label(text = "Ciphertext",
                            pos_hint = {'x':.4375, 'top':.525},
                            size_hint = (.2,.2),
                            font_size = 13)
        self.ciphertextdisplay = Label(text = '',
                            pos_hint = {'x':0, 'top':.65},
                            size_hint = (1,1),
                            markup = True,
                            font_size = 10)

        self.encryptbutton = Button(text = 'Encrypt',
                            pos_hint = {'x':.5, 'top':.495},
                            size_hint = (.475,.05),
                            on_release = self.encryptpressed)

        self.instructions = Label(text = 'Type your message into the plaintext box\n' +
                                        'and press the encrypt button. The BLAKE2 encrypted\n' +
                                        'message will display at the bottom of the page.',
                            pos_hint = {'x':.135, 'top':.725},
                            size_hint = (.2,.2))

        #add widgets to the main layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.linkalg)
        self.r.add_widget(self.linkinfo)
        self.r.add_widget(self.plaintextlabel)
        #self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.encryptbutton)
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.tb)
        return self.r

    def encryptpressed(self, *args):
        f.write('encrypt button pressed\n')
        text = self.plaintextinput.text
        self.encoded = self.encrypt(text)
        self.ciphertextdisplay.text = '[color=ff0000][b]' + self.encoded + '[/b][/color]'


    def encrypt(self, text, *args):
        return blake2.BLAKE2b(text).hexdigest()

    def link1(self, *args):
        f.write('opening https://blake2.net/ ...\n')
        webbrowser.open("https://blake2.net/")

    def link2(self, *args):
        f.write('opening https://github.com/buggywhip/blake2_py ...\n')
        webbrowser.open("https://github.com/buggywhip/blake2_py")
################################################################################
#End BLAKE2 Page
################################################################################

################################################################################
#Begin Highlights Page
################################################################################
class HighlightsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Junior Code Breakers entered\n')
        MyApp.current = self
        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        #create the topbar and add the title to it
        self.tb = self.topbar.create('Highlights')

        #components of the page
        self.text1 = Label(text = 'If you want a quick overview of what the CD-ROM contains, then you can dip into\n' +
                            'the following highlights, which range from encryption tools to video clips to animations.',
                            pos_hint = {'x':.4, 'top':.95},
                            size_hint = (.2,.2))
        self.button1 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.1, 'top':.7},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.onepressed)
        self.label1 = Label(text = 'Atbash Cipher - an early and' +
                                    '\nelementary substitution cipher that\n' +
                                    'you can experiment with.',
                            pos_hint = {'x':.215, 'top':.765},
                            size_hint = (.2,.2))
        self.button2 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.1, 'top':.5},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.twopressed)
        self.label2 = Label(text = 'First Codebreakers - an interview\n' +
                                    'with the man who uncovered\n' +
                                    'ancient Arab manuscripts on\n' +
                                    'codebreaking.',
                            pos_hint = {'x':.215, 'top':.565},
                            size_hint = (.2,.2))
        self.button3 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.1, 'top':.3},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.threepressed)
        self.label3 = Label(text = 'Frequency Analysis - an\n' +
                                    'explanation of the first\n' +
                                    'codebreaking technique, incl. a\n' +
                                    'clip from The Science of Secrecy.',
                            pos_hint = {'x':.215, 'top':.365},
                            size_hint = (.2,.2))
        self.button4 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.8, 'top':.7},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.fourpressed)
        self.label4 = Label(text = 'Vigenere Tool - encrypt messages\n' +
                                    'with a system that thwarts simple\n' +
                                    'frequency analysis',
                            pos_hint = {'x':.535, 'top':.765},
                            size_hint = (.2,.2))
        self.button5 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.8, 'top':.5},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.fivepressed)
        self.label5 = Label(text = 'ADFGVX cipher - a cipher used in\n' +
                                    'the First World War, which\n' +
                                    'involves substitution and\n' +
                                    'transposition.',
                            pos_hint = {'x':.535, 'top':.565},
                            size_hint = (.2,.2))
        self.button6 = Button(text = '[b][color=ff0000]>[/color][/b]',
                            pos_hint = {'x':.8, 'top':.3},
                            size_hint = (.05,.05),
                            markup = True,
                            on_release = self.sixpressed)
        self.label6 = Label(text = 'Cliff Cocks interview - the first ever\n' +
                                    'interview with a GCHQ codebreaker\n' +
                                    '- a real exclusive.',
                            pos_hint = {'x':.535, 'top':.365},
                            size_hint = (.2,.2))

        #add widgets to the main layout
        self.r.add_widget(self.label1)
        self.r.add_widget(self.label2)
        self.r.add_widget(self.label3)
        self.r.add_widget(self.label4)
        self.r.add_widget(self.label5)
        self.r.add_widget(self.label6)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.button6)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    #button functions to create new pages
    def onepressed(self, *args):
        f.write('highlights - atbash pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AtbashPage().create())

    def twopressed(self, *args):
        f.write('highlights - first codebreakers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(InventionInBaghdadPage().create())

    def threepressed(self, *args):
        f.write('highlights - frequency analysis pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowFreqPage().create())

    def fourpressed(self, *args):
        f.write('highlights - vigenere pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(VigenerePage().create())

    def fivepressed(self, *args):
        f.write('highlights - adfgvx cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ADFGVXPage().create())

    def sixpressed(self, *args):
        f.write('highlights - cliff cocks interview pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(JamesAndCliffordPage().create())
################################################################################
#End Highlights Page
################################################################################

################################################################################
#Begin Junior Codebreakers Page
################################################################################
class JCBPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Junior Code Breakers entered\n')
        MyApp.current = self
        self.leftx = -0.2
        self.rightx = .3

        #root layout of the instance
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create('Junior Codebreakers')
        #setup layouts
        self.leftc = RelativeLayout(size_hint = (.5,.6),
                                    pos_hint = {'left':1})
        self.rightc = RelativeLayout(size_hint = (.5,.6),
                                    pos_hint = {'right':1})
        self.buttonlay = RelativeLayout(pos_hint = {'center_x':.5, 'center_y':.5},
                                        size_hint = (.6,1))

        self.lefttext = Label(text = 'Some of the material in this application is quite\n' +
                                    'complicated, particularly in later chapters.\n\n' +
                                    'This section is a collection of pages that are\n' +
                                    'ideal for junior codebreakers. Just click on the\n' +
                                    'first page to begin.',
                            pos_hint = {'x':.2, 'top':.9},
                            size_hint = (.2,.2))
        self.righttext = Label(text = 'The pages start with the most ancient techniques\n' +
                                        'used to protect messages from prying eyes. The\n' +
                                        'first page introduces a form of transposition\n' +
                                        'cipher, which means that it moves the letters of\n' +
                                        'the message, creating an anagram.',
                            pos_hint = {'x':.65, 'top':.915},
                            size_hint = (.2,.2))

        #column 1
        self.railfence = Button(text = 'Transposition - Railfence',
                            pos_hint = {'x':self.leftx, 'center_y':1},
                            size_hint = (.9,.06),
                            on_release = self.railfencepressed)
        self.latin = Button(text = 'Transposition - Latin Square',
                            pos_hint = {'x':self.leftx, 'center_y':.875},
                            size_hint = (.9,.06),
                            on_release = self.latinsqpressed)
        self.caesar = Button(text = 'Caesar Cipher',
                            pos_hint = {'x':self.leftx, 'center_y':.75},
                            size_hint = (.9,.06),
                            on_release = self.caesarpressed)
        self.pigpen = Button(text = 'Pigpen Cipher',
                            pos_hint = {'x':self.leftx, 'center_y':.625},
                            size_hint = (.9,.06),
                            on_release = self.pigpenpressed)
        self.pigpengrave = Button(text = 'Pigpen Gravestone',
                            pos_hint = {'x':self.leftx, 'center_y':.5},
                            size_hint = (.9,.06),
                            on_release = self.pigpengravepressed)
        self.atbash = Button(text = 'Atbash Cipher',
                            pos_hint = {'x':self.leftx, 'center_y':.375},
                            size_hint = (.9,.06),
                            on_release = self.atbashpressed)
        self.mono = Button(text = 'General Monoalphabetic',
                            pos_hint = {'x':self.leftx, 'center_y':.25},
                            size_hint = (.9,.06),
                            on_release = self.genmonopressed)
        #add components to left layout
        self.leftc.add_widget(self.railfence)
        self.leftc.add_widget(self.latin)
        self.leftc.add_widget(self.caesar)
        self.leftc.add_widget(self.pigpen)
        self.leftc.add_widget(self.pigpengrave)
        self.leftc.add_widget(self.atbash)
        self.leftc.add_widget(self.mono)

        #column 2
        self.howfreq = Button(text = 'How Frequency Analysis Works',
                            pos_hint = {'x':self.rightx, 'center_y':1},
                            size_hint = (.9,.06),
                            on_release = self.freqpressed)
        self.digraph = Button(text = 'Digraph Substitution',
                            pos_hint = {'x':self.rightx, 'center_y':.875},
                            size_hint = (.9,.06),
                            on_release = self.digraphpressed)
        self.playfair = Button(text = 'Playfair Cipher',
                            pos_hint = {'x':self.rightx, 'center_y':.75},
                            size_hint = (.9,.06),
                            on_release = self.playfairpressed)
        self.homo = Button(text = 'Homophonic Cipher',
                            pos_hint = {'x':self.rightx, 'center_y':.625},
                            size_hint = (.9,.06),
                            on_release = self.homophonicpressed)
        self.morse = Button(text = 'Morse Code',
                            pos_hint = {'x':self.rightx, 'center_y':.5},
                            size_hint = (.9,.06),
                            on_release = self.morsepressed)
        self.dancing = Button(text = 'Dancing Men Cipher',
                            pos_hint = {'x':self.rightx, 'center_y':.375},
                            size_hint = (.9,.06),
                            on_release = self.dancingpressed)
        self.meetenigma = Button(text = 'Meet the Enigma Machine',
                            pos_hint = {'x':self.rightx, 'center_y':.25},
                            size_hint = (.9,.06),
                            on_release = self.meetpressed)
        self.codetalkers = Button(text = 'Codetalkers',
                            pos_hint = {'x':self.rightx, 'center_y':.125},
                            size_hint = (.9,.06),
                            on_release = self.codetalkerspressed)

        #add components to right layout
        self.rightc.add_widget(self.howfreq)
        self.rightc.add_widget(self.digraph)
        self.rightc.add_widget(self.playfair)
        self.rightc.add_widget(self.homo)
        self.rightc.add_widget(self.morse)
        self.rightc.add_widget(self.dancing)
        self.rightc.add_widget(self.meetenigma)
        self.rightc.add_widget(self.codetalkers)

        #add the rest of components to main layout
        self.buttonlay.add_widget(self.leftc)
        self.buttonlay.add_widget(self.rightc)
        self.r.add_widget(self.lefttext)
        self.r.add_widget(self.righttext)
        self.r.add_widget(self.tb)
        self.r.add_widget(self.buttonlay)
        return self.r

    #button functions
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

    def railfencepressed(self, *args):
        f.write('railfence button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RailfencePage().create())

    def latinsqpressed(self, *args):
        f.write('latin square pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(LatinSquarePage().create())

    def pigpenpressed(self, *args):
        f.write('pigpen pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PigpenPage().create())

    def pigpengravepressed(self, *args):
        f.write('pigpen grave pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PigpenGravePage().create())

    def genmonopressed(self, *args):
        f.write('general Monoalphabetic pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(GenMonoPage().create())

    def freqpressed(self, *args):
        f.write('frequency analysis pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowFreqPage().create())

    def playfairpressed(self, *args):
        f.write('playfair pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PlayfairPage().create())

    def digraphpressed(self, *args):
        f.write('digraph pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(DigraphPage().create())

    def homophonicpressed(self, *args):
        f.write('homophonic pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HomophonicPage().create())

    def morsepressed(self, *args):
        f.write('morse pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MorsePage().create())

    def dancingpressed(self, *args):
        f.write('dancing men pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(DancingMenPage().create())

    def meetpressed(self, *args):
        f.write('meet enigma pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MeetEnigmaPage().create())

    def codetalkerspressed(self, *args):
        f.write('codetalkers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CodetalkersPage().create())
################################################################################
#End Junior Codebreakers Page
################################################################################

################################################################################
#Begin Railfence Cipher Page
################################################################################
class RailfencePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('railfence page entered\n')
        MyApp.current = self
        self.big = []
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Railfence Cipher")
        self.active = RelativeLayout(pos_hint = {'bottom':1},
                                    size_hint = (1,.5))
        self.passive = RelativeLayout(pos_hint = {'top':1},
                                    size_hint = (1,.5))
        self.tooltop = 1.1

        #setup components
        with open('texts/railfenceciphertext.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':.975},
                            size_hint = (.5,.5))

        self.shiftlabel = Label(text = 'Number of Lines',
                                pos_hint = {'x':.1, 'y':1.15},
                                size_hint = (.05,.05))
        self.decrem = Button(text = '<', pos_hint = {'x':.05, 'top':self.tooltop},
                            size_hint = (.05,.05),
                            on_release = self.decr)
        self.shiftnum = Label(text = '2', font_size = '20sp', pos_hint = {'x':.1, 'top':self.tooltop},
                            size_hint = (.05,.05))
        self.increm = Button(text = '>', pos_hint = {'x':.15, 'top':self.tooltop},
                            size_hint = (.05,.05),
                            on_release = self.incr)

        self.plaintextinput = maxinput(text = '',
                                    pos_hint = {'x':.25, 'top':1.2},
                                    size_hint = (.65, .15),
                                    font_name = 'font/RobotoMono-Regular')
        self.plaintextinput.max_chars = 55
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.4, 'top':1.3},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.25, 'top':.225},
                                            size_hint = (.65, .15),
                                            disabled = True,
                                            font_name = 'font/RobotoMono-Regular')
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.4, 'top':.325},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.05, 'top':.2},
                                        size_hint = (.15,.1),
                                        on_release = self.encipherPressed,
                                        disabled = True)

        self.raillabel = Label(text = '',
                                        pos_hint = {'x':.5, 'top':.7},
                                        size_hint = (.15,.1),
                                        markup = True,
                                        font_name = 'font/RobotoMono-Regular',
                                        font_size = 16)
        self.railbutton = Button(text = 'Create Railfence',
                                        pos_hint = {'x':.05, 'top':.35},
                                        size_hint = (.15,.1),
                                        on_release = self.rail)

        self.instr1 = Label(text = 'You can see how the Railfence Cipher works by:\n' +
                                    '1. Typing your message into the Plaintext box\n' +
                                    '2. Click the Railfence button\n' +
                                    '3. Click the Create Ciphertext button to encrypt\n',
                                        pos_hint = {'x':.2, 'top':.55},
                                        size_hint = (.2,.2))

        self.passive.add_widget(self.text)
        self.passive.add_widget(self.instr1)

        self.active.add_widget(self.shiftlabel)
        self.active.add_widget(self.decrem)
        self.active.add_widget(self.shiftnum)
        self.active.add_widget(self.increm)
        self.active.add_widget(self.plaintextinput)
        self.active.add_widget(self.plaintextlabel)
        self.active.add_widget(self.ciphertextdisplay)
        self.active.add_widget(self.ciphertextlabel)
        self.active.add_widget(self.encipherbutton)
        self.active.add_widget(self.railbutton)
        self.active.add_widget(self.raillabel)

        self.r.add_widget(self.tb)
        self.r.add_widget(self.passive)
        self.r.add_widget(self.active)
        return self.r

    #when the encipher button is pressed set the ciphertextdisplay text to
    #the newly encrypted text
    def encipherPressed(self, *args):
        f.write("encipher pressed\n")
        self.ciphertextdisplay.text = ''
        self.ciphertextdisplay.text = self.encode()

    def rail(self, *args):
        f.write('creating railfence...\n')
        self.encipherbutton.disabled = False
        self.raillabel.text = ''
        self.ciphertextdisplay.text = ''
        self.big = []
        text = self.plaintextinput.text
        text = text.replace(' ', '')
        n = int(self.shiftnum.text)
        f.write(text + '\n')
        f.write('n: ' + str(n) + '\n')
        textlist = []
        for c in text:
            textlist.append(str(c))
        count = n
        newstr = ''

        for i in range(count):
            newlist = []
            for k in range(len(textlist)):
                if (k % count) == 0:
                    try:
                        newlist.append(textlist[k + i])
                        newstr = newstr + textlist[k + i]
                    except Exception as e:
                        pass
            self.big.append(newlist)

        #create the text for the label
        railtext = '[color=#ff0000]'
        nm = 1
        #iterate through the lists in big
        for l in self.big:
            #iterate through the letters in the inner list
            for c in l:
                #creates the string so that the rail appearance is shown through spaces
                railtext = railtext + c + str(count*' ')
            railtext = railtext + '\n' + str(nm*' ')
            nm += 1
        railtext += '[/color]'
        self.raillabel.text = railtext


    def encode(self, *args):
        f.write('railfence encoding...\n')
        newstr = ''
        for l in self.big:
            newstr = newstr + ''.join(l)
        return newstr

    #increments the rail amount
    def incr(self, *args):
        if(int(self.shiftnum.text) == 9):
            self.shiftnum.text = '0'
        else:
            temp = int(self.shiftnum.text) + 1
            self.shiftnum.text = str(temp)

    #decrements the rail amount
    def decr(self, *args):
        if(int(self.shiftnum.text) == 0):
            pass
        else:
            temp = int(self.shiftnum.text) - 1
            self.shiftnum.text = str(temp)

    def checkinput(self, *args):
        if len(self.plaintextinput.text) > 50:
            self.plaintextinput.disabled = True
################################################################################
#End Railfence Cipher Page
################################################################################

################################################################################
#Begin Latin Square Cipher Page
################################################################################
class LatinSquarePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('latin square page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Latin Square")

        with open('texts/latinsquare.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.05, 'top':.7},
                            size_hint = (.5,.5),
                            font_size = 14)

        self.lsimage = Image(source = 'pics/wordsqu3.png',
                                    pos_hint = {'x':.55, 'top':.9},
                                    size_hint = (.7,.5))

        self.imagetext = Label(text = 'The Manchester Museum\n' +
                                        'The University of Manchester',
                                        pos_hint = {'x':.775, 'top':.55},
                                        size_hint = (.25,.25),
                                        font_size = 11)

        self.lsquareimage = Image(source = 'pics/latsqcrop.png',
                                    pos_hint = {'x':.55, 'top':.65},
                                    size_hint = (.25,.25))

        self.deciphimage = Image(source = 'pics/paternoster.bmp',
                                    pos_hint = {'x':.475, 'top':.5},
                                    size_hint = (.6,.6))


        self.r.add_widget(self.text)
        self.r.add_widget(self.lsimage)
        self.r.add_widget(self.imagetext)
        self.r.add_widget(self.lsquareimage)
        self.r.add_widget(self.deciphimage)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Latin Square Cipher Page
################################################################################

################################################################################
#Begin Atbash Cipher Page
################################################################################
class AtbashPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('atbash page entered\n')
        MyApp.current = self
        #create cipher alphabet
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.stoptext = ''

        #create the list as a string
        self.stralpha = ''.join(self.alpha)
        #reverse the string
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

        self.atbashimage = Image(source = 'pics/BABEL.png',
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
                            pos_hint = {'x':.675, 'top':.7},
                            size_hint = (.27,.1))
        self.alphabet = TextInput(text = self.stralpha,
                                    pos_hint = {'x':.65, 'top':.6},
                                    size_hint = (.32,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.clabel = Label(text = 'Ciphertext Alphabet',
                            pos_hint = {'x':.675, 'top':.5},
                            size_hint = (.27,.1))
        #joins the reversed alphabet and creates a string out of it
        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet = TextInput(text = self.strnewalpha,
                                    pos_hint = {'x':.65, 'top':.4},
                                    size_hint = (.32,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.2},
                                    size_hint = (.35, .15))
        self.plaintextinput.max_chars = 35
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

        #add components
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

    #encryption function for atbashen
    def atbashen(self, text, spaces, *args):
        enciphered = ""
        text = text.lower()

        #iterate throught the plaintext letters
        for letter in text:
            #iterate throught the original alphabet
            for i in range(len(self.alpha)):
                #append the reversed letter
                if self.alpha[i] == letter:
                    enciphered += self.newalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "
        return enciphered

    #when the encipher button is pressed
    #calls the function atbashen
    #sets the ciphertextdisplay text to the newly encipher text
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
        #create the two alphabets
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #using deque to allow shifting of the lists
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
                                    size_hint = (.315,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.clabel = Label(text = 'Ciphertext Alphabet',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = (.27,.1))

        #rotates the newalphabet by the shift amount
        self.newalpha.rotate(-(int(self.shiftnum.text)))
        self.strnewalpha = "".join(list(self.newalpha))
        self.cipheralphabet = TextInput(text = self.strnewalpha,
                                    pos_hint = {'x':.5, 'top':.6},
                                    size_hint = (.315,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.4},
                                    size_hint = (.35, .35))
        self.plaintextinput.max_chars = 150
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

        #add components to layout
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

    #function called when the encipher button is pressed
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

    #increases the shift amount
    #updates the alphabet display
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

    #decreases the shift amount
    #updates the alphabet display
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
#Begin Pigpen Gravestone Page
################################################################################
class PigpenGravePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('pigpen gravestone page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Pigpen Gravestone")

        #elements of the page
        with open('texts/pigpengravestone.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.45, 'top':.725},
                            size_hint = (.5,.5),
                            font_size = 15)

        self.image1 = Image(source = 'pics/piggrave/pigcypmd.png',
                            pos_hint = {'x':-.2, 'top':.9},
                            size_hint = (.8,.8))

        self.image2 = Image(source = 'pics/piggrave/PIG4.png',
                            pos_hint = {'x':.505, 'top':.95},
                            size_hint = (.4,.4))

        self.image3 = Image(source = 'pics/piggrave/PIG3.png',
                            pos_hint = {'x':.455, 'top':.5},
                            size_hint = (.5,.5))

        self.label = Label(text = 'The meaning of the ciphertext at the foot of the gravestone\nappears to be "Holiness of the Lord".',
                            pos_hint = {'x':.6, 'top':.2},
                            size_hint = (.2,.2),
                            font_size = 15)
        self.smalllabel = Label(text = 'Photograph by John Mee',
                            pos_hint = {'x':.4, 'top':.125},
                            size_hint = (.2,.2),
                            font_size = 11)

        #add components to the layout
        self.r.add_widget(self.text)
        self.r.add_widget(self.image1)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.image3)
        self.r.add_widget(self.label)
        self.r.add_widget(self.smalllabel)

        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Pigpen Gravestone Page
################################################################################

################################################################################
#Begin Pigpen Cipher Page
################################################################################
class PigpenPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('pigpen page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.images = []

        #appends image file path to the list of images
        for i in self.alpha:
            self.images.append('pics/pigpen/' + i + '.bmp')

        #setup layouts
        self.r = RelativeLayout()
        self.r2 = RelativeLayout()
        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Pigpen Cipher")

        #elements of the page
        self.instructions = Label(text = 'Type your message into the box labeled Plaintext, then\n' +
                                            'click the button labeled Encipher Text to encrypt your message.',
                                    pos_hint = {'x':.6, 'top':.8},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.plaintextinput = maxinput(pos_hint = {'x':.55, 'top':.7},
                                    size_hint = (.4, .2))
        self.plaintextinput.max_chars = 50
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.35, 'top':.7},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.55, 'top':.4},
                                            size_hint = (.4, .2),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.35, 'top':.4},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.55, 'top':.475},
                                        size_hint = (.15,.05),
                                        on_release = self.encipherPressed)

        with open('texts/pigpenciphertext.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':1.1},
                            size_hint = (.5,.5),
                            font_size = 14)

        self.examplelabel = Label(text = 'For instance:',
                            pos_hint = {'x':0, 'top':.2},
                            size_hint = (.2,.2))

        self.alabel = Label(text = 'A = ',
                            pos_hint = {'x':.1, 'top':.2},
                            size_hint = (.2,.2))

        self.aimage = Image(source = 'pics/pigpen/a2.bmp',
                            pos_hint = {'x':.135, 'top':.2},
                            size_hint = (.2,.2))

        self.blabel = Label(text = 'B = ',
                            pos_hint = {'x':.2, 'top':.2},
                            size_hint = (.2,.2))

        self.bimage = Image(source = 'pics/pigpen/b2.bmp',
                            pos_hint = {'x':.235, 'top':.2},
                            size_hint = (.2,.2))

        self.ylabel = Label(text = 'Y = ',
                            pos_hint = {'x':.1, 'top':.15},
                            size_hint = (.2,.2))

        self.yimage = Image(source = 'pics/pigpen/y2.bmp',
                            pos_hint = {'x':.135, 'top':.15},
                            size_hint = (.2,.2))

        self.zlabel = Label(text = 'Z = ',
                            pos_hint = {'x':.2, 'top':.15},
                            size_hint = (.2,.2))

        self.zimage = Image(source = 'pics/pigpen/z3.bmp',
                            pos_hint = {'x':.235, 'top':.15},
                            size_hint = (.2,.2))

        self.piggy0 = Image(source = 'pics/pigpen/PIGGY0.bmp',
                            pos_hint = {'x':0, 'top':.65},
                            size_hint = (.2,.2))

        self.piggy1 = Image(source = 'pics/pigpen/PIGGY1.bmp',
                            pos_hint = {'x':.2, 'top':.65},
                            size_hint = (.2,.2))

        self.piggy2 = Image(source = 'pics/pigpen/PIGGY2.bmp',
                            pos_hint = {'x':0, 'top':.4},
                            size_hint = (.2,.2))

        self.piggy3 = Image(source = 'pics/pigpen/PIGGY3.bmp',
                            pos_hint = {'x':.2, 'top':.4},
                            size_hint = (.2,.2))

        #add components to the layout
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.text)
        self.r.add_widget(self.piggy0)
        self.r.add_widget(self.piggy1)
        self.r.add_widget(self.piggy2)
        self.r.add_widget(self.piggy3)

        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)

        self.r.add_widget(self.examplelabel)
        self.r.add_widget(self.alabel)
        self.r.add_widget(self.aimage)
        self.r.add_widget(self.blabel)
        self.r.add_widget(self.bimage)
        self.r.add_widget(self.ylabel)
        self.r.add_widget(self.yimage)
        self.r.add_widget(self.zlabel)
        self.r.add_widget(self.zimage)

        self.r.add_widget(self.tb)
        return self.r

    #function called when the encipher button is pressed
    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        self.r2.clear_widgets()
        self.r.remove_widget(self.r2)
        self.pigpenEncode(self.plaintextinput.text)

    #encrypts the plaintext with the pigpen cipher
    def pigpenEncode(self, text, *args):
        self.templist = []
        tem = .49
        top = .42
        for j in text:
            f.write('w ' + j + '\n')
            if j == ' ':
                self.templist.append(Image(source = 'pics/pigpen/space.bmp'))
            else:
                for i in range(len(self.alpha)):
                    if j == self.alpha[i]:
                        self.templist.append(Image(source = self.images[i]))

        for i in range(len(self.templist)):
            tem = tem + .03

            f.write('| ' + str(self.templist[i].source) + ' ' + str(tem) + '\n')
            if tem >= .89:
                top = top - .05
                tem = .52
            self.templist[i].pos_hint = {'x':tem, 'top':top}
            self.templist[i].size_hint = (.1,.1)
            self.r2.add_widget(self.templist[i])

        self.r.add_widget(self.r2)
################################################################################
#End Pigpen Cipher Page
################################################################################

################################################################################
#Begin General Monoalphabetic Shift Page
################################################################################
class GenMonoPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('general Monoalphabetic page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        shuffle(self.newalpha)


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
        self.tb = self.topbar.create("General Monoalphabetic Cipher")

        #elements of the page
        self.randomize = Button(text = 'Randomize Cipher\nAlphabet',
                            pos_hint = {'x':.025, 'top':.8},
                            size_hint = (.2,.15),
                            on_release = self.genrandomPressed)

        self.alabel = Label(text = 'Plaintext Alphabet',
                            pos_hint = {'x':.5, 'top':.9},
                            size_hint = (.27,.1))
        self.alphabet = TextInput(text = self.stralpha,
                                    pos_hint = {'x':.475, 'top':.8},
                                    size_hint = (.315,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.clabel = Label(text = 'Ciphertext Alphabet',
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = (.27,.1))

        self.strnewalpha = "".join(self.newalpha)
        self.cipheralphabet = TextInput(text = self.strnewalpha,
                                    pos_hint = {'x':.475, 'top':.6},
                                    size_hint = (.315,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')

        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.4},
                                    size_hint = (.35, .35))
        self.plaintextinput.max_chars = 150
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
                                        pos_hint = {'x':.025, 'top':.6},
                                        size_hint = (.2,.15),
                                        on_release = self.encipherPressed)

        with open('texts/generalmono.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':.725},
                            size_hint = (.5,.5))

        self.instructions = Label(text = 'Click the button labeled "Randomize Cipher Alphabet" to generate one of the\n' +
                                            '400,000,000,000,000,000,000,000,000 possible permutations of the alphabet.',
                                    pos_hint = {'x':.25, 'top':.3},
                                    size_hint = (.5,.5))


        self.active.add_widget(self.randomize)
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
        self.passive.add_widget(self.instructions)

        self.r.add_widget(self.passive)
        self.r.add_widget(self.active)
        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.monoencrypt(self.plaintextinput.text)
        self.ciphertextdisplay.text = enciphered

    def genrandomPressed(self, *args):
        f.write('generate random cipher pressed\n')
        shuffle(self.newalpha)
        self.cipheralphabet.text = "".join(self.newalpha)

    def monoencrypt(self, word, *args):
        enciphered = ""

        #iterate through the string of text
        for letter in word:
            #iterate through the alphabet list
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    enciphered += self.newalpha[i]
            if (letter == " "):
                enciphered += " "

        return enciphered
################################################################################
#End General Monoalphabetic Page
################################################################################

################################################################################
#Begin Frequency Analysis How Page
################################################################################
class HowFreqPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('how Frequency Analysis works entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("How Frequency Analysis Works")

        with open('texts/freqanal.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':.6},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.vid = VideoPlayer(source = 'video/freqful3.avi',
                            pos_hint = {'x':.55, 'top':.5},
                            size_hint = (.45,.45),
                            allow_fullscreen = False)

        self.freqimage = Image(source = 'pics/Letter_frequency-wide.png',
                            pos_hint = {'x':.25, 'top':1.075},
                            size_hint = (.55,.55))

        self.r.add_widget(self.freqimage)
        self.r.add_widget(self.vid)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Frequency Analysis How Page
################################################################################

################################################################################
#Begin Digraph Cipher Page
################################################################################
class DigraphPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('digraph page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.alpha1 = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        self.alpha2 = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])
        self.table = ''
        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Digraph Substitution")

        #elements of the page
        self.tablelabel = Label(text = self.table,
                                    pos_hint = {'x':.4, 'top':.7},
                                    size_hint = (.5,.5),
                                    font_name = 'font/RobotoMono-Regular',
                                    font_size = 11)
        self.plaintextinput = maxinput(pos_hint = {'x':.025, 'top':.335},
                                    size_hint = (.25, .1))
        self.plaintextinput.max_chars = 55
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.015, 'top':.395},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.025, 'top':.2},
                                            size_hint = (.25, .1),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.015, 'top':.265},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.075, 'top':.09},
                                        size_hint = (.15,.04),
                                        on_release = self.encipherPressed,
                                        disabled = True)

        self.digraphbutton = Button(text = "Form Digraphs",
                                        pos_hint = {'x':.075, 'top':.04},
                                        size_hint = (.15,.04),
                                        on_release = self.formPressed)
        self.randdigraph = Button(text = "Randomize Digraph",
                                        pos_hint = {'x':.575, 'top':.85},
                                        size_hint = (.2,.04),
                                        on_release = self.randomDigraph)

        with open('texts/digraph.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':-.343, 'top':1.15},
                            font_size = 14)

        self.r.add_widget(self.randdigraph)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tablelabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.digraphbutton)

        self.r.add_widget(self.tb)
        self.randomDigraph()
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        self.digraphbutton.disabled = False
        self.randdigraph.disabled = False
        self.encipherbutton.disabled = True

        dig = self.plaintextinput.text

        dig = dig.strip()
        dig = dig.split(' ')
        f.write('plaintext digraph: ' + str(dig) + '\n')
        tempstr = ''
        for di in dig:
            index1 = self.alpha.index(di[0])
            index2 = self.alpha.index(di[1])
            tempstr = str(tempstr) + ''.join(self.dub[index2][index1]) + ' '

        self.ciphertextdisplay.text = str(tempstr)

    def formPressed(self, *args):
        f.write('form digraphs pressed\n')
        self.randdigraph.disabled = True
        self.digraphbutton.disabled = True
        self.encipherbutton.disabled = False
        text = self.plaintextinput.text
        text = text.replace(" ", "")
        text = text.strip()
        tempstr = ''

        count = 0
        for letter in text:
            if count == 1:
                tempstr = tempstr + letter + ' '
                count = 0
            else:
                tempstr = tempstr + letter
                count = count + 1

        f.write('length: ' + str(len(tempstr)) + '\n')
        if (len(text) % 2) != 0:
            tempstr = tempstr + 'x'
        self.plaintextinput.text = tempstr

    def randomDigraph(self, *args):

        self.random1 = randint(0, 26)
        self.random2 = randint(0, 26)

        self.alpha1.rotate(self.random1)
        self.alpha2.rotate(self.random2)

        self.stralpha1 = "".join(list(self.alpha1))
        self.stralpha2 = "".join(list(self.alpha2))
        f.write('alpha1: ' + self.stralpha1 + '\n')
        f.write('alpha2: ' + self.stralpha2 + '\n')

        self.listalpha1 = list(self.alpha1)
        self.listalpha2 = list(self.alpha2)
        self.dub = []

        for letter in self.listalpha1:
            templist = []
            for letter2 in self.listalpha2:
                templist.append((letter2, letter))
            self.dub.append(templist)

        self.table = '  ' + ' |'.join(self.alpha) + '\n'

        for col in range(len(self.dub)):
            self.table = self.table + self.alpha[col] + '|'
            for tup in self.dub[col]:
                self.table = self.table + ''.join(tup) + '|'
            self.table = self.table + '\n'

        self.tablelabel.text = self.table
################################################################################
#End Digraph Cipher Page
################################################################################

################################################################################
#Begin Playfair Cipher Page
################################################################################
class PlayfairPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('playfair page entered\n')
        MyApp.current = self
        self.keyword = 'charles'
        self.comb = []
        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Playfair Cipher")

        with open('texts/playfaircipher.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.95},
                            size_hint = (.5,.5))

        with open('texts/playfaircipher2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.38, 'top':.565},
                            size_hint = (.5,.5))

        self.plaintextinput = maxinput(text = 'meet me at hammersmith bridge tonight',
                                        pos_hint = {'x':.25, 'top':.125},
                                        size_hint = (.325,.1),
                                        font_name = 'font/RobotoMono-Regular')
        self.plaintextinput.max_chars = 48
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.19, 'top':.245},
                                    size_hint = (.2,.2),
                                    font_size = 12)

        self.ciphertextdisplay = TextInput(pos_hint = {'x':.65, 'top':.125},
                                        size_hint = (.325,.1),
                                        disabled = True,
                                        font_name = 'font/RobotoMono-Regular')
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.59, 'top':.245},
                                    size_hint = (.2,.2),
                                    font_size = 12)

        self.digraphbutton = Button(text = 'Form Digraphs',
                                    pos_hint = {'x':.05, 'top':.125},
                                    size_hint = (.15,.05),
                                    on_release = self.form)

        self.encipherbutton = Button(text = 'Encipher Text',
                                    pos_hint = {'x':.05, 'top':.065},
                                    size_hint = (.15,.05),
                                    on_release = self.encipherPressed,
                                    disabled = True)
        self.keyworddisplay = maxinput(text = self.keyword,
                                        pos_hint = {'x':.075, 'top':.49},
                                        size_hint = (.1,.05))
        self.keyworddisplay.bind(text=self.textchange)
        self.keyworddisplay.max_chars = 8
        self.keywordlabel = Label(text = 'Keyword',
                                    pos_hint = {'x':.075, 'top':.555},
                                    size_hint = (.1,.1),
                                    font_size = 13)

        self.tablelabel = Label(text = '',
                                    pos_hint = {'x':.085, 'top':.33},
                                    size_hint = (.1,.1),
                                    font_size = 18,
                                    line_height = 1.15,
                                    font_name = 'font/RobotoMono-Regular')
        self.creategrid()
        self.grid = Image(source = 'pics/grid.png',
                        pos_hint = {'x':.025, 'top':.4},
                        size_hint = (.2,.25))

        self.r.add_widget(self.grid)
        self.r.add_widget(self.tablelabel)
        self.r.add_widget(self.keyworddisplay)
        self.r.add_widget(self.keywordlabel)
        self.r.add_widget(self.digraphbutton)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.text)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        self.digraphbutton.disabled = True
        self.encipherbutton.disabled = True
        enciphered = self.encrypt()
        self.ciphertextdisplay.text = enciphered

    def textchange(self, *args):
        kw = self.keyworddisplay.text
        templist = []
        for c in kw:
            if c not in templist:
                templist.append(c)
        self.keyworddisplay.text = ''.join(templist)
        self.creategrid()
        self.digraphbutton.disabled = False

    def encrypt(self, *args):
        final = ''
        templist = []
        newlist = []
        ditext = str(self.plaintextinput.text)
        dilist = ditext.split(" ")
        #set newlist up into a 2 dimensional list
        #5 rows i.e. 5 lists within a list
        #each index of the inner list corresponds to a column
        for i in range(len(self.comb)):
            if (i+1) % 5 == 0:
                templist.append(self.comb[i])
                newlist.append(templist)
                templist = []
            else:
                templist.append(self.comb[i])
        #f.write(str(newlist) + '\n')

        for i in dilist:
            if i == '':
                dilist.remove(i)
        #f.write(str(dilist) + '\n')

        for di in dilist:
            #if both letter in the di are in the same row
            #then they are replaced by the letter to the right
            #of them
            pass1 = False
            for inner in newlist:
                if di[0] in inner and di[1] in inner:
                    try:
                        final += inner[inner.index(di[0]) + 1]
                    except Exception as e:
                        final += inner[0]
                    try:
                        final += inner[inner.index(di[1]) + 1] + ' '
                    except Exception as e:
                        final += inner[0] + ' '
                    pass1 = True
                    break
            if pass1:
                continue
            #if both letters are in the same column
            #then they are replaced by the letter beneath
            #them
            i1 = 0
            i2 = 0
            inner1 = 0
            inner2 = 0
            for inner in range(len(newlist)):
                inn = newlist[inner]
                for i in range(len(inn)):
                    if inn[i] == di[0]:
                        i1 = i
                        inner1 = inner
                    if inn[i] == di[1]:
                        i2 = i
                        inner2 = inner
            if i1 == i2:
                index = i1
                try:
                    final += newlist[inner1+1][index]
                except Exception as e:
                    final += newlist[0][index]
                try:
                    final += newlist[inner2+1][index] + ' '
                except Exception as e:
                    final += newlist[0][index] + ' '
                continue

            #if the letters are neither in the same column
            #nor row then the letter is replaced by a letter of
            #the same row of the first letter and of the same
            #column of the second letter and vice versa
            loc1 = []
            loc2 = []
            for inner in range(len(newlist)):
                inn = newlist[inner]
                for i in range(len(inn)):
                    if di[0] == inn[i]:
                        loc1.append(inner)
                        loc1.append(i)
                    if di[1] == inn[i]:
                        loc2.append(inner)
                        loc2.append(i)
            final += newlist[loc1[0]][loc2[1]]
            final += newlist[loc2[0]][loc1[1]] + ' '

        return final

    def form(self, *args):
        self.encipherbutton.disabled = False
        self.digraphbutton.disabled = True
        text = self.plaintextinput.text
        text = text.replace(" ", "")
        text = text.strip()
        #f.write('text: ' + text + '\n')
        tempstr = ''

        count = 0
        yes = 0
        for letter in range(len(text)):
            #f.write(tempstr + '\n')
            if count == 1:
                tempstr = tempstr + text[letter] + ' '
                count = 0
            else:
                try:
                    f.write('match ' + text[letter+1] + '\n')
                    yes = 1
                except Exception as e:
                    yes = 0

                if yes and text[letter] == text[letter+1]:
                    tempstr = tempstr + text[letter] + 'x '
                    count = 0
                else:
                    tempstr = tempstr + text[letter]
                    count += 1


        #f.write('length: ' + str(len(tempstr)) + '\n')
        #f.write(str(len(tempstr)) + '\n')
        check = tempstr.replace(' ', '')

        if (len(check) % 2) != 0:
            tempstr = tempstr + 'x'


        self.plaintextinput.text = tempstr

    def creategrid(self, *args):
        f.write('creating grid...\n')
        #alphabet without j
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        newalpha = []
        for letter in self.keyworddisplay.text:
            for i in self.alpha:
                #f.write(self.alpha[letter] + '==' + self.keyword[i] + '\n')
                if letter == i:
                    self.alpha.remove(i)

        keylist = list(self.keyworddisplay.text)
        shuffle(self.alpha)
        self.comb = keylist + self.alpha
        #f.write('combined list: ' + str(self.comb) + '\n')

        count = 0
        tempstr = ''
        for i in self.comb:
            if count == 5:
                tempstr += '\n'
                count = 0
            tempstr += i + '  '
            count += 1

        self.tablelabel.text = tempstr
################################################################################
#End Playfair Cipher Page
################################################################################

################################################################################
#Begin Homophonic Page
################################################################################
class HomophonicPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('homophonic page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.big = []
        self.bigdict = {}

        self.stralpha = '  '.join(self.alpha)
        #setup layouts
        self.r = RelativeLayout()
        self.verticalnums = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Homophonic Cipher")

        #elements of the page
        self.plaintextinput = TextInput(pos_hint = {'x':.2, 'top':.15},
                                    size_hint = (.35, .15))
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.225},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.15},
                                            size_hint = (.35, .15),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.225},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.015, 'top':.15},
                                        size_hint = (.175,.075),
                                        on_release = self.encipherPressed)
        self.alphadisplay = Label(text = self.stralpha,
                                        pos_hint = {'x':.4, 'top':.615},
                                        size_hint = (.2,.2),
                                        font_name = 'font/RobotoMono-Regular',
                                        font_size = 16)
        self.createlists()

        with open('texts/homophonic.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':.95},
                            size_hint = (.5,.5))


        self.r.add_widget(self.alphadisplay)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.verticalnums)
        self.r.add_widget(self.text)

        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.encrypt()
        self.ciphertextdisplay.text = enciphered

    def encrypt(self, *args):
        f.write("encrypting homophonic...\n")
        text = self.plaintextinput.text
        encrypted = ""
        for letter in text:
            temp = self.bigdict.get(letter)
            encrypted += str(choice(temp)) + ' '

        return encrypted

    def createlists(self, *args):
        numlist = [8, 2, 3, 4, 12, 2, 2, 6, 6, 1, 1, 4, 2, 6, 7,
                    2, 1, 6, 6, 9, 3, 1, 2, 1, 2, 1]
        listrange = range(0, 100)

        for i in numlist:
            smol = []
            for k in range(i):
                num = choice(listrange)
                listrange.remove(num)
                smol.append(num)
            self.big.append(smol)
        f.write("big: " + str(self.big) + '\n')

        tempx = -.4725
        temptop = .825
        for smol in self.big:
            temp = Label(text = '',
                                pos_hint = {'x':tempx, 'top':temptop},
                                size_hint = (1,1),
                                font_size = 12,
                                valign = 'top',
                                halign = 'center',
                                font_name = 'font/RobotoMono-Regular')
            temp.text_size = (temp.width*2, temp.height*2)


            for i in smol:
                temp.text += str(i) + '\n'
            tempx += .03775
            self.verticalnums.add_widget(temp)



        for i in range(len(self.alpha)):
            self.bigdict[self.alpha[i]] = self.big[i]
################################################################################
#End Homophonic Page
################################################################################

################################################################################
#Begin Morse Code Page
################################################################################
class MorsePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('homophonic page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.morsealpha = ['.-', '-...', '-.-.', '-..', '.',
                            '..-.', '--.', '....', '..', '.---',
                            '-.-', '.-..', '--', '-.', '---', '.--.',
                            '--.-', '.-.', '...', '-', '..-', '...-',
                            '.--', '-..-', '-.--', '--..']

        self.stralpha = '|'.join(self.alpha)
        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Morse Code")

        #elements of the page
        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.175},
                                    size_hint = (.35, .15))
        self.plaintextinput.max_chars = 20
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.25},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.175},
                                            size_hint = (.35, .15),
                                            disabled = True,
                                            font_size = 24)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.25},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.015, 'top':.175},
                                        size_hint = (.175,.075),
                                        on_release = self.encipherPressed)

        self.morseimage = Image(source = 'pics/morse.jpg',
                                pos_hint = {'x':.665, 'top':.85},
                                size_hint = (.5,.5))

        with open('texts/morse.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.95},
                            size_hint = (.5,.5))

        with open('texts/morse2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.15, 'top':.6},
                            size_hint = (.5,.5))

        self.vid = VideoPlayer(source = 'video/morseky1.avi',
                            pos_hint = {'x':.015, 'top':.95},
                            size_hint = (.45,.45),
                            state = 'play',
                            options = {'eos': 'loop'},
                            allow_fullscreen = False)

        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)

        self.r.add_widget(self.vid)
        self.r.add_widget(self.morseimage)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)

        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        encrypted = self.morseEncrypt(self.plaintextinput.text)
        self.ciphertextdisplay.text = encrypted

    def morseEncrypt(self, word, *args):
        encrypted = ''
        for letter in word:
            for i in range(len(self.alpha)):
                if letter == self.alpha[i]:
                    encrypted = encrypted + self.morsealpha[i] + ' '

        return encrypted
################################################################################
#End Morse Code Page
################################################################################

################################################################################
#Begin Dancing Men Cipher Page
################################################################################
class DancingMenPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('dancing men page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.images = []

        for i in self.alpha:
            self.images.append('pics/dancingmen/' + i + '.bmp')

        #setup layouts
        self.r = RelativeLayout()
        self.r2 = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Dancing Men Cipher")

        #elements of the page
        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.185},
                                    size_hint = (.35, .175))
        self.plaintextinput.max_chars = 17
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.275},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.185},
                                            size_hint = (.35, .175),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.275},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.025, 'top':.125},
                                        size_hint = (.15,.05),
                                        on_release = self.encipherPressed)

        self.imagedisplay = RelativeLayout()
        tempx = 0
        for image in self.images:
            temp = Image(source = image)
            temp.pos_hint = {'x':tempx, 'top':.45}
            temp.size_hint = (.075,.075)
            self.imagedisplay.add_widget(temp)
            tempx = tempx + .0375

        self.alphalabel = Label(text = '  '.join(self.alpha),
                            pos_hint = {'x':.25, 'top':.6},
                            size_hint = (.5,.5),
                            font_name = 'font/RobotoMono-Regular',
                            font_size = 16)

        with open('texts/dancingmen.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.05, 'top':.95},
                            size_hint = (.5,.5))

        self.image = Image(source = 'pics/dancingmen/danc-01.bmp',
                            pos_hint = {'x':.55, 'top':.95},
                            size_hint = (.5,.5))

        self.r.add_widget(self.alphalabel)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text)
        self.r.add_widget(self.imagedisplay)

        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        #self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)

        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        self.r2.clear_widgets()
        self.r.remove_widget(self.r2)
        self.encodeDancing(self.plaintextinput.text)

    def encodeDancing(self, word, *args):
        templist = []
        x = .5325
        top = .184
        for letter in word:
            if letter == ' ':
                x = x + .04
            else:
                for i in range(len(self.alpha)):
                    if(self.alpha[i] == letter):
                        tempimage = Image(source = self.images[i])
                        x = x + .04

                        if x >= .89:
                            top = top - .08
                            x = .572
                            tempimage.pos_hint = {'x':x, 'top':top}
                            tempimage.size_hint = (.1,.1)
                        else:
                            tempimage.pos_hint = {'x':x, 'top':top}
                            tempimage.size_hint = (.1,.1)
                        self.r2.add_widget(tempimage)

        self.r.add_widget(self.r2)
################################################################################
#End Dancing Men Cipher Page
################################################################################


################################################################################
#Begin Meet Enigma Page
################################################################################
class MeetEnigmaPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('meet enigma entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Meet Enigma")

        with open('texts/enigmameet.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.95},
                            size_hint = (.5,.5),
                            font_size = 16)

        with open('texts/enigmameet2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':0, 'top':.6},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.vid = VideoPlayer(source = 'video/En1_1.avi',
                            pos_hint = {'x':.5, 'top':.55},
                            size_hint = (.45,.45),
                            allow_fullscreen = False)

        self.r.add_widget(self.vid)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Meet Enigma Page
################################################################################

################################################################################
#Begin Codetalkers Page
################################################################################
class CodetalkersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Codetalkers entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Codetalkers")

        with open('texts/codetalkers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.95},
                            size_hint = (.5,.5),
                            font_size = 14)

        with open('texts/codetalkers2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.5, 'top':.375},
                            size_hint = (.5,.5),
                            font_size = 14)

        with open('texts/codetalkers3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.5, 'top':.625},
                            size_hint = (.5,.5),
                            font_size = 12,
                            font_name = 'font/RobotoMono-Regular')

        self.image = Image(source = 'pics/talkers.png',
                            pos_hint = {'x':-.025, 'top':.5},
                            size_hint = (.55,.55))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Codetalkers Page
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
                            pos_hint = {'x':.1, 'top':.975},
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

        self.image = Image(source = "pics/enigma.png",
                            pos_hint = {'x':.05, 'top':.6},
                            size_hint = (.6,.6))
        self.imagelabel = Label(text = 'Image source: https://www.scienceabc.com/',
                            pos_hint = {'x':.6, 'top':.125},
                            size_hint = (.2,.2),
                            font_size = 12)

        self.r.add_widget(self.birthbutton)
        self.r.add_widget(self.imagelabel)
        self.r.add_widget(self.image)
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
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MOFS().create())

    def agePressed(self, *args):
        f.write('age of the internet pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AOTI().create())

    def futurePressed(self, *args):
        f.write('future of Cryptography pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(FOC().create())
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
        buttonx = .775
        buttonht = .165
        buttonw = .125
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Birth of Cryptography")

        with open('texts/birthofc.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.7},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Transposition",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Substitution",
                                        pos_hint = {'x':buttonx, 'top':.725},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Cracking the\nSubstitution\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.55},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Key Secrets",
                                        pos_hint = {'x':buttonx, 'top':.375},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "The\nTragedy of\nMary Queen\nof Scots",
                                        pos_hint = {'x':buttonx, 'top':.2},
                                        size_hint = (buttonht,buttonw),
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
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CrackingSubstitutionPage().create())

    def fourPressed(self, *args):
        f.write('key secrets pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(KeySecretsPage().create())

    def fivePressed(self, *args):
        f.write('tragedy of mary queen of scots pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TragedyPage().create())
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
        buttonx = .8
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
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Latin Square",
                                        pos_hint = {'x':buttonx, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Scytale",
                                        pos_hint = {'x':buttonx, 'top':.55},
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
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RailfencePage().create())

    def twoPressed(self, *args):
        f.write('latin square pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(LatinSquarePage().create())

    def threePressed(self, *args):
        f.write('scytale pressed\n')
        #MyApp.trail.append(self)
        #root.clear_widgets()
        #root.add_widget(RailfencePage().create())
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
        buttonx = .75
        buttonht = .175
        buttonw = .115

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Substitution")

        with open('texts/substitution.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.7},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Caesar\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.875},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Kama-Sutra\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.725},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Pigpen\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.575},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Atbash\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.425},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "Affine\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.275},
                                        size_hint = (buttonht,buttonw),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.button6 = Button(text = "General Mono-\nalphabetic\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.125},
                                        size_hint = (buttonht,buttonw),
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
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(KamasutraPage().create())

    def threePressed(self, *args):
        f.write('pigpen pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PigpenPage().create())

    def fourPressed(self, *args):
        f.write('atbash pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AtbashPage().create())

    def fivePressed(self, *args):
        f.write('affine pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AffinePage().create())

    def sixPressed(self, *args):
        f.write('general Monoalphabetic pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(GenMonoPage().create())
################################################################################
#End Substitution Page
################################################################################

################################################################################
#Begin Kamasutra Shift Page
################################################################################
class KamasutraPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('kamasutra page entered\n')
        MyApp.current = self
        self.newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.cipheralpha = []

        #setup layouts
        self.r = RelativeLayout()
        self.r2 = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Kama-Sutra Cipher")

        #elements of the page
        self.randomize = Button(text = 'Randomize Cipher\nAlphabet',
                            pos_hint = {'x':.015, 'top':.2},
                            size_hint = (.175,.075),
                            on_release = self.genrandomPressed)

        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.175},
                                    size_hint = (.35, .15))
        self.plaintextinput.max_chars = 150
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.25},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.6, 'top':.175},
                                            size_hint = (.35, .15),
                                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.25},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.015, 'top':.1},
                                        size_hint = (.175,.075),
                                        on_release = self.encipherPressed)

        with open('texts/kamasutra.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.975},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.instructions = Label(text = 'Type your message into the box labeled Plaintext, then click the\n' +
                                        'button labeled Encipher Text to encrypt your message.',
                                    pos_hint = {'x':.25, 'top':.525},
                                    size_hint = (.5,.5))

        self.image = Image(source = 'pics/KAMAbk.bmp',
                            pos_hint = {'x':.6, 'top':1.05},
                            size_hint = (.6,.6))



        shuffle(self.newalpha)
        j = 0
        temp = []
        count = 0
        for i in self.newalpha:
            if j < 1:
                temp.append(i)
                j += 1
            else:
                temp.append(i)
                self.cipheralpha.append(temp)
                j = 0
                temp = []
            count += 1

        f.write('cipheralpha: ' + str(self.cipheralpha) + '\n')
        x = .1
        top = .5
        for pair in self.cipheralpha:
            templabel = Label(text = pair[0] + '\n\n' + pair[1],
                                font_size = 16)
            spacelabel = Label(text = '|\n\n|',
                                font_size = 16)
            templabel.pos_hint = {'x':x, 'top':top}
            templabel.size_hint = (.05,.05)
            x = x + .03
            spacelabel.pos_hint = {'x':x, 'top':top}
            spacelabel.size_hint = (.05,.05)
            x = x + .03
            self.r2.add_widget(templabel)
            self.r2.add_widget(spacelabel)

        self.r.add_widget(self.randomize)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)

        self.r.add_widget(self.text)
        self.r.add_widget(self.instructions)
        self.r.add_widget(self.image)
        self.r.add_widget(self.r2)
        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.kamaencrypt(self.plaintextinput.text)
        self.ciphertextdisplay.text = enciphered

    def genrandomPressed(self, *args):
        f.write('generate random cipher pressed\n')
        self.cipheralpha = []
        self.r2.clear_widgets()
        self.r.remove_widget(self.r2)
        shuffle(self.newalpha)
        j = 0
        temp = []
        count = 0
        for i in self.newalpha:
            if j < 1:
                temp.append(i)
                j += 1
            else:
                temp.append(i)
                self.cipheralpha.append(temp)
                j = 0
                temp = []
            count += 1
        f.write('cipheralpha: ' + str(self.cipheralpha) + '\n')

        tempx = .1
        temptop = .5
        for pair in self.cipheralpha:
            templabel = Label(text = pair[0] + '\n\n' + pair[1],
                                font_size = 16)
            spacelabel = Label(text = '|\n\n|',
                                font_size = 16)
            templabel.pos_hint = {'x':tempx, 'top':temptop}
            templabel.size_hint = (.05,.05)
            tempx = tempx + .03
            spacelabel.pos_hint = {'x':tempx, 'top':temptop}
            spacelabel.size_hint = (.05,.05)
            tempx = tempx + .03
            self.r2.add_widget(templabel)
            self.r2.add_widget(spacelabel)

        self.r.add_widget(self.r2)

    def kamaencrypt(self, word, *args):
        enciphered = ""
        for i in word:
            for k in self.cipheralpha:
                if i in k:
                    if k[0] == i:
                        enciphered += k[1]
                    else:
                        enciphered += k[0]

            if (i == " "):
                enciphered += " "

        return enciphered
################################################################################
#End Kamasutra Page
################################################################################

################################################################################
#Begin Affine Page
################################################################################
class AffinePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('affine cipher entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Affine Cipher")

        with open('texts/affine.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':0, 'top':.8},
                            size_hint = (.5,.5),
                            font_size = 16)

        with open('texts/affine2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.5, 'top':.8},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Affine Page
################################################################################

################################################################################
#Begin Cracking Substitution Page
################################################################################
class CrackingSubstitutionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('cracking Substitution page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cracking the Substitution Cipher")

        with open('texts/crackingsubstitution.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.9},
                            size_hint = (.5,.5),
                            font_size = 14)

        self.button1 = Button(text = "Invention in\nBaghdad",
                                        pos_hint = {'x':.8, 'top':.875},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "How it Works",
                                        pos_hint = {'x':.8, 'top':.7},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Finer Points",
                                        pos_hint = {'x':.8, 'top':.525},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Statistics",
                                        pos_hint = {'x':.8, 'top':.35},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("invention in baghdad pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(InventionInBaghdadPage().create())

    def twoPressed(self, *args):
        f.write('how it works pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowFreqPage().create())

    def threePressed(self, *args):
        f.write('finer points pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(FinerPointsPage().create())

    def fourPressed(self, *args):
        f.write('statistics pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(StatisticsPage().create())
################################################################################
#End Cracking Substitution Page
################################################################################

################################################################################
#Begin InventionInBaghdad Page
################################################################################
class InventionInBaghdadPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('invention in baghdad entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Invention in Baghdad")

        with open('texts/inventioninbagh.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.95},
                            size_hint = (.5,.5),
                            font_size = 16)

        with open('texts/inventioninbagh2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.03, 'top':.5},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.vid = VideoPlayer(source = 'video/mray2.avi',
                                pos_hint = {'x':.5, 'top':.525},
                                size_hint = (.5,.5),
                                state = 'stop')

        self.r.add_widget(self.vid)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End InventionInBaghdad Page
################################################################################

################################################################################
#Begin Finer Points Page
################################################################################
class FinerPointsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('finer points entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Finer Points")

        with open('texts/finerpoints.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.7},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Finer Points Page
################################################################################

################################################################################
#Begin Statistics Page
################################################################################
class StatisticsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('statistics page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Statistics")

        with open('texts/statistics.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.935},
                            size_hint = (.5,.5),
                            font_size = 14)

        self.image = Image(source = 'pics/stats-edt.png',
                            pos_hint = {'x':0.025, 'top':.69},
                            size_hint = (.9,.9))


        self.r.add_widget(self.text1)
        self.r.add_widget(self.image)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Statistics Page
################################################################################


################################################################################
#Begin Key Secrets Page
################################################################################
class KeySecretsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('key secrets page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Key Secrets")

        with open('texts/keysecrets.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':1.05},
                            size_hint = (.5,.5),
                            font_size = 16)

        with open('texts/keysecrets2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.15, 'top':.425},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.button1 = Button(text = "Number of\nKeys for\nVarious\nCiphers",
                                        pos_hint = {'x':.8, 'top':.375},
                                        size_hint = (.15,.15),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Kerckhoffs'\nPrinciple",
                                        pos_hint = {'x':.8, 'top':.175},
                                        size_hint = (.15,.15),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.image = Image(source = 'pics/keysecrets.png',
                            pos_hint = {'x':.05, 'top':1.005},
                            size_hint = (.9,.9))

        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("number of keys for various ciphers pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(VariousCiphersPage().create())

    def twoPressed(self, *args):
        f.write('kerckhoffs principle pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(KerckhoffsPage().create())
################################################################################
#End Key Secrets Page
################################################################################

################################################################################
#Begin Various Ciphers Page
################################################################################
class VariousCiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('various ciphers entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Number of Keys for Various Ciphers")

        with open('texts/variousciphers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.425, 'top':.9},
                            size_hint = (.15,.15))

        self.table = Image(source = 'pics/keystable.png',
                            pos_hint = {'x':.1, 'top':.8},
                            size_hint = (.8,.8))

        self.r.add_widget(self.table)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Various Ciphers Page
################################################################################

################################################################################
#Begin Kerckhoffs Page
################################################################################
class KerckhoffsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Kerckhoffs principle entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Kerckhoffs Principle")

        with open('texts/kerckhoffs.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.425, 'top':.85},
                            size_hint = (.15,.15),
                            font_size = 16)

        with open('texts/kerckhoffs2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.425, 'top':.525},
                            size_hint = (.15,.15),
                            font_size = 16)

        with open('texts/kerckhoffs3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.45, 'top':.2},
                            size_hint = (.15,.15),
                            font_size = 16)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Kerckhoffs Page
################################################################################

################################################################################
#Begin Tragedy of Mary Queen Scots Page
################################################################################
class TragedyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('tragedy of mary queen scots page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Tragedy of Mary Queen of Scots")

        with open('texts/mary.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.9},
                            size_hint = (.5,.5),
                            font_size = 16)

        self.button1 = Button(text = "The Babington\nPlot",
                                        pos_hint = {'x':.8, 'top':.775},
                                        size_hint = (.15,.15),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Cracking the\nBabington\nCipher",
                                        pos_hint = {'x':.8, 'top':.575},
                                        size_hint = (.15,.15),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "The Execution\nof Mary",
                                        pos_hint = {'x':.8, 'top':.375},
                                        size_hint = (.15,.15),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.image = Image(source = 'pics/maryciph.bmp',
                            pos_hint = {'x':.15, 'top':.5},
                            size_hint = (.5,.5))

        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("the babington plot pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BabingtonPlotPage().create())

    def twoPressed(self, *args):
        f.write('cracking the babington cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CrackingBabingtonPage().create())

    def threePressed(self, *args):
        f.write('execution of mary pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MaryExPage().create())
################################################################################
#End Tragedy of Mary Queen of Scots Page
################################################################################

################################################################################
#Begin Babington Plot Page
################################################################################
class BabingtonPlotPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('babington plot page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Babington Plot")

        with open('texts/babingtonplot.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.425, 'top':.7},
                            size_hint = (.15,.15),
                            font_size = 16)

        self.video = VideoPlayer(source = 'video/mqsexp3.avi',
                            pos_hint = {'x':.5, 'top':.4},
                            size_hint = (.4,.4),
                            state = 'stop',
                            allow_fullscreen = False)

        self.instructions = Label(text = "The video clip shows Babington's list of cipher\n" +
                                        "substitutions and how they would have been used\n" +
                                        "to encrypt a message.",
                                    pos_hint = {'x':.2, 'top':.3},
                                    size_hint = (.15,.15))

        self.r.add_widget(self.instructions)
        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Babington Plot Page
################################################################################

################################################################################
#Begin Cracking Babington Plot Page
################################################################################
class CrackingBabingtonPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('cracking babington plot page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cracking the Babington Cipher")

        with open('texts/crackingbabington.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.7},
                            size_hint = (.15,.15),
                            font_size = 16)

        with open('texts/crackingbabington2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.1925, 'top':.325},
                            size_hint = (.15,.15),
                            font_size = 16)

        self.video = VideoPlayer(source = 'video/marcrac2.avi',
                            pos_hint = {'x':.5, 'top':.5},
                            size_hint = (.5,.5),
                            state = 'stop',
                            allow_fullscreen = False)

        self.image = Image(source = 'pics/babing4.png',
                            pos_hint = {'x':0, 'top':1.35},
                            size_hint = (1,1))

        self.r.add_widget(self.image)
        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Cracking Babington Plot Page
################################################################################

################################################################################
#Begin Cracking Babington Plot Page
################################################################################
class MaryExPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('mary execution page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Execution of Mary Queen of Scots")

        with open('texts/exmary.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.75},
                            size_hint = (.15,.15),
                            font_size = 16)

        with open('texts/exmary2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = '[i]' + escape_markup(data2) + '[/i]',
                            markup = True,
                            pos_hint = {'x':.1925, 'top':.325},
                            size_hint = (.15,.15),
                            font_size = 14)

        self.video = VideoPlayer(source = 'video/maryex11.avi',
                            pos_hint = {'x':.5, 'top':.5},
                            size_hint = (.5,.5),
                            state = 'stop',
                            allow_fullscreen = False)

        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Mary Execution Page
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
        self.tb = self.topbar.create("The Uncrackable Code")

        with open('texts/uncrackablecode.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.9},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Vigenere\nCipher",
                                        pos_hint = {'x':.8, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Alternative\nCiphers",
                                        pos_hint = {'x':.8, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Encryption for\nthe Masses",
                                        pos_hint = {'x':.8, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Cracking the\nVigenere\nCipher",
                                        pos_hint = {'x':.8, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("vigenere cipher pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(VigenerePage().create())

    def twoPressed(self, *args):
        f.write('alternative ciphers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AlternativeCiphersPage().create())

    def threePressed(self, *args):
        f.write('encryption for the masses pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(EncryptionForMassesPage().create())

    def fourPressed(self, *args):
        f.write('cracking the vigenere pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CrackingVigenerePage().create())
################################################################################
#End Uncrackable Code Page
################################################################################

################################################################################
#Begin Vigenere Page
################################################################################
class VigenerePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('vigenere page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Vigenere Cipher")

        with open('texts/vigenere.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.7},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Swapping\nCipher\nAlphabets",
                                        pos_hint = {'x':.8, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "The Vigenere\nSquare",
                                        pos_hint = {'x':.8, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "How Vigenere\nWorks",
                                        pos_hint = {'x':.8, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Why is\nVigenere so\nStrong?",
                                        pos_hint = {'x':.8, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("swapping cipher alphabets pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SwappingPage().create())

    def twoPressed(self, *args):
        f.write('vigenere square pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(VigenereSquarePage().create())

    def threePressed(self, *args):
        f.write('how vigenere works pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowVigenerePage().create())

    def fourPressed(self, *args):
        f.write('why vigenere strong pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(StrongVigenerePage().create())
################################################################################
#End Vigenere Page
################################################################################

################################################################################
#Begin Swapping Cipher Page
################################################################################
class SwappingPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('swapping ciphers page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.newalpha1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.newalpha2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        shuffle(self.newalpha1)
        shuffle(self.newalpha2)

        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Swapping Cipher Alphabets")

        #elements of the page
        self.stralpha = ' '.join(self.alpha)
        self.alabel = Label(text = 'Plaintext Alphabet',
                            pos_hint = {'x':.73, 'top':.45},
                            size_hint = (.27,.1),
                            font_size = 11)
        self.alphabet = Label(text = self.stralpha,
                                    pos_hint = {'x':.15, 'top':.425},
                                    size_hint = (.65,.05),
                                    font_name = 'font/RobotoMono-Regular')

        self.clabel1 = Label(text = 'Ciphertext Alphabet 1',
                            pos_hint = {'x':.735, 'top':.35},
                            size_hint = (.27,.1),
                            font_size = 11)

        self.strnewalpha1 = " ".join(self.newalpha1)
        self.cipheralphabet1 = Label(text = '[color=#ff0000]' + escape_markup(self.strnewalpha1) + '[/color]',
                                    markup = True,
                                    pos_hint = {'x':.15, 'top':.325},
                                    size_hint = (.65,.05),
                                    font_name = 'font/RobotoMono-Regular')

        self.clabel2 = Label(text = 'Ciphertext Alphabet 2',
                            pos_hint = {'x':.735, 'top':.29},
                            size_hint = (.27,.1),
                            font_size = 11)

        self.strnewalpha2 = " ".join(self.newalpha2)
        self.cipheralphabet2 = Label(text = '[color=#0000cc]' + escape_markup(self.strnewalpha2) + '[/color]',
                                    markup = True,
                                    pos_hint = {'x':.15, 'top':.265},
                                    size_hint = (.65,.05),
                                    font_name = 'font/RobotoMono-Regular')


        self.plaintextinput = maxinput(pos_hint = {'x':.2, 'top':.1},
                                    size_hint = (.375, .1))
        self.plaintextinput.max_chars = 28
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.25, 'top':.175},
                                    size_hint = (.27,.1))

        self.ciphertextdisplay = Label(text = '',
                                            pos_hint = {'x':.6, 'top':.13},
                                            size_hint = (.375, .1),
                                            markup = True,
                                            font_size = 20)

        self.ciphertextdisplay2 = Label(text = '',
                                            pos_hint = {'x':.6, 'top':.1},
                                            size_hint = (.375, .1),
                                            font_size = 20)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.65, 'top':.175},
                                    size_hint = (.27,.1))

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.025, 'top':.05},
                                        size_hint = (.15,.05),
                                        on_release = self.encipherPressed)

        self.randomizebutton = Button(text = "Randomize",
                                        pos_hint = {'x':.025, 'top':.1},
                                        size_hint = (.15,.05),
                                        on_release = self.randomize)

        with open('texts/swappingcipher.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.25, 'top':.9},
                            size_hint = (.5,.5))

        self.r.add_widget(self.alabel)
        self.r.add_widget(self.alphabet)
        self.r.add_widget(self.clabel1)
        self.r.add_widget(self.cipheralphabet1)
        self.r.add_widget(self.clabel2)
        self.r.add_widget(self.cipheralphabet2)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextdisplay2)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.randomizebutton)

        self.r.add_widget(self.text)

        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        enciphered = self.swapencrypt(self.plaintextinput.text)
        self.ciphertextdisplay.text = enciphered[0]
        self.ciphertextdisplay2.text = enciphered[1]

    def randomize(self, *args):
        f.write('randomize button pressed\n')
        shuffle(self.newalpha1)
        shuffle(self.newalpha2)
        self.cipheralphabet1.text = '[color=#ff0000]' + escape_markup(" ".join(self.newalpha1)) + '[/color]'
        self.cipheralphabet2.text = '[color=#0000cc]' + escape_markup(" ".join(self.newalpha2)) + '[/color]'


    def swapencrypt(self, word, *args):

        enciphered = ""
        enciphered2 = ""

        count = 0
        for letter in word:
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    if count == 0:
                        enciphered += '[color=#ff3333]' + escape_markup(self.newalpha1[i]) + '[/color]'
                        enciphered2 += self.newalpha1[i]
                        count = 1
                    else:
                        enciphered += '[color=#3333ff]' + escape_markup(self.newalpha2[i]) + '[/color]'
                        enciphered2 += self.newalpha2[i]
                        count = 0
            if (letter == " "):
                enciphered += " "

        return [enciphered, enciphered2]
################################################################################
#End Swapping Cipher Page
################################################################################

################################################################################
#Begin Vigenere Square Page
################################################################################
class VigenereSquarePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('vigenere square page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.templist = []
        for i in range(len(self.alpha)):
            tempalpha = deque(self.alpha)
            tempalpha.rotate(len(self.alpha) - (i+1))
            self.templist.append(list(tempalpha))

        self.table = '     ' + '|'.join(self.alpha) + '\n'
        self.table += '   -----------------------------------------------------\n'
        count = 1
        for alph in self.templist:
            if count < 10:
                self.table += str(count) + '  | ' + "|".join(alph) + '\n'
            else:
                self.table += str(count) + ' | ' + "|".join(alph) + '\n'
            count += 1
        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Vigenere Square")

        #elements of the page
        self.tablelabel = Label(text = self.table,
                                    pos_hint = {'x':.45, 'top':.8},
                                    size_hint = (.5,.5),
                                    font_name = 'font/RobotoMono-Regular',
                                    font_size = 11)

        self.nextbutton = Button(text = "Next Page",
                                        pos_hint = {'x':.45, 'top':.09},
                                        size_hint = (.15,.04),
                                        on_release = self.nextPressed)


        with open('texts/vigeneresquare.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.6},
                            font_size = 14,
                            size_hint = (.15,.15))

        self.r.add_widget(self.text)
        self.r.add_widget(self.tablelabel)
        self.r.add_widget(self.nextbutton)

        self.r.add_widget(self.tb)
        return self.r

    def nextPressed(self, *args):
        f.write('next button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(VigenereSquarePage2().create())
################################################################################
#End Vigenere Square Page
################################################################################

################################################################################
#Begin Vigenere Square 2 Page
################################################################################
class VigenereSquarePage2(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('vigenere square page entered\n')
        MyApp.current = self
        self.firstkeyword = ''
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.templist = []
        for i in range(len(self.alpha)):
            tempalpha = deque(self.alpha)
            tempalpha.rotate(len(self.alpha) - (i+1))
            self.templist.append(list(tempalpha))

        self.table = '     ' + '|'.join(self.alpha) + '\n'
        self.table += '   -----------------------------------------------------\n'
        count = 1
        for alph in self.templist:
            if count < 10:
                self.table += str(count) + '  | ' + "|".join(alph) + '\n'
            else:
                self.table += str(count) + ' | ' + "|".join(alph) + '\n'
            count += 1
        #setup layouts
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Vigenere Square")

        #elements of the page
        self.tablelabel = Label(text = self.table,
                                    pos_hint = {'x':.45, 'top':.8},
                                    size_hint = (.5,.5),
                                    font_name = 'font/RobotoMono-Regular',
                                    font_size = 11,
                                    markup = True)

        self.keywordinput = TextInput(pos_hint = {'x':.55, 'top':.185},
                                    size_hint = (.4, .05),
                                    text = 'white',
                                    font_name = 'font/RobotoMono-Regular')
        self.keywordlabel = Label(text = 'Keyword',
                                    pos_hint = {'x':.375, 'top':.205},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.plaintextinput = TextInput(pos_hint = {'x':.55, 'top':.12},
                                    size_hint = (.4, .05),
                                    text = 'divert troops to east ridge',
                                    font_name = 'font/RobotoMono-Regular')
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.375, 'top':.14},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.ciphertextdisplay = TextInput(text = '',
                                            pos_hint = {'x':.55, 'top':.055},
                                            size_hint = (.4, .05),
                                            disabled = True,
                                            font_name = 'font/RobotoMono-Regular')
        self.ciphertextlabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.375, 'top':.075},
                                    size_hint = (.27,.1),
                                    font_size = 13)

        self.encipherbutton = Button(text = "Encipher Text",
                                        pos_hint = {'x':.075, 'top':.125},
                                        size_hint = (.15,.04),
                                        on_release = self.encipherPressed,
                                        disabled = True)

        self.repeatbutton = Button(text = "Repeat Keyword",
                                        pos_hint = {'x':.075, 'top':.05},
                                        size_hint = (.15,.04),
                                        on_release = self.repeatPressed)


        with open('texts/vigeneresquare2.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.6},
                            font_size = 14,
                            size_hint = (.15,.15))

        self.r.add_widget(self.text)
        self.r.add_widget(self.tablelabel)
        self.r.add_widget(self.keywordinput)
        self.r.add_widget(self.keywordlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.repeatbutton)

        self.r.add_widget(self.tb)
        return self.r

    def encipherPressed(self, *args):
        f.write('encipher button pressed\n')
        self.repeatbutton.disabled = False
        self.encipherbutton.disabled = True
        enciphered = self.encrypt()
        self.ciphertextdisplay.text = enciphered

    def repeatPressed(self, *args):
        f.write('repeat button pressed\n')
        self.repeatbutton.disabled = True
        self.encipherbutton.disabled = False
        self.firstkeyword = self.keywordinput.text
        self.plaintextinput.text = self.plaintextinput.text.replace(' ','')
        keyword = self.keywordinput.text
        text = self.plaintextinput.text
        tempkeyword = ''
        times = len(text) / len(keyword)

        for i in range(times):
            tempkeyword += keyword

        leftover = len(text) - len(tempkeyword)
        tempkeyword += keyword[:leftover]

        self.keywordinput.text = tempkeyword

    def encrypt(self, *args):
        enciphered = ''
        keyword = self.firstkeyword
        fullkeyword = self.keywordinput.text
        text = self.plaintextinput.text
        indexes = []
        for letter in keyword:
            for i in range(len(self.templist)):
                alph = self.templist[i]
                if alph[0] == letter:
                    f.write('index: ' + str(i) + '\n')
                    f.write(alph[0] + ' | ' + letter + '\n')
                    if i not in indexes:
                        indexes.append(i)
        indexes = sorted(indexes, key=int)
        f.write(str(indexes) + '\n')

        #"[color=#e9ff00][/color]"
        self.table = '     ' + '|'.join(self.alpha) + '\n'
        self.table += '   -----------------------------------------------------\n'
        count = 0
        yes = False
        for alph in range(len(self.templist)):
            try:
                if indexes[count] == alph:
                    yes = True
                    count += 1
                else:
                    yes = False
            except IndexError:
                yes = False

            if yes:
                f.write(str(self.templist[alph]) + '\n')
                if alph < 9:
                    self.table += '[color=#e9ff00]' + str(alph+1) + '  | ' + "|".join(self.templist[alph]) + '[/color]\n'
                else:
                    self.table += '[color=#e9ff00]' + str(alph+1) + ' | ' + "|".join(self.templist[alph]) + '[/color]\n'
            else:
                if alph < 9:
                    self.table += str(alph+1) + '  | ' + "|".join(self.templist[alph]) + '\n'
                else:
                    self.table += str(alph+1) + ' | ' + "|".join(self.templist[alph]) + '\n'

        f.write(self.table)

        self.tablelabel.text = self.table

        for j in range(len(text)):
            for index in indexes:
                if self.templist[index][0] == fullkeyword[j]:
                    enciphered += self.templist[index][self.alpha.index(text[j])]

        return enciphered
################################################################################
#End Vigenere Square 2 Page
################################################################################

################################################################################
#Begin How Vigenere Works Page
################################################################################
class HowVigenerePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('how vigenere works page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("How Vigenere Works")

        with open('texts/howvigenereworks.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.45, 'top':.8},
                            size_hint = (.15,.15),
                            font_size = 16)

        self.video = VideoPlayer(source = 'video/chf3-1-7.avi',
                            pos_hint = {'x':.215, 'top':.7},
                            size_hint = (.6,.6),
                            state = 'stop',
                            allow_fullscreen = False)

        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End How Vigenere Works Page
################################################################################

################################################################################
#Begin Why so strong Vigenere Page
################################################################################
class StrongVigenerePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('why vigenere strong page entered\n')
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.monoalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.letterdict = {}
        self.firstkeyword = ''

        shuffle(self.monoalpha)
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Why is Vigenere so Strong")

        with open('texts/strongvigenere.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.425, 'top':.9},
                            size_hint = (.15,.15),
                            font_size = 16)

        self.plaintext = TextInput(text = 'aged twenty six, Vigenere was sent to Rome on a diplomatic' +
        'mission. It was here that he became acquainted with the writings of Alberti, Trithemius and Porta, ' +
        'and his interest in cryptography was ignited. For many years, cryptography was nothing more than a ' +
        'tool that helped him in his diplomatic work, but, at the age of thirty nine, Vigenere decided ' +
        'that he had amassed enough money to be able to abandon his career and concentrate on a life of study' +
        ' It was only then that he began research into a new cipher.',
                            pos_hint = {'x':.05, 'top':.75},
                            size_hint = (.6,.2),
                            font_size = 11,
                            disabled = True)
        self.getfreq(self.plaintext.text)

        self.plainscrollview = ScrollView(size_hint=(1, None), size=(self.plaintext.width, self.plaintext.height))

        self.enciphermono = Button(text = 'Encipher Mono',
                            pos_hint = {'x':.25, 'top':.535},
                            size_hint = (.15,.05),
                            on_release = self.monoen)

        self.plaintextfreq = Image(source = 'pics/strongvigenere/plaintextfreq.png',
                                    pos_hint = {'x':.575, 'top':.9},
                                    size_hint = (.5,.5))

        self.monocipher = TextInput(text = '',
                                    pos_hint = {'x':.05, 'top':.45},
                                    size_hint = (.6,.2),
                                    multiline = True,
                                    font_size = 11,
                                    disabled = True)

        self.vigcipher = TextInput(text = '',
                                    pos_hint = {'x':.05, 'top':.3},
                                    size_hint = (.15,.15),
                                    disabled = True)

        self.alphal = Label(text = ' '.join(self.alpha),
                            pos_hint = {'x':.275, 'top':.59},
                            size_hint = (.15,.15),
                            font_name = 'font/RobotoMono-Regular')

        self.monol = Label(text = '[color=#ff0000]' + escape_markup(' '.join(self.monoalpha)) + '[/color]',
                            pos_hint = {'x':.275, 'top':.56},
                            size_hint = (.15,.15),
                            font_name = 'font/RobotoMono-Regular',
                            markup = True)

        self.monofreq = Image(source = 'pics/strongvigenere/monofreq.png',
                                    pos_hint = {'x':.575, 'top':.6},
                                    size_hint = (.5,.5))


        self.enciphervig = Button(text = 'Encipher Vigenere',
                            pos_hint = {'x':.25, 'top':.235},
                            size_hint = (.2,.05),
                            on_release = self.vigen)

        self.vig = TextInput(text = '',
                            pos_hint = {'x':.05, 'top':.225},
                            size_hint = (.6,.2),
                            multiline = True,
                            font_size = 11,
                            disabled = True)

        """self.plaingraph = Graph(xlabel = 'Letter', ylabel = 'Frequency', x_ticks_minor=5,
                                x_ticks_major=25, y_ticks_major=1,
                                y_grid_label=True, x_grid_label=True, padding=5,
                                x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1,
                                pos_hint = {'x':.5, 'top':.5},
                                size_hint = (.4,.4))"""
        #plot = MeshLinePlot(color = [1,0,0,1])

        #plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        #plot.points = [(for i in self.letterdict.values())]
        #self.plaingraph.add_plot(plot)

        #self.r.add_widget(self.plainscrollview)

        #self.r.add_widget(self.plaingraph)
        self.r.add_widget(self.plaintextfreq)
        self.r.add_widget(self.plaintext)
        self.r.add_widget(self.enciphermono)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def vigen(self, *args):
        enciphered = self.vigencrypt()
        self.vig.text = enciphered
        self.r.remove_widget(self.enciphervig)
        self.r.add_widget(self.vig)



    def monoen(self, *args):
        enciphered = self.monoencrypt(self.plaintext.text, True)
        self.monocipher.text = enciphered
        #self.monocipher.foreground_color = (255, 0, 0)
        self.r.remove_widget(self.enciphermono)
        self.r.add_widget(self.monocipher)
        self.r.add_widget(self.alphal)
        self.r.add_widget(self.monol)
        self.r.add_widget(self.monofreq)
        self.r.add_widget(self.enciphervig)

    def monoencrypt(self, word, spaces, *args):
        enciphered = ""

        #iterate through the string of text
        for letter in word:
            #iterate through the alphabet list
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    enciphered += self.monoalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "

        return enciphered

    def getfreq(self, text, *args):
        f.write('getting frequencies...\n')
        text = text.lower()
        text = text.replace(' ', '')
        text = text.replace('.', '')
        text = text.replace(',', '')

        for i in self.alpha:
            self.letterdict[str(i)] = 0
        for letter in text:
            self.letterdict[str(letter)] = self.letterdict[str(letter)] + 1

        f.write(str(self.letterdict) + '\n')

    def vigencrypt(self, *args):
        enciphered = ''
        keyword = 'charlesv'
        text = self.plaintext.text
        text = text.lower()
        #text = text.replace(' ', '')
        text = text.replace('.', '')
        text = text.replace(',', '')
        tempkeyword = ''
        times = len(text) / len(keyword)

        for i in range(times):
            tempkeyword += keyword

        leftover = len(text) - len(tempkeyword)
        tempkeyword += keyword[:leftover]

        fullkeyword = tempkeyword
        indexes = []
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        self.templist = []
        for i in range(len(self.alpha)):
            tempalpha = deque(self.alpha)
            tempalpha.rotate(len(self.alpha) - (i+1))
            self.templist.append(list(tempalpha))

        for letter in keyword:
            for i in range(len(self.templist)):
                alph = self.templist[i]
                if alph[0] == letter:
                    #f.write('index: ' + str(i) + '\n')
                    #f.write(alph[0] + ' | ' + letter + '\n')
                    if i not in indexes:
                        indexes.append(i)
        indexes = sorted(indexes, key=int)
        #f.write(str(indexes) + '\n')

        for j in range(len(text)):
            #f.write(str(text[j]) + '\n')
            for index in indexes:
                if self.templist[index][0] == fullkeyword[j]:
                    try:
                        enciphered += self.templist[index][self.alpha.index(str(text[j]))]
                    except Exception as e:
                        enciphered += ' '

        return enciphered
################################################################################
#End Why so strong Vigenere Page
################################################################################

################################################################################
#Begin Alternative Ciphers Page
################################################################################
class AlternativeCiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('alternative ciphers page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Alternative Ciphers")

        with open('texts/alternativeciphers.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.125, 'top':.7},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Digraph\nSubstitution",
                                        pos_hint = {'x':.75, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Playfair Cipher",
                                        pos_hint = {'x':.75, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Homophonic\nCipher",
                                        pos_hint = {'x':.75, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Book Ciphers",
                                        pos_hint = {'x':.75, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("digraph pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(DigraphPage().create())

    def twoPressed(self, *args):
        f.write('playfair pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PlayfairPage().create())

    def threePressed(self, *args):
        f.write('homophonic cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HomophonicPage().create())

    def fourPressed(self, *args):
        f.write('book ciphers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BookCiphersPage().create())

################################################################################
#End Alternative Ciphers Page
################################################################################

################################################################################
#Begin Book Ciphers Page
################################################################################
class BookCiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('book ciphers page entered\n')
        MyApp.current = self
        self.keytexts = ["On either side of the river lie long fields of barley " +
                            "and of rye, that clothes the world and meets the " +
                            "the sky; and through the field the road runs by to many " +
                            "towered Camelot, and up and down the people go, gazing " +
                            "where the lillies blwo round an island there below, the " +
                            "island of Shalott."]
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Book Ciphers")

        with open('texts/bookciphers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.325, 'top':.75},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.button = Button(text = 'Beale Ciphers',
                            pos_hint = {'x':.8, 'top':.5},
                            size_hint = (.15,.05),
                            on_release = self.beale)

        self.keytext = TextInput(text = self.keytexts[0],
                            pos_hint = {'x':.3, 'top':.4},
                            size_hint = (.695,.2),
                            disabled = True)
        self.keytextlabel = Label(text = 'Keytext',
                            pos_hint = {'x':.575, 'top':.5},
                            size_hint = (.15,.15),
                            font_size = 12)

        self.plaintext = TextInput(text = 'mary had a little lamb',
                            pos_hint = {'x':.3, 'top':.15},
                            size_hint = (.32,.15),
                            disabled = True)
        self.plaintextlabel = Label(text = 'Plaintext',
                            pos_hint = {'x':.375, 'top':.25},
                            size_hint = (.15,.15),
                            font_size = 12)

        self.ciphertext = TextInput(text = '',
                            pos_hint = {'x':.675, 'top':.15},
                            size_hint = (.32,.15),
                            disabled = True)
        self.ciphertextlabel = Label(text = 'Ciphertext',
                            pos_hint = {'x':.75, 'top':.25},
                            size_hint = (.15,.15),
                            font_size = 12)

        self.encipherbutton = Button(text = 'Encipher',
                            pos_hint = {'x':.1, 'top':.2},
                            size_hint = (.15,.05),
                            on_release = self.encipherpressed)



        self.r.add_widget(self.keytextlabel)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.encipherbutton)
        self.r.add_widget(self.plaintext)
        self.r.add_widget(self.ciphertext)
        self.r.add_widget(self.keytext)
        self.r.add_widget(self.button)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def beale(self, *args):
        f.write('beale ciphers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TheBealeCiphersPage().create())

    def encipherpressed(self, *args):
        f.write('encipher button pressed\n')
        self.ciphertext.text = self.encrypt()


    def encrypt(self, *args):
        keytext = self.keytext.text
        keytext = keytext.lower()
        keytext = keytext.replace(' ', '')
        keytext = keytext.replace(',', '')
        keytext = keytext.replace('.', '')
        enciphered = ''
        plaintext = self.plaintext.text
        temptext = plaintext.replace(' ', '')

        letterdict = {}
        #populate dictionary of the possible letters and their indexes
        for i in range(len(keytext)):
            letterdict[str(keytext[i])] = [i] + letterdict.get(str(keytext[i]), [])

        f.write(str(letterdict))

        #iterate through the plaintext and randomly choose indexes of the letters
        #within the plaintext
        for letter in temptext:
            templist = letterdict.get(letter)
            enciphered += str(choice(templist)) + ' '

        return enciphered

################################################################################
#End Book Ciphers Page
################################################################################

################################################################################
#Begin Beale Ciphers Page
################################################################################
class TheBealeCiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('beale ciphers page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Beale Ciphers")

        with open('texts/bealeciphers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.225, 'top':.6},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.image = Image(source = 'pics/beale/beale1.bmp',
                            pos_hint = {'x':.4, 'top':.8},
                            size_hint = (.7,.7))


        self.button1 = Button(text = "The Beale Papers Page 1",
                                        pos_hint = {'x':.05, 'top':.075},
                                        size_hint = (.25,.05),
                                        on_release = self.onePressed)

        self.button2 = Button(text = "The Beale Papers Page 2",
                                        pos_hint = {'x':.375, 'top':.075},
                                        size_hint = (.25,.05),
                                        on_release = self.twoPressed)

        self.button3 = Button(text = "The Beale Papers Page 3",
                                        pos_hint = {'x':.7, 'top':.075},
                                        size_hint = (.25,.05),
                                        on_release = self.threePressed)


        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("page1 pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BealePage1().create())

    def twoPressed(self, *args):
        f.write('page2 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BealePage2().create())

    def threePressed(self, *args):
        f.write('page3 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BealePage3().create())
################################################################################
#End Beale Ciphers Page
################################################################################


################################################################################
#Begin Beale Page 1
################################################################################
class BealePage1(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('beale page 1 entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Beale Papers Page 1")

        self.image = Image(source = 'pics/beale/beale3.bmp',
                            pos_hint = {'x':.125, 'top':.85},
                            size_hint = (.8,.8))

        self.r.add_widget(self.image)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Beale Page 1
################################################################################


################################################################################
#Begin Beale Page 2
################################################################################
class BealePage2(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('beale page 2 entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Beale Papers Page 2")

        self.image = Image(source = 'pics/beale/beale2.bmp',
                            pos_hint = {'x':.125, 'top':.85},
                            size_hint = (.8,.8))

        self.button = Button(text = 'Decipher',
                            pos_hint = {'x':.075, 'top':.85},
                            size_hint = (.15,.05),
                            on_release = self.decipherpressed)

        self.button2 = Button(text = 'Beale Paper 2',
                            pos_hint = {'x':.075, 'top':.85},
                            size_hint = (.15,.05),
                            on_release = self.beale2pressed)

        self.image2 = Image(source = 'pics/beale/beale2text.bmp',
                            pos_hint = {'x':.125, 'top':.85},
                            size_hint = (.8,.8))

        self.r.add_widget(self.button)
        self.r.add_widget(self.image)
        self.r.add_widget(self.tb)
        return self.r

    def decipherpressed(self, *args):
        f.write('decipher pressed\n')
        self.r.remove_widget(self.button)
        self.r.remove_widget(self.image)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.image2)

    def beale2pressed(self, *args):
        f.write('beale 2 paper pressed\n')
        self.r.remove_widget(self.button2)
        self.r.remove_widget(self.image2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.image)
################################################################################
#End Beale Page 2
################################################################################


################################################################################
#Begin Beale Page 3
################################################################################
class BealePage3(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('beale page 3 entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Beale Papers Page 3")

        self.image = Image(source = 'pics/beale/beale4.bmp',
                            pos_hint = {'x':.125, 'top':.85},
                            size_hint = (.8,.8))

        self.r.add_widget(self.image)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Beale Page 3
################################################################################

################################################################################
#Begin Encryption for the Masses Code Page
################################################################################
class EncryptionForMassesPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('encryption for the masses page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Encryption for the Masses")

        with open('texts/encryptionforthemasses.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.15, 'top':.75},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Morse Code",
                                        pos_hint = {'x':.8, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Dancing Men\nCipher",
                                        pos_hint = {'x':.8, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Agony\nColumns",
                                        pos_hint = {'x':.8, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Pinprick\nCipher",
                                        pos_hint = {'x':.8, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("morse code pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MorsePage().create())

    def twoPressed(self, *args):
        f.write('dancing men cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(DancingMenPage().create())

    def threePressed(self, *args):
        f.write('agony columns pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AgonyColumnsPage().create())

    def fourPressed(self, *args):
        f.write('pinprick cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PinprickPage().create())
################################################################################
#End Encryption for the Masses Page
################################################################################

################################################################################
#Begin Agony Columns Page
################################################################################
class AgonyColumnsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('agony columns page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Agony Columns")

        with open('texts/agonycolumns.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.775},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.image = Image(source = 'pics/agonycolumns.png',
                            pos_hint = {'x':.1, 'top':.65},
                            size_hint = (.8,.8))

        self.caption = Label(text = '[i]' + escape_markup('The bottom left note is encrypted with a transposition cipher, in which each word' +
                            ' is written backwards. The lower\nright note has been encrypted with the atbash substitution ' +
                            'cipher, in which the ciphertext alphabet is the reverse of\nthe normal alphabet: a becomes Z, ' +
                            'b becomes Y, and so on.') + '[/i]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            font_size = 12,
                            markup = True)

        self.r.add_widget(self.caption)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Agony Columns Page
################################################################################


################################################################################
#Begin Pinprick Cipher Page
################################################################################
class PinprickPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('pinprick page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Pinprick Cipher")

        with open('texts/pinprickcipher.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.7},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.image = Image(source = 'pics/pin.png',
                            pos_hint = {'x':.4, 'top':.4},
                            size_hint = (.4,.4))

        self.dot1 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.27, 'top':.8},
                            size_hint = (.005,.005))
        self.dot2 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.3375, 'top':.745},
                            size_hint = (.005,.005))
        self.dot3 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.38, 'top':.659},
                            size_hint = (.005,.005))
        self.dot4 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.307, 'top':.574},
                            size_hint = (.005,.005))
        self.dot5 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.445, 'top':.517},
                            size_hint = (.005,.005))
        self.dot6 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.5675, 'top':.4575},
                            size_hint = (.005,.005))
        self.dot7 = Image(source = 'pics/pigpen/c.bmp',
                            pos_hint = {'x':.298, 'top':.405},
                            size_hint = (.005,.005))

        self.caption = Label(text = 'The name of one of the people responsible for\n' +
                            'overhauling the postal system is encrypted on this page.',
                            pos_hint = {'x':.15, 'top':.3},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.r.add_widget(self.dot1)
        self.r.add_widget(self.dot2)
        self.r.add_widget(self.dot3)
        self.r.add_widget(self.dot4)
        self.r.add_widget(self.dot5)
        self.r.add_widget(self.dot6)
        self.r.add_widget(self.dot7)
        self.r.add_widget(self.caption)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Pinprick Cipher Page
################################################################################


################################################################################
#Begin Cracking the Vigenere Page
################################################################################
class CrackingVigenerePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('cracking the vigenere page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cracking the Vigenere Cipher")

        with open('texts/crackingthevigenerecipher.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.1, 'top':.6},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/babbage3.bmp',
                            pos_hint = {'x':.3, 'top':.75},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Charles\nBabbage",
                                        pos_hint = {'x':.8, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button5 = Button(text = "Forgotten\nGenius",
                                        pos_hint = {'x':.8, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)
        self.namelabel = Label(text = "[b]Charles Babbage[/b]",
                                markup = True,
                                pos_hint = {'x':.475, 'top':.3},
                                size_hint = (.15,.15))
        self.creditlabel = Label(text = 'Copyright Science Museum\nScience and Society Picture Library',
                                pos_hint = {'x':.475, 'top':.25},
                                size_hint = (.15,.15),
                                font_size = 11)

        self.r.add_widget(self.creditlabel)
        self.r.add_widget(self.namelabel)
        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("charles babbage pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CharlesBabbagePage().create())

    def fivePressed(self, *args):
        f.write('forgotten genius pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ForgottenGeniusPage().create())
################################################################################
#End Cracking the Vigenere Page
################################################################################


################################################################################
#Begin Charles Babbage Page
################################################################################
class CharlesBabbagePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('charles babbage page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Charles Babbage")

        with open('texts/charlesbabbage.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.375, 'top':.6},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/chf5-1-3.avi',
                            pos_hint = {'x':.55, 'top':.4},
                            size_hint = (.4,.4),
                            allow_fullscreen = False)

        self.button1 = Button(text = "Babbage's\nComputers",
                            pos_hint = {'x':.8, 'top':.9},
                            size_hint = (.15,.1),
                            on_release = self.button1pressed)
        self.button2 = Button(text = "Babbage the\nCodebreaker",
                            pos_hint = {'x':.8, 'top':.75},
                            size_hint = (.15,.1),
                            on_release = self.button2pressed)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def button1pressed(self, *args):
        f.write('babbages computers pressed\n')
        for child in MyApp.current.r.children:
            try:
                if child.source[0] == 'v':
                    child.state = 'stop'
                else:
                    pass
            except AttributeError:
                pass
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BabbagesComputersPage().create())

    def button2pressed(self, *args):
        f.write('babbage the codebreaker pressed')
        for child in MyApp.current.r.children:
            try:
                if child.source[0] == 'v':
                    child.state = 'stop'
                else:
                    pass
            except AttributeError:
                pass
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BabbageCodebreakerPage().create())
################################################################################
#End Charles Babbage Page
################################################################################


################################################################################
#Begin Babbage's Computers Page
################################################################################
class BabbagesComputersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('babbages computers page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Babbage's Computers")

        with open('texts/babbagescomputers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.75},
                            size_hint = (.2,.2))

        with open('texts/babbagescomputers2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.6, 'top':.325},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/babbagecomp.jpg',
                            pos_hint = {'x':-.05, 'top':.525},
                            size_hint = (.6,.6))
        self.imagelabel = Label(text = 'Image from: http://www.computerhistory.org/babbage/',
                            pos_hint = {'x':.125, 'top':.125},
                            size_hint = (.2,.2),
                            font_size = 12)

        self.r.add_widget(self.image)
        self.r.add_widget(self.imagelabel)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Babbage's Computers Page
################################################################################


################################################################################
#Begin Babbage the Codebreaker Page
################################################################################
class BabbageCodebreakerPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('babbage the codebreaker page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Babbage the Codebreaker")

        with open('texts/babbagethecodebreaker.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.75},
                            size_hint = (.2,.2))

        with open('texts/babbagethecodebreaker2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.2, 'top':.325},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/chf4-2-2.avi',
                            pos_hint = {'x':.55, 'top':.45},
                            size_hint = (.4,.4),
                            allow_fullscreen = False)

        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Babbage the Codebreaker Page
################################################################################


################################################################################
#Begin Forgotten Genius Page
################################################################################
class ForgottenGeniusPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('forgetten genius page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Forgetten Genius")

        with open('texts/forgottengenius.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2))
        with open('texts/forgottengenius2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.175, 'top':.55},
                            size_hint = (.2,.2))
        with open('texts/forgottengenius3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.4, 'top':.2},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/chf6-1-2.avi',
                            pos_hint = {'x':.475, 'top':.7},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Forgetten Genius Page
################################################################################

################################################################################
#Begin Mechanisation of Secrecy Page
################################################################################
class MOFS(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Mechanisation of Secrecy page entered\n')
        MyApp.current = self
        btnsz = (.15, .11)
        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Mechanisation of Secrecy")

        with open('texts/mechanisationofsecrecy.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.3, 'top':.75},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "World War I",
                                        pos_hint = {'x':.825, 'top':.9},
                                        size_hint = btnsz,
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Building\nEnigma",
                                        pos_hint = {'x':.825, 'top':.75},
                                        size_hint = btnsz,
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Using the\nEnigma",
                                        pos_hint = {'x':.825, 'top':.6},
                                        size_hint = btnsz,
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Cracking the\nEnigma",
                                        pos_hint = {'x':.825, 'top':.45},
                                        size_hint = btnsz,
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "Enigma's\nImpact on\nWorld War\nII",
                                        pos_hint = {'x':.825, 'top':.3},
                                        size_hint = btnsz,
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.button6 = Button(text = "Other World\nWar II\nCiphers",
                                        pos_hint = {'x':.825, 'top':.15},
                                        size_hint = btnsz,
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
        f.write("world war I pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(WorldWarIPage().create())

    def twoPressed(self, *args):
        f.write('building enigma pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BuildingEnigmaPage().create())

    def threePressed(self, *args):
        f.write('using the enigma pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(UsingEnigmaPage().create())

    def fourPressed(self, *args):
        f.write('cracking the enigma pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CrackingTheEnigmaPage().create())

    def fivePressed(self, *args):
        f.write('enigmas impact on wwII pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(EnigmasImpactOnWWIIPage().create())

    def sixPressed(self, *args):
        f.write('other world war II ciphers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(OtherWWIICiphersPage().create())
################################################################################
#End Mechanisation of Secrecy Page
################################################################################


################################################################################
#Begin World War I Page
################################################################################
class WorldWarIPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('world war i page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("World War I")

        with open('texts/ww1.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.3, 'top':.75},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Codes",
                                        pos_hint = {'x':.825, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "The\nZimmermann\nTelegram",
                                        pos_hint = {'x':.825, 'top':.725},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Cracking\nZimmermann",
                                        pos_hint = {'x':.825, 'top':.55},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "The\nWeakness of\nCodes",
                                        pos_hint = {'x':.825, 'top':.375},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "ADFGVX\nCipher",
                                        pos_hint = {'x':.825, 'top':.2},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.image = Image(source = 'pics/ZIMBIT.bmp',
                            pos_hint = {'x':.05, 'top':.65},
                            size_hint = (.8,.8))

        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("codes pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CodesPage().create())

    def twoPressed(self, *args):
        f.write('the zimmermann telegram pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TheZimmermannTelegramPage().create())

    def threePressed(self, *args):
        f.write('cracking zimmermann pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CrackingZimmermannPage().create())

    def fourPressed(self, *args):
        f.write('the weakness of codes pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(WeaknessOfCodesPage().create())

    def fivePressed(self, *args):
        f.write('adfgvx cipher pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ADFGVXPage().create())

################################################################################
#End Mechanisation of Secrecy Page
################################################################################

################################################################################
#Begin Codes Page
################################################################################
class CodesPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('codes page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Codes")

        with open('texts/codes.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.375, 'top':.8},
                            size_hint = (.2,.2))
        with open('texts/codes2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.175, 'top':.375},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/zimmer32.avi',
                            pos_hint = {'x':.55, 'top':.45},
                            size_hint = (.4,.4),
                            allow_fullscreen = False)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Codes Page
################################################################################


################################################################################
#Begin The Zimmermann Telegram Page
################################################################################
class TheZimmermannTelegramPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('The Zimmermann Telegram page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Zimmermann Telegram")

        with open('texts/thezimmermantelegram.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.375, 'top':.75},
                            size_hint = (.2,.2))
        with open('texts/thezimmermantelegram2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.195, 'top':.375},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/zimmer92.avi',
                            pos_hint = {'x':.55, 'top':.45},
                            size_hint = (.4,.4),
                            allow_fullscreen = False)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End The Zimmermann Telegram Page
################################################################################


################################################################################
#Begin Cracking Zimmermann Page
################################################################################
class CrackingZimmermannPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('cracking zimmermann page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cracking Zimmermann")

        with open('texts/crackingzimmerman.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2),
                            font_size = 14)
        with open('texts/crackingzimmermandecode.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.4},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.image = Image(source = 'pics/zimmer.bmp',
                            pos_hint = {'x':-0.085, 'top':.75},
                            size_hint = (.7,.7))

        self.video = VideoPlayer(source = 'video/dgscb2.avi',
                            pos_hint = {'x':.5, 'top':.5},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.description = Label(text = "The video clip shows de Grey's replica code\n" +
                                "book, and the section that follows explains\n" +
                                "how he might have compiled it.",
                                pos_hint = {'x':.65, 'top':.7},
                                size_hint = (.2,.2))

        self.decoded = Button(text = 'Decoded Telegram',
                                pos_hint = {'x':.65, 'top':.75},
                                size_hint = (.2,.05),
                                on_release = self.decodePressed)
        self.close = Button(text = 'Close',
                                pos_hint = {'x':.65, 'top':.75},
                                size_hint = (.2,.05),
                                on_release = self.closePressed)


        self.r.add_widget(self.text1)
        self.r.add_widget(self.decoded)
        self.r.add_widget(self.image)
        self.r.add_widget(self.video)
        self.r.add_widget(self.description)
        self.r.add_widget(self.tb)
        return self.r

    def decodePressed(self, *args):
        f.write("decode button pressed\n")
        self.r.add_widget(self.text2)
        self.r.add_widget(self.close)
        self.r.remove_widget(self.decoded)
        self.r.remove_widget(self.video)
        self.r.remove_widget(self.description)

    def closePressed(self, *args):
        f.write("close button pressed\n")
        self.r.remove_widget(self.text2)
        self.r.remove_widget(self.close)
        self.r.add_widget(self.decoded)
        self.r.add_widget(self.video)
        self.r.add_widget(self.description)
################################################################################
#End Cracking Zimmermann Page
################################################################################

################################################################################
#Begin The Weakness of Codes Page
################################################################################
class WeaknessOfCodesPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('The weakness of codes page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Weakness of Codes")

        with open('texts/theweaknessofcodes.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.825},
                            size_hint = (.2,.2))
        with open('texts/theweaknessofcodes2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.157, 'top':.385},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/degdk2-2.avi',
                            pos_hint = {'x':.5, 'top':.55},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End The Weakness of Codes Page
################################################################################


################################################################################
#Begin ADFGVX Cipher Page
################################################################################
class ADFGVXPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('ADFGVX page entered\n')
        MyApp.current = self
        self.alphanum = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                '7', '8', '9']
        self.a = ['a', 'd', 'f', 'g', 'v', 'x']

        self.dub = []

        for i in self.a:
            templist = []
            for a in self.a:
                rand = randint(0, len(self.alphanum))
                templist.append(self.alphanum[rand-1])
                self.alphanum.remove(self.alphanum[rand-1])
            self.dub.append(templist)

        f.write(str(self.dub) + '\n')

        self.table = ''
        self.table += '   ' + ' '.join(self.a) + '\n'
        for i in range(len(self.dub)):
            self.table += self.a[i] + '| '
            for j in self.dub[i]:
                self.table += j + ' '
            self.table += '\n'

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("ADFGVX Cipher")

        with open('texts/adfgvxcipher.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.855},
                            size_hint = (.2,.2),
                            font_size = 14)
        with open('texts/adfgvxcipher2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.485},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.tablelabel = Label(text = self.table,
                                    pos_hint = {'x':-.01, 'top':.55},
                                    size_hint = (.3,.3),
                                    font_name = 'font/RobotoMono-Regular',
                                    font_size = 16)

        self.randomizebutton = Button(text = 'Randomize Grid',
                                    pos_hint = {'x':.07, 'top':.6},
                                    size_hint = (.15,.05),
                                    on_release = self.randomizeGrid)
        self.keywordinput = maxinput(text = 'MARK',
                                    pos_hint = {'x':.275, 'top':.6},
                                    size_hint = (.2,.05),
                                    font_name = 'font/RobotoMono-Regular')
        self.keywordinput.max_chars = 5
        self.keywordinput.bind(text=self.textchange)
        self.keywordlabel = Label(text = 'Keyword',
                                    pos_hint = {'x':.325, 'top':.675},
                                    size_hint = (.1,.1),
                                    font_size = 12)

        self.plaintextinput = maxinput(text = 'attack at 10pm',
                                    pos_hint = {'x':.275, 'top':.5},
                                    size_hint = (.2,.1),
                                    font_name = 'font/RobotoMono-Regular')
        self.plaintextinput.max_chars = 26
        self.plaintextlabel = Label(text = 'Plaintext',
                                    pos_hint = {'x':.325, 'top':.575},
                                    size_hint = (.1,.1),
                                    font_size = 12)

        self.stage1ciphertext = TextInput(text = '',
                                    pos_hint = {'x':.275, 'top':.35},
                                    size_hint = (.2,.1),
                                    disabled = True)
        self.stage1label = Label(text = 'Stage 1 Ciphertext',
                                    pos_hint = {'x':.325, 'top':.425},
                                    size_hint = (.1,.1),
                                    font_size = 12)

        self.keyword1 = Label(text = self.keywordinput.text,
                                    pos_hint = {'x':-0.005, 'top':.275},
                                    size_hint = (.1,.05),
                                    font_name = 'font/RobotoMono-Regular')
        self.keyword1text = TextInput(text = '',
                                    pos_hint = {'x':.015, 'top':.225},
                                    size_hint = (.115,.2),
                                    font_name = 'font/RobotoMono-Regular')

        rand = randint(1, len(self.keywordinput.text))
        newstrlist = deque(list(self.keywordinput.text))
        newstrlist.rotate(rand)
        self.keyword2 = Label(text = ''.join(list(newstrlist)),
                                    pos_hint = {'x':.13, 'top':.275},
                                    size_hint = (.1,.05),
                                    font_name = 'font/RobotoMono-Regular')
        self.keyword2text = TextInput(text = '',
                                    pos_hint = {'x':.15, 'top':.225},
                                    size_hint = (.115,.2),
                                    font_name = 'font/RobotoMono-Regular')

        self.stage1button = Button(text = 'Stage 1',
                                    pos_hint = {'x':.32, 'top':.05},
                                    size_hint = (.145,.045),
                                    on_release = self.stage1Pressed)
        self.gridbutton = Button(text = 'Form Grid',
                                    pos_hint = {'x':.47, 'top':.05},
                                    size_hint = (.145,.045),
                                    disabled = True,
                                    on_release = self.gridPressed)
        self.transposebutton = Button(text = 'Transpose Grid',
                                    pos_hint = {'x':.62, 'top':.05},
                                    size_hint = (.145,.045),
                                    disabled = True,
                                    on_release = self.transposePressed)
        self.finalstagebutton = Button(text = 'Final Stage',
                                    pos_hint = {'x':.77, 'top':.05},
                                    size_hint = (.145,.045),
                                    disabled = True,
                                    on_release = self.finalstagePressed)

        self.ciphertextdisplay = TextInput(text = '',
                                    pos_hint = {'x':.35, 'top':.165},
                                    size_hint = (.5,.1),
                                    disabled = True,
                                    font_name = 'font/RobotoMono-Regular')
        self.clabel = Label(text = 'Ciphertext',
                                    pos_hint = {'x':.325, 'top':.21},
                                    size_hint = (.15,.05),
                                    font_size = 11)

        self.r.add_widget(self.clabel)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.stage1button)
        self.r.add_widget(self.gridbutton)
        self.r.add_widget(self.transposebutton)
        self.r.add_widget(self.finalstagebutton)
        self.r.add_widget(self.keyword1)
        self.r.add_widget(self.keyword1text)
        self.r.add_widget(self.keyword2)
        self.r.add_widget(self.keyword2text)
        self.r.add_widget(self.stage1ciphertext)
        self.r.add_widget(self.stage1label)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.keywordlabel)
        self.r.add_widget(self.keywordinput)
        self.r.add_widget(self.randomizebutton)
        self.r.add_widget(self.tablelabel)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def textchange(self, *args):
        f.write('keyword changed\n')
        self.keyword1.text = self.keywordinput.text
        rand = randint(1, len(self.keywordinput.text))
        newstrlist = deque(list(self.keywordinput.text))
        newstrlist.rotate(rand)
        self.keyword2.text = ''.join(list(newstrlist))
        self.stage1ciphertext.text = ''
        self.stage1button.disabled = False
        self.gridbutton.disabled = True
        self.transposebutton.disabled = True
        self.finalstagebutton.disabled = True
        self.keyword1text.text = ''
        self.keyword2text.text = ''
        self.ciphertextdisplay.text = ''



    def randomizeGrid(self, *args):
        f.write('randomize grid pressed\n')
        self.alphanum = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                '7', '8', '9']
        self.a = ['a', 'd', 'f', 'g', 'v', 'x']
        self.dub = []

        for i in self.a:
            templist = []
            for a in self.a:
                rand = randint(0, len(self.alphanum))
                templist.append(self.alphanum[rand-1])
                self.alphanum.remove(self.alphanum[rand-1])
            self.dub.append(templist)

        f.write(str(self.dub) + '\n')

        self.table = ''
        self.table += '   ' + ' '.join(self.a) + '\n'
        for i in range(len(self.dub)):
            self.table += self.a[i] + '| '
            for j in self.dub[i]:
                self.table += j + ' '
            self.table += '\n'
        self.tablelabel.text = self.table

    def stage1Pressed(self, *args):
        f.write('stage 1 button pressed\n')
        text = self.plaintextinput.text
        ditext = ''
        for letter in text:
            index = []
            if letter == ' ':
                pass
            else:
                for i in range(len(self.dub)):
                    if letter in self.dub[i]:
                        index = [i, self.dub[i].index(letter)]
                ditext += self.a[index[0]] + self.a[index[1]] + ' '

        self.stage1ciphertext.text = ditext
        self.stage1button.disabled = True
        self.gridbutton.disabled = False

    def gridPressed(self, *args):
        f.write('grid button pressed\n')
        ditext = self.stage1ciphertext.text
        keyword = self.keywordinput.text
        ditext = ditext.replace(' ', '')
        grid = ''
        count = len(keyword)
        for letter in ditext:
            grid += letter
            count = count - 1
            if count == 0:
                grid += '\n'
                count = len(keyword)

        templist = grid.split('\n')
        if '' in templist:
            templist.remove('')
        length = len(templist[0])
        for group in templist:
            if len(group) != length:
                n = length - len(group)
                newgroup = group + n*'x'
                templist.remove(group)
                templist.append(newgroup)

        grid = '\n'.join(templist)

        self.keyword1text.text = grid
        self.gridbutton.disabled = True
        self.transposebutton.disabled = False

    def transposePressed(self, *args):
        f.write('transpose button pressed\n')
        keyword = self.keyword1.text
        keyword2 = self.keyword2.text
        listgrid = self.keyword1text.text.split('\n')
        f.write(str(listgrid) + '\nkeyword1 = ' + keyword + '\nkeyword2 = ' + keyword2 + '\n')
        indexes = []
        newlistgrid = []
        for letter in range(len(keyword2)):
            for i in range(len(keyword)):
                if keyword2[letter] == keyword[i]:
                    f.write(str(keyword2[letter]) + ' == ' + str(keyword[i]) + ' ' + str(letter) + ' == ' + str(i) + '\n')
                    indexes.append(i)
                    break
        f.write('indexes: ' + str(indexes) + '\n')
        for j in listgrid:
            if j == '':
                pass
            else:
                tempnew = ''
                for n in indexes:
                    tempnew += j[n]
                newlistgrid.append(tempnew)

        self.keyword2text.text = '\n'.join(newlistgrid)
        self.transposebutton.disabled = True
        self.finalstagebutton.disabled = False

    def finalstagePressed(self, *args):
        f.write('final stage button pressed\n')
        text = self.keyword2text.text.split('\n')
        final = ''
        length = len(self.keywordinput.text) - 1
        count = len(self.keywordinput.text) - 1
        f.write('count: ' + str(count) + '\n')
        for i in range(length):
            for group in text:
                final += group[length - count]
            count = count - 1

        self.ciphertextdisplay.text = final
        self.finalstagebutton.disabled = True
        self.stage1button.disabled = False
################################################################################
#End ADFGVX Cipher Page
################################################################################

################################################################################
#Begin Building Enigma Page
################################################################################
class BuildingEnigmaPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Building Enigma page entered\n')
        MyApp.current = self
        buttonx = .8
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Building Enigma")

        with open('texts/buildingenigma1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.275, 'top':.9},
                            size_hint = (.2,.2))
        with open('texts/buildingenigma2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.085, 'top':.45},
                            size_hint = (.2,.2))
        self.image = Image(source = 'pics/ENIGCU.png',
                            pos_hint = {'x':.275, 'top':.65},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Meet the\nMachine",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Complete\nOverview",
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("meet the machine pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MeetEnigmaPage().create())

    def twoPressed(self, *args):
        f.write('complete overview pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CompleteOverviewPage().create())
################################################################################
#End Building Enigma Page
################################################################################

################################################################################
#Begin Complete Overview Page
################################################################################
class CompleteOverviewPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Complete Overview page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Complete Overview")

        with open('texts/completeoverview1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.365, 'top':.9},
                            size_hint = (.2,.2))

        with open('texts/completeoverview2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.15, 'top':.5},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/En2_1.avi',
                            pos_hint = {'x':.475, 'top':.7},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.image = Image(source = 'pics/eniglogo.png',
                            pos_hint = {'x':.4, 'top':.2},
                            size_hint = (.2,.2))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Plugboard Page
################################################################################

################################################################################
#Begin Using Enigma Page
################################################################################
class UsingEnigmaPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Using Enigma page entered\n')
        MyApp.current = self
        buttonx = .8
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Using the Enigma")

        with open('texts/usingtheenigma1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.275, 'top':.9},
                            size_hint = (.2,.2))
        with open('texts/usingtheenigma2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.085, 'top':.45},
                            size_hint = (.2,.2))
        self.image = Image(source = 'pics/enigma.png',
                            pos_hint = {'x':.275, 'top':.65},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "What is the\nkey?",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "How many\nkeys?",
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Agreeing a\nkey",
                                        pos_hint = {'x':buttonx, 'top':.6},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)


        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("what is the key pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(WhatIsTheKeyPage().create())

    def twoPressed(self, *args):
        f.write('how many pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowManyKeysPage().create())

    def threePressed(self, *args):
        f.write('agreeing a key pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AgreeingAKeyPage().create())
################################################################################
#End Using Enigma Page
################################################################################


################################################################################
#Begin What is the key Page
################################################################################
class WhatIsTheKeyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('what is the key page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("What is the key?")

        with open('texts/whatisthekey1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.365, 'top':.825},
                            size_hint = (.2,.2))

        with open('texts/whatisthekey2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.14, 'top':.4},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/bigenig2.png',
                            pos_hint = {'x':.5, 'top':.5},
                            size_hint = (.4,.4))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End What is the key Page
################################################################################


################################################################################
#Begin How Many Keys Page
################################################################################
class HowManyKeysPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('how many keys page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("How many keys?")

        with open('texts/howmanykeys1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.365, 'top':.85},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/howmanykeys.png',
                            pos_hint = {'x':.075, 'top':.9},
                            size_hint = (.8,.8))

        self.calc = Label(text = 'Total no. of keys = 60 x 17,576 x 676 x 150,738,274,937,250\n\n' +
                                '                           = 107,458,687,327,250,619,360,000 keys\n\n' +
                                '                           = 100,000 billion billion keys',
                            pos_hint = {'x':.35, 'top':.3},
                            size_hint = (.2,.2),
                            font_size = 16)

        self.r.add_widget(self.image)
        self.r.add_widget(self.calc)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End How Many Keys Page
################################################################################


################################################################################
#Begin Agreeing a key Page
################################################################################
class AgreeingAKeyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Agreeing a key page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Agreeing a Key")

        with open('texts/agreeingakey1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.325, 'top':.935},
                            size_hint = (.2,.2))

        with open('texts/agreeingakey2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.1, 'top':.575},
                            size_hint = (.2,.2))

        with open('texts/agreeingakey3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.26, 'top':.175},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/enigkey6.png',
                            pos_hint = {'x':.4, 'top':.8},
                            size_hint = (.6,.6))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Agreeing a key Page
################################################################################


################################################################################
#Begin Cracking the Enigma Page
################################################################################
class CrackingTheEnigmaPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Cracking the Enigma page entered\n')
        MyApp.current = self
        buttonx = .8
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cracking the Enigma")

        with open('texts/crackingtheenigma.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.3, 'top':.8},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/rounders.png',
                            pos_hint = {'x':.15, 'top':.5},
                            size_hint = (.5,.5))

        self.button1 = Button(text = "Polish\nCodebreakers",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Bletchley\nPark",
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Cribs",
                                        pos_hint = {'x':buttonx, 'top':.6},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Turing's\nBombe",
                                        pos_hint = {'x':buttonx, 'top':.45},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "Flaws in the\nEnigma",
                                        pos_hint = {'x':buttonx, 'top':.3},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.button6 = Button(text = "By Hook\nor\nby Crook",
                                        pos_hint = {'x':buttonx, 'top':.15},
                                        size_hint = (.15,.1),
                                        on_release = self.sixPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.button6)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("polish codebreakers pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PolishCodebreakersPage().create())

    def twoPressed(self, *args):
        f.write('bletchley park pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BletchleyParkPage().create())

    def threePressed(self, *args):
        f.write('cribs pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CribsPage().create())

    def fourPressed(self, *args):
        f.write('turings bombe pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TuringsBombePage().create())

    def fivePressed(self, *args):
        f.write('flaws in the enigma pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(FlawsInTheEnigmaPage().create())

    def sixPressed(self, *args):
        f.write('by hook or by crook pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ByHookOrByCrookPage().create())
################################################################################
#End Cracking the Enigma Page
################################################################################


################################################################################
#Begin Polish Codebreakers Page
################################################################################
class PolishCodebreakersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Polish Codebreakers page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Polish Codebreakers")

        with open('texts/polishcodebreakers1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.6, 'top':.85},
                            size_hint = (.2,.2))

        with open('texts/polishcodebreakers2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.375, 'top':.595},
                            size_hint = (.2,.2))

        with open('texts/polishcodebreakers3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.2, 'top':.31},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/POLISH.png',
                            pos_hint = {'x':-.05, 'top':1.05},
                            size_hint = (.6,.6))

        self.image2 = Image(source = 'pics/rejewski.png',
                            pos_hint = {'x':.5, 'top':.425},
                            size_hint = (.4,.4))

        self.namelabel = Label(text = '[b]Marian\nRejewski[/b]',
                            pos_hint = {'x':.8, 'top':.3},
                            size_hint = (.15,.15),
                            font_size = 16,
                            markup = True)

        self.r.add_widget(self.namelabel)
        self.r.add_widget(self.image)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Polish Codebreakers Page
################################################################################


################################################################################
#Begin Bletchley Park Page
################################################################################
class BletchleyParkPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Bletchley Park page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Bletchley Park")

        with open('texts/bletchleypark.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.8},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/bletch2.png',
                            pos_hint = {'x':.05, 'top':.55},
                            size_hint = (.6,.6))

        self.piclabel = Label(text = "[i]In August 1939, Britain's senior\n" +
                                    "codebreakers visited Bletchley Park to\n" +
                                    "assess its suitability as the site for the new\n" +
                                    "Government Code and Cypher School. To\n" +
                                    "avoid arousing suspicion from locals, they\n" +
                                    "claimed to be part of Captain Ridley's\n" +
                                    "shooting party.\n\n(Courtesy of Barbara Eachus)" +
                                    "[/i]",
                            pos_hint = {'x':.75, 'top':.35},
                            size_hint = (.15,.15),
                            markup = True,
                            font_size = 13)

        self.website = TextInput(text = 'http://www.bletchleypark.org.uk',
                            pos_hint = {'x':.65, 'top':.08},
                            size_hint = (.3,.05),
                            disabled = True)
        self.weblabel = Label(text = '[b]Website[/b]',
                            pos_hint = {'x':.635, 'top':.145},
                            size_hint = (.1,.1),
                            font_size = 12,
                            markup = True)

        self.r.add_widget(self.weblabel)
        self.r.add_widget(self.website)
        self.r.add_widget(self.piclabel)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Bletchley Park Page
################################################################################


################################################################################
#Begin Cribs Page
################################################################################
class CribsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Cribs page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Cribs")

        with open('texts/cribs1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.39, 'top':.925},
                            size_hint = (.2,.2))

        with open('texts/cribs2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.475},
                            size_hint = (.2,.2))

        self.label = Label(text = '[b]Plaintext + Key = Ciphertext[/b]',
                            pos_hint = {'x':.385, 'top':.825},
                            size_hint = (.2,.2),
                            markup = True,
                            font_size = 20)

        self.r.add_widget(self.label)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Cribs Page
################################################################################


################################################################################
#Begin Turing's Bombe Page
################################################################################
class TuringsBombePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Turings Bombe page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Turing's Bombe")

        with open('texts/turingsbombe1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.2, 'top':.7},
                            size_hint = (.2,.2))

        with open('texts/turingsbombe2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.335, 'top':.325},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/TURING2.png',
                            pos_hint = {'x':.5, 'top':.95},
                            size_hint = (.6,.6))

        self.bombeloop = Image(source = 'pics/bombeloop.png',
                            pos_hint = {'x':.3, 'top':.3},
                            size_hint = (.45,.45))

        self.r.add_widget(self.bombeloop)
        self.r.add_widget(self.bombebutton)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Turing's Bombe Page
################################################################################

################################################################################
#Begin Flaws in the Enigma Page
################################################################################
class FlawsInTheEnigmaPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Flaws in the Enigma page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Flaws in the Enigma")

        with open('texts/flawsintheenigma1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.65},
                            size_hint = (.2,.2))

        with open('texts/flawsintheenigma2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.39, 'top':.2},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/3rotors.png',
                            pos_hint = {'x':.4, 'top':.85},
                            size_hint = (.6,.6))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Flaws in the Enigma Page
################################################################################

################################################################################
#Begin By Hook or by Crook Page
################################################################################
class ByHookOrByCrookPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('By Hook or by Crook page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("By Hook or by Crook")

        with open('texts/byhookorbycrook1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.6, 'top':.625},
                            size_hint = (.2,.2))

        with open('texts/byhookorbycrook2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.39, 'top':.175},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/HOOK.png',
                            pos_hint = {'x':-0.1, 'top':.875},
                            size_hint = (.6,.6))

        self.label = Label(text = '[b][i]Tommy Brown\n(copyright David Brown)[/i][/b]',
                            markup = True,
                            pos_hint = {'x':.125, 'top':.335},
                            size_hint = (.2,.2),
                            font_size = 12)

        self.r.add_widget(self.label)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End By Hook or by Crook Page
################################################################################

################################################################################
#Begin Enigma's Impact on WWII Page
################################################################################
class EnigmasImpactOnWWIIPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write("Enigma's Impact on WWII page entered\n")
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Enigma's Impact on WWII")

        with open('texts/enigmasimpactonww21.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.6, 'top':.785},
                            size_hint = (.2,.2))

        with open('texts/enigmasimpactonww22.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.355},
                            size_hint = (.2,.2),
                            font_size = 13)

        self.image = Image(source = 'pics/blettop.png',
                            pos_hint = {'x':.01, 'top':1.035},
                            size_hint = (.6,.6))

        self.button = Button(text = 'Secret\nSuccess',
                            pos_hint = {'x':.875, 'top':.9},
                            size_hint = (.1,.1),
                            on_release = self.buttonpressed)

        self.r.add_widget(self.button)
        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('secret success button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SecretSuccessPage().create())
################################################################################
#End Enigma's Impact on WWII Page
################################################################################


################################################################################
#Begin Secret Success Page
################################################################################
class SecretSuccessPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Secret Success page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Secret Success")

        with open('texts/secretsuccess1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.8},
                            size_hint = (.2,.2))

        with open('texts/secretsuccess2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.385, 'top':.35},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/confiden.png',
                            pos_hint = {'x':0.5, 'top':.925},
                            size_hint = (.4,.4))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Secret Success Page
################################################################################

################################################################################
#Begin Other WWII Ciphers Page
################################################################################
class OtherWWIICiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write("Other WWII Ciphers page entered\n")
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Other World War II Ciphers")

        with open('texts/otherww2ciphers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.325, 'top':.85},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.lorenz)

        with open('texts/otherww2ciphers2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.515},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.lorenz)

        self.button = Button(text = 'Codetalkers',
                            pos_hint = {'x':.875, 'top':.9},
                            size_hint = (.125,.1),
                            on_release = self.buttonpressed)

        self.label = Label(text = '[i]For pictures, click on the yellow words. Further information about\n' +
                                    'Second World War cipher can be found on the following web sites:[/i]',
                            pos_hint = {'x':.4, 'top':.3},
                            size_hint = (.2,.2),
                            markup = True,
                            font_size = 13)

        self.lorenzimage = Image(source = 'pics/lorentz.png',
                            pos_hint = {'x':.25, 'top':.85},
                            size_hint = (.5,.5))
        self.lorenzlabel = Label(text = '[i]Typex cipher machine\n' +
                                        'Courtesy of The Bletchley Park Trust\n[/i]' +
                                        '[color=ffff66][b][ref=lorentz]Click here to view the text[/ref][/b][/color]',
                            pos_hint = {'x':0, 'top':.85},
                            size_hint = (1,1),
                            halign = 'center',
                            markup = True,
                            on_ref_press = self.imagepressed)
        self.typeximage = Image(source = 'pics/typex3.png',
                            pos_hint = {'x':.25, 'top':.85},
                            size_hint = (.5,.5))
        self.typexlabel = Label(text = '[i]Lorenz SZ40 machine\n' +
                                        'Courtesy of The Bletchley Park Trust\n[/i]' +
                                        '[color=ffff66][b][ref=lorentz]Click here to view the text[/ref][/b][/color]',
                            pos_hint = {'x':0, 'top':.85},
                            size_hint = (1,1),
                            halign = 'center',
                            markup = True,
                            on_ref_press = self.imagepressed)

        self.hyperlink1 = Label(text = 'Codes and Ciphers of the Second World War\n' +
                                        '[color=ffff66][b][ref=hype1]http://www.codesandciphers.org.uk/[/ref][/b][/color]',
                            pos_hint = {'x':.1, 'top':.225},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.hype1pressed,
                            font_size = 13)

        self.hyperlink2 = Label(text = 'National Cryptologic Museum\n' +
                                        'Fort Meade, Maryland, USA\n' +
                                        '[color=ffff66][b][ref=hype1]https://www.nsa.gov/about/cryptologic-heritage/museum/[/ref][/b][/color]',
                            pos_hint = {'x':.1725, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.hype2pressed,
                            font_size = 13)
        self.hyperlink3 = Label(text = 'Crypto Machine Menu Page\n' +
                                        '[color=ffff66][b][ref=hype1]http://jproc.ca/crypto/menu.html[/ref][/b][/color]',
                            pos_hint = {'x':.65, 'top':.225},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.hype3pressed,
                            font_size = 13)

        self.hyperlink4 = Label(text = 'Military Communications and Electronics Museum\n' +
                                        'Kingston, Ontario, Canada\n' +
                                        '[color=ffff66][b][ref=hype1]http://www.c-and-e-museum.org/[/ref][/b][/color]',
                            pos_hint = {'x':.6975, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.hype4pressed,
                            font_size = 13)

        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.hyperlink3)
        self.r.add_widget(self.hyperlink4)
        self.r.add_widget(self.label)
        self.r.add_widget(self.button)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('codetalkers button pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CodetalkersPage().create())

    def lorenz(self, *args):
        f.write('lorenz text pressed\n')
        self.r.remove_widget(self.text1)
        self.r.remove_widget(self.text2)
        self.r.add_widget(self.lorenzimage)
        self.r.add_widget(self.lorenzlabel)

    def typex(self, *args):
        f.write('typex text pressed\n')
        self.r.remove_widget(self.text1)
        self.r.remove_widget(self.text2)
        self.r.add_widget(self.typeximage)
        self.r.add_widget(self.typexlabel)

    def imagepressed(self, *args):
        f.write('image pressed\n')
        self.r.remove_widget(self.lorenzimage)
        self.r.remove_widget(self.lorenzlabel)
        self.r.remove_widget(self.typeximage)
        self.r.remove_widget(self.typexlabel)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)

    def hype1pressed(self, *args):
        f.write('hyperlink pressed\n')
        webbrowser.open("http://www.codesandciphers.org.uk/")

    def hype2pressed(self, *args):
        f.write('hyperlink pressed\n')
        webbrowser.open("https://www.nsa.gov/about/cryptologic-heritage/museum/")

    def hype3pressed(self, *args):
        f.write('hyperlink pressed\n')
        webbrowser.open("http://jproc.ca/crypto/menu.html")

    def hype4pressed(self, *args):
        f.write('hyperlink pressed\n')
        webbrowser.open("http://www.c-and-e-museum.org/")
################################################################################
#End Other WWII Ciphers Page
################################################################################

################################################################################
#Begin Age of the Internet Page
################################################################################
class AOTI(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Age of the Internet page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Age of the Internet")

        with open('texts/ageoftheinternet.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.3, 'top':.8},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Computer\nCryptography",
                                        pos_hint = {'x':.825, 'top':.925},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Key\nDistribution\nProblem",
                                        pos_hint = {'x':.825, 'top':.775},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "God\nRewards\nFools",
                                        pos_hint = {'x':.825, 'top':.625},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Public Key\nCryptography",
                                        pos_hint = {'x':.825, 'top':.475},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "Not Just\nSecrets",
                                        pos_hint = {'x':.825, 'top':.325},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.button6 = Button(text = "The Secret\nHistory",
                                        pos_hint = {'x':.825, 'top':.175},
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
        f.write("computer cryptography pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ComputerCryptographyPage().create())

    def twoPressed(self, *args):
        f.write('key distribution problem pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(KeyDistributionProblemPage().create())

    def threePressed(self, *args):
        f.write('god rewards fools pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(GodRewardsFoolsPage().create())

    def fourPressed(self, *args):
        f.write('public key cryptography pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PublicKeyCryptographyPage().create())

    def fivePressed(self, *args):
        f.write('not just secrets pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(NotJustSecretsPage().create())

    def sixPressed(self, *args):
        f.write('the secret history pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TheSecretHistoryPage().create())

################################################################################
#End Age of the Internet Page
################################################################################


################################################################################
#Begin Computer Cryptography Page
################################################################################
class ComputerCryptographyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Computer Cryptography page entered\n')
        MyApp.current = self
        buttonx = .8
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Computer Cryptography")

        with open('texts/computercryptography.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.3, 'top':.725},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Substitution",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Transposition",
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Data\nEncryption\nStandard",
                                        pos_hint = {'x':buttonx, 'top':.6},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Other Modern\nCiphers",
                                        pos_hint = {'x':buttonx, 'top':.45},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.plaintextinput = maxinput(text = 'HELLO',
                                        pos_hint = {'x':.5, 'top':.35},
                                        size_hint = (.25,.05))
        self.plaintextinput.max_chars = 8
        self.plaintextlabel = Label(text = 'Plaintext',
                                        pos_hint = {'x':.475, 'top':.4},
                                        size_hint = (.15,.05),
                                        font_size = 13)

        self.asciibutton = Button(text = 'Turn Plaintext into ASCII',
                                        pos_hint = {'x':.5, 'top':.285},
                                        size_hint = (.25,.05),
                                        on_release = self.p2apress)

        self.asciidisplay = TextInput(text = '',
                                        pos_hint = {'x':.5, 'top':.225},
                                        size_hint = (.25,.2),
                                        font_name = 'font/RobotoMono-Regular',
                                        disabled = True)
        self.asciibin = RelativeLayout()
        self.createDisplay()

        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.asciibutton)
        self.r.add_widget(self.asciidisplay)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("Substitution pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CCSubstitutionPage().create())

    def twoPressed(self, *args):
        f.write('Transposition pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(CCTranspositionPage().create())

    def threePressed(self, *args):
        f.write('data encryption standard pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(DESPage().create())

    def fourPressed(self, *args):
        f.write('other modern ciphers pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(OtherModernCiphersPage().create())

    def createDisplay(self, *args):
        f.write('creating ascii display...\n')
        posx = .2
        count = 0
        postop = .125
        for letter in reversed(self.alpha):
            if count == 13:
                postop = .125
                posx = .05
            letter = letter.upper()
            f.write('bin ' + letter + ': ' + str(self.text_to_bits(letter)) + '\n')
            templabel = Label(text = (letter + " | " + str(self.text_to_bits(letter)) + ' ' + str(ord(letter))),
                                pos_hint = {'x':posx, 'top':postop},
                                size_hint = (.15,.15),
                                font_size = 12,
                                font_name = 'font/RobotoMono-Regular')
            self.asciibin.add_widget(templabel)
            postop += .025
            count += 1
        self.r.add_widget(self.asciibin)


    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def p2apress(self, *args):
        f.write('plaintext to ascii button pressed\n')
        self.asciidisplay.text = ''
        text = self.plaintextinput.text
        count = 0
        for letter in text:
            count += 1
            letter = letter.upper()
            self.asciidisplay.text = self.asciidisplay.text + str(self.text_to_bits(letter)) + ' '
            if count == 2:
                self.asciidisplay.text = self.asciidisplay.text + '\n'

################################################################################
#End Computer Cryptography Page
################################################################################


################################################################################
#Begin CC Substitution Page
################################################################################
class CCSubstitutionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write("cc substitution page entered\n")
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Substitution")

        with open('texts/ccsubstitution.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.8},
                            size_hint = (.2,.2))

        with open('texts/ccsubstitution2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.25},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/ascii-ex.png',
                            pos_hint = {'x':.15, 'top':.75},
                            size_hint = (.7,.7))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End CC Substitution Page
################################################################################


################################################################################
#Begin CC Transposition Page
################################################################################
class CCTranspositionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write("cc Transposition page entered\n")
        MyApp.current = self
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.templist1 = []
        self.templist2 = []

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Transposition")

        with open('texts/cctransposition1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.clickref)

        with open('texts/cctransposition2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.2},
                            size_hint = (.2,.2))

        self.messageinput = TextInput(text = 'HELLO',
                            pos_hint = {'x':.25, 'top':.66},
                            size_hint = (.5,.05),
                            disabled = True)
        self.messagelabel = Label(text = '[b]Message[/b]',
                            pos_hint = {'x':.11, 'top':.735},
                            size_hint = (.2,.2),
                            font_size = 12,
                            markup = True)
        self.plaintextbin = Label(text = str(self.text_to_bits(self.messageinput.text)),
                            pos_hint = {'x':.4, 'top':.65},
                            size_hint = (.2,.2),
                            font_size = 16,
                            font_name = 'font/RobotoMono-Regular')
        self.plaintextlabel = Label(text = '[b]Plaintext[/b]',
                            pos_hint = {'x':.11, 'top':.653},
                            size_hint = (.2,.2),
                            font_size = 12,
                            markup = True)

        self.railfencebutton = Button(text = 'Railfence',
                            pos_hint = {'x':.085, 'top':.45},
                            size_hint = (.1,.035),
                            on_release = self.railfencepressed)
        self.createciphertext = Button(text = 'Create Ciphertext',
                            pos_hint = {'x':.025, 'top':.29},
                            size_hint = (.165,.035),
                            on_release = self.createpressed,
                            disabled = True)

        self.label1 = Label(text = '',
                            pos_hint = {'x':.4, 'top':.55},
                            size_hint = (.2,.2),
                            font_size = 14,
                            font_name = 'font/RobotoMono-Regular',
                            markup = True)
        self.label2 = Label(text = '',
                            pos_hint = {'x':.4175, 'top':.5},
                            size_hint = (.2,.2),
                            font_size = 14,
                            font_name = 'font/RobotoMono-Regular',
                            markup = True)

        self.ciphertextdisplay = Label(text = '',
                            pos_hint = {'x':.25, 'top':.3},
                            size_hint = (.5,.05),
                            font_name = 'font/RobotoMono-Regular',
                            markup = True,
                            font_size = 16)

        self.r.add_widget(self.createciphertext)
        self.r.add_widget(self.ciphertextdisplay)
        self.r.add_widget(self.railfencebutton)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.messagelabel)
        self.r.add_widget(self.plaintextbin)
        self.r.add_widget(self.messageinput)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def clickref(self, *args):
        f.write('click reference to railfence page pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RailfencePage().create())

    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def railfencepressed(self, *args):
        f.write('railfence button pressed\n')
        bintext = self.plaintextbin.text
        listbin = list(bintext)
        count = 0
        for i in range(len(listbin)):
            if count == 0:
                self.templist1.append(listbin[i])
                count = 1
            else:
                self.templist2.append(listbin[i])
                count = 0

        self.label1.text = '[color=ff0000]' + '  '.join(self.templist1) + '[/color]'
        self.label2.text = '[color=ff0000]' + '  '.join(self.templist2) + '[/color]'
        self.r.add_widget(self.label1)
        self.r.add_widget(self.label2)
        self.createciphertext.disabled = False

    def createpressed(self, *args):
        f.write('create ciphertext pressed\n')
        newlist = ''.join(self.templist1 + self.templist2)
        self.ciphertextdisplay.text = '[color=ff0000]' + str(newlist) + '[/color]'
################################################################################
#End CC Substitution Page
################################################################################


################################################################################
#Begin Data Encryption Standard Page
################################################################################
class DESPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Data Encryption Standard page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Data Encryption Standard")

        with open('texts/dataencryptionstandard.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.55},
                            size_hint = (.2,.2))

        self.button = Button(text = "How DES\nWorks",
                            pos_hint = {'x':.875, 'top':.9},
                            size_hint = (.1,.1),
                            on_release = self.pressed)

        self.r.add_widget(self.button)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def pressed(self, *args):
        f.write('how des works pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowDESWorksPage().create())
################################################################################
#End Data Encryption Standard Page
################################################################################


################################################################################
#Begin How DES Works Page
################################################################################
class HowDESWorksPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('How DES Works page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("How DES Works")

        with open('texts/howdesworks.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.55},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/howdesworks.png',
                            pos_hint = {'x':.275, 'top':.9},
                            size_hint = (.9,.9))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End How DES Works Page
################################################################################


################################################################################
#Begin Other Modern Ciphers Page
################################################################################
class OtherModernCiphersPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Other Modern Ciphers page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Other Modern Ciphers")

        with open('texts/othermodernciphers.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.6},
                            size_hint = (.2,.2))

        self.label = Label(text = "For the latest information on the AES, you can visit:",
                            pos_hint = {'x':.195, 'top':.185},
                            size_hint = (.2,.2))
        self.hyperlink1 = Label(text = '[color=ffff00][ref=h1]http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf[/ref][/color]',
                            pos_hint = {'x':.25, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.h1,
                            font_size = 14)
        self.hyperlink2 = Label(text = '[color=ffff00][ref=h1]http://csrc.nist.gov/archive/aes/rijndael/Rijndael-ammended.pdf[/ref][/color]',
                            pos_hint = {'x':.2735, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.h2,
                            font_size = 14)

        self.r.add_widget(self.label)
        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf ...\n')
        webbrowser.open('http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf')

    def h2(self, *args):
        f.write('opening http://csrc.nist.gov/archive/aes/rijndael/Rijndael-ammended.pdf ...\n')
        webbrowser.open('http://csrc.nist.gov/archive/aes/rijndael/Rijndael-ammended.pdf')
################################################################################
#End Other Modern Ciphers Page
################################################################################

################################################################################
#Begin Key Distribution Problem Page
################################################################################
class KeyDistributionProblemPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Key Distribution Problem page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Key Distribution Problem")

        with open('texts/keydistributionproblem1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.25, 'top':.9},
                            size_hint = (.2,.2))

        with open('texts/keydistributionproblem2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.32, 'top':.675},
                            size_hint = (.2,.2))

        with open('texts/keydistributionproblem3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.14, 'top':.35},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/pub2new2.avi',
                            pos_hint = {'x':.475, 'top':.5},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Key Distribution Problem Page
################################################################################


################################################################################
#Begin God Rewards Fools Page
################################################################################
class GodRewardsFoolsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('God Rewards Fools page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("God Rewards Fools")

        with open('texts/godrewardsfools1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.275, 'top':.85},
                            size_hint = (.2,.2))

        with open('texts/godrewardsfools2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.145, 'top':.425},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/pub3new3.avi',
                            pos_hint = {'x':.475, 'top':.55},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.label = Label(text = '[i]The video clip shows Diffie and Hellman\n' +
                                    'talking about embarking on their\n' +
                                    'cryptographic research.[/i]',
                            pos_hint = {'x':.625, 'top':.675},
                            size_hint = (.2,.2),
                            markup = True,
                            font_size = 14)

        self.r.add_widget(self.label)
        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End God Rewards Fools Page
################################################################################


################################################################################
#Begin Public Key Cryptography Page
################################################################################
class PublicKeyCryptographyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Public Key Cryptography page entered\n')
        MyApp.current = self
        buttonx = .825
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Public Key Cryptography")

        with open('texts/publickeycryptography.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.55, 'top':.6},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Asymmetric\nCipher",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Rivest,\nShamir and\nAdelman",
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "RSA\nEncryption\nTool",
                                        pos_hint = {'x':buttonx, 'top':.6},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "Prime Number\nQuestions",
                                        pos_hint = {'x':buttonx, 'top':.45},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "RSA in\nPractice",
                                        pos_hint = {'x':buttonx, 'top':.3},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.image = Image(source = 'pics/diffie2.png',
                                        pos_hint = {'x':-.15, 'top':.9},
                                        size_hint = (.8,.8))

        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("asymmetric cipher pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AsymmetricCipherPage().create())

    def twoPressed(self, *args):
        f.write('rivest, shamir and adelman pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RivestShamirAdelmanPage().create())

    def threePressed(self, *args):
        f.write('rsa encryption tool pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RSAEncryptionToolPage().create())

    def fourPressed(self, *args):
        f.write('prime number questions pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PrimeNumberQuestionsPage().create())

    def fivePressed(self, *args):
        f.write('rsa in practice pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RSAInPracticePage().create())
################################################################################
#End Public Key Cryptography Page
################################################################################


################################################################################
#Begin Asymmetric Cipher Page
################################################################################
class AsymmetricCipherPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Asymmetric Cipher page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Asymmetric Cipher")

        with open('texts/asymmetriccipher1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.275, 'top':.775},
                            size_hint = (.2,.2))

        with open('texts/asymmetriccipher2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.145, 'top':.35},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/pub4new2.avi',
                            pos_hint = {'x':.475, 'top':.525},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.label = Label(text = '[i]The video clip shows Diffie and Hellman\n' +
                                    'talking about embarking on their\n' +
                                    'cryptographic research.[/i]',
                            pos_hint = {'x':.625, 'top':.675},
                            size_hint = (.2,.2),
                            markup = True,
                            font_size = 14)

        #self.r.add_widget(self.label)
        self.r.add_widget(self.video)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Asymmetric Cipher Page
################################################################################


################################################################################
#Begin Rivest, Sharmir and Adelman Page
################################################################################
class RivestShamirAdelmanPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Rivest, Sharmir and Adelman page entered\n')
        MyApp.current = self
        buttonx = .825
        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Rivest, Sharmir and Adelman")

        with open('texts/rsa.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.3, 'top':.85},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Modular\nArithmetic",
                                        pos_hint = {'x':buttonx, 'top':.9},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = 'A One-way\nFunction',
                                        pos_hint = {'x':buttonx, 'top':.75},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Broad\nArgument",
                                        pos_hint = {'x':buttonx, 'top':.6},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "RSA\nAlgorithm",
                                        pos_hint = {'x':buttonx, 'top':.45},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.button5 = Button(text = "How do you\ncalculate d?",
                                        pos_hint = {'x':buttonx, 'top':.3},
                                        size_hint = (.15,.1),
                                        on_release = self.fivePressed,
                                        font_size = 14)

        self.image = Image(source = 'pics/rsalogo2.png',
                                        pos_hint = {'x':-.025, 'top':.275},
                                        size_hint = (.4,.4))

        self.video = VideoPlayer(source = 'video/adle1-1.avi',
                                        pos_hint = {'x':.325, 'top':.5},
                                        size_hint = (.5,.5),
                                        allow_fullscreen = False)

        self.label = Label(text = '[i]The video clip shows an interview with\n' +
                                    'Len Adleman, co-discoverer of the\n' +
                                    'RSA encryption algorithm. He explains\n' +
                                    'how surprised he was by the reaction\n' +
                                    'to his cipher. He never expected that it\n' +
                                    'would lead to a multi-billion dollar\n' +
                                    'company, RSA Data Security Inc.[/i]',
                                        pos_hint = {'x':.1, 'top':.375},
                                        size_hint = (.2,.2),
                                        markup = True,
                                        font_size = 14)

        self.r.add_widget(self.label)
        self.r.add_widget(self.video)
        self.r.add_widget(self.image)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.button5)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r


    def onePressed(self, *args):
        f.write("modular arithmetic pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ModularArithmeticPage().create())

    def twoPressed(self, *args):
        f.write('a one way function pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(OneWayFunctionPage().create())

    def threePressed(self, *args):
        f.write('broad argument pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BroadArgumentPage().create())

    def fourPressed(self, *args):
        f.write('rsa algorithm pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RSAAlgorithmPage().create())

    def fivePressed(self, *args):
        f.write('how do you calculate d pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(HowDoYouCalculateDPage().create())
################################################################################
#End Rivest, Sharmir and Adelman Page
################################################################################


################################################################################
#Begin Modular Arithmetic Page
################################################################################
class ModularArithmeticPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Modular Arithmetic page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Modular Arithmetic")

        with open('texts/modulararithmetic1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.225, 'top':.775},
                            size_hint = (.2,.2))

        with open('texts/modulararithmetic2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.345, 'top':.4},
                            size_hint = (.2,.2))

        self.label = Label(text = "5 x 4 = 20\n" +
                                "            20 / 7 = 2, remainder 6\n" +
                                "5 x 4 = 6(mod 7).",
                            pos_hint = {'x':.345, 'top':.2},
                            size_hint = (.2,.2))

        self.r.add_widget(self.label)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Modular Arithmetic Page
################################################################################


################################################################################
#Begin One Way Function Page
################################################################################
class OneWayFunctionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('One Way Function page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("One-way Function")

        with open('texts/onewayfunction1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.7},
                            size_hint = (.2,.2),
                            font_size = 14)

        with open('texts/onewayfunction2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.175},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.image = Image(source = 'pics/oneway.png',
                            pos_hint = {'x':.2, 'top':.52},
                            size_hint = (.6,.6))

        self.r.add_widget(self.image)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End One Way Function Page
################################################################################


################################################################################
#Begin Broad Argument Page
################################################################################
class BroadArgumentPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Broad Argument page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Broad Argument")

        with open('texts/broadargument1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.35, 'top':.775},
                            size_hint = (.2,.2))

        with open('texts/broadargument4.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.625, 'top':.835},
                            size_hint = (.2,.2))

        with open('texts/broadargument2.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.175, 'top':.45},
                            size_hint = (.2,.2))

        with open('texts/broadargument3.txt', 'r') as myfile:
            data4 = myfile.read()
        self.text4 = Label(text = data4,
                            pos_hint = {'x':.3, 'top':.15},
                            size_hint = (.2,.2))

        self.label = Label(text = '[i]A prime number is one that has no divisors. For example, 7\n' +
                                    'is a prime number because no numbers, except 1 and 7, will\n' +
                                    'divide into it without leaving a remainder. However, 8 is not\n' +
                                    'a prime number, because it can be divided by 2 and 4.',
                            pos_hint = {'x':.1875, 'top':.3},
                            size_hint = (.2,.2),
                            markup = True)

        self.image = Image(source = 'pics/RSA.png',
                            pos_hint = {'x':.475, 'top':.61},
                            size_hint = (.6,.6))
        self.button = Button(text = 'Broad Argument Page 2',
                            pos_hint = {'x':.75, 'top':.9},
                            size_hint = (.225,.05),
                            on_release = self.page2)

        self.r.add_widget(self.image)
        self.r.add_widget(self.button)
        self.r.add_widget(self.label)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.text4)
        self.r.add_widget(self.tb)
        return self.r

    def page2(self, *args):
        f.write('broad argument page 2 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(BroadArgument2Page().create())
################################################################################
#End Broad Argument Page
################################################################################


################################################################################
#Begin Broad Argument 2 Page
################################################################################
class BroadArgument2Page(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Broad Argument 2 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Broad Argument")

        with open('texts/broadargumentpage2.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.6},
                            size_hint = (.2,.2))

        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Broad Argument 2 Page
################################################################################


################################################################################
#Begin RSA Algorithm Page
################################################################################
class RSAAlgorithmPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('RSA Algorithm page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("RSA Algorithm")

        with open('texts/rsaalgorithmpage1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.65},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.button = Button(text = 'RSA Algorithm Page 2',
                            pos_hint = {'x':.75, 'top':.05},
                            size_hint = (.225,.035),
                            on_release = self.page2)

        self.label1 = Label(text = 'C = 88^7(mod 187) x 88^2(mod 187) x 88^1(mod 187)',
                            pos_hint = {'x':.4, 'top':.275},
                            size_hint = (.2,.2))
        self.label2 = Label(text = '88^1 = 88 = 88(mod 187)         88^2 = 7744 = 77(mod187)            88^4 = 59,969,536 = 132(mod187)',
                            pos_hint = {'x':.4, 'top':.225},
                            size_hint = (.2,.2))
        self.label3 = Label(text = 'C = 88^7 = 88^4 x 88^2 x 88^1 = 88 x 7 x 132 = 894,432 = 11 (mod 187)',
                            pos_hint = {'x':.4, 'top':.175},
                            size_hint = (.2,.2))

        self.r.add_widget(self.label1)
        self.r.add_widget(self.label2)
        self.r.add_widget(self.label3)
        self.r.add_widget(self.button)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def page2(self, *args):
        f.write('rsa algorithm page 2 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(RSAAlgorithm2Page().create())
################################################################################
#End RSA Algorithm Page
################################################################################


################################################################################
#Begin RSA Algorithm 2 Page
################################################################################
class RSAAlgorithm2Page(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('RSA Algorithm 2 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("RSA Algorithm")

        with open('texts/rsaalgorithmpage2.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.55},
                            size_hint = (.2,.2),
                            font_size = 14)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End RSA Algorithm 2 Page
################################################################################


################################################################################
#Begin How Do You Calculate D Page
################################################################################
class HowDoYouCalculateDPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('How Do You Calculate D page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("How Do You Calculate D?")

        with open('texts/howdoyoucalculated1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.85},
                            size_hint = (.2,.2))

        with open('texts/howdoyoucalculated2.txt', 'r') as myfile:
            data2 = myfile.read()
        data2 = data2.replace('\t', '    ')
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.4, 'top':.4},
                            size_hint = (.2,.2))

        self.hyperlink1 = Label(text = '[color=ffff00][ref=h1]http://mathforum.org/dr.math/problems/duong10.13.97.html[/ref][/color]',
                            pos_hint = {'x':.65, 'top':.9},
                            size_hint = (.2,.2),
                            on_ref_press = self.h1,
                            markup = True,
                            font_size = 13)

        self.hyperlink2 = Label(text = '[color=ffff00][ref=h2]http://mathworld.wolfram.com/EuclideanAlgorithm.html[/ref][/color]',
                            pos_hint = {'x':.65, 'top':.85},
                            size_hint = (.2,.2),
                            on_ref_press = self.h2,
                            markup = True,
                            font_size = 13)

        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening http://mathforum.org/dr.math/problems/duong10.13.97.html ...\n')
        webbrowser.open('http://mathforum.org/dr.math/problems/duong10.13.97.html')

    def h2(self, *args):
        f.write('opening http://mathworld.wolfram.com/EuclideanAlgorithm.html ...\n')
        webbrowser.open('http://mathworld.wolfram.com/EuclideanAlgorithm.html')
################################################################################
#End How Do You Calculate D Page
################################################################################


################################################################################
#Begin RSA Encryption Tool Page
"""TO DO:
- fix encryption algorithm
- possible cap
"""
################################################################################
class RSAEncryptionToolPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('RSA Encryption Tool page entered\n')
        MyApp.current = self
        topline = .75
        inputwidth = .35
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.numalpha = []
        for i in range(len(self.alpha)):
            if i < 10:
                self.numalpha.append('0' + str(i))
            else:
                self.numalpha.append(str(i))

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("RSA Encryption Tool")

        with open('texts/rsaencryptiontool.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.275, 'top':.925},
                            size_hint = (.2,.2))

        self.pinput = TextInput(text = '',
                            pos_hint = {'x':.065, 'top':topline},
                            size_hint = (.05,.05))
        self.plabel = Label(text = 'p =',
                            pos_hint = {'x':.025, 'top':topline},
                            size_hint = (.05,.05))
        self.qinput = TextInput(text = '',
                            pos_hint = {'x':.145, 'top':topline},
                            size_hint = (.05,.05))
        self.qlabel = Label(text = 'q =',
                            pos_hint = {'x':.105, 'top':topline},
                            size_hint = (.05,.05))

        self.nlabel = Label(text = 'N = p x q =',
                            pos_hint = {'x':.3, 'top':topline},
                            size_hint = (.05,.05))
        self.ndisplay = TextInput(text = '',
                            pos_hint = {'x':.375, 'top':topline},
                            size_hint = (.075,.05))

        self.einput = TextInput(text = '',
                            pos_hint = {'x':.545, 'top':topline},
                            size_hint = (.075,.05))
        self.elabel = Label(text = 'e =',
                            pos_hint = {'x':.5, 'top':topline},
                            size_hint = (.05,.05))

        self.dinput = TextInput(text = '',
                            pos_hint = {'x':.685, 'top':topline},
                            size_hint = (.075,.05))
        self.dlabel = Label(text = 'd =',
                            pos_hint = {'x':.645, 'top':topline},
                            size_hint = (.05,.05))

        self.autoprime = Button(text = 'Auto Select Primes',
                            pos_hint = {'x':.035, 'top':.625},
                            size_hint = (.175,.05),
                            on_release = self.autoselect)

        self.enter = Button(text = 'Enter',
                            pos_hint = {'x':.2, 'top':topline},
                            size_hint = (.065,.04),
                            on_release = self.enterpressed)
        self.pnot = Label(text = '',
                            pos_hint = {'x':.05, 'top':.725},
                            size_hint = (.1,.1))
        self.qnot = Label(text = '',
                            pos_hint = {'x':.05, 'top':.7},
                            size_hint = (.1,.1))
        self.bounds = Label(text = '',
                            pos_hint = {'x':.6, 'top':.7},
                            size_hint = (.1,.1))
        self.publicalg = Label(text = 'Your public encryption algorithm is: M = C[sup]e[/sup](mod N):\n',
                            pos_hint = {'x':.5, 'top':.65},
                            size_hint = (.1,.1),
                            markup = True,
                            font_name = 'font/RobotoMono-Regular',
                            font_size = 16)
        self.privatealg = Label(text = 'Your private decryption algorithm is: C = M[sup]d[/sup](mod N):\n',
                            pos_hint = {'x':.505, 'top':.575},
                            size_hint = (.1,.1),
                            markup = True,
                            font_name = 'font/RobotoMono-Regular',
                            font_size = 16)

        self.label = Label(text = 'Bob can use your public encryption algorithm to send messages to you. In this\n' +
                                'tool, Bob types in a message. Letters are paired up and then turned into numbers.\n' +
                                'The 4-digit numbers are then put into the encryption algorithm.',
                            pos_hint = {'x':.335, 'top':.45},
                            size_hint = (.1,.1))

        self.plaintextinput = TextInput(text = 'attack now',
                            pos_hint = {'x':.35, 'top':.3},
                            size_hint = (inputwidth,.05),
                            font_name = 'font/RobotoMono-Regular')
        self.plaintextlabel = Label(text = 'Plaintext',
                            pos_hint = {'x':.255, 'top':.325},
                            size_hint = (.1,.1),
                            font_size = 12)
        self.digraphdisplay = TextInput(text = '',
                            pos_hint = {'x':.35, 'top':.225},
                            size_hint = (inputwidth,.05),
                            font_name = 'font/RobotoMono-Regular')
        self.digraphlabel = Label(text = 'Digraph',
                            pos_hint = {'x':.255, 'top':.25},
                            size_hint = (.1,.1),
                            font_size = 12)
        self.numeralinput = TextInput(text = '',
                            pos_hint = {'x':.35, 'top':.15},
                            size_hint = (inputwidth,.05),
                            font_name = 'font/RobotoMono-Regular')
        self.numerallabel = Label(text = 'Numerals',
                            pos_hint = {'x':.255, 'top':.175},
                            size_hint = (.1,.1),
                            font_size = 12)
        self.ciphertextinput = TextInput(text = '',
                            pos_hint = {'x':.35, 'top':.075},
                            size_hint = (inputwidth,.05),
                            font_name = 'font/RobotoMono-Regular')
        self.ciphertextlabel = Label(text = 'Ciphertext',
                            pos_hint = {'x':.255, 'top':.1},
                            size_hint = (.1,.1),
                            font_size = 12)

        self.alphalabel = Label(text = '[color=0000ff]',
                            pos_hint = {'x':.875, 'top':.5},
                            size_hint = (.1,.1),
                            font_name = 'font/RobotoMono-Regular',
                            markup = True)
        self.numalphalabel = Label(text = '[color=ff0000]',
                            pos_hint = {'x':.9, 'top':.5},
                            size_hint = (.1,.1),
                            font_name = 'font/RobotoMono-Regular',
                            markup = True)
        self.digraphbutton = Button(text = 'Form Digraphs',
                            pos_hint = {'x':.035, 'top':.225},
                            size_hint = (.19,.05),
                            on_release = self.formdigraphs)
        self.convertonum = Button(text = 'Convert to Numerals',
                            pos_hint = {'x':.035, 'top':.15},
                            size_hint = (.19,.05),
                            disabled = True,
                            on_release = self.convert2numerals)
        self.encrypt = Button(text = 'Encipher',
                            pos_hint = {'x':.035, 'top':.075},
                            size_hint = (.19,.05),
                            disabled = True,
                            on_release = self.encrypt)
        self.reset = Button(text = 'Reset',
                            pos_hint = {'x':.775, 'top':.925},
                            size_hint = (.1,.05),
                            on_release = self.reset)

        for letter in range(len(self.alpha)):
            self.alphalabel.text = self.alphalabel.text + self.alpha[letter] + '\n'
            self.numalphalabel.text = self.numalphalabel.text + self.numalpha[letter] + '\n'
        self.alphalabel.text = self.alphalabel.text + '[/color]'
        self.numalphalabel.text = self.numalphalabel.text + '[/color]'

        self.r.add_widget(self.reset)
        self.r.add_widget(self.alphalabel)
        self.r.add_widget(self.numalphalabel)
        self.r.add_widget(self.pnot)
        self.r.add_widget(self.qnot)
        self.r.add_widget(self.bounds)
        self.r.add_widget(self.enter)
        self.r.add_widget(self.autoprime)
        self.r.add_widget(self.einput)
        self.r.add_widget(self.elabel)
        self.r.add_widget(self.dinput)
        self.r.add_widget(self.dlabel)
        self.r.add_widget(self.nlabel)
        self.r.add_widget(self.ndisplay)
        self.r.add_widget(self.pinput)
        self.r.add_widget(self.plabel)
        self.r.add_widget(self.qinput)
        self.r.add_widget(self.qlabel)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def autoselect(self, *args):
        f.write('auto select primes pressed\n')
        self.pinput.text = str(59)
        self.qinput.text = str(83)
        self.enterpressed()

    def check(self, *args):
        f.write('checking primes...\n')
        pn = (self.is_prime(int(self.pinput.text)))
        qn = (self.is_prime(int(self.qinput.text)))
        f.write('p bool: ' + str(pn) + ' q bool: ' + str(qn) + '\n')
        f.write('pn == False:' + str(pn == False) + '\n')
        if(pn == False):
            f.write('updating pnot text...\n')
            self.pnot.text = 'p is not a prime'
        if(qn == False):
            f.write('updating qnot text...\n')
            self.qnot.text = 'q is not a prime'
        if(pn == False or qn == False):
            return False
        else:
            return True

    def enterpressed(self, *args):
        f.write('enter pressed\n')
        self.enter.disabled = True
        self.autoprime.disabled = True
        self.pnot.text = ''
        self.qnot.text = ''
        self.bounds.text = ''
        p = int(self.pinput.text)
        q = int(self.qinput.text)
        if(self.check() == False):
            f.write('either p or q is not prime\n')
            return
        n = p * q
        if(n < 2525 or n > 10000):
            f.write('n is not in the bounds\n')
            self.bounds.text = 'N is not in the bounds of 2,525 and 10,000'
            return

        self.ndisplay.text = str(p * q)
        picked = False
        phi = (p - 1)*(q - 1)
        e = 0
        while(not picked):
            rande = randint(1, (phi/50))
            if(gcd(rande, phi) == 1):
                e = rande
                picked = True
        self.einput.text = str(e)
        picked2 = False
        d = 0
        while(not picked2):
            randd = randint(1, phi)
            if(((randd * e) % phi) == 1):
                d = randd
                picked2 = True
        self.dinput.text = str(d)
        self.publicalg.text = self.publicalg.text + 'M = C[sup]' + str(e) + '[/sup](mod' + str(n) + ')'
        self.privatealg.text = self.privatealg.text + 'C = M[sup]' + str(d) + '[/sup](mod' + str(n) + ')'
        self.r.add_widget(self.publicalg)
        self.r.add_widget(self.privatealg)
        self.r.add_widget(self.label)
        self.r.add_widget(self.digraphbutton)
        self.r.add_widget(self.plaintextinput)
        self.r.add_widget(self.plaintextlabel)
        self.r.add_widget(self.ciphertextinput)
        self.r.add_widget(self.ciphertextlabel)
        self.r.add_widget(self.digraphdisplay)
        self.r.add_widget(self.digraphlabel)
        self.r.add_widget(self.numeralinput)
        self.r.add_widget(self.numerallabel)
        self.r.add_widget(self.convertonum)
        self.r.add_widget(self.encrypt)

    def is_prime(self, n):
        if n==2 or n==3:
            return True
        if n%2==0 or n<2:
            return False
        for i in range(3,int(n**0.5)+1,2):   # only odd numbers
            if n%i==0:
                return False
        return True

    def formdigraphs(self, *args):
        f.write('form digraphs pressed\n')
        self.digraphbutton.disabled = True
        self.convertonum.disabled = False
        text = self.plaintextinput.text

        tempstr = ''

        count = 0
        for letter in text:
            if letter == ' ':
                letter = 'x'
            if count == 1:
                tempstr = tempstr + letter + ' '
                count = 0
            else:
                tempstr = tempstr + letter
                count = count + 1

        self.digraphdisplay.text = tempstr

    def convert2numerals(self, *args):
        f.write('convert to numerals pressed\n')
        self.convertonum.disabled = True
        self.encrypt.disabled = False
        di = self.digraphdisplay.text
        temp = ''
        for letter in di:
            if letter == ' ':
                temp += ' '
            else:
                for i in range(len(self.alpha)):
                    if letter == self.alpha[i]:
                        temp += self.numalpha[i]

        self.numeralinput.text = temp

    def encrypt(self, *args):
        f.write('encrypt pressed\n')
        listdi = self.numeralinput.text.split()
        new = ''
        e = int(self.einput.text)
        n = int(self.ndisplay.text)
        for group in listdi:
            tempint = int(group)
            f.write('calc = (tempint**e) mod n\n')

            calc = (tempint**e) % n
            f.write(str(calc) + ' = (' + str(tempint) + '**' + str(e) + ')mod ' + str(n) + '\n')
            new += str(calc) + ' '

        self.ciphertextinput.text = new

    def reset(self, *args):
        f.write('resetting rsa encryption tool....\n')
        self.autoprime.disabled = False
        self.digraphbutton.disabled = False
        self.convertonum.disabled = True
        self.encrypt.disabled = True
        self.publicalg.text = 'Your public encryption algorithm is: M = C[sup]e[/sup](mod N):\n'
        self.privatealg.text = 'Your private decryption algorithm is: C = M[sup]d[/sup](mod N):\n'
        self.pinput.text = ''
        self.qinput.text = ''
        self.einput.text = ''
        self.ndisplay.text = ''
        self.dinput.text = ''
        self.plaintextinput.text = 'attack now'
        self.ciphertextinput.text = ''
        self.digraphdisplay.text = ''
        self.numeralinput.text = ''
        self.r.remove_widget(self.publicalg)
        self.r.remove_widget(self.privatealg)
        self.r.remove_widget(self.label)
        self.r.remove_widget(self.digraphbutton)
        self.r.remove_widget(self.plaintextinput)
        self.r.remove_widget(self.plaintextlabel)
        self.r.remove_widget(self.ciphertextinput)
        self.r.remove_widget(self.ciphertextlabel)
        self.r.remove_widget(self.digraphdisplay)
        self.r.remove_widget(self.digraphlabel)
        self.r.remove_widget(self.numeralinput)
        self.r.remove_widget(self.numerallabel)
        self.r.remove_widget(self.convertonum)
        self.r.remove_widget(self.encrypt)
################################################################################
#End RSA Encryption Tool Page
################################################################################



################################################################################
#Begin Prime Number Questions Page
################################################################################
class PrimeNumberQuestionsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Prime Number Questions page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Prime Number Questions")

        with open('texts/primenumberquestions.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.55, 'top':.85},
                            size_hint = (.2,.2))

        self.hyperlink1 = Label(text = '[b]The Prime Pages[/b]\n[color=ffff00][ref=h1]http://www.utm.edu/research/primes/[/ref][/color]\n' +
                                        'Everything you ever wanted to know about prime numbers.',
                            pos_hint = {'x':.475, 'top':.65},
                            size_hint = (.2,.2),
                            on_ref_press = self.h1,
                            markup = True)

        self.hyperlink2 = Label(text = '[b]Ask Dr. Math[/b]\n[color=ffff00][ref=h2]http://mathforum.org/dr.math/faq/faq.prime.num.html[/ref][/color]\n' +
                                        'A more gentle introduction to the subject of prime numbers.',
                            pos_hint = {'x':.4825, 'top':.525},
                            size_hint = (.2,.2),
                            on_ref_press = self.h2,
                            markup = True)


        self.hyperlink3 = Label(text = "[b]World's Largest Prime[/b]\n[color=ffff00][ref=h2]http://www.utm.edu/research/primes/largest.html#largest[/ref][/color]\n" +
                                        "2[sup]13466917[/sup] - 1, find out about the world's biggest prime number discovered so far.",
                            pos_hint = {'x':.555, 'top':.4},
                            size_hint = (.2,.2),
                            on_ref_press = self.h3,
                            markup = True)

        self.image = Image(source = 'pics/PRIME.png',
                            pos_hint = {'x':-.2, 'top':.85},
                            size_hint = (.7,.7))

        self.r.add_widget(self.image)
        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.hyperlink3)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening http://www.utm.edu/research/primes/ ...\n')
        webbrowser.open('http://www.utm.edu/research/primes/')

    def h2(self, *args):
        f.write('opening http://mathforum.org/dr.math/faq/faq.prime.num.html ...\n')
        webbrowser.open('http://mathforum.org/dr.math/faq/faq.prime.num.html')

    def h3(self, *args):
        f.write('opening http://www.utm.edu/research/primes/largest.html#largest ...\n')
        webbrowser.open('http://www.utm.edu/research/primes/largest.html#largest')
################################################################################
#End Prime Number Questions Page
################################################################################


################################################################################
#Begin RSA In Practice Page
################################################################################
class RSAInPracticePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('RSA In Practice page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("RSA In Practice")

        with open('texts/rsainpractice.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.1, 'top':.85},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/adle2-2.avi',
                            pos_hint = {'x':0, 'top':.65},
                            size_hint = (.4,.4),
                            allow_fullscreen = False)

        self.videolabel = Label(text = '[i]In the video clip, Len Adleman, one of the\n' +
                                    'co-inventors of RSA, explains that RSA is\n' +
                                    'used for security on the Internet. This has\n' +
                                    'resulted in RSA being one of the most\n' +
                                    'widely used pieces of software in the world.' +
                                    '[/i]',
                            pos_hint = {'x':.1, 'top':.25},
                            size_hint = (.2,.2),
                            markup = True)


        self.hyperlink1 = Label(text = '[b]SSL[/b]\n[color=ffff00][ref=h1]https://www.digicert.com/ssl-cryptography.htm[/ref][/color]\n' +
                                        'Secure Sockets Layer (SSL) is the industry-\n' +
                                        'standard method for protecting data exchange on\n' +
                                        'the web. These sites explain the relationship\n' +
                                        'between RSA and SSL.',
                            pos_hint = {'x':.535, 'top':.9},
                            size_hint = (.2,.2),
                            on_ref_press = self.h1,
                            markup = True)

        self.hyperlink2 = Label(text = '[b]PKI[/b]\n[color=ffff00][ref=h2]http://searchsecurity.techtarget.com/definition/PKI[/ref][/color]\n' +
                                        'Public Key Infrastructure (PKI) is the phrase used\n' +
                                        'to describe what is required to make RSA operate\n' +
                                        'in the real world. For example, if you have a public\n' +
                                        'key, how will you make it publicly available? How\n' +
                                        'will other people know that the public key is truly\n' +
                                        'yours, rather than fake created by someone?',
                            pos_hint = {'x':.545, 'top':.65},
                            size_hint = (.2,.2),
                            on_ref_press = self.h2,
                            markup = True)

        self.hyperlink3 = Label(text = '[b]RSA FAQ[/b]\n[color=ffff00][ref=h1]https://uk.emc.com/emc-plus/rsa-labs/historical/crypto-faq.htm[/ref][/color]',
                            pos_hint = {'x':.6, 'top':.4},
                            size_hint = (.2,.2),
                            on_ref_press = self.h3,
                            markup = True)

        self.button = Button(text = 'Is RSA Secure?',
                            pos_hint = {'x':.825, 'top':.1},
                            size_hint = (.14,.075),
                            on_release = self.buttonpress)

        self.r.add_widget(self.video)
        self.r.add_widget(self.button)
        self.r.add_widget(self.videolabel)
        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.hyperlink3)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening https://www.digicert.com/ssl-cryptography.htm ...\n')
        webbrowser.open('https://www.digicert.com/ssl-cryptography.htm')

    def h2(self, *args):
        f.write('opening http://searchsecurity.techtarget.com/definition/PKI ...\n')
        webbrowser.open('http://searchsecurity.techtarget.com/definition/PKI')

    def h3(self, *args):
        f.write('opening https://uk.emc.com/emc-plus/rsa-labs/historical/crypto-faq.htm ...\n')
        webbrowser.open('https://uk.emc.com/emc-plus/rsa-labs/historical/crypto-faq.htm')

    def buttonpress(self, *args):
        f.write('is rsa secure pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(IsRSASecurePage().create())
################################################################################
#End RSA In Practice Page
################################################################################


################################################################################
#Begin Is RSA Secure? Page
################################################################################
class IsRSASecurePage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Is RSA Secure? page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Is RSA Secure?")

        with open('texts/isrsasecure1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.9},
                            size_hint = (.2,.2))

        with open('texts/isrsasecure2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.5, 'top':.7},
                            size_hint = (.2,.2))

        with open('texts/isrsasecure3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.5, 'top':.45},
                            size_hint = (.2,.2))

        with open('texts/isrsasecure4.txt', 'r') as myfile:
            data4 = myfile.read()
        self.text4 = Label(text = data4,
                            pos_hint = {'x':.5, 'top':.2},
                            size_hint = (.2,.2))

        self.image1 = Image(source = 'pics/secure3.png',
                            pos_hint = {'x':-.05, 'top':.81},
                            size_hint = (.4,.4))
        self.image2 = Image(source = 'pics/insecure.png',
                            pos_hint = {'x':-.05, 'top':.55},
                            size_hint = (.4,.4))
        self.image3 = Image(source = 'pics/secure3.png',
                            pos_hint = {'x':-.05, 'top':.31},
                            size_hint = (.4,.4))

        self.hyperlink1 = Label(text = '[color=ffff00][ref=h1]FAQ About RSA Challenges[/ref][/color]',
                            pos_hint = {'x':.5, 'top':.35},
                            size_hint = (.2,.2),
                            on_ref_press = self.h1,
                            markup = True)

        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.text4)
        self.r.add_widget(self.image1)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.image3)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening https://singapore.emc.com/emc-plus/rsa-labs/historical/the-rsa-factoring-challenge-faq.htm ...\n')
        webbrowser.open('https://singapore.emc.com/emc-plus/rsa-labs/historical/the-rsa-factoring-challenge-faq.htm')
################################################################################
#End Is RSA Secure? Page
################################################################################

################################################################################
#Begin Not Just Secrets Page
################################################################################
class NotJustSecretsPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Not Just Secrets page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Not Just Secrets")

        with open('texts/notjustsecrets1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.675},
                            size_hint = (.2,.2))

        with open('texts/notjustsecrets2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.625, 'top':.6},
                            size_hint = (.2,.2))

        self.hyperlink1 = Label(text = 'To find out how US President Clinton and Irish Prime Minister Bertie Ahern put their digital\n' +
                                        'signatures on a document, click [color=ffff00][ref=h1]here[/ref][/color].',
                            pos_hint = {'x':.4, 'top':.25},
                            size_hint = (.2,.2),
                            on_ref_press = self.h1,
                            markup = True)

        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening http://www.nytimes.com/1998/09/10/news/clinton-signs-off-on-digital-advance.html ...\n')
        webbrowser.open('http://www.nytimes.com/1998/09/10/news/clinton-signs-off-on-digital-advance.html')
################################################################################
#End Not Just Secrets Page
################################################################################


################################################################################
#Begin The Secret History Page
################################################################################
class TheSecretHistoryPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('The Secret History page entered\n')
        MyApp.current = self
        buttonx = .825
        buttonsize = (.15,.15)

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The Secret History")

        with open('texts/thesecrethistory1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.125, 'top':.8},
                            size_hint = (.2,.2))

        with open('texts/thesecrethistory2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.525, 'top':.8},
                            size_hint = (.2,.2))

        self.button1 = Button(text = 'James Ellis\nAnd\nClifford Cocks',
                            pos_hint = {'x':buttonx, 'top':.8},
                            size_hint = buttonsize,
                            on_release = self.button1pressed)
        self.button2 = Button(text = 'Malcolm\nWilliamson',
                            pos_hint = {'x':buttonx, 'top':.55},
                            size_hint = buttonsize,
                            on_release = self.button2pressed)
        self.button3 = Button(text = '25 Year\nSecret',
                            pos_hint = {'x':buttonx, 'top':.3},
                            size_hint = buttonsize,
                            on_release = self.button3pressed)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.tb)
        return self.r

    def button1pressed(self, *args):
        f.write('james ellis and clifford cocks pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(JamesAndCliffordPage().create())

    def button2pressed(self, *args):
        f.write('malcolm williamson pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(MalcolmWilliamsonPage().create())

    def button3pressed(self, *args):
        f.write('25 year secret pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(YearSecretPage().create())
################################################################################
#End The Secret History Page
################################################################################

################################################################################
#Begin James Ellis and Clifford Cocks Page
################################################################################
class JamesAndCliffordPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('James Ellis and Clifford Cocks page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("James Ellis and Clifford Cocks")

        with open('texts/jamesandclifford1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.175, 'top':.85},
                            size_hint = (.2,.2))

        with open('texts/jamesandclifford2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.625, 'top':.85},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/ellis3.png',
                            pos_hint = {'x':0, 'top':.6},
                            size_hint = (.5,.5))

        self.video = VideoPlayer(source = 'video/cocks1-1.avi',
                            pos_hint = {'x':.475, 'top':.65},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.videolabel = Label(text = '[i]Clifford Cocks tells how he first heard about the\n' +
                                        'concept of an asymmetric cipher. This is the first\n' +
                                        'ever interview with a GCHQ cryptographer.[/i]',
                            pos_hint = {'x':.625, 'top':.2},
                            size_hint = (.2,.2),
                            markup = True)

        self.imagelabel = Label(text = '[i]James Ellis[/i]',
                            pos_hint = {'x':.15, 'top':.175},
                            size_hint = (.2,.2),
                            markup = True)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.image)
        self.r.add_widget(self.imagelabel)
        self.r.add_widget(self.video)
        self.r.add_widget(self.videolabel)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End James Ellis and Clifford Cocks Page
################################################################################

################################################################################
#Begin Malcolm Williamson Page
################################################################################
class MalcolmWilliamsonPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Malcolm Williamson page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Malcolm Williamson")

        with open('texts/malcolmwilliamson1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.85},
                            size_hint = (.2,.2))

        with open('texts/malcolmwilliamson2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.6, 'top':.85},
                            size_hint = (.2,.2))

        self.image1 = Image(source = 'pics/MALCWILL.png',
                            pos_hint = {'x':.5, 'top':.6625},
                            size_hint = (.6,.6))
        self.image2 = Image(source = 'pics/MGS.png',
                            pos_hint = {'x':.025, 'top':.725},
                            size_hint = (.6,.6))
        self.label1 = Label(text = '[i]Malcolm Williamson in a photo of the British team\n' +
                                    'arriving for the Mathematical Olympiad in 1968 in\n' +
                                    'Moscow. Williamson is second from the left. Clifford\n' +
                                    'Cocks was also in the team and is on the right.[/i]',
                            pos_hint = {'x':.25, 'top':.25},
                            size_hint = (.2,.2),
                            markup = True)
        self.label2 = Label(text = '[i]Malcolm Williamson(1999)[/i]',
                            pos_hint = {'x':.675, 'top':.175},
                            size_hint = (.2,.2),
                            markup = True)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.image1)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.label1)
        self.r.add_widget(self.label2)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Malcolm Williamson Page
################################################################################

################################################################################
#Begin 25 Year Secret Page
################################################################################
class YearSecretPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('25 Year Secret page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("25 Year Secret")

        with open('texts/25yearsecret.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.175, 'top':.8},
                            size_hint = (.2,.2))

        with open('texts/25yearsecret2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.625, 'top':.8},
                            size_hint = (.2,.2))

        self.video = VideoPlayer(source = 'video/cocks2-3.avi',
                            pos_hint = {'x':.475, 'top':.5},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.videolabel = Label(text = "[i]Clifford Cocks' attitude is simple:\n" +
                                        '\"You do not get involved in this business\n' +
                                        'for public recognition.\" In the video\n' +
                                        'clip, however, he explains that working\n' +
                                        'for a top secret organisation did have\n' +
                                        'some drawbacks. For example, working\n' +
                                        'at home (where he discovered RSA)\n' +
                                        'was made surprisingly difficult because\n' +
                                        'of the security issues.[/i]',
                            pos_hint = {'x':.2, 'top':.35},
                            size_hint = (.2,.2),
                            markup = True)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.video)
        self.r.add_widget(self.videolabel)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End 25 Year Secret Page
################################################################################


################################################################################
#Begin Future of Cryptography Page
################################################################################
class FOC(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Future of Cryptography page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()

        #create the topbar navigation
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Future of Cryptography (1999)")

        with open('texts/futureofcryptography.txt', 'r') as myfile:
            data = myfile.read()
        self.text = Label(text = data,
                            pos_hint = {'x':.3, 'top':.725},
                            size_hint = (.2,.2))

        self.button1 = Button(text = "Politics of\nEncryption",
                                        pos_hint = {'x':.825, 'top':.85},
                                        size_hint = (.15,.1),
                                        on_release = self.onePressed,
                                        font_size = 14)

        self.button2 = Button(text = "Steganography",
                                        pos_hint = {'x':.825, 'top':.65},
                                        size_hint = (.15,.1),
                                        on_release = self.twoPressed,
                                        font_size = 14)

        self.button3 = Button(text = "Quantum\nCryptography",
                                        pos_hint = {'x':.825, 'top':.45},
                                        size_hint = (.15,.1),
                                        on_release = self.threePressed,
                                        font_size = 14)

        self.button4 = Button(text = "The End?",
                                        pos_hint = {'x':.825, 'top':.25},
                                        size_hint = (.15,.1),
                                        on_release = self.fourPressed,
                                        font_size = 14)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text)
        self.r.add_widget(self.tb)
        return self.r

    def onePressed(self, *args):
        f.write("politics of encryption pressed\n")
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(PoliticsOfEncryptionPage().create())

    def twoPressed(self, *args):
        f.write('steganography pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(SteganographyPage().create())

    def threePressed(self, *args):
        f.write('quantum cryptography pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography1().create())

    def fourPressed(self, *args):
        f.write('the end? pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(TheEndPage().create())
################################################################################
#End Future of Cryptography Page
################################################################################

################################################################################
#Begin Politics of Encryption Page
################################################################################
class PoliticsOfEncryptionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Politics of Encryption page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Politics of Encryption")

        with open('texts/politicsofencryption.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.55, 'top':.65},
                            size_hint = (.2,.2))

        self.image = Image(source = 'pics/philzimm.png',
                            pos_hint = {'x':-.1, 'top':.875},
                            size_hint = (.6,.6))

        self.button1 = Button(text = 'Pro Encryption',
                            pos_hint = {'x':.825, 'top':.9},
                            size_hint = (.15,.15),
                            on_release = self.button1pressed)
        self.button2 = Button(text = 'Anti Encryption',
                            pos_hint = {'x':.825, 'top':.7},
                            size_hint = (.15,.15),
                            on_release = self.button2pressed)

        self.imagelabel = Label(text = 'Phil Zimmerman',
                            pos_hint = {'x':.115, 'top':.325},
                            size_hint = (.2,.2))

        self.hyperlink1 = Label(text = '[color=ffff00][ref=h1]http://www.philzimmermann.com[/color][/ref]',
                            pos_hint = {'x':.4, 'top':.2},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.h1)

        self.hyperlink2 = Label(text = '[color=ffff00][ref=h2]http://www.pgpi.org[/color][/ref]',
                            pos_hint = {'x':.4, 'top':.15},
                            size_hint = (.2,.2),
                            markup = True,
                            on_ref_press = self.h2)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.imagelabel)
        self.r.add_widget(self.image)
        self.r.add_widget(self.hyperlink1)
        self.r.add_widget(self.hyperlink2)
        self.r.add_widget(self.tb)
        return self.r

    def h1(self, *args):
        f.write('opening http://www.philzimmermann.com ...\n')
        webbrowser.open('http://www.philzimmermann.com')

    def h2(self, *args):
        f.write('opening http://www.pgpi.org ...\n')
        webbrowser.open('http://www.pgpi.org')

    def button1pressed(self, *args):
        f.write('pro encryption pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ProEncryptionPage().create())

    def button2pressed(self, *args):
        f.write('anti encryption pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(AntiEncryptionPage().create())
################################################################################
#End Politics of Encryption Page
################################################################################


################################################################################
#Begin Pro Encryption Page
################################################################################
class ProEncryptionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Pro Encryption page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Pro Encryption")

        with open('texts/proencryption.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.6},
                            size_hint = (.2,.2),
                            font_size = 18)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Pro Encryption Page
################################################################################

################################################################################
#Begin Anti Encryption Page
################################################################################
class AntiEncryptionPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Anti Encryption page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Anti Encryption")

        with open('texts/antiencryption.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.4, 'top':.6},
                            size_hint = (.2,.2),
                            font_size = 18)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Anti Encryption Page
################################################################################

################################################################################
#Begin Steganography Page
################################################################################
class SteganographyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Steganography page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Steganography")

        with open('texts/steganography.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.65, 'top':.65},
                            size_hint = (.2,.2))

        self.label1 = Label(text = '[i]The Ancient Greeks were masters of\n' +
                                    'steganography. Herodotus chronicled one\n' +
                                    'example, whereby the message was not\n' +
                                    'inscribed in wax, but written on the wooden\n' +
                                    'tablet underneath the wax. The video clip\n' +
                                    'describes one of the most bizarre examples\n' +
                                    'of steganography.[/i]',
                            pos_hint = {'x':.15, 'top':.35},
                            size_hint = (.2,.2),
                            markup = True)

        self.video = VideoPlayer(source = 'video/shave2.avi',
                            pos_hint = {'x':0, 'top':.9},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.button = Button(text = 'Modern\nSteganography',
                            pos_hint = {'x':.85, 'top':.9},
                            size_hint = (.125,.125),
                            on_release = self.buttonpressed,
                            font_size = 14)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.button)
        self.r.add_widget(self.label1)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('modern steganography pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(ModernSteganographyPage().create())
################################################################################
#End Steganography Page
################################################################################

################################################################################
#Begin Modern Steganography Page
################################################################################
class ModernSteganographyPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Modern Steganography page entered\n')
        MyApp.current = self
        textht = .8
        imght = .45
        btnht = .55

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Modern Steganography")

        with open('texts/modernsteganography1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.025, 'top':textht},
                            size_hint = (.2,.2))

        with open('texts/modernsteganography2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.275, 'top':textht},
                            size_hint = (.2,.2))

        with open('texts/modernsteganography3.txt', 'r') as myfile:
            data3 = myfile.read()
        self.text3 = Label(text = data3,
                            pos_hint = {'x':.525, 'top':textht},
                            size_hint = (.2,.2))

        with open('texts/modernsteganography4.txt', 'r') as myfile:
            data4 = myfile.read()
        self.text4 = Label(text = data4,
                            pos_hint = {'x':.775, 'top':textht},
                            size_hint = (.2,.2))

        self.baby1 = Image(source = 'pics/modsteg/baby4.png',
                            pos_hint = {'x':-.075, 'top':imght},
                            size_hint = (.4,.4))
        self.ascii1 = Image(source = 'pics/modsteg/modsteg1.png',
                            pos_hint = {'x':.175, 'top':imght},
                            size_hint = (.4,.4))
        self.ascii2 = Image(source = 'pics/modsteg/modsteg2.png',
                            pos_hint = {'x':.425, 'top':imght},
                            size_hint = (.4,.4))
        self.baby2 = Image(source = 'pics/modsteg/baby4.png',
                            pos_hint = {'x':.675, 'top':imght},
                            size_hint = (.4,.4))

        self.button1 = Button(text = 'Show Pixels',
                            pos_hint = {'x':.0175, 'top':btnht},
                            size_hint = (.225,.05),
                            on_release = self.button1pressed)
        self.button2 = Button(text = 'Show Greyscale Numbers',
                            pos_hint = {'x':.2675, 'top':btnht},
                            size_hint = (.225,.05),
                            on_release = self.button2pressed,
                            disabled = True)
        self.button3 = Button(text = 'Add Message',
                            pos_hint = {'x':.5175, 'top':btnht},
                            size_hint = (.225,.05),
                            on_release = self.button3pressed,
                            disabled = True)
        self.button4 = Button(text = 'Show New Picture',
                            pos_hint = {'x':.7675, 'top':btnht},
                            size_hint = (.225,.05),
                            on_release = self.button4pressed,
                            disabled = True)

        self.r.add_widget(self.button1)
        self.r.add_widget(self.button2)
        self.r.add_widget(self.button3)
        self.r.add_widget(self.button4)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.text3)
        self.r.add_widget(self.text4)
        self.r.add_widget(self.tb)
        return self.r

    def button1pressed(self, *args):
        f.write('show pixels pressed\n')
        self.r.add_widget(self.baby1)
        self.button1.disabled = True
        self.button2.disabled = False
    def button2pressed(self, *args):
        f.write('show greyscale numbers pressed\n')
        self.r.add_widget(self.ascii1)
        self.button2.disabled = True
        self.button3.disabled = False
    def button3pressed(self, *args):
        f.write('add message pressed\n')
        self.r.add_widget(self.ascii2)
        self.button3.disabled = True
        self.button4.disabled = False
    def button4pressed(self, *args):
        f.write('show new picture pressed\n')
        self.r.add_widget(self.baby2)
        self.button4.disabled = True
################################################################################
#End Modern Steganography Page
################################################################################

################################################################################
#Begin Quantum Cryptography Page 1
################################################################################
class QuantumCryptography1(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography1.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.45},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography2.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.575},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '1',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))

        self.label = Label(text = '[b]This explanation of quantum cryptography is\n' +
                                    'from an article [Simon Singh] wrote for New\n' +
                                    'Scientist magazine in 1999.[/b]',
                            pos_hint = {'x':.15, 'top':.9},
                            size_hint = (.2,.2),
                            markup = True)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.label)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 2 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography2().create())
################################################################################
#End Quantum Cryptography Page 1
################################################################################

################################################################################
#Begin Quantum Cryptography Page 2
################################################################################
class QuantumCryptography2(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 2 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography3.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.575},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography4.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.575},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '2',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 2 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography3().create())
################################################################################
#End Quantum Cryptography Page 2
################################################################################



################################################################################
#Begin Quantum Cryptography Page 3
################################################################################
class QuantumCryptography3(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography5.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.565},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography6.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.595},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '3',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))


        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 4 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography4().create())
################################################################################
#End Quantum Cryptography Page 3
################################################################################



################################################################################
#Begin Quantum Cryptography Page 4
################################################################################
class QuantumCryptography4(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 4 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography7.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.7},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography8.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.775},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '4',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))

        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 5 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography5().create())
################################################################################
#End Quantum Cryptography Page 4
################################################################################

################################################################################
#Begin Quantum Cryptography Page 5
################################################################################
class QuantumCryptography5(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 5 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography9.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.595},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography10.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.585},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '5',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))


        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 6 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography6().create())
################################################################################
#End Quantum Cryptography Page 5
################################################################################

################################################################################
#Begin Quantum Cryptography Page 6
################################################################################
class QuantumCryptography6(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 6 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography11.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.55},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography12.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.595},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '6',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))


        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 7 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography7().create())
################################################################################
#End Quantum Cryptography Page 6
################################################################################

################################################################################
#Begin Quantum Cryptography Page 7
################################################################################
class QuantumCryptography7(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 7 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography13.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.55},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography14.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.62},
                            size_hint = (.2,.2))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '7',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))


        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 8 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography8().create())
################################################################################
#End Quantum Cryptography Page 7
################################################################################

################################################################################
#Begin Quantum Cryptography Page 8
################################################################################
class QuantumCryptography8(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 8 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        with open('texts/quantumcryptography15.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.75},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography16.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.4},
                            size_hint = (.2,.2))

        self.image1 = Image(source = 'pics/QALICE.png',
                            pos_hint = {'x':0, 'top':.5},
                            size_hint = (.5,.5))

        self.image2 = Image(source = 'pics/QBOB.png',
                            pos_hint = {'x':.5, 'top':1},
                            size_hint = (.5,.5))

        self.button = Button(text = 'Next Page',
                            pos_hint = {'x':.875, 'top':.075},
                            size_hint = (.1,.05),
                            on_release = self.buttonpressed,
                            font_size = 14)
        self.pagenum = Label(text = '8',
                            pos_hint = {'x':.75, 'top':.15},
                            size_hint = (.2,.2))

        self.r.add_widget(self.image1)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.button)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r

    def buttonpressed(self, *args):
        f.write('quantum cryptography 9 pressed\n')
        MyApp.trail.append(self)
        root.clear_widgets()
        root.add_widget(QuantumCryptography9().create())
################################################################################
#End Quantum Cryptography Page 8
################################################################################

################################################################################
#Begin Quantum Cryptography Page 9
################################################################################
class QuantumCryptography9(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('Quantum Cryptography 9 page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("Quantum Cryptography")

        imght = .3
        imgsz = (.25,.25)
        with open('texts/quantumcryptography17.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.15, 'top':.7},
                            size_hint = (.2,.2))

        with open('texts/quantumcryptography18.txt', 'r') as myfile:
            data2 = myfile.read()
        self.text2 = Label(text = data2,
                            pos_hint = {'x':.65, 'top':.7},
                            size_hint = (.2,.2))

        self.image1 = Image(source = 'pics/qcrypt9/STL.png',
                            pos_hint = {'x':0.05, 'top':imght},
                            size_hint = imgsz)

        self.image2 = Image(source = 'pics/qcrypt9/STLENC.png',
                            pos_hint = {'x':.375, 'top':imght},
                            size_hint = imgsz)

        self.image3 = Image(source = 'pics/qcrypt9/STLDEC.png',
                            pos_hint = {'x':.7, 'top':imght},
                            size_hint = imgsz)

        self.pagenum = Label(text = '9',
                            pos_hint = {'x':.8, 'top':.125},
                            size_hint = (.2,.2))

        self.label = Label(text = '[i]Original picture, encrypted picture sent by the Los Alamos experiment, ' +
                                    'and the decrypted result.[/i]',
                            pos_hint = {'x':.35, 'top':.125},
                            size_hint = (.2,.2),
                            markup = True)

        self.r.add_widget(self.image1)
        self.r.add_widget(self.image2)
        self.r.add_widget(self.image3)
        self.r.add_widget(self.label)
        self.r.add_widget(self.text1)
        self.r.add_widget(self.text2)
        self.r.add_widget(self.pagenum)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End Quantum Cryptography Page 9
################################################################################


################################################################################
#Begin The End? Page
################################################################################
class TheEndPage(ButtonBehavior):
    def __init__(self):
        pass

    def create(self):
        f.write('The End? page entered\n')
        MyApp.current = self

        self.r = RelativeLayout()
        self.topbar = TopBar()
        MyApp.topbar = self.topbar
        self.tb = self.topbar.create("The End?")

        with open('texts/theend.txt', 'r') as myfile:
            data1 = myfile.read()
        self.text1 = Label(text = data1,
                            pos_hint = {'x':.125, 'top':.8},
                            size_hint = (.2,.2),
                            font_size = 16)

        self.video = VideoPlayer(source = 'video/end3.avi',
                            pos_hint = {'x':.45, 'top':.9},
                            size_hint = (.5,.5),
                            allow_fullscreen = False)

        self.r.add_widget(self.text1)
        self.r.add_widget(self.video)
        self.r.add_widget(self.tb)
        return self.r
################################################################################
#End The End? Page
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
        self.home = Button(text = 'home', size_hint = (.06,.07), pos_hint = {'right':1},
                            on_release = self.home_press)
        self.index = Button(text = '?', size_hint = (.05,.07), pos_hint = {'right':.935},
                            on_release = self.index_press)

        if(MyApp.trail == []):
            self.back.disabled = True
        else:
            self.back.disabled = False


        self.r.add_widget(self.titlelabel)
        self.r.add_widget(self.back)
        self.r.add_widget(self.home)
        self.r.add_widget(self.index)
        return self.r

    def back_press(self, *args):
        f.write('back pressed\n')
        for child in MyApp.current.r.children:
            try:
                if child.source[0] == 'v':
                    child.state = 'stop'
                else:
                    pass
            except AttributeError:
                pass
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

class maxinput(TextInput):
    max_chars = None
    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text)+len(substring) > self.max_chars):
            return
        super(maxinput, self).insert_text(substring, from_undo)

if __name__ == '__main__':
    f.write("-----------------------------------------------------\n")
    f.write(time.strftime("%d/%m/%Y %I:%M:%S"))
    f.write('\n')
    MyApp().run()
    f.write("-----------------------------------------------------\n")
