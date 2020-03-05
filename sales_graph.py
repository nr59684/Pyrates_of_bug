import matplotlib, numpy, sys
matplotlib.use('TkAgg')
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
def sales_graph():

    userItemData = pd.read_csv('ratings.csv')

    root = Tk.Tk()
    itemList2 = list(userItemData["ItemId"].tolist())
    for i in range(len(itemList2)):
        itemList2[i] = int(itemList2[i])
    d_fre = {}
    for item in itemList2:
        if (item in d_fre):
            d_fre[item] += 1
        else:
            d_fre[item] = 1
    f = Figure(figsize=(5,4), dpi=100)
    ax = f.add_subplot(111)
    objects = tuple(d_fre.keys())
    y_pos = np.arange(len(objects))
    data = tuple(d_fre.values())

    ind = numpy.arange(5)  # the x locations for the groups
    width = .5

    rects1 = ax.bar(ind, data, width)

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

