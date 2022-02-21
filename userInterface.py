#!/usr/bin/env python3

from tkinter import *
import tkinter.messagebox as tkMessageBox
import dataCollection
# import mysql.connector
# from mysql.connector import Error

root = Tk()
root.title("Basic Thickness Measurement")
 
width = 640
height = 490
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#=======================================VARIABLES=====================================
THICKNESS = StringVar()
TOLERANCE = StringVar()
desiredThickness = 0
desiredTolerance = 0.0
MEASURED = 0
TARE = 0
job = None
#=======================================METHODS=======================================
# def Database():
#     global conn, cursor
#     conn = mysql.connector.connect(host='localhost',
#                                          database='registerdb',
#                                          user='root',
#                                          password='')
#     cursor = conn.cursor()


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
def clear_text():
    global job
    thickness.delete(0,END)
    tolerance.delete(0,END)
    lbl_measured.config(text='')
    lbl_result.config(text='')
    if job is not None:
        root.after_cancel(job)
    
def setThickness():
    global desiredThickness, desiredTolerance, TARE
    TARE = 0
    if THICKNESS.get() and TOLERANCE.get():
        desiredThickness = float(THICKNESS.get())
        desiredTolerance = float(TOLERANCE.get())
    else:
        desiredThickness = 0
        desiredTolerance = 0
    measureThickness()
    
def measureThickness():
    global MEASURED, TARE, job
    MEASURED = dataCollection.measureAverage()
    measureTare = round(abs(MEASURED - TARE),2)
    lbl_measured.config(text=measureTare)
    job = root.after(200,measureThickness)
    if round(abs(desiredThickness - measureTare),2) > desiredTolerance:
        lbl_result.config(text='Warning.' , fg="red")
    else:
        lbl_result.config(text='Passed.',fg="green")

    
def tareThickness():
    global MEASURED, TARE
    TARE = MEASURED


#=====================================FRAMES====================================
TitleFrame = Frame(root, height=100, width=640, bd=1, relief=SOLID)
TitleFrame.pack(side=TOP)
RegisterFrame = Frame(root)
RegisterFrame.pack(side=TOP, pady=20)

#=====================================LABEL WIDGETS=============================
lbl_title = Label(TitleFrame, text="Thickness Measurement", font=('arial', 18), bd=1, width=640)
lbl_title.pack()
lbl_desired = Label(RegisterFrame, text="Desired thickness (cm):", font=('arial', 18), bd=18)
lbl_desired.grid(row=1)
lbl_tolerance = Label(RegisterFrame, text="Tolerance (cm):", font=('arial', 18), bd=18)
lbl_tolerance.grid(row=2)
lbl_thickness = Label(RegisterFrame, text="Measured thickness (cm):", font=('arial', 18), bd=18)
lbl_thickness.grid(row=4)
lbl_measured = Label(RegisterFrame, text="0.00", font=('arial', 18), bd=18)
lbl_measured.grid(row=4, column=1)
lbl_result = Label(RegisterFrame, text="", font=('arial', 25))
lbl_result.grid(row=5, columnspan=2)


#=======================================ENTRY WIDGETS===========================
thickness = Entry(RegisterFrame, font=('arial', 20), textvariable=THICKNESS, width=15)
thickness.grid(row=1, column=1)
tolerance = Entry(RegisterFrame, font=('arial', 20), textvariable=TOLERANCE, width=15)
tolerance.grid(row=2, column=1)
# pass1 = Entry(RegisterFrame, font=('arial', 20), textvariable=PASS, width=15, show="*")
# pass1.grid(row=2, column=1)
# name = Entry(RegisterFrame, font=('arial', 20), textvariable=NAME, width=15)
# name.grid(row=3, column=1)

#========================================BUTTON WIDGETS=========================
btn_set=Button(RegisterFrame, font=('arial', 20), text="Set", command=setThickness)
btn_set.grid(row=3, columnspan=2)
btn_tare=Button(RegisterFrame, font=('arial', 20), text="Tare", command=tareThickness)
btn_tare.grid(row=7, columnspan=2)
btn_clear=Button(RegisterFrame, font=('arial', 20), text="Clear", command=clear_text)
btn_clear.grid(row=9, columnspan=2, padx=30,pady=30)
#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
   
