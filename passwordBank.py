from cryptography.fernet import Fernet

#Global options
ADDENTRY = 1
VIEW = 2
LOAD = 3
SAVE = 4
QUIT = 5



def main():
    #Gets users choice, and calls apropriate function
    
    currentPassDict = loadFromFile()

    userChoice = 0
    running = True
    while running:
        userChoice = getUserChoice()
        
        if userChoice == ADDENTRY:
            addEntry(currentPassDict)
        if userChoice == LOAD:
            loadFromFile()
        if userChoice == SAVE:
            saveToFile(currentPassDict)
        if userChoice == VIEW:
            viewDatabase(currentPassDict)
        if userChoice == QUIT:
            saveToFile(currentPassDict)
            encryptFile('key.key', 'passList.txt')
            running = False

def getUserChoice():
    #prints users choices and returns the users choice
    print()
    userChoice = 0
    print()
    print('Pick a choice from below: ')
    print("__________________________")
    print("1: Add an entry to the database")
    print("2: View the database")
    print("3: Load an existing databse")
    print("4: Save to file")
    print("5: Quit this program")
    
    while userChoice > QUIT or userChoice < ADDENTRY:
        userChoice = int(input("Enter your Choice: "))
        
    return userChoice

def viewDatabase(passDict):
    #Prints the entire database
    print()
    for key in passDict:
        print("For: ", key)
        print("username and password:", passDict[key])
        print()

def addEntry(passDict):
    #Allows the user to add an entry to the database
    print()
    userName = input("Enter the username: ")
    password = input("Enter the password: ")
    usedFor = input("Where is this login used: ")
    
    userAndPass = [userName, password]

    passDict[usedFor] = userAndPass
    return passDict
    
def saveToFile(DictToSave):
    #Saves DictToSave to passlist.txt
    print()
    print("WARNING: THIS WILL OVERWRITE EXITING FILE")
    print("ENSURE THE CURRENT LIST IS UP TO DATE BEFORE SAVING")
    procceed = False
    askToContinue = input("Would you like to continue? (y/[n])")
    if askToContinue.lower() == 'y':
        procceed = True
    else:
        print("Invalid input, aborting save")
        return None
    
    if procceed == True:
        with open('passList.txt', 'w') as passFile:
            passFile.write(str(DictToSave))
            
            
            
def loadFromFile():
    #loads passList.txt
    print()
    print("Loading current passlist.txt")
       
    decryptFile('key.key', 'passList.txt')
    
    with open('passList.txt', 'r') as passFile:
        data = passFile.read()
        return eval(data)

def generateKeyFile():
    key = Fernet.generate_key()
    with open('key.key', 'wb+') as keyFile:
        keyFile.write(key)
        
def loadKey(keyFile):
    with open(keyFile, 'rb+') as keyFile:
        key = keyFile.read()
    return key

def encrypt(keyFile, string):
    key = loadKey(keyFile)
    f = Fernet(key)
    
    string = string.encode('UTF-8')
    token = f.encrypt(string)
    
    return token

def decrypt(keyFile, token):
    key = loadKey(keyFile)
    f = Fernet(key)
    
    string = f.decrypt(token)
    string = string[2:-1]
    
    return string

def encryptFile(keyFile, file):
    with open(file, 'rb+') as myFile:
        secret = str(myFile.read())
        token = encrypt(keyFile, secret)
        
        myFile.truncate(0)
        myFile.seek(0)
        myFile.write(token)
        
def decryptFile(keyFile, file):
    with open(file, 'rb+') as myFile:
        token = myFile.read()
        secret = decrypt(keyFile, token)
        secret = secret.decode('UTF-8')
    
    with open(file, 'w') as myFile:
        myFile.write(str(secret))

main()