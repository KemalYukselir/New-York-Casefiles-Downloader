import requests
import shutil
import codecs

# importing os module
import os

class PdfHandle:
    def __init__(self) -> None:
        self.PATH = ""
        self.directory = ""
        self.cwd = ""

        # This is needed for duplicate pdf files
        self.duplicateFileCount = 0

    def createDir(self, caseId):
        try:
            self.cwd = os.getcwd() 
            caseId = caseId.replace("/","")
            print("Current Directory is: ", self.cwd)

            # Directory
            self.directory = "Case " + str(caseId)

            # Parent Directory path
            parent_dir = self.cwd

            # Path
            self.PATH = os.path.join(parent_dir, self.directory)

            # First remove the path
            try:
                shutil.rmtree(self.PATH)
            except:
                pass

            # Create the directory
            os.mkdir(self.PATH)
            print("Directory '% s' created" % self.directory)
        except FileExistsError:
            pass

    def downloadCasePage(self, pageSource, id):
        # then generate full path using os lib
        full_path = os.path.join(self.PATH, id + ".html")

        #open file in write mode with encoding
        f = codecs.open(full_path, "wb", "utf−8")

        #write page source content to file
        f.write(pageSource)


    def checkDuplicatePdfFiles(self, pdfName):
        duplicateCount = 0

        while True:
            
            if duplicateCount == 0:
                PATH = self.cwd + "/" + self.directory + "/" + pdfName + ".pdf"
            else:
                PATH = self.cwd + "/" + self.directory + "/" + pdfName + ' (%s)' % str(duplicateCount) + ".pdf" 

            if (os.path.isfile(PATH)):
                duplicateCount += 1
            else:
                break
            
 
        if duplicateCount > 0:
            return pdfName + " (%s)" % duplicateCount
        else:
            return pdfName

    # Downloading the pdf files
    def downloadPDF(self, url, pdfName):
        pdfName = pdfName.replace("/","").replace(":","")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }


        response = requests.get(url, headers=headers)

        # Checking duplicate files
        pdfNameFinal = self.checkDuplicatePdfFiles(pdfName)
        print("Final pdf name:" + pdfNameFinal)
        pdfNameFinal = pdfNameFinal + ".pdf"
        

        # then generate full path using os lib
        full_path = os.path.join(self.PATH, pdfNameFinal)

        # Creating the pdf files
        pdf = open(full_path, 'wb')
        pdf.write(response.content)
        pdf.close()

