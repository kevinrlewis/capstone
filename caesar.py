from collections import deque

#runs the two functions with test parameters
def main():
    print caesarEncrypt(2, "hello my name is kevin", 1)
    print caesarDecrypt(2, "jgnnq oa pcog ku mgxkp", 1)

#decrypts a given caesar shift encrypted text by the shift
#amount provided
def caesarDecrypt(shift, text, spaces):
    alpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'])

    newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'])

    text = text.lower()
    #rotate the list by the given shift amount
    newalpha.rotate(-(shift))
    deciphered = ""

    #iterate through the letters in the string
    for letter in text:
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


#encrypts text by a given shift amount
def caesarEncrypt(shift, text, spaces):
    alpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'])

    newalpha = deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'])

    text = text.lower()
    #shift the alphabet by the given amount
    newalpha.rotate(-(shift))
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


if __name__ == "__main__":
    main()
