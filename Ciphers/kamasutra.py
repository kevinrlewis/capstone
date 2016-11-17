from random import shuffle


newalpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z']

cipheralpha = []

def main():
    temp = kamaencrypt("hello my name is kevin", 1)
    print temp
    print kamadecrypt(temp, 1)

def kamaencrypt(word, spaces):
    global newalpha

    shuffle(newalpha)

    enciphered = ""

    j = 0
    global cipheralpha
    temp = []
    count = 0
    for i in newalpha:
        if j < 1:
            temp.append(i)
            j += 1
        else:
            temp.append(i)
            cipheralpha.append(temp)
            j = 0
            temp = []
        count += 1

    for i in word:
        for k in cipheralpha:
            if i in k:
                if k[0] == i:
                    enciphered += k[1]
                else:
                    enciphered += k[0]

        if (i == " ") and spaces:
            enciphered += " "

    return enciphered


def kamadecrypt(word, spaces):
    deciphered = ""

    for i in word:
        for k in cipheralpha:
            if i in k:
                if k[0] == i:
                    deciphered += k[1]
                else:
                    deciphered += k[0]

        if (i == " ") and spaces:
            deciphered += " "

    return deciphered


if __name__ == "__main__":
    main()
