from random import shuffle

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z']

newalpha1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z']

newalpha2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z']


def main():
    temp = swapencrypt("hello my name is kevin", 1)
    print temp
    print swapdecrypt(temp, 1)


def swapencrypt(word, spaces):
    global alpha

    randomize()

    enciphered = ""

    count = 0
    for letter in word:
        for i in range(len(alpha)):
            if alpha[i] == letter:
                if count == 0:
                    enciphered += newalpha1[i]
                    count = 1
                else:
                    enciphered += newalpha2[i]
                    count = 0
        if (letter == " ") and spaces:
            enciphered += " "

    return enciphered

def swapdecrypt(word, spaces):

    deciphered = ""

    count = 0
    for letter in word:
        if count == 0:
            for i in range(len(newalpha1)):
                if letter == newalpha1[i]:
                    deciphered += alpha[i]
                    count = 1
            if (letter == " ") and spaces:
                deciphered += " "
        else:
            for i in range(len(newalpha2)):
                if letter == newalpha2[i]:
                    deciphered += alpha[i]
                    count = 0
            if (letter == " ") and spaces:
                deciphered += " "


    return deciphered



def randomize():
    global newalpha1
    global newalpha2

    #randomize the 2 alphabets
    shuffle(newalpha1)
    shuffle(newalpha2)

if __name__ == "__main__":
    main()
