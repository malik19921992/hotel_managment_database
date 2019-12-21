#!/usr/bin/env python3

import tkinter
import tkinter.ttk as ttk
import tkinter.font as tkfont

'''
open test7.py:
from line 70

 find bbox
 use bbox to color square of selected aria

'''
# def setup_background():

#     global __font
#     global can

#     __font = tkfont.Font()
#     can = tkinter.Canvas(treeview,background="light green",borderwidth=0,highlightthickness=0)

def selectItem(event):

	x, y, widget = event.x, event.y, event.widget
	iid = widget.identify_row(y)
	item = widget.item(widget.focus())
	itemText = item['text']
	itemValues = item['values']
	column = event.widget.identify_column(x)

	print("                   ")
	print(f'item :         {item}'       )
	print(f'iid         :  {iid}'        )
	print(f'itemText    :  {itemText}'   )
	print(f'itemValues  :  {itemValues}' )
	print(f'column      :  {column}'     )


	#print(treeview.(x=123 y=30))

fen = tkinter.Tk()

can = tkinter.Canvas(fen , height=570,width=790,bg="light gray")

can.create_text(85,45,fill="black",font="albattar 20 bold",text="Hotel Name",tags="NAME")

treeview = ttk.Treeview(fen,columns=("Room Name","Room Type"))

style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 9,'bold'))

treeview.heading("#0", text="Room No")
treeview.column("#0", width = 90, anchor = "w")

treeview.heading("#1", text=" Room Name",anchor = "w")
treeview.column("#1", width = 200, anchor = "w")

treeview.heading("#2", text=" Room Type",anchor = "w")
treeview.column("#2", width = 270, anchor = "w")

treeview.pack()

treeview.place(x=10,y=80)




treeview.insert("" , "end" , text = "1", values = ('single room','one bed'))
treeview.insert("" , "end" , text = "2", values = ('single room','two beds'))

tkinter.Canvas(treeview,background="light green",borderwidth=0,highlightthickness=0)

treeview.tag_configure('bb', background='light gray')

treeview.bind('<ButtonRelease-1>', selectItem)

can.pack()

fen.mainloop()
