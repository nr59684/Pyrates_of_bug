from DefaultPage import *
from sales_graph import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
class AdminHomePage(DefaultPage):
    def __init__(self,root,admin_details):
        self.details=admin_details
        self.dct_IntVar = {}
        super().__init__(root)
        self.m = Message(self.panel, width=600, font="castellar 20 bold ",
                         text="Admin Page", bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=320, y=20)
        self.add_admin_details()
        self.add_buttons()

    def add_buttons(self):
        self.pending_button = Button(self.f, text="View Sales", width=20, height=2, bg="white", fg="black",activebackground="gray",command=self.view_sales())
        self.pending_button.place(x=400, y=90)
        self.completed_button = Button(self.f, text="View Graph", width=25, height=2, bg="white", fg="black",activebackground="gray",command=sales_graph())
        self.completed_button.place(x=550, y=90)


    def add_menu_frame(self):
        self.menu_frame = Frame(self.f, height=420, width=450)
        self.menu_frame.place(x=400, y=140)
        self.img_diary = ImageTk.PhotoImage(Image.open("DiaryAdmin.jpg"))
        self.diary_panel = Label(self.menu_frame, image=self.img_diary, width=450, height=420)
        self.diary_panel.pack()
        self.diary_panel.pack_propagate(0)
        self.menu_frame.pack_propagate(0)

    def view_completed_orders(self):
        self.add_menu_frame()
        query="Select * from world.FoodOrder where IsComplete=1 order by FoodOrderId limit 5"
        result=DatabaseHelper.get_all_data(query)
        self.text_font=("MS Serif",12)
        for i in range(len(result)):
            self.dct_IntVar[result[i][0]]=IntVar()
        Label(self.menu_frame, font="Times 12", text="CustomerId").grid(row=1, column=1,pady=10)
        Message(self.menu_frame, font="Times 12", text="FoodItems", width=300).grid(row=1, column=2,sticky="w",pady=10)
        for i in range(len(result)):
            Label(self.menu_frame,font=self.text_font,text=result[i][1]).grid(row=i+2,column=1,pady=5)
            Message(self.menu_frame,font=self.text_font,text=result[i][2],width=300).grid(row=i+2,column=2,sticky="w",pady=5)
        self.menu_frame.grid_propagate(0)


    def view_sales(self):
        self.add_menu_frame()
        userItemData = pd.read_csv('ratings.csv')

        itemList2 = list(userItemData["ItemId"].tolist())
        for i in range(len(itemList2)):
            itemList2[i] = int(itemList2[i])
        d_fre = {}

        for item in itemList2:
            if (item in d_fre):
                d_fre[item] += 1
            else:
                d_fre[item] = 1

        self.text_font=("MS Serif",12)
        for i in d_fre.keys():
            self.dct_IntVar[d_fre[i]]=IntVar()
        Label(self.menu_frame, font="Times 12", text="ProductId").grid(row=1, column=1,pady=10)
        Message(self.menu_frame, font="Times 12", text="Frequency", width=300).grid(row=1, column=2,sticky="w",pady=10)
        for i in d_fre.keys():

            Label(self.menu_frame,font=self.text_font,text=i).grid(row=i+2,column=1,pady=5)
            Message(self.menu_frame,font=self.text_font,text=d_fre[i],width=300).grid(row=i+2,column=2,sticky="w",pady=5)
        self.menu_frame.grid_propagate(0)


    def add_admin_details(self):
        print(self.details)
        self.profile_pic = ImageTk.PhotoImage(Image.open(self.details[4]))
        self.c=Canvas(self.panel,width=100,height=180)
        #self.photo_l= Label(self.f, image=self.img)
        self.canvas_pic=self.c.create_image(0,0,image=self.profile_pic,anchor=NW)
        self.c.place(x=40,y=100)
        self.panel.pack()
        self.panel.pack_propagate(0)
        self.m = Message(self.f, width=150, font="Roman 15 italic",
                         text="Name= "+self.details[1], bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=40, y=300)
        self.m = Message(self.f, width=250, font="Roman 15 italic",
                         text="Email: "+self.details[3], bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=40, y=350)

if __name__ == '__main__':
    root=Tk()
    a=AdminHomePage(root,(2, 'Ritesh', 'SGT', 'riteshagicha@gmail.com', 'nileshPic3.jpg'))
    root.mainloop()