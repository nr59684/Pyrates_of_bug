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

