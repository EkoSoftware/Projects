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

def myCipher(string, key):
    for i, char in enumerate(string):
        match char:
            case 'å': char.replace('å','aoaoaoao')
            case 'ä': char.replace('ä','aeaeaeae')
            case 'ö': char.replace('ö','oeoeoeoe')
    
    length = len(key)
    keyBytes = key.encode('utf-8')
    strBytes = string.encode('utf-8')
    
    encryption = []
    for i, byte in enumerate(strBytes):
        keyByte = keyBytes[i % length]
        cryptedByte = (byte + keyByte) % 256
        encryption.append(cryptedByte)
    
    return bytes(encryption)
    
def myDecipher(string, key):
    length = len(key)
    keyBytes = key.encode('utf-8')
    strBytes = string

    decryption = []
    for i, byte in enumerate(strBytes):
        keyByte = keyBytes[i % length]
        decryptedByte = (byte - keyByte) % 256
        decryption.append(decryptedByte)

    decrypted_String = [chr(x) for x in decryption]
    text = ''.join(decrypted_String)
    
    for i, char in enumerate(string):
        match char:
            case 'aoaoaoao': char.replace('aoaoaoao','å')
            case 'aeaeaeae': char.replace('aeaeaeae','ä')
            case 'oeoeoeoe': char.replace('oeoeoeoe','ö')
    
    return text

if __name__ == '__main__':
    from myEncryption import myGetEncryptionKey
    key = myGetEncryptionKey(1024)
    print(f'key : {key}')
    
    while True:
        uinput = input("Message to encrypt\n>")
        enc = myCipher(uinput, key)
        print(f'Encrypted message:\n{enc}')
        dec = myDecipher(enc, key)
        print(f'Deciphered message:\n{dec}')
        
        #uinput = input("Message to decrypt\n>")
    

    

