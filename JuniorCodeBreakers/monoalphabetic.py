from random import shuffle

newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z']

def main():
    temp = monoencrypt("hello my name is kevin", 1)
    print temp
    print monodecrypt(temp, 1)

def monoencrypt(word, spaces):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    global newalpha

    shuffle(newalpha)

    enciphered = ""

    #iterate through the string of text
    for letter in word:
        #iterate through the alphabet list
        for i in range(len(alpha)):
            if alpha[i] == letter:
                enciphered += newalpha[i]
        if (letter == " ") and spaces:
            enciphered += " "

    return enciphered

def monodecrypt(word, spaces):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    deciphered = ""

    #iterate through the letters in the string
    for letter in word:
        #iterate through the shifted alphabet
        for i in range(len(newalpha)):
            #if the letter matches the index in the shifted alphabet
            #add that letter to the return string
            if newalpha[i] == letter:
                deciphered += alpha[i]
        #add spaces
        if (letter == " ") and spaces:
            deciphered += " "

    return deciphered



if __name__ == "__main__":
    main()
