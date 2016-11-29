def main():
    #print "enciphered: ", atbashen("jnyxxvgrnatre", 1)
    print "deciphered: ", atbashde("DLIGSTZRMKRKVXVIGZRMGB", 1)

def atbashen(text, spaces):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    newalpha = alpha[::-1]
    enciphered = ""
    text = text.lower()

    for letter in text:
        for i in range(len(alpha)):
            if alpha[i] == letter:
                enciphered += newalpha[i]
        if (letter == " ") and spaces:
            enciphered += " "

    return enciphered




def atbashde(text, spaces):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

    newalpha = alpha[::-1]
    deciphered = ""
    text = text.lower()

    for letter in text:
        for i in range(len(newalpha)):
            if newalpha[i] == letter:
                deciphered += alpha[i]
        if (letter == " ") and spaces:
            deciphered += " "

    return deciphered




if __name__ == "__main__":
    main()
