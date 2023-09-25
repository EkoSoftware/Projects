import os
clear = "cls" if os.name == "nt" else "clear"

# T9 skrivsätt
def my_encode(string):
    string = string.lower()
    tempstring = ""

    def get_key(char):
        for key, value in t9_alphabet.items():
            if value == char: 
                return key
        return None

    t9_alphabet = {
        '1': '.', '11': ',', '111': '!', '1111':'?', '11111': "'",
        '2': 'a', '22': 'b', '222': 'c', '2222': 'å', '22222': 'ä', '222222': 'ö',
        '3': 'd', '33': 'e', '333': 'f',
        '4': 'g', '44': 'h', '444': 'i',
        '5': 'j', '55': 'k', '555': 'l',
        '6': 'm', '66': 'n', '666': 'o', 
        '7': 'p', '77': 'q', '777': 'r', '7777': 's',
        '8': 't', '88': 'u', '888': 'v',
        '9': 'w', '99': 'x', '999': 'y', '9999': 'z',
        '0': ' '}

    for char in string:
        tempstring += get_key(char)+'|'
    return tempstring



def my_decode(string):

    string = str(string).split('|')
    #string = str(string).split('0')
    print(string)
    tempstring = ""
    t9_alphabet = {
        '1': '.', '11': ',', '111': '!', '1111':'?', '11111': "'",
        '2': 'a', '22': 'b', '222': 'c', '2222': 'å', '22222': 'ä', '222222': 'ö',
        '3': 'd', '33': 'e', '333': 'f',
        '4': 'g', '44': 'h', '444': 'i',
        '5': 'j', '55': 'k', '555': 'l',
        '6': 'm', '66': 'n', '666': 'o',
        '7': 'p', '77': 'q', '777': 'r', '7777': 's',
        '8': 't', '88': 'u', '888': 'v',
        '9': 'w', '99': 'x', '999': 'y', '9999': 'z',
        '0': ' ',
        '|': ''}
    
    def get_value(char):
        
        for key, value in t9_alphabet.items():
            if key == char:
                return value
        return ''
    
    
    for char in string: tempstring += get_value(char)
    return tempstring



while True:
    os.system(clear)
    choice = input("1. Encode\n2. Decode\nWhat would you like to do?\n>")
    if choice == "1" or choice.title() == "Encode":
        user = input("Message to encode:\n> ")
        print(f"Your encoded message\n{my_encode(user)}")
    elif choice == "2" or choice.title() == "Decode":
        user = input("Message to decode:\n> ")
        print(f"Your decoded message\n{my_decode(user)}")
    input("'q' to exit else Enter to continue\n >")
        
