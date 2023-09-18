import os

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
        '2': 'a', '22': 'b', '222': 'c',
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


print(my_encode("Simon"))

def my_decode(string):

    string = str(string).split('|')
    #string = str(string).split('0')
    print(string)
    tempstring = ""
    t9_alphabet = {
        '1': '.', '11': ',', '111': '!', '1111':'?', '11111': "'",
        '2': 'a', '22': 'b', '222': 'c',
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

print(my_decode("7777|444|6|666|66|"))

while True:
    if os.name == "nt": 
        os.system("cls")
    else:
        os.system("clear")
    user = input("Message to encode\n> ")
    print(f"Your encoded message\n{my_encode(user)}")