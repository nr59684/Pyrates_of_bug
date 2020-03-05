import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
userItemData = pd.read_csv('ratings.csv')
userItemData.head()
itemList=list(set(userItemData["ItemId"].tolist()))
userCount=len(set(userItemData["ItemId"].tolist()))
itemAffinity= pd.DataFrame(columns=('item1', 'item2', 'score'))
rowCount=0
for ind1 in range(len(itemList)):
    item1Users = userItemData[userItemData.ItemId==itemList[ind1]]["userId"].tolist()
    #print("Item 1 ", item1Users)
    for ind2 in range(ind1, len(itemList)):
        if ( ind1 == ind2):
            continue
        item2Users=userItemData[userItemData.ItemId==itemList[ind2]]["userId"].tolist()
        #print("Item 2",item2Users)
        commonUsers= len(set(item1Users).intersection(set(item2Users)))
        score=commonUsers / userCount
        itemAffinity.loc[rowCount] = [itemList[ind1],itemList[ind2],score]
        rowCount +=1
        itemAffinity.loc[rowCount] = [itemList[ind2],itemList[ind1],score]
        rowCount +=1
#print(itemAffinity.head())
searchItem=int(input("Enter product ID : "))
recoList=itemAffinity[itemAffinity.item1==searchItem]\
        [["item2","score"]]\
        .sort_values("score", ascending=[0])
        
#print("Recommendations for item,",searchItem,"\n",  recoList)

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
        for F in (Home,Admin_Login,Customer_Login):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,sticky="nsew")
        self.show_frame(Home)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()
def qf(p):
    print(p)
class Home(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label1=tk.Label(self,text="INNER PATTERN EVOLUTION",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        btn1=tk.Button(self,text="ADMIN",command=lambda: controller.show_frame(Admin_Login))
        btn1.pack()
        btn2=tk.Button(self,text="CUSTOMER",command=lambda: controller.show_frame(Customer_Login))
        btn2.pack()
class Admin_Login (tk.Frame):
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
        btn2=tk.Button(self,text="LOGIN",command=None)
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
class Admin_Graph (tk.Frame):
    def __init__ (self,parent,controller):
        tk.Frame.__init__(self,parent)
        label1=tk.Label(self,text="GRAPH",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        btn1=tk.Button(self,text="HOME",command=lambda: controller.show_frame(Home))
        btn1.pack()
        x_list=[1,2,3,4,5]
        y_list=[10,20,30,40,50]
        f=Figure(figsize=(5,5),dpi=100)
        a=f.add_subplot(111)
        a.plot(x_list,y_list)
        canvas=FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
app=IPE()
app.mainloop()