import random


# Generate keys
def myGetEncryptionKey(cut):
    length = 256
    def generatePassword(length):
        # Randomizer
        def myScramble():
            lower = "qwertyuiopasdfghjklzxcvbnm"
            upper = lower.upper()
            
            choices = True, False
            up = random.choice(choices)
            low = random.choice(choices)

            allchars = ""
            while True:

                up = random.choice(choices)
                low = random.choice(choices)
                
                if up: allchars += upper
                if low: allchars += lower
                
                if not any([up, low]):
                    continue
                while len(allchars) < 32:
                    allchars += myScramble()

                return allchars

        # Keypart
        key = ''
        while len(key) < length:
            for x in range(random.randint(1,5),random.randint(16,30)):
                samples = []
                password = "".join(random.sample(myScramble(),32))
                samples.append(password)

            key += random.choice(samples)

        return key[:length]
    
    # Final Key
    key = ''
    while len(key) < length:
        scramble = generatePassword(random.randint(1,(length//random.randint(3,15) // random.randint(2,6))))
        key += scramble
    return key[:cut]

def myCipher(text, key, salt=0):
    encryption = ''
    while len(key) < len(text):
        key += key
    key = key[:len(text)]
    #print(f'Key adjusted for message: "{key}"')
    
    for i, char in enumerate(text):
        value = ord(char) + ord(key[i])
        if salt: value += salt
        encryption += chr(value)
    
    return encryption

def myDecipher(text, key, salt=0):
    decryption = ''
    while len(key) < len(text):
        key += key
    key = key[:len(text)]
    
    for i, char in enumerate(text):
        value = ord(char) - ord(key[i])
        if salt: value -= salt
        decryption += chr(value)

    return decryption

if __name__ == '__main__':
    from myEncryption import myGetEncryptionKey
    key = myGetEncryptionKey(1024)
    print(f'key : {key}')
    
    while True:
        uinput = input("Message to encrypt\n>")
        enc = myCipher(uinput, key, 1337)
        print(f'Encrypted message:\n{enc}')
        dec = myDecipher(enc, key, 1337)
        print(f'Deciphered message:\n{dec}')
        
        #uinput = input("Message to decrypt\n>")
    

    

