from time import localtime
from myEncryption import myGetEncryptionKey


# Creates a text file for storing keys which are unique based on the day of the month
def myGenerateKeys(path='myKeys.txt'):    
    try:
        open(path, 'x').close()
    except FileExistsError:
        while True:
            uinput = input("You are about to overwrite existing keys\nDo you want to continue? Yes/No\n>").strip().title()
            match uinput[0]:
                case "Y": break
                case "N": return print('Key generation was cancelled by the user.')
                case ___: continue
                
    with open(path, 'w') as file:
        for day in range(1,32):
            key = myGetEncryptionKey(1024)
            file.write(f'{key}\n')
            
            
    return print(f'Keys written to path "{path}"')
            
# Gets the daily key
def myReadKeys(path='myKeys.txt'):
    try:open(path,'r').close()
    except FileNotFoundError:
        myGenerateKeys()
        
    year,month,day,hour,minute,second,_,_,_ = localtime()
    
    with open(path, 'r') as file:
        lines = file.readlines()
        today = lines[day-1]
        key = today.split()[-1]
        return key
    
# If for some reason you want to make new keys.
if __name__ == '__main__':
    myGenerateKeys()
    print(f'Todays key:\n{myReadKeys()}')