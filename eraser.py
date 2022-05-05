### Version 2.0 ###
# This script will redact all overall marks from a Jumprope Mastery Report

import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PdfFileWriter
import os


def openfile(event=None):
    '''
    Opens a dialog box and allows a file to be selected.
    '''
    lblDone['text'] = ""
    filepaths = filedialog.askopenfiles()

    # This won't run if you hit "Cancel" - to avoid generating an exception
    counter = 0
    if filepaths:
        # filepaths is a tuple of file paths, so loop through them all
        totalfiles = len(filepaths)
        for filepath in filepaths:
            # Handle the error if a non-pdf file is selected
            try:
                # Show progress
                redact(filepath.name)
                counter += 1
                lblDone['text'] = f"{counter}/{totalfiles} files done"
                root.update()
            except:
                lblDone['text'] = "Only select pdf files!"


def redact(filename):
    '''
    Takes a file and redacts it by combining the pdf with pre-made redaction pdf images.
    '''
    lblDone['text'] = "Processing..."
    root.update()
    # Open the pdf file selected
    with open(filename, "rb") as pdf_file:
        pdf_read = PdfFileReader(pdf_file)
        pages = int(pdf_read.numPages)  # Get the number of pages

        # Open the first page watermark file
        with open("watermark1.pdf", "rb") as watermark1:
            watermark1_read = PdfFileReader(watermark1)
            watermarkpage1 = watermark1_read.getPage(0)

            # Open the other pages watermark file
            with open("watermark2.pdf", "rb") as watermark2:
                watermark2_read = PdfFileReader(watermark2)
                watermarkpage2 = watermark2_read.getPage(0)

                # Create the new pdf object which will have the merged pages
                newpdf = PdfFileWriter()

                # Make a list of pages to do FULL redacting dependent on number of pages per student
                # Get the number of pages per student from the entry box
                stpages = int(entPages.get())
                firstpages = []
                # Find out how many first pages are in the pdf
                multiples = int(pages / stpages)
                for x in range(multiples):
                    pgindex = stpages * x
                    # Add the index of ever first page to a list
                    firstpages.append(pgindex)

                # Make a list of pages to do side redacting
                otherpages = []
                for x in range(pages):
                    if x not in firstpages:
                        otherpages.append(x)

                # Loop through all the pages, deciding on whether it is a firstpage or otherpage
                for pg in range(pages):
                    currentpage = pdf_read.getPage(pg)
                    if pg in firstpages:
                        currentpage.mergePage(watermarkpage1)
                    elif pg in otherpages:
                        currentpage.mergePage(watermarkpage2)

                    newpdf.addPage(currentpage)

                # Write the file
                newfilename = filename[:-4] + "_Redacted.pdf"
                with open(newfilename, "wb") as outputfile:
                    newpdf.write(outputfile)


###TKINTER GUI###
root = tk.Tk()
root.geometry('400x240')
root.resizable(False, False)
root.title('Jumprope Eraser')
root.config(bg="#323332")
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
root.iconbitmap(os.path.join(__location__, 'eraser.ico'))

### INSTRUCTIONS ###
lblInstructions = tk.Label(
    root,
    text="This will redact overall marks from\nthe Jumprope Mastery Report(s) selected.\nVersion 2.0 by Jonathan Kung\n",
    bg="#323332",
    fg="#cf7f4b",
    font="Courier 15 bold"
)

lblInstructions.pack(pady=5)

### NUMBER OF PAGES ###
# Frame
frame = tk.Frame()
frame.config(background="#323332")

# Label
lblPages = tk.Label(
    master=frame,
    text="# of pages per student:",
    bg="#323332",
    fg="#cf7f4b",
    font="Courier 15 bold"
)
lblPages.pack(side="left")

# Entry
entPages = tk.Entry(
    master=frame,
    width=3,
    bg="#cf7f4b",
    font="Courier 15 bold",
    justify="center"
)
entPages.insert(0, "1")
entPages.pack(side="left")
entPages.focus_set()
entPages.select_range(0, tk.END)

frame.pack()

### BUTTON TO GET FILE(S) ###
btnGetfile = tk.Button(
    root,
    text="SELECT PDF FILE(S)",
    width=17,
    fg="#323332",
    font="Courier 20 bold",
    command=openfile
)

btnGetfile.pack(pady=5)

# Click Enter to activate button as well
root.bind('<Return>', openfile)

### STATUS LABEL ###
lblDone = tk.Label(
    root,
    bg="#323332",
    fg="#cf7f4b",
    font="Courier 20 bold",
    text="")

lblDone.pack(pady=5)

### CLOSE BUTTON ###
btnExit = tk.Button(
    root,
    text="Close",
    width=7,
    fg="#323332",
    font="Courier 15 bold",
    command=root.quit
)

btnExit.pack(pady=5)

root.mainloop()
