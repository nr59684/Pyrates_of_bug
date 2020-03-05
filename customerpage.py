from DefaultPage import *
from tkinter import messagebox
import pandas as pd
class CustomerHomePage(DefaultPage):
    def __init__(self,root,customer_details):
        self.customer_details=customer_details
        self.text_font = ("corbell", 12)
        self.dct_IntVar = {}
        super().__init__(root)
        self.m = Message(self.panel, width=600, font="Corbell 20 bold italic",
                         text="Customer Page", bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=320, y=20)
        self.add_menu()

    def add_menu_items(self):
        self.menu_b5 = Button(self.menu_frame, text="Buy", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=self.place_order)
        self.menu_b5.place(x=350,y=10)
        self.menu_items_frame=Frame(self.menu_frame,height=350,width=350)
        self.menu_items_frame.place(x=50,y=50)
        self.diary2_img = ImageTk.PhotoImage(Image.open("Diary2.jpg"))
        self.diary2_panel = Label(self.menu_items_frame, image=self.diary2_img)
        self.diary2_panel.pack()
        self.diary2_panel.pack_propagate(0)
        userItemData = pd.read_csv('ratings.csv')
        itemList2 = list(userItemData["ItemId"].tolist())

        for i in range(len(itemList2)):
            itemList2[i] = int(itemList2[i])
        d_fre = {}
        price=100
        for i in range (len(itemList2)):
            d_fre[itemList2[i]]=price
            price=price+100

        for i in d_fre.keys():
            self.dct_IntVar[d_fre[i]] = IntVar()
        Label(self.menu_frame, font="Times 12", text="ProductId").place(x=100,y=100)
        Message(self.menu_frame, font="Times 12", text="Price", width=300).place(x=200,y=100)
        j = 1.5
        for i in d_fre.keys():

            Checkbutton(self.menu_frame, text=i, font=self.text_font,variable=self.dct_IntVar.get(d_fre[i])).place(x=100,y=100*j)
            #Label(self.menu_frame, font=self.text_font, text=i).grid(row=i + 2, column=2, pady=5)
            Message(self.menu_frame, font=self.text_font, text=d_fre[i], width=300).place(x=200,y=100*j)
            j+=0.5
        self.menu_frame.grid_propagate(0)


    def place_order(self):
        selected_items=[]
        for key,value in self.dct_IntVar.items():
            if(value.get()==1):
                selected_items.append(key)
        print(selected_items)
        if(len(selected_items)==0):
            messagebox.showwarning("No order","Please select atleast one product")
            return
        userItemData = pd.read_csv('ratings.csv')
        res = list(userItemData["ItemId"].tolist())
        self.order_confirmation(selected_items,res)

    def order_confirmation(self,selected_items,res):
        confirmation_window = Toplevel()
        f = Frame(confirmation_window, height=200, width=400)
        f.pack()
        purchased_items="\n".join(str(selected_items))
        total=0
        for item in selected_items:
            total+=item
        message=f"The cost of items purchased are \n {purchased_items} \n Total bill is {total}"
        l=Label(f,text=message)
        l.grid(row=1,column=0,columnspan=2)
        b1 = Button(f, text="Confirm", height=2, width=10,
                    command=lambda :self.send_order_to_admin(selected_items,total,confirmation_window))
        b1.grid(row=3, column=0, padx=10, sticky='e')
        b2 = Button(f, text="Reset", height=2, width=10)
        b2.grid(row=3, column=1, padx=10, sticky='w')
        f.grid_propagate(0)
    def recomendations(self):
        userItemData = pd.read_csv('ratings.csv')
        userItemData.head()
        itemList = list(set(userItemData["ItemId"].tolist()))
        userCount = len(set(userItemData["ItemId"].tolist()))

        itemAffinity = pd.DataFrame(columns=('item1', 'item2', 'score'))
        rowCount = 0
        for ind1 in range(len(itemList)):
            item1Users = userItemData[userItemData.ItemId == itemList[ind1]]["userId"].tolist()
            print("Item 1 ", item1Users)
            for ind2 in range(ind1, len(itemList)):
                if (ind1 == ind2):
                    continue
                item2Users = userItemData[userItemData.ItemId == itemList[ind2]]["userId"].tolist()
                print("Item 2", item2Users)
                commonUsers = len(set(item1Users).intersection(set(item2Users)))
                score = commonUsers / userCount
                itemAffinity.loc[rowCount] = [itemList[ind1], itemList[ind2], score]
                rowCount += 1
                itemAffinity.loc[rowCount] = [itemList[ind2], itemList[ind1], score]
                rowCount += 1

        print(itemAffinity.head())
        searchItem = itemList[1]
        recoList = itemAffinity[itemAffinity.item1 == searchItem] \
            [["item2", "score"]] \
            .sort_values("score", ascending=[0])
        self.menu_items_frame2 = Frame(self.menu_frame, height=350, width=350)
        self.menu_items_frame2.grid(row=5, column=5, pady=5)
        Label(self.menu_items_frame2, font="Times 12", text=str(recoList)).grid(row=1, column=1, pady=10)
        self.menu_items_frame2.grid_propagate(0)

    def send_order_to_admin(self,order_list,total,window):
        self.menu_items_frame1 = Frame(self.menu_frame, height=350, width=350)
        self.menu_items_frame1.grid(row=5, column=5,pady=5)
        b11 = Button(self.menu_items_frame1, text="Recomendations", height=2, width=20,
                    command=lambda: self.recomendations())
        b11.grid(row=3, column=1, padx=10, sticky='w')

        print(total)
        print(self.customer_details)
        self.menu_items_frame1.grid_propagate(0)
        window.destroy()
        messagebox.showinfo("Success","Thank you for placing the order with us.")

    def view_order_status(self):
        query="Select * from world.FoodOrder where IsComplete=0 and CustomerId=%d"
        args=(self.customer_details[0],)
        result=DatabaseHelper.get_data(query,args)
        if(result is None or len(result)==0):
            messagebox.showinfo("No order","You do not have any pending order with us.")
        else:
            details=result[2]
            total=result[3]
            message=f"Your order for {details} and total amount {total} is with us.Should be delivered soon"
            messagebox.showinfo("Pending order",message)

    def add_menu(self):
        self.menu_frame=Frame(self.panel,height=450,width=450,bg="white")
        self.menu_frame.place(x=400,y=110)
        self.menu_frame.pack_propagate(0)
        self.menu_img = ImageTk.PhotoImage(Image.open("2menu.jpg"))
        self.menu_panel = Label(self.menu_frame, image=self.menu_img)
        #self.menu_message = Message(self.menu_frame, width=600, font="Roman 20 bold italic",text="Menu", bg="white", relief=SOLID, borderwidth=2)
        #self.menu_message.place(x=200, y=10)

        self.check_buttons=[]

        self.menu_b3 = Button(self.menu_frame, text="Product Menu", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=lambda :self.add_menu_items())
        self.menu_b3.place(x=350,y=400)

        self.menu_b4 = Button(self.menu_frame, text="View Order Status", width=15, height=2, bg="ivory2", fg="black",activebackground="white",command=self.view_order_status)

        self.menu_b4.place(x=30,y=10)
        self.menu_panel.pack()
        self.menu_panel.grid_propagate(0)


if __name__ == '__main__':
    root=Tk()
    c=CustomerHomePage(root,(1,2,3,4))
    root.mainloop()