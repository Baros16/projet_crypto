import bibliotheque as b


ve = int(input("Appuyer sur 1 pour crypter et sur 2 pour decrypter"))
if ve == 1:
    text = input("entre le message a coder")
    cle = input(" entrer la cle")
    result = b.crypter_message(text, cle)
    print(f"{result}")
else:
    text = input("entre le message a coder")
    cle = input(" entrer la cle")
    result = b.decrypter_message(text, cle)
    print(f"{result}")
