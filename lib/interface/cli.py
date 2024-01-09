from termcolor import colored 
from lib.handler.readIdsFile import readIds
from lib.handler.automatedCases import automatedCases
from datetime import datetime
import time
import sys


welcomeSignature = r"""
               _                        _           _    _____                    
    /\        | |                      | |         | |  / ____|                   
   /  \  _   _| |_ ___  _ __ ___   __ _| |_ ___  __| | | |     __ _ ___  ___  ___ 
  / /\ \| | | | __/ _ \| '_ ` _ \ / _` | __/ _ \/ _` | | |    / _` / __|/ _ \/ __|
 / ____ \ |_| | || (_) | | | | | | (_| | ||  __/ (_| | | |___| (_| \__ \  __/\__ \
/_/    \_\__,_|\__\___/|_| |_| |_|\__,_|\__\___|\__,_|  \_____\__,_|___/\___||___/
                                                                                  
"""
welcomeSignature = colored(welcomeSignature,"blue")

class App():
    def __init__(self) -> None:
        self.startUp()

    def stylePrintStatus(self, line):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S") 
        
        the_style = "[" + str(colored(current_time,'green')) + "] " + colored(line,'white')
        print (the_style)
        
    def startUp(self):
        print(welcomeSignature)
        self.checkIdFile()

    def checkIdFile(self):
        self.stylePrintStatus("Checkings Case Id File ...")
        caseIdsList = readIds()
        time.sleep(2.5)
        if len(caseIdsList) > 0:
            self.stylePrintStatus("Imported IDs ...")
            self.printIds(caseIdsList)
        else:
            self.stylePrintStatus("No ids found ...")

    def printIds(self,ids):
        self.stylePrintStatus("Cases found in file[%s]" % (len(ids)))
        time.sleep(1.5)
        self.stylePrintStatus("Case IDS: [First 5]")
        try:
            for i in range(5):
                time.sleep(0.5)
                self.stylePrintStatus(ids[i])  
        except IndexError:
            pass

        self.printMenu()  

    def printMenu(self):    
        self.stylePrintStatus("Select one of the options below:")
        self.stylePrintStatus("1. Start")
        self.stylePrintStatus("2. Quit")

        userInput = input("Response: ")
        userInput = int(userInput.replace(" ",""))

        self.startApplication(userInput)


    def startApplication(self, userInput):
        try:
            if (userInput == 1):
                automatedCases()
            elif (userInput == 2):
                self.stylePrintStatus("Quitting application ...")
                time.sleep(2.5)
                sys.exit()
            else: 
                self.printMenu()

        except ValueError:
            self.printMenu()

