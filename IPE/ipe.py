import tkinter as tk
from tkinter import ttk
import matplotlib, numpy, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

#CALCULATIONS FOR RECOMMENDATIONS
userItemData = pd.read_csv('ratings.csv')
userItemData.head()
itemList=list(set(userItemData["ItemId"].tolist()))
userCount=len(set(userItemData["ItemId"].tolist()))

itemAffinity= pd.DataFrame(columns=('item1', 'item2', 'score'))
rowCount=0
for ind1 in range(len(itemList)):
    item1Users = userItemData[userItemData.ItemId==itemList[ind1]]["userId"].tolist()
    print("Item 1 ", item1Users)
    for ind2 in range(ind1, len(itemList)):
        if ( ind1 == ind2):
            continue
        item2Users=userItemData[userItemData.ItemId==itemList[ind2]]["userId"].tolist()
        print("Item 2",item2Users)
        commonUsers= len(set(item1Users).intersection(set(item2Users)))
        score=commonUsers / userCount
        itemAffinity.loc[rowCount] = [itemList[ind1],itemList[ind2],score]
        rowCount +=1
        itemAffinity.loc[rowCount] = [itemList[ind2],itemList[ind1],score]
        rowCount +=1

print(itemAffinity.head())
searchItem=int(input("Enter product ID : "))
recoList=itemAffinity[itemAffinity.item1==searchItem]\
        [["item2","score"]]\
        .sort_values("score", ascending=[0])
        
print("Recommendations for item,",searchItem,"\n",  recoList)


#SALES-ITEM GRAPH
itemList2=list(userItemData["ItemId"].tolist())
for i in range (len(itemList2)):
    itemList2[i]=int(itemList2[i])
d_fre = {} 
for item in itemList2: 
    if (item in d_fre): 
        d_fre[item] += 1
    else: 
        d_fre[item] = 1
print(d_fre)
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
objects=tuple(d_fre.keys())
y_pos = np.arange(len(objects))
fre=d_fre.values()
plt.bar(y_pos, fre, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Frequency of Sales')
plt.title('Sales of different products')
plt.show()



#AFFINITY-ITEMS GRAPH
#??

from pymysql import *

class DatabaseHelper():
    @staticmethod
    def get_all_data(query,parameters=None):
        conn = connect(host='localhost', database='world', user='root', password='groot')
        cur=conn.cursor()
        if(parameters is None):
            cur.execute(query)
        else:
            cur.execute(query%parameters)
        result=cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def get_data(query,parameters=None):
        conn = connect(host='localhost', database='world', user='root', password='groot')
        cur=conn.cursor()
        if(parameters is None):
            cur.execute(query)
        else:
            cur.execute(query%parameters)
        result=cur.fetchone()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def execute_query(query,parameters=None):
        conn = connect(host='localhost', database='world', user='root', password='groot')
        cur = conn.cursor()
        if(parameters is None):
            cur.execute(query)
        else:
            cur.execute(query % parameters)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_all_data_multiple_input(query,params):
        conn = connect(host='localhost', database='world', user='root', password='groot')
        cur = conn.cursor()
        format_strings = ','.join(['%s'] * len(params))
        cur.execute(query % format_strings,params)
        result= cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def execute_all_data_multiple_input(query,params):
        conn = connect(host='localhost', database='world', user='root', password='groot')
        cur = conn.cursor()
        format_strings = ','.join(['%s'] * len(params))
        print(format_strings)
        cur.execute(query % format_strings,params)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def display(query,args=None):
  #      self.root = Tk()
        cur=DatabaseHelper.conn.cursor()
        if args is None:
            cur.execute(query)
        else:
            cur.execute(query % args)
        rows=cur.fetchall()
        tple=tuple(rows)
        # for row in rows:
        #     for data in row:
        #         b=Label(self.root,text=data)
        #         b.grid(row=r,column=c)
        #         c=c+1
        #     r=r+1
        #     c=0
        # self.root.mainloop()
        return tple



#GUI
LARGE_FONT=("Verdana",12)
class IPE (tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self,"IPE")
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.frames={}
        for F in (DefaultPage,MainPage,Admin_Graph):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,sticky="nsew")
        self.show_frame(DefaultPage)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

#Home page

class DefaultPage (tk.Frame,IPE):
    def __init__ (self,parent,controller):
        self.f=Frame(self,height=1080,width=1920)
        self.f.pack()
        self.img = ImageTk.PhotoImage(Image.open("final2.jpg"))
        self.panel = Label(self.f, image=self.img)
        self.panel.pack()
        self.panel.pack_propagate(0)
        self.m = Message(self.f, width=600, font="Castellar 20 bold ",
                         text="Wall Mart",bg="white",relief=SOLID
                         ,borderwidth=2)
        self.m.place(x=720, y=20)
        self.footer=Label(self.panel,bg="ivory3",height=1,text="@Copyright 2019 Wall Mart & Co. All rights reserved")
        self.footer.pack_propagate(0)
        self.footer.pack(side=BOTTOM,fill=X)
        self.f.pack_propagate(0)


class MainPage (tk.Frame,IPE):
    def __init__ (self,parent,controller):
        self.add_widgets()

    def getLoginScreen(self,login_type):
        login_window=Toplevel()
        f=Frame(login_window,height=200,width=400)
        l1 = Label(f, width=20, text="Enter username: ")
        self.e1 = Entry(f, width=30, fg='black', bg='white')
        self.e1.focus_set()
        self.e2 = Entry(f, width=30, fg='black', bg='white', show='*')
        l2 = Label(f, width=20, text="Enter password: ")
        l1.grid(row=1, column=1, padx=10, pady=10)
        l2.grid(row=2, column=1, padx=10, pady=10)
        self.e1.grid(row=1, column=4, padx=10, pady=10)
        self.e2.grid(row=2, column=4, padx=10, pady=10)
        b1 = Button(f, text="Submit", height=2, width=10, command=lambda: self.validate(self,login_window,login_type))
        b1.grid(row=3, column=1, padx=10, sticky='e')
        b2 = Button(f, text="Reset", height=2, width=10, command=lambda: self.reset())
        b2.grid(row=3, column=4, padx=10, sticky='w')
        f.pack()
        f.grid_propagate(0)

    def reset(self):
        self.e1.delete(0,END)
        self.e2.delete(0, END)

    def add_widgets(self):
        self.admin_button = Button(self.panel, text="Admin login", command=lambda: self.getLoginScreen("Admin"), width=20,height=2, activebackground="gray")
        self.admin_button.place(x=675, y=150)
        self.user_button = Button(self.panel, text="User login", command=lambda: self.getLoginScreen("User"), width=20,height=2, activebackground="gray")
        self.user_button.place(x=845, y=150)
        self.new_user_button = Button(self.panel, text="New user? Sign up here", width=20, height=2,activebackground="gray", activeforeground="white", borderwidth=2, relief=RIDGE,command=self.sign_up_form)
        self.new_user_button.place(x=760, y=220)

    def sign_up_form(self):
        text_font = ("corbel", 12)
        registration_window=Toplevel()
        f=Frame(registration_window,width=650,height=400,bg="white")
        Message(f, font="Castellar 20 bold", text="Wall Mart", width=300).grid(row=0, column=0,columnspan=3, pady=5)
        Message(f, text="Register with us to get the best shopping experience.", width=600,font="corbel 20 ",bg="white", relief=SOLID,borderwidth=2).grid(row=1,column=0,columnspan=3)
        f.pack()
        l=Label(f,text="Name",font=text_font)
        l.grid(row=2,column=0,padx=10,pady=10)
        self.register_e1=Entry(f)
        self.register_e1.grid(row=2,column=1,padx=10,pady=10)
        self.register_e1.focus_set()
        l=Label(f,text="Contact",font=text_font)
        l.grid(row=3, column=0, padx=10, pady=10)
        self.register_e2 = Entry(f)
        self.register_e2.grid(row=3, column=1, padx=10, pady=10)
        l = Label(f, text="Email Id:",font=text_font)
        l.grid(row=4, column=0, padx=10, pady=10)
        self.register_e3 = Entry(f)
        self.register_e3.grid(row=4, column=1, padx=10, pady=10)
        l = Label(f, text="Password",font=text_font)
        l.grid(row=5, column=0, padx=10, pady=10)
        self.register_e4 = Entry(f,show="*")
        self.register_e4.grid(row=5, column=1, padx=10, pady=10)
        l = Label(f, text="Re-enter Password",font=text_font)
        l.grid(row=6, column=0, padx=10, pady=10)
        self.register_e5 = Entry(f,show="*")
        self.register_e5.grid(row=6, column=1, padx=10, pady=10)
        b1=Button(f,text="Register", width=20, height=2, bg="white", fg="black",activebackground="gray",command=lambda: self.register_user(registration_window))
        b1.grid(row=7,column=0,padx=10,pady=10,sticky="e")
        b2 = Button(f, text="Reset", width=20, height=2, bg="white", fg="black",activebackground="gray",command=self.register_reset)
        b2.grid(row=7, column=1, padx=10, pady=10,sticky="w")
        f.grid_propagate(0)

    def register_reset(self):
        self.register_e1.delete(0,END)
        self.register_e2.delete(0, END)
        self.register_e3.delete(0, END)
        self.register_e4.delete(0, END)
        self.register_e5.delete(0, END)

    def register_user(self,registration_window):
        name=self.register_e1.get()
        contact=self.register_e2.get()
        email=self.register_e3.get()
        pwd=self.register_e4.get()
        pwd2=self.register_e5.get()
        if(name=="" or contact=="" or email=="" or pwd==""):
            messagebox.showwarning("Mandatory fields","Please fill all the fields")
            registration_window.focus_set()
        elif(pwd!=pwd2):
            messagebox.showerror("Password Error","Passwords don't match.Please re-enter")
            registration_window.focus_set()
        else:
            query="Insert into Customer1(CustomerName, CustomerPassword,CustomerContact, CustomerEmailId) Values ('%s','%s','%s','%s')"
            args=(name,pwd,contact,email)
            DatabaseHelper.execute_query(query %args)
            messagebox.showinfo("Success","User registered successfully. Please login")
            registration_window.destroy()

    def validate(self,login_window,login_type):
        username=self.e1.get()
        pwd = self.e2.get()
        if(login_type=="Admin"):
            query = "Select * from world.Admin where AdminName= '%s' and AdminPassword='%s'"
        else:
            query = "Select * from world.Customer1 where CustomerName= '%s' and CustomerPassword='%s'"
        parameters=(username,pwd)
        result=DatabaseHelper.get_data(query,parameters)
        if(result is None or len(result)==0):
            messagebox.showerror("Login Failed","Incorrect credentials")
        else:
            messagebox.showinfo('Login Success',"Login successfuly completed")
            login_window.destroy()
            self.f.destroy()
            self.panel.destroy()
            if(login_type=="Admin"):
                self.redirect=AdminHomePage(self,result)
            else:
                self.redirect=CustomerHomePage(self,result)
        print(username)
        print(pwd)
class Admin_Graph (tk.Frame):
    def __init__ (self,parent,controller):
        tk.Frame.__init__(self, parent)
        f = Figure(figsize=(5,4), dpi=100)
        ax = f.add_subplot(111)
        data = (20, 35, 30, 35, 27)
        ind = numpy.arange(5)  # the x locations for the groups
        width = .5
        rects1 = ax.bar(ind, data, width)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


app=IPE()
app.mainloop()
