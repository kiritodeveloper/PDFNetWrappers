#---------------------------------------------------------------------------------------
# Copyright (c) 2001-2018 by PDFTron Systems Inc. All Rights Reserved.
# Consult LICENSE.txt regarding license information.
#---------------------------------------------------------------------------------------

import site
site.addsitedir("../../../PDFNetC/Lib")
import sys
from PDFNetPython import *

# Relative path to the folder containing the test files.
input_path = "../../TestFiles/"

def ProcessElements(reader):
    element = reader.Next()
    while element != None:		# Read page contents
        if element.GetType() == Element.e_path:  	    # Process path data...
            data = element.GetPathData()
            points = data.GetPoints()
        elif element.GetType() == Element.e_text:		# Process text strings...
            data = element.GetTextString()
            if sys.version_info.major >= 3:
                data = ascii(data)
            print(data)
        elif element.GetType() == Element.e_form:		# Process form XObjects
            reader.FormBegin()
            ProcessElements(reader)
            reader.End()
        element = reader.Next()

def main():
    PDFNet.Initialize()
    
    # Extract text data from all pages in the document
    print("-------------------------------------------------")
    print("Sample 1 - Extract text data from all pages in the document.")
    print("Opening the input pdf...")
    
    doc = PDFDoc(input_path + "newsletter.pdf")
    doc.InitSecurityHandler()
    
    page_reader = ElementReader()
    
    itr = doc.GetPageIterator()
    
    # Read every page
    while itr.HasNext():
        page_reader.Begin(itr.Current())
        ProcessElements(page_reader)
        page_reader.End()
        itr.Next()
    
    # Close the open document to free up document memory sooner.    
    doc.Close()
    print("Done.")
    
if __name__ == '__main__':
    main()
