from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from databasehelper import *
class DefaultPage:
    def __init__(self,root):
        self.root=root
        self.root.iconbitmap('carIcon.ico')
        self.f=Frame(root,height=1080,width=1920)
        self.f.pack()
        self.img = ImageTk.PhotoImage(Image.open("final2.jpg"))
        self.panel = Label(self.f, image=self.img)
        self.panel.pack()
        self.panel.pack_propagate(0)
        self.m = Message(self.f, width=600, font="Castellar 20 bold ",
                         text="SAFEDRIVE",bg="white",relief=SOLID
                         ,borderwidth=2)
        self.m.place(x=725, y=20)
        self.footer=Label(self.panel,bg="ivory3",height=1,text="@Copyright 2020 SAFEDRIVE & Co. All rights reserved")
        self.footer.pack_propagate(0)
        self.footer.pack(side=BOTTOM,fill=X)
        self.f.pack_propagate(0)



