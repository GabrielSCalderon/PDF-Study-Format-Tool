import os
import sys
import datetime
import time
import reportlab # pip install reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import pink, black, red, blue, green, gray, darkgray
from shutil import copyfile
import PyPDF2 # pip install PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import magenta, pink, blue, green, red, white, black, yellow, purple, gold
from tkinter import filedialog
from tkinter import *
import tkinter as tk
from io import StringIO
# import fitz # pip install pymupdf
from pathlib import Path
import csv
# import pytesseract
from PIL import Image
import re
import xml.etree.ElementTree as ET
# import nltk
import string
# from nltk.stem import WordNetLemmatizer
# import numpy as np



##############
## Setup #####
##############
    
def starter_variables():    
    global today_string
    today_string = str(datetime.date.today().strftime("%m-%d-%y"))
    global today_object
    today_object = datetime.date.today()
    global maindir
    maindir = os.path.dirname(os.path.realpath(sys.argv[0]))
    global python_title
    python_title = os.path.basename(__file__)
    global python_title_base
    python_title_base = python_title[:-3]

starter_variables()

def minimize_windows_console():
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )


##############
## LOGGER ####
##############

def startLogger(): 
    import logging
    """
    Uses:
    - logger.debug() 
    - logger.info()
    - logger.exceptions() = gives traceback
    """
    log_file_name = python_title[:-3]+".log"
    # Check for previous logger instance
    if __name__ in logging.root.manager.loggerDict.keys():
        pass # Do not create another instance of the same logger
    else:
        # CREATE LOGGER INSTANCE BASED ON THE MODULE IMPORTED OR __MAIN__ AND SET THE BASE LOG LEVEL TO DEBUG
        global logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        # CREATE THE STRING FORMAT THAT LOG RECORDS WILL USE (THIS FORMAT CAN BE USED FOR MULTIPLE LOG HANDLERS)
        # (Name of File):(Time):(Name of Logger):(Logged Info)
        formatter = logging.Formatter('%(filename)s:%(asctime)s:%(name)s:%(message)s')
        # FILE HANDLERS, WRITE THE LOGGER INFO TO A FILE
        file_handler = logging.FileHandler(log_file_name)
        # file_handler.setLevel(logging.DEBUG) #Sets specific level for saving log information
        file_handler.setFormatter(formatter)
        # STREAM HANDLERS, PRINT OUT THE LOGGER INFO IN THE CONSOLE
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        # ADD HANDLERS TO THE LOGGER INSTANCE
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

startLogger()
    
logger.debug("Program ran.")


##############
## Main ######
##############

pass # Could consider adding the threading module to separate resources for running the GUI and converting the pdf to images so there isn't a load screen
pass # Also consider writing function to minimize newlines to just 1, so if there is 2, delete 1, if 3, delete 2 and so on


def select_py_file():
    try:
        global window_file_path
        global window_filename
        global window_filename_wo_ext
        global window_file_parentdir
        window_file_path = filedialog.askopenfilename(title = "Select file", filetypes = (("PDF Files","*.pdf"),("All files","*.*")))
        window_filename = os.path.basename(window_file_path) #filename 
        window_filename_wo_ext = os.path.splitext(window_filename)[0] #filename without extension
        window_file_parentdir = os.path.dirname(window_file_path)
        global selected_file_var
        change_text = ''
        if len(window_file_path) > 50:
            change_text = "..." + window_file_path[-50:]
        else:
            change_text = window_file_path
        selected_file_var.set("Selected File: "+ change_text)
    # try:
    #     pass
    except:
        print('Error with file selection.')
    
def createPagePdf_noteboxes(trash_path, tmpfilename):
    # get the size of the selected pdf to help define dimensions for noteboxes
    with open(trash_path, "rb") as tf:
        input1_file = PdfFileReader(tf)
        size_pdf_height = input1_file.getPage(0).mediaBox.getHeight()
        size_pdf_width = input1_file.getPage(0).mediaBox.getWidth()
        num = input1_file.getNumPages() #getting number of pages of selected pdf file
        tf.close()

    c = canvas.Canvas(tmpfilename)
    form = pdfform.AcroForm
    form.fields = []
    completionform = c.acroForm
    # this function draws the individual numbers on each page in the temp pdf
    for i in range(1,num+1):
        # gray box background
        # c.setFillColorRGB(r=(211/255),g= (211/255),b=(211/255))
        # c.rect(0,0,size_pdf_width, 320,fill=1, stroke=0) 
        # draw noteboxes
        c.setPageSize((size_pdf_width, 325))
        c.setFont("Courier", 14)
        c.setFillColorRGB(255,0,0)
        # print((float(size_pdf_width)-float(10+50)))
        form.textField(form, canvas=c, title=f'textbox-notes{str(i)}', xmin=10, ymin=10, xmax=(float(size_pdf_width)-float(10+52)), ymax=300, value="", multiline=20)
        #### CHECKBOXES FOR COMPLETION

        #First pass
        completionform.checkbox(name=f'firstpass{str(i)}', tooltip='firstpass', checked=False,
                    x=(float(size_pdf_width)-float(10+50)), y=250,
                    buttonStyle='star', borderStyle='solid',
                    borderWidth=1, borderColor=black, fillColor=white, textColor=darkgray,
                    forceBorder=True, size=50)

        c.setFont("Courier", 10)    
        c.setFillColorRGB(r=(128/255),g= (128/255),b=(128/255)) # Gray
        c.drawString((float(size_pdf_width)-float(10+50)), 240, "1st Pass")


        #Reviewed
        c.setFillColorRGB(0,0,0)
        completionform.checkbox(name=f'reviewed{str(i)}', tooltip='reviewed', checked=False,
                    x=(float(size_pdf_width)-float(10+50)), y=175,
                    buttonStyle='star', borderStyle='solid',
                    borderWidth=1, borderColor=black, fillColor=white, textColor=green,
                    forceBorder=True, size=50)

        c.setFont("Courier", 10)    
        c.setFillColorRGB(r=(0/255),g= (100/255),b=(0/255))
        c.drawString((float(size_pdf_width)-float(10+50)), 165, "Reviewed")

        #Study Buddy
        completionform.checkbox(name=f'studybuddy{str(i)}', tooltip='studybuddy', checked=False,
                    x=(float(size_pdf_width)-float(10+50)), y=95,
                    buttonStyle='star', borderStyle='solid',
                    borderWidth=1, borderColor=black, fillColor=white, textColor=gold,
                    forceBorder=True, size=50)
        
        c.setFont("Courier", 8)    
        c.setFillColorRGB(r=(210/255),g= (105/255),b=(30/255))
        c.drawString((float(size_pdf_width)-float(10+50)), 85, "Study Buddy")

        #Tricky
        completionform.checkbox(name=f'tricky{str(i)}', tooltip='tricky', checked=False,
                    x=(float(size_pdf_width)-float(10+50)), y=20,
                    buttonStyle='star', borderStyle='solid',
                    borderWidth=1, borderColor=black, fillColor=white, textColor=purple,
                    forceBorder=True, size=50)

        c.setFont("Courier", 10)    
        c.setFillColorRGB(r=(138/255),g= (43/255),b=(226/255))
        c.drawString((float(size_pdf_width)-float(10+50)), 10, "Tricky")
        
        # Draw "Notes" string
        c.setFillColorRGB(255,0,0)
        c.setFont("Courier", 22)
        note_header_text = f"[Slide {str(i)} of {str(num)}: Note Box]"
        c.drawString((float(size_pdf_width) - float(c.stringWidth(note_header_text)))/2, 302, note_header_text)

        # create a rectangle around the notes section
        c.roundRect(5, 5, float(size_pdf_width)-float(10), 314, 4, stroke = 1, fill = 0)

        c.showPage() # this function I believe adds another page to the canvas...
    c.save()

def merge_notebox_slides_vertical(out_filename, slide_filename, notebox_filename):
    """ Merge the first page of two PDFs slide-to-notebox """
    # open the PDF files to be merged
    with open(slide_filename, "rb") as slide_file, open(notebox_filename, "rb") as notebox_file, open(out_filename, 'wb') as output_file:
        slide_pdf = PyPDF2.PdfFileReader(slide_file)
        notebox_pdf = PyPDF2.PdfFileReader(notebox_file)
        output = PyPDF2.PdfFileWriter()

        # loop through all pages of the slides pdf
        page_count = slide_pdf.getNumPages()
        for page_number in range(page_count):
            slide_page = slide_pdf.pages[page_number]
            notebox_page = notebox_pdf.pages[page_number]
            print("Creating noteboxes on page {} of {}".format(page_number+1, page_count))
            # print("*******Height of notebox: {}".format(notebox_page.mediaBox.getHeight()))
            page = output.addBlankPage(
                width= max(slide_page.mediaBox.getWidth(), notebox_page.mediaBox.getWidth()),
                height = slide_page.mediaBox.getHeight() + notebox_page.mediaBox.getHeight(),
            )
            # draw the pages on that new page
            page.mergeTranslatedPage(slide_page, 0, notebox_page.mediaBox.getHeight())
            page.mergeTranslatedPage(notebox_page, 0, 0)

        # write to file
        output.write(output_file)
        slide_file.close()
        notebox_file.close()
    os.remove(slide_filename)
    os.remove(notebox_filename)
    # time.sleep(5)

def add_page_noteboxes(pdf_file_path):
    # time.sleep(5)
    original_path = pdf_file_path
    original_base = os.path.basename(original_path) #the name of the file itself with extension
    window_file_parentdir = os.path.dirname(original_path) #the parent folder for the selected file
    os.chdir(window_file_parentdir)

    #make a duplicate of the original file to use the original name for writing the pdf 
    trash_file_name = "trash_"+original_base
    # print(trash_file_name)
    with open(trash_file_name, "w") as tf:
        trash_path = os.path.join(window_file_parentdir, trash_file_name)
        copyfile(original_path, trash_path)
        tf.close()
    changed_base = "trash_"+original_base

    #recreate the original file name
    path = os.path.join(window_file_parentdir, original_path)
    base = os.path.basename(path)

    tmpfilename = "notebox_trash.pdf"
    # Add the noteboxes to the pdf
    createPagePdf_noteboxes(trash_path, tmpfilename)

    # test the slide-notebox code
    merge_notebox_slides_vertical(original_base, trash_path, tmpfilename)
    print("Finished adding note boxes!")
    # Remove temporary files
    os.chdir(maindir)

def run_program():
    if window_file_path == None:
        print("No python file selected.")
    else:
        # Main Function Switches
        add_page_noteboxes(window_file_path)
        
        # console output and shit
        print()
        print('File Path: ', window_file_path)
        print('File Name: ', window_filename)
        print('File Name w/o Ext: ', window_filename_wo_ext)
        task_created_text = "Program ran."
        run_program_var.set(task_created_text)


#########################
### Tkinter GUI Setup ###
#########################


def tkinterGUISetup():
    # USER-INPUT GUI:
    #File open dialog to get desired pdf
    global window
    window = Tk()
    window.title(python_title_base)
    #If you have a large number of widgets, like it looks like you will for your
    #game you can specify the attributes for all widgets simply like this.
    window.option_add("*Button.Background", "black")
    window.option_add("*Button.Foreground", "red")
    window.option_add("*Radiobutton.Background", "black")
    window.option_add("*Radiobutton.Foreground", "red")
    #You can set the geometry attribute to change the window windows size
    window.geometry("500x500") #You want the size of the app to be 500x500
    window.resizable(0, 0) #Don't allow resizing in the x or y direction

    global back
    back = tk.Frame(master=window,bg='black')
    back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
    back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the window window

    ### AUTHOR
    global author
    author = tk.Label(master=back, text='Made by TeddyBear', bg='red', fg='black')
    author.pack()

    global blank1
    blank1 = tk.Label(master=back, text='\r\n', bg='black', fg='red')
    blank1.pack()

    ### SELECT PYTHON FILE
    global window_file_path
    global window_filename
    global window_filename_wo_ext
    global window_file_parentdir

    window_file_path = None
    window_filename = None
    window_filename_wo_ext = None
    window_file_parentdir = None

    global select_py_file
    selected_py_file = tk.Button(master=back, text='Select PDF File', command=select_py_file, padx = 20)
    selected_py_file.pack()

    global selected_file_var
    selected_file_var = StringVar()
    selected_file_var.set('')
    tk.Label(master=back, textvariable = selected_file_var, padx = 20, bg='black', fg='yellow').pack()

    blank1 = tk.Label(master=back, text='\r\n', bg='black', fg='red')
    blank1.pack()

    global run_program_var
    global run_program_label
    run_program_var = StringVar()
    run_program_var.set("")
    run_program_label = tk.Label(master=back, textvariable=run_program_var, bg='black', fg='yellow').pack()

    global run_program_button
    run_program_button = tk.Button(master = back, text = 'Run Program', command = run_program, padx = 20)
    run_program_button.pack()
    blank1 = tk.Label(master=back, text='\r\n', bg='black', fg='red')
    blank1.pack()

    ### CLOSE BUTTON
    global close
    close = tk.Button(master=back, text='Quit', command=window.destroy, padx = 20)
    close.pack()


tkinterGUISetup()
window.mainloop() 
