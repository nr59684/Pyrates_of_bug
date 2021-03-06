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
        for F in (Home,Admin_Login,Customer_Login,Admin_Graph):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,sticky="nsew")
        self.show_frame(Home)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()
class Home(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=1080,width=1920)
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
class Admin_Login (tk.Frame,IPE):
    def __init__ (self,parent,controller):
        tk.Frame.__init__(self,parent)
        label1=tk.Label(self,text="ADMIN LOGIN",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        label2=tk.Label(self,text="ADMIN ID",font=LARGE_FONT)
        label2.pack(pady=10,padx=10)
        label3=tk.Label(self,text="PASSWORD",font=LARGE_FONT)
        label3.pack(pady=10,padx=10)
        btn1=tk.Button(self,text="HOME",command=lambda: controller.show_frame(Home))
        btn1.pack()
        btn2=tk.Button(self,text="LOGIN",command=lambda: controller.show_frame(Admin_Graph))
        btn2.pack()
class Customer_Login (tk.Frame):
    def __init__ (self,parent,controller):
        tk.Frame.__init__(self,parent)
        label1=tk.Label(self,text="CUSTOMER LOGIN",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        label2=tk.Label(self,text="CUSTOMER ID",font=LARGE_FONT)
        label2.pack(pady=10,padx=10)
        label3=tk.Label(self,text="PASSWORD",font=LARGE_FONT)
        label3.pack(pady=10,padx=10)
        btn1=tk.Button(self,text="HOME",command=lambda: controller.show_frame(Home))
        btn1.pack()
        btn2=tk.Button(self,text="LOGIN",command=None)
        btn2.pack()
        btn3=tk.Button(self,text="REGISTER",command=None)
        btn3.pack()

        
app=IPE()
app.mainloop()
