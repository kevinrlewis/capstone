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
#arg1 = cipher type (r,c,a,gm,di,p,h,ks,s,v,adfgvx)
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
    dig = DigraphSub()
    play = Playfair()
    adf = ADFGVX()

    #railfence
    #print "ciphertext: " + railfence.encrypt('kevin', 2)
    #print "deciphered: " + railfence.decrypt('kvnei', 2)

    """caesar done"""
    #caesar
    #print "ciphertext: " + caesar.encrypt('hello my name is kevin', 2, True)
    #print "deciphered: " + caesar.decrypt(2, "jgnnq oa pcog ku mgxkp")
    #caesar.iterdecrypt('pmttw ug vium qa smdqv')

    """atbash done"""
    #atbash
    #print "ciphertext: " + atbash.encrypt('hello my name is kevin')
    #print "plaintext deciphered: " + atbash.decrypt('svool nb mznv rh pverm')

    """genmono done"""
    #general monoalphabetic
    #print "ciphertext: " + genmono.encrypt('hello my name is kevin')
    print 'deciphered: ' + genmono.decrypt('emvvg zi kazm wf rmqwk', 'anjumxoewcrvzkgtlsfpyqbhid')

    #homophonic
    #print "ciphertext: " + homophonic.encrypt('hello my name is kevin')

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

#transposition cipher
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
        print "textlist: " + str(textlist)
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

        print "big: " + str(self.big)

        newstr = ''
        #iterate through the lists in big
        for l in self.big:
            newstr = newstr + ''.join(l)
        return newstr

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
    def encrypt(self, text, shift, spaces, *args):
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
        enciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if alpha[i] == letter:
                    enciphered += newalpha[i]
            if (letter == " ") and spaces:
                enciphered += " "
        k.write(str(shift))
        return enciphered

    def decrypt(self, shift, text, *args):
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
        deciphered = ""

        #iterate through the string of text
        for letter in text:
            #iterate through the alphabet list
            for i in range(len(alpha)):
                if newalpha[i] == letter:
                    deciphered += alpha[i]
            if (letter == " "):
                deciphered += " "
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
            deciphered = ""

            #iterate through the string of text
            for letter in text:
                #iterate through the alphabet list
                for i in range(len(alpha)):
                    if newalpha[i] == letter:
                        deciphered += alpha[i]
                if (letter == " "):
                    deciphered += " "
            print deciphered

#reversed alphabet
#mirrored indexes
class Atbash():
    def __init__(self):
        pass

    #encryption function for atbashen
    def encrypt(self, text, *args):
        print "plaintext: " + text
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
            if (letter == " "):
                enciphered += " "
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
            if (letter == " "):
                deciphered += " "
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
        k.write(''.join(self.newalpha))
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

        final = final.replace(' ', '')
        return final

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
        length = len(keyword) - 1
        count = length
        for i in range(length):
            for group in temptext:
                final += group[length - count]
            count = count - 1

        return final

if __name__ == '__main__':
    main()
