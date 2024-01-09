import time

from lib.handler.createPDF import PdfHandle

class EDocuments:
    def __init__(self, browser, testCaseID, allPageFields, casePageSource):
        self.browser = browser
        self.testCaseID = testCaseID
        self.allPageFields = allPageFields
        self.casePageSource = casePageSource
       
        # Arrays
        self.allFields = []
        self.documentNames = []
        self.fileLinks = []

        self.findAllFields()
        self.getDocuments()
        self.startPdfDownloads()

    def findAllFields(self):
        # Getting all fields present on the page
        for field in self.allPageFields:
            try:
                self.allFields.append(field.text)
            except:
                continue

    def getDocuments(self):
        # Go through all fields and check if it has an onlick.
        for documentName in self.allFields:
            try:
                eDocument = self.browser.find_element("link text", documentName).get_attribute("onclick").split("'")[1]
                self.documentNames.append(documentName)
                self.fileLinks.append(eDocument)
            except:
                continue

    def startPdfDownloads(self):
        # Create a directory with pdfs -- if there are any pdfs
        if len(self.fileLinks) >= 1:
            fileHandle = PdfHandle()
            fileHandle.createDir(self.testCaseID)
            fileHandle.downloadCasePage(self.casePageSource,self.testCaseID)

            for i in range(len(self.fileLinks)):
                fileHandle.downloadPDF(self.fileLinks[i], self.documentNames[i])
            
            self.browser.close()

        else:
            print("No files detected...")



