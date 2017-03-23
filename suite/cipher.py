import sys
import os
from collections import deque
from random import shuffle
from random import randint
from random import choice
from fractions import gcd

#arg1 = cipher type (r,c,a,gm,di,p,h,ks,s,v,adfgvx,aes)
#arg2 = encrypt or decrypt
#arg3 = file or text (file or text)
#
def main():
    print sys.argv
    railfence = Railfence()
    caesar = Caesar()
    atbash = Atbash()
    genmono = GenMono()
    homophonic = Homophonic()
    kama = KamaSutra()
    swap = Swapping()
    vig = Vigenere()
    #print "ciphertext: " + railfence.encrypt('hello', 2)
    #print "ciphertext: " + caesar.encrypt('hello my name is kevin', 2, True)
    #print "ciphertext: " + atbash.encrypt('hello my name is kevin', True)
    #print "ciphertext: " + genmono.encrypt('hello my name is kevin')
    #print "ciphertext: " + homophonic.encrypt('hello my name is kevin')
    #print "ciphertext: " + kama.encrypt('hello my name is kevin')
    #print "ciphertext: " + swap.encrypt('hello my name is kevin')
    print "ciphertext: " + vig.encrypt('white', 'divert troops to east ridge')
class Railfence():
    def __init__(self):
        pass

    def encrypt(self, text, shiftnum, *args):
        print "plaintext: " + text + " shift: " + str(shiftnum)

        self.big = []
        text = text.replace(' ', '')
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

    def decrypt(self, text, shiftnum, *args):
        pass

#given text and shift amount
#the alphabet is shifted and enciphered text
#is created through mirrored indexes
class Caesar():
    def __init__(self):
        pass

    #encrypts text by a given shift amount
    def encrypt(self, text, shift, spaces, *args):
        print "plaintext: " + text + " shift: " + str(shiftnum) + " spaces: " + str(spaces)
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
        enciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if alpha[i] == letter:
                    enciphered += newalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "
        return enciphered

    def decrypt(self, know, shift, text, spaces, *args):
        pass

#reversed alphabet
#mirrored indexes
class Atbash():
    def __init__(self):
        pass

    #encryption function for atbashen
    def encrypt(self, text, spaces, *args):
        print "plaintext: " + text + " spaces: " + str(spaces)
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
            if (letter == " ") and spaces:
                enciphered += " "
        return enciphered

    def decrypt(self, text, *args):
        pass

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

        return enciphered

    def decrypt(self, text, *args):
        pass

class DigraphSub():
    def __init__(self):
        pass

class Playfair():
    def __init__(self):
        pass

#enciphers text with numbers depending on the frequency
#of the letter in the plaintext
class Homophonic():
    def __init__(self):
        pass

    def encrypt(self, text, *args):
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
            if letter == " ":
                pass
            else:
                temp = self.bigdict.get(letter)
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

class ADFGVX():
    def __init__(self):
        pass

class AES():
    def __init__(self):
        pass

if __name__ == '__main__':
    main()
