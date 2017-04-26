import sys
import os
import itertools
from collections import deque
from random import shuffle
from random import randint
from random import choice
from fractions import gcd


#key file
try:
    os.remove('key')
except OSError:
    print 'file does not exist'
k = open('key', 'w+')
#arg[1] = cipher type (r,c,a,gm,di,p,ho,ks,s,v,adfgvx)
#arg[2] = f or t (file or text)
#arg[3] = path or text
#arg[4] = encrypt or decrypt
#
def main():
    print sys.argv
    arg = sys.argv

    print "railfence - r\ncaesar - c\natbash - a\ngeneral monoalphabetic - gm"
    print "digraph - d\nplayfair - p\nhomophonic - ho\nkama-sutra - ks\nswapping - s"
    print "vigenere - v\nadfgvx - adfgvx\n\n"
    ciph = raw_input("enter in cipher choice: ")

    if ciph == 'r':
        #introduce the cipher
        print 'the railfence cipher is transposition cipher that uses a shift'
        print 'amount to encrypt plaintext\n'
        #initialize the class
        railfence = Railfence()
        print 'options for railfence\nencrypt - e'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        #determine if the user is using a file or text
        choice2 = fileortext()
        #if the user has a file
        if choice2[0] == 'f':
            #retrieve the file from the returned list
            fil = choice2[1]
            #read the lines and convert it into a string as plaintext
            lines = fil.readlines()
            plaintext = ''.join(lines)
            #get the shift amount
            shift = getshiftamount()
            print railfence.encrypt(plaintext, shift)
        #if the user has text
        elif choice2[0] == 't':
            plaintext = choice2[1]
            shift = getshiftamount()
            print railfence.encrypt(plaintext, shift)
    elif ciph == 'c':
        caesar = Caesar()
        print 'the caesar cipher is substitution cipher that uses a shift'
        print 'amount to encrypt plaintext by shifting the english alphabet\n'
        print 'options for caesar\nencrypt - e\ndecrypt - d\niterative decryption - i'
        choice1 = raw_input('enter choice: ')
        if choice1 == 'e':
            #encrypt
            choice2 = fileortext()
            if choice2[0] == 'f':
                fil = choice2[1]
                lines = fil.readlines()
                plaintext = ''.join(lines)
                shift = getshiftamount()
                print caesar.encrypt(plaintext, shift)
            elif choice2[0] == 't':
                plaintext = choice2[1]
                shift = getshiftamount()
                print caesar.encrypt(plaintext, shift)
        elif choice1 == 'd':
            #decrypt
            choice2 = fileortext()
            if choice2[0] == 'f':
                fil = choice2[1]
                lines = fil.readlines()
                plaintext = ''.join(lines)
                shift = getshiftamount()
                print caesar.decrypt(plaintext, shift)
            elif choice2[0] == 't':
                plaintext = choice2[1]
                shift = getshiftamount()
                print caesar.decrypt(plaintext, shift)
        elif choice1 == 'i':
            #iterative decryption
            choice2 = fileortext()
            if choice2[0] == 'f':
                fil = choice2[1]
                lines = fil.readlines()
                plaintext = ''.join(lines)
                print caesar.iterdecrypt(plaintext)
            elif choice2[0] == 't':
                plaintext = choice2[1]
                print caesar.iterdecrypt(plaintext)
    elif ciph == 'a':
        atbash = Atbash()
        #introduce the cipher
        print 'the atbash cipher is substitution cipher that uses the backwards'
        print 'alphabet to encrypt plaintext\n'
        print 'options for atbash\nencrypt - e\ndecrypt - d'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        if choice1 == 'e':
            #determine if the user is using a file or text
            choice2 = fileortext()
            #if the user has a file
            if choice2[0] == 'f':
                #retrieve the file from the returned list
                fil = choice2[1]
                #read the lines and convert it into a string as plaintext
                lines = fil.readlines()
                plaintext = ''.join(lines)
                print atbash.encrypt(plaintext)
            #if the user has text
            elif choice2[0] == 't':
                plaintext = choice2[1]
                print atbash.encrypt(plaintext)
        elif choice1 == 'd':
            #determine if the user is using a file or text
            choice2 = fileortext()
            #if the user has a file
            if choice2[0] == 'f':
                #retrieve the file from the returned list
                fil = choice2[1]
                #read the lines and convert it into a string as plaintext
                lines = fil.readlines()
                plaintext = ''.join(lines)
                print atbash.decrypt(plaintext)
            #if the user has text
            elif choice2[0] == 't':
                plaintext = choice2[1]
                print atbash.decrypt(plaintext)
        else:
            print 'invalid input - exiting...'
            sys.exit()
    elif ciph == 'gm':
        genmono = GenMono()
        #introduce the cipher
        print 'the general monoalphabetic cipher is substitution cipher that'
        print 'uses a shuffled alphabet to encrypt plaintext\n'
        print 'options for general monoalphabetic\nencrypt - e\ndecrypt - d'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        if choice1 == 'e':
            #determine if the user is using a file or text
            choice2 = fileortext()
            #if the user has a file
            if choice2[0] == 'f':
                #retrieve the file from the returned list
                fil = choice2[1]
                #read the lines and convert it into a string as plaintext
                lines = fil.readlines()
                plaintext = ''.join(lines)
                print genmono.encrypt(plaintext)
            #if the user has text
            elif choice2[0] == 't':
                plaintext = choice2[1]
                print genmono.encrypt(plaintext)
        elif choice1 == 'd':
            #determine if the user is using a file or text
            choice2 = fileortext()
            #retrieve the shuffled alphabet key to decrypt the plaintext
            shuffledalphabet = raw_input("please enter the shuffled alphabet to decrypt\n(no spaces just letters): ")
            #if the user has a file
            if choice2[0] == 'f':
                #retrieve the file from the returned list
                fil = choice2[1]
                #read the lines and convert it into a string as plaintext
                lines = fil.readlines()
                plaintext = ''.join(lines)
                print genmono.decrypt(plaintext, shuffledalphabet)
            #if the user has text
            elif choice2[0] == 't':
                plaintext = choice2[1]
                print genmono.decrypt(plaintext, shuffledalphabet)
        else:
            print 'invalid input - exiting...'
            sys.exit()
    elif ciph == 'd':
        dig = DigraphSub()
        #introduce the cipher
        print 'the digraph cipher is a substitution cipher that uses a'
        print 'grid of digraphs(pairs of letters) to encrypt plaintext'
        print 'that has been split into digraphs\n'
        print 'options for digraph\nencrypt - e'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        #determine if the user is using a file or text
        choice2 = fileortext()
        #if the user has a file
        if choice2[0] == 'f':
            #retrieve the file from the returned list
            fil = choice2[1]
            #read the lines and convert it into a string as plaintext
            lines = fil.readlines()
            plaintext = ''.join(lines)
            print dig.encrypt(plaintext)
        #if the user has text
        elif choice2[0] == 't':
            plaintext = choice2[1]
            print dig.encrypt(plaintext)
    elif ciph == 'p':
        play = Playfair()
        #introduce the cipher
        print 'the playfair cipher is substitution cipher that uses'
        print 'digraphs(pairs of letters) and a keyword in the plaintext to encrypt'
        print 'plaintext. A grid is created that contains the keyword and then'
        print 'the rest of the alphabet randomized.\n'
        print 'options for playfair\nencrypt - e'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        #determine if the user is using a file or text
        choice2 = fileortext()
        #if the user has a file
        if choice2[0] == 'f':
            #retrieve the file from the returned list
            fil = choice2[1]
            #read the lines and convert it into a string as plaintext
            lines = fil.readlines()
            plaintext = ''.join(lines)
            keyword = getkeyword()
            print play.encrypt(keyword, plaintext)
        #if the user has text
        elif choice2[0] == 't':
            plaintext = choice2[1]
            keyword = getkeyword()
            print play.encrypt(keyword, plaintext)
    elif ciph == 'ho':
        homophonic = Homophonic()
        #introduce the cipher
        print 'the homophonic cipher is substitution cipher that uses a'
        print 'letter frequency and randomize numbers to encrypt plaintext,'
        print 'the encryption can use any letters or numbers but in this '
        print 'encryption we are using numbers\n'
        print 'options for railfence\nencrypt - e'
        #get input from the user for their goal
        choice1 = raw_input('enter choice: ')
        #determine if the user is using a file or text
        choice2 = fileortext()
        #if the user has a file
        if choice2[0] == 'f':
            #retrieve the file from the returned list
            fil = choice2[1]
            #read the lines and convert it into a string as plaintext
            lines = fil.readlines()
            plaintext = ''.join(lines)
            print homophonic.encrypt(plaintext)
        #if the user has text
        elif choice2[0] == 't':
            plaintext = choice2[1]
            print homophonic.encrypt(plaintext)
    elif ciph == 'ks':
        kama = KamaSutra()
    elif ciph == 's':
        swap = Swapping()
    elif ciph == 'v':
        vig = Vigenere()
    elif ciph == 'adfgvx':
        adf = ADFGVX()
    else:
        print 'invalid command - exiting...'
        sys.exit()

    #kama-sutra
    #print "ciphertext: " + kama.encrypt('hello my name is kevin')

    #swapping cipher
    #print "ciphertext: " + swap.encrypt('hello my name is kevin')

    #vigenere cipher
    #print "ciphertext: " + vig.encrypt('white', 'divert troops to east ridge')

    #digraph substitution
    #print "ciphertext: " + dig.encrypt('hello my name is kevin')

    #playfair cipher
    #print "ciphertext: " + play.encrypt('charles', 'meet me at hammersmith bridge tonight')

    #ADFGVX
    #print "ciphertext: " + adf.encrypt('mark', 'attack at 10pm')

def fileortext():
    choice = raw_input("file or text (f or t): ")
    if choice == 'f':
        filname = raw_input("enter file path: ")
        fil = open(filname, 'r')
        return ['f', fil]
    elif choice == 't':
        text = raw_input("enter text: ")
        return ['t', text]

def getshiftamount():
    shiftamount = raw_input("enter shift amount: ")
    return shiftamount

def getkeyword():
    keyword = raw_input("enter keyword: ")
    return keyword

#transposition cipher
class Railfence():
    def __init__(self):
        pass

    def encrypt(self, text, shiftnum, *args):
        self.big = []
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        n = int(shiftnum)
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

        newstr = ''
        #iterate through the lists in big
        for l in self.big:
            newstr = newstr + ''.join(l)
        return newstr

    #not finished
    def decrypt(self, text, shiftnum, *args):
        text = text.replace(' ', '')
        textlist = []
        for c in text:
            textlist.append(str(c))
        print textlist

        count = 0
        big = []
        for j in range(len(textlist)):
            templist = []
            for i in range(shiftnum):
                if j%(i+1):
                    pass

        return ''

#given text and shift amount
#the alphabet is shifted and enciphered text
#is created through mirrored indexes
class Caesar():
    def __init__(self):
        pass

    #encrypts text by a given shift amount
    def encrypt(self, text, shift, *args):
        #print "plaintext: " + text + " shift: " + str(shiftnum) + " spaces: " + str(spaces)
        #create the two alphabets
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #using deque to allow shifting of the lists
        newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        newalpha.rotate(-(int(shift)))
        text = text.lower()
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        enciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if alpha[i] == letter:
                    enciphered += newalpha[i]
        return enciphered

    def decrypt(self, text, shift, *args):
        #create the two alphabets
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #using deque to allow shifting of the lists
        newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        newalpha.rotate(-(int(shift)))
        text = text.lower()
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        deciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if newalpha[i] == letter:
                    deciphered += alpha[i]
        return deciphered

    #iterate through all possible shifted alphabets
    #to decipher text
    def iterdecrypt(self, text, *args):
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #using deque to allow shifting of the lists
        newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        for i in range(26):
            newalpha.rotate(-(int(1)))
            text = text.lower()
            text = text.replace(' ', '')
            text = text.replace('\n', '')
            deciphered = ""

            #iterate through the string of text
            for letter in text:
                #iterate through the alphabet list
                for j in range(len(alpha)):
                    if newalpha[j] == letter:
                        deciphered += alpha[j]
            print str(i+1) + " " + deciphered

#reversed alphabet
#mirrored indexes
class Atbash():
    def __init__(self):
        pass

    #encryption function for atbashen
    def encrypt(self, text, *args):
        enciphered = ""
        text = text.lower()
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #reverse the list
        self.newalpha = self.alpha[::-1]

        #iterate throught the plaintext letters
        for letter in text:
            #iterate throught the original alphabet
            for i in range(len(self.alpha)):
                #append the reversed letter
                if self.alpha[i] == letter:
                    enciphered += self.newalpha[i]
        return enciphered

    def decrypt(self, text, *args):
        deciphered = ""
        text = text.lower()
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        #reverse the list
        self.newalpha = self.alpha[::-1]
        #iterate throught the plaintext letters
        for letter in text:
            #iterate throught the original alphabet
            for i in range(len(self.newalpha)):
                #append the reversed letter
                if self.newalpha[i] == letter:
                    deciphered += self.alpha[i]
        return deciphered

#shuffles english alphabet with shuffle from the random library
class GenMono():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        shuffle(self.newalpha)
        enciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    enciphered += self.newalpha[i]
            if (letter == " "):
                enciphered += " "
        print 'shuffled alphabet: ' + ''.join(self.newalpha)
        return enciphered

    #able to decipher if shuffled alphabet is known
    def decrypt(self, text, alphabet, *args):
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        newalpha = list(alphabet)
        deciphered = ''
        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if newalpha[i] == letter:
                    deciphered += alpha[i]
            if (letter == " "):
                deciphered += " "

        return deciphered

#digraph is created from two shuffled alphabets
#depending on every pairs of two letters in the plaintext
#there is an enciphered pair
class DigraphSub():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.alpha1 = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        self.alpha2 = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'])

        self.random1 = randint(0, 26)
        self.random2 = randint(0, 26)

        self.alpha1.rotate(self.random1)
        self.alpha2.rotate(self.random2)

        self.listalpha1 = list(self.alpha1)
        self.listalpha2 = list(self.alpha2)
        self.dub = []

        for letter in self.listalpha1:
            templist = []
            for letter2 in self.listalpha2:
                templist.append((letter2, letter))
            self.dub.append(templist)

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

        if (len(text) % 2) != 0:
            tempstr = tempstr + 'x'
        dig = tempstr
        dig = dig.strip()
        dig = dig.split(' ')
        enciphered = ''
        for di in dig:
            index1 = self.alpha.index(di[0])
            index2 = self.alpha.index(di[1])
            enciphered = str(enciphered) + ''.join(self.dub[index2][index1]) + ' '
        enciphered = enciphered.replace(' ', '')
        return enciphered

#given keyword and text
class Playfair():
    def __init__(self):
        pass

    def encrypt(self, keyword, text, *args):
        #grid
        self.comb = []
        #alphabet without j
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        newalpha = []
        for letter in keyword:
            for i in self.alpha:
                if letter == i:
                    self.alpha.remove(i)

        keylist = list(keyword)
        shuffle(self.alpha)
        self.comb = keylist + self.alpha

        #create di text
        text = text.replace(" ", "")
        text = text.strip()
        tempstr = ''

        count = 0
        yes = 0
        for letter in range(len(text)):
            if count == 1:
                tempstr = tempstr + text[letter] + ' '
                count = 0
            else:
                try:
                    #check for index error
                    text[letter+1]
                    yes = 1
                except Exception as e:
                    yes = 0
                if yes and text[letter] == text[letter+1]:
                    tempstr = tempstr + text[letter] + 'x '
                    count = 0
                else:
                    tempstr = tempstr + text[letter]
                    count += 1

        check = tempstr.replace(' ', '')

        if (len(check) % 2) != 0:
            tempstr = tempstr + 'x'
        print tempstr
        #end creating digraphed text

        final = ''
        templist = []
        newlist = []
        ditext = tempstr
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

        for i in dilist:
            if i == '':
                dilist.remove(i)

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
            #print 'newlist: ' + str(newlist)
            for inner in range(len(newlist)):
                inn = newlist[inner]
                if di[0] == 'j':
                    di = 'i' + di[1]
                elif di[1] == 'j':
                    di = di[0] + 'i'
                for i in range(len(inn)):
                    if di[0] == inn[i]:
                        loc1.append(inner)
                        loc1.append(i)
                    if di[1] == inn[i]:
                        loc2.append(inner)
                        loc2.append(i)
            final += newlist[loc1[0]][loc2[1]]
            final += newlist[loc2[0]][loc1[1]] + ' '

        final = final.replace(' ', '')
        return final

#enciphers text with numbers depending on the frequency
#of the letter in the plaintext
class Homophonic():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
        temp = range(33, 65) + range(91, 97) + range(123, 127)
        self.symbols = []
        for i in temp:
            self.symbols.append(chr(i))
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.big = []
        self.bigdict = {}
        #normal frequency distributed list
        numlist = [8, 2, 3, 4, 12, 2, 2, 6, 6, 1, 1, 4, 2, 6, 7,
                    2, 1, 6, 6, 9, 3, 1, 2, 1, 2, 1]
        #list from 0 to 99
        listrange = range(0, 100)
        text = text.lower()
        text = text.replace(' ', '')

        for i in numlist:
            smol = []
            for k in range(i):
                num = choice(listrange)
                listrange.remove(num)
                smol.append(num)
            self.big.append(smol)
        for i in range(len(self.alpha)):
            self.bigdict[self.alpha[i]] = self.big[i]
        encrypted = ""
        for letter in text:
            if letter == " " or letter in self.symbols:
                pass
            else:
                temp = self.bigdict.get(letter)
                if temp == None:
                    pass
                else:
                    encrypted += str(choice(temp)) + ' '

        return encrypted

    #not sure if this is implementable
    def decrypt(self):
        pass

#pairs in english alphabet
class KamaSutra():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
        self.newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        self.cipheralpha = []
        #set up pairs
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

        print self.cipheralpha

        enciphered = ""
        for i in text:
            for k in self.cipheralpha:
                if i in k:
                    if k[0] == i:
                        enciphered += k[1]
                    else:
                        enciphered += k[0]

            if (i == " "):
                enciphered += " "

        return enciphered

    def decrypt(self, *args):
        pass

#two shuffled alphabets
class Swapping():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
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
        print self.alpha
        print self.newalpha1
        print self.newalpha2

        enciphered = ""
        count = 0
        for letter in text:
            for i in range(len(self.alpha)):
                if self.alpha[i] == letter:
                    if count == 0:
                        enciphered += self.newalpha1[i]
                        count = 1
                    else:
                        enciphered += self.newalpha2[i]
                        count = 0
            if (letter == " "):
                enciphered += " "

        return enciphered

    def decrypt(self, *args):
        pass

#given a keyword and text an encrypted form of the text is created
#a grid is created of all possible shifted english alphabets
class Vigenere():
    def __init__(self):
        pass

    def encrypt(self, keyword, text, *args):
        self.firstkeyword = ''
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

        #list with all possible shifted alphabets
        self.templist = []

        #remove spaces from text
        text = text.replace(' ', '')

        #loop through alphabet
        #populate templist
        for i in range(len(self.alpha)):
            tempalpha = deque(self.alpha)
            tempalpha.rotate(len(self.alpha) - (i+1))
            self.templist.append(list(tempalpha))

        enciphered = ''
        #keyword repeated to equal length of text
        repeatedkeyword = ''
        #repeat the keyword
        tempkeyword = ''
        times = len(text) / len(keyword)
        for i in range(times):
            tempkeyword += keyword
        leftover = len(text) - len(tempkeyword)
        tempkeyword += keyword[:leftover]
        repeatedkeyword = tempkeyword


        indexes = []
        #loop through the original keyword
        for letter in keyword:
            #loop through all of the shifted alphabets
            for i in range(len(self.templist)):
                alph = self.templist[i]
                #if the first letter of the shifted alphabet
                #equals the letter in the keyword
                if alph[0] == letter:
                    #if the index does not already exist
                    #in the index list then add the index
                    #to the list
                    if i not in indexes:
                        indexes.append(i)
        #sort the index list by integer
        indexes = sorted(indexes, key=int)

        #iterate through the given text
        for j in range(len(text)):
            #iterate through the index list
            for index in indexes:
                #if the first letter of the shifted alphabet
                #equals the letter in the repeated keyword
                if self.templist[index][0] == repeatedkeyword[j]:
                    #append the letter in the same row as the shifted alphabet
                    enciphered += self.templist[index][self.alpha.index(text[j])]

        return enciphered

#user gives a keyword and text
#keyword is transposed
#text is changed into two letter pairs
#based on shuffled adfgvx grid the encipher ditext is created
#then transposed based on keyword
class ADFGVX():
    def __init__(self):
        pass

    def encrypt(self, keyword, text, *args):
        self.alphanum = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                '7', '8', '9']
        self.a = ['a', 'd', 'f', 'g', 'v', 'x']
        #grid
        self.dub = []
        rand = randint(1, len(keyword))
        newstrlist = deque(list(keyword))
        newstrlist.rotate(rand)
        keyword2 = ''.join(list(newstrlist))

        #create the grid
        for i in self.a:
            templist = []
            for a in self.a:
                rand = randint(0, len(self.alphanum))
                templist.append(self.alphanum[rand-1])
                self.alphanum.remove(self.alphanum[rand-1])
            self.dub.append(templist)

        #grid created above

        #create ditext
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
        #ditext created

        #form keyword grid
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

        #keyword1text.text
        grid = '\n'.join(templist)
        #formed keyword grid

        #transpose keyword grid
        listgrid = grid.split('\n')
        indexes = []
        newlistgrid = []
        for i in range(len(keyword)):
            for letter in range(len(keyword2)):
                if keyword2[letter] == keyword[i]:
                    indexes.append(letter)
                    break
        for j in listgrid:
            if j == '':
                pass
            else:
                tempnew = ''
                for n in indexes:
                    tempnew += j[n]
                newlistgrid.append(tempnew)
        newnewgrid = '\n'.join(newlistgrid)
        #end transpose keyword grid

        #final stage
        temptext = newnewgrid.split('\n')
        final = ''
        length = len(keyword)
        count = length
        for i in range(length):
            for group in temptext:
                final += group[length - count]
            count = count - 1

        return final

if __name__ == '__main__':
    main()
