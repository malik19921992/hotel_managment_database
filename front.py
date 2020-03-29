#!/usr/bin/env python3

import tkinter
import tkinter.ttk as ttk
import tkinter.font as tkfont
import os
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

'''
open test7.py:
from line 70
 find bbox
 use bbox to color square of selected aria

def selectItem(event):
	global x,y,widget,iid,item,itemText,itemValues,column,cell_value
	print(f'event: {event}')
	print("================================")
	x, y, widget = event.x, event.y, event.widget
	iid = widget.identify_row(y)
	item = widget.item(widget.focus())
	itemText = item['text']
	itemValues = item['values']
	column = event.widget.identify_column(x)
	cell_value = itemValues[int(column[1]) - 1]
	print(f"x: {x} , y: {y}")
	print(f'widget: {widget}')
	print(event.widget)
	print("==================================")
	print('column[1] = ',column[1])
	print('cell_value = ',cell_value)
	print("===============================")
	print(f'item :         {item}'       )
	print(f'iid         :  {iid}'        )
	print(f'itemText    :  {itemText}'   )
	print(f'itemValues  :  {itemValues}' )
	print(f'column      :  {column}'     )
	#Leave method if mouse pointer clicks on Treeview area without data
	if not column or not iid:
		return
	#Leave method if selected item's value is empty
	if not len(itemValues):
		return
	#Get value of selected Treeview cell
	if column == "#0":
		cell_value = itemText
	else:
		cell_value = itemValues[int(column[1]) - 1]

	print('column[1] = ',column[1])
	print('self.cell_value = ',cell_value)
	#Leave method if selected Treeview cell is empty
	if not cell_value:
		return
	#Get the bounding box of selected cell, a tuple (x, y, w, h), where
	# x, y are coordinates of the upper left corner of that cell relative
	#      to the widget, and
	# w, h are width and height of the cell in pixels.
	# If the item is not visible, the method returns an empty string.
	bbox = widget.bbox(iid, column)
	print('bbox = ', bbox)
	if not bbox:
		return
	#Update and show selection in Canvas Overlay
	color_selection(bbox, column)
	print('Selected Cell Value = ', cell_value)
	#print(treeview.(x=123 y=30))


def color_selection(bbox, column):
	global canv
	print('@@@@ def show_selection(self, parent, bbox, column):')
	x, y,width, height = bbox
	fudgeTreeColumnx = 25 #Determined by trial & error
	fudgeColumnx = 15     #Determined by trial & error
	textw = __font.measure(cell_value)
	print('textw = ',textw)
	# Make Canvas size to fit selected cell
	canv.configure(width=width, height=height)
	#Position canvas-textbox in Canvas
	print('can.coords(canv_text) = ',canv.coords(canv_text))
	if column == "#0":
		canv.coords(canv_text,fudgeTreeColumnx,height/2)
	else:
		canv.coords(canv_text,(width-(textw-fudgeColumnx))/2.0,height/2)
	#Update value of canvas-textbox with the value of the selected cell. 
	canv.itemconfigure(canv_text,text=cell_value)
	#Overlay Canvas over Treeview cell
	canv.place(anchor=tkinter.NW, x=x, y=y)

'''

#COLORS:
LGREEN        =    "light green"
GREEN         =    "green"
RED           =    "red"
BLACK         =    "black"
WHITE         =    "white"
FIREBRICK1    =    "firebrick1"
LIGHTPINK1    =    "lightpink1"
PINK1         =    "pink1"
BROWN1        =    "brown1"

cars = ["Abarth","Alfa Romeo","Aston Martin","Audi","Bentley","BMW","Bugatti","Cadillac","Chevrolet","Chrysler","Citroën","Dacia","Daewoo","Daihatsu","Dodge","Donkervoort","DS","Ferrari","Fiat","Fisker","Ford","Honda","Hummer","Hyundai","Infiniti","Iveco","Jaguar","Jeep","Kia","KTM","Lada","Lamborghini","Lancia","Land Rover","Landwind","Lexus","Lotus","Maserati","Maybach","Mazda","McLaren","Mercedes-Benz","MG","Mini","Mitsubishi","Morgan","Nissan","Opel","Peugeot","Porsche","Renault","Rolls-Royce","Rover","Saab","Seat","Skoda","Smart","SsangYong","Subaru","Suzuki","Tesla","Toyota","Volkswagen","Volvo"]
item = {}

def Table_Height():
	global HEIGHT
	if len(item) <= 8 :
		HEIGHT =  len(item)
	elif len(item) > 8:
		HEIGHT = 8
	treeview.configure(height=HEIGHT)

	#show scrollbar if table length more than 14 raws:
	if HEIGHT >= 8:
		vsb = ttk.Scrollbar(fen, orient="vertical", command=treeview.yview)
		vsb.place(x=75+200+200+100+10, y=80, height=180)

def setup_background(BACKGROUND_COLOR,FONT_COLOR):
    global __font
    global canv
    global canv_text
    __font = tkfont.Font()
    canv = tkinter.Canvas(treeview,background=BACKGROUND_COLOR,borderwidth=0,highlightthickness=0)
    canv_text = canv.create_text(0, 0,fill=FONT_COLOR,anchor='w')


def internal_color_selection(bbox, column,cell_value):
	global canv
	#print('@@@@ def show_selection(self, parent, bbox, column):')
	x, y,width, height = bbox
	fudgeTreeColumnx = 25 #Determined by trial & error
	fudgeColumnx = 15     #Determined by trial & error
	textw = __font.measure(cell_value)
	#print('textw = ',textw)
	# Make Canvas size to fit selected cell
	canv.configure(width=width, height=height)
	#Position canvas-textbox in Canvas
	#print('can.coords(canv_text) = ',canv.coords(canv_text))
	if column == "#0":
		canv.coords(canv_text,fudgeTreeColumnx,height/2)
	else:
		canv.coords(canv_text,(width-(textw-fudgeColumnx))/2.0,height/2)
	#Update value of canvas-textbox with the value of the selected cell. 
	canv.itemconfigure(canv_text,text=cell_value)
	#Overlay Canvas over Treeview cell
	canv.place(anchor=tkinter.NW, x=x, y=y)


def internalSelectItem(COLUMN_NUM,RAW_NUM,ITEM,BACKGROUND_COLOR,FONT_COLOR,COLUMN_NAME):
	setup_background(BACKGROUND_COLOR,FONT_COLOR)
	curitem = treeview.focus()
	item = treeview.item(ITEM)
	itemText = item['text']
	itemValues = item['values']
	iid = f'I00{RAW_NUM}'
	itemText = RAW_NUM
	column = f'#{COLUMN_NUM}'
	cell_value = itemValues[int(column[1]) - 1]
	fen.update()
	bbox = treeview.bbox(iid, column=COLUMN_NAME)
	# print("internal use function")
	# print("================================")
	# print(f'item: {item}'                )
	# print(f'itemtext: {itemText}'        )
	# print(f'itemValues: {itemValues}'    )
	# print(f'cell_value: {cell_value}'    )
	# print(f'iid: {iid}'                  )
	# print(f'column      :  {column}'     )
	# print(f'column[1] = {column[1] }'    )
	# print(f'bbox = {bbox}'               )
	if not bbox:
		return
	#Update and show selection in Canvas Overlay
	internal_color_selection(bbox, column,cell_value)


def callback():
	print(value1)

def country_choice():
	# if you want to print all list with details
	# import pprint
	# pprint.pprint(dict(countrylist))
	print(countrylist.current(), countrylist.get())

####################################################
#date list:#########################################
date_list = []

six_months_after = date.today() + relativedelta(months=+6)
six_months_before = date.today() + relativedelta(months=-6)
m_before    =   six_months_after.month
m_after     =   six_months_after.month
d_before    =   six_months_before.day
d_after     =   six_months_after.day
y_before    =   six_months_before.year
y_after     =   six_months_after.year

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt = date(y_before,m_before,d_before)
end_dt = date(y_after,m_after,d_after)
for dt in daterange(start_dt, end_dt):
    date_list.append(dt.strftime("%Y-%m-%d"))
######################################################

fen = tkinter.Tk()
fen.title('Hotel')
can = tkinter.Canvas(fen , height=570,width=790,bg="light gray")
can.create_text(85,45,fill="black",font="albattar 20 bold",text="Hotel Name",tags="NAME")
#height=4 for only 4 lines:
HEIGHT=0
treeview = ttk.Treeview(fen,columns=("Room Name","Room Type","Room Status") ,height=HEIGHT)
style = ttk.Style()
#adjust hieght for each rows
style.configure("Treeview.Heading", font=(None, 9,'bold'),background="light gray")
treeview.heading("#0", text="Room No", anchor = "w")
treeview.column("#0", width = 75, anchor = "w")
treeview.heading("#1", text=" Room Name",anchor = "w")
treeview.column("#1", width = 200, anchor = "w")
treeview.heading("#2", text=" Room Type",anchor = "w")
treeview.column("#2",width=200,anchor = "w")  #width = 270
treeview.heading("#3", text="Room Status",anchor = "c")
treeview.column("#3",width=100,anchor = "c")
#rectangle in background
can.create_rectangle(9, 80, 600, 261, outline="white", fill="grey")
treeview.pack(fill=tkinter.BOTH,expand=1)
treeview.place(x=10,y=80)
#=============================================================================================
item[0] = treeview.insert("" , "end" , text = "1", values = ('single room','one bed','IN USE'),tag='gray')
Table_Height()
#internalSelectItem(3,1,item0,BROWN1,WHITE,"Room Status")
#=============================================================================================
item[1] = treeview.insert("" , "end" , text = "2", values = ('single room','two beds','Free'))
Table_Height()
#internalSelectItem(3,2,item1,LGREEN,BLACK,"Room Status")
#=============================================================================================
item[2] = treeview.insert("" , "end" , text = "3", values = ('single room','tow beds','IN USE'),tag='gray')
Table_Height()
#internalSelectItem(3,3,item2,BROWN1,WHITE,"Room Status")
#=============================================================================================
item[3] = treeview.insert("" , "end" , text = "4", values = ('single room','one bed','Free'))
Table_Height()
#internalSelectItem(3,4,item3,LGREEN,BLACK,"Room Status")
#===========================================================================================
item[4]   =  treeview.insert("" , "end" , text = "5", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
item[5]   =  treeview.insert("" , "end" , text = "6", values = ('single room','one bed','Free'))
Table_Height()
item[6]   =  treeview.insert("" , "end" , text = "7", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
item[7]   =  treeview.insert("" , "end" , text = "8", values = ('single room','one bed','Free'))
Table_Height()
item[8]   =  treeview.insert("" , "end" , text = "9", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
item[9]   =  treeview.insert("" , "end" , text = "10", values = ('single room','one bed','Free'))
Table_Height()
item[10]  =  treeview.insert("" , "end" , text = "11", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
item[11]  =  treeview.insert("" , "end" , text = "12", values = ('single room','one bed','Free'))
Table_Height()
item[12]  =  treeview.insert("" , "end" , text = "13", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
item[13]  =  treeview.insert("" , "end" , text = "14", values = ('single room','one bed','Free'))
Table_Height()
item[14]  =  treeview.insert("" , "end" , text = "15", values = ('single room','one bed','Free'),tag='gray')
Table_Height()
#print(item.keys())
#print(len(item))
def v(event):
	pass
######################################################################################
#rooms view options:##################################################################
Room_View = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
Room_View.place(relx=0.77, rely=0.217, anchor=tkinter.NW)
tkinter.Label(fen, text='Rooms View Options').place(relx=.79, rely=0.217,anchor=tkinter.W)
tkinter.Label(Room_View, text="   Only Show:                   ").pack(pady=10)
buttom1 = tkinter.Radiobutton(Room_View, text='All Rooms',variable=v,value=3).pack( side=tkinter.TOP, anchor=tkinter.NW)
buttom2 = tkinter.Radiobutton(Room_View, text='Free Rooms',variable=v,value=3).pack( side=tkinter.TOP, anchor=tkinter.NW)
buttom3 = tkinter.Radiobutton(Room_View, text='Rooms In Use',variable=v,value=3).pack( side=tkinter.TOP, anchor=tkinter.NW)
tkinter.Label(Room_View, text="             ").pack(side=tkinter.TOP, anchor=tkinter.NW)
#tkinter.Label(Room_View, text="             ").pack(side=tkinter.TOP, anchor=tkinter.NW)
#tkinter.Label(Room_View, text="             ").pack(side=tkinter.TOP, anchor=tkinter.NW)
###########################################################################################
#clock:####################################################################################
Time = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
Time.place(relx=0.77, rely=0.07, anchor=tkinter.NW)
tkinter.Label(fen, text='Time').place(relx=.79, rely=0.07,anchor=tkinter.W)
#tkinter.Label(Time, text="    ").pack(side=tkinter.TOP, anchor=tkinter.S)
#tkinter.Label(Time, text="   ").pack(side=tkinter.TOP, anchor=tkinter.S)
clock = tkinter.Label(Time, text="  03:09:30  ",font=("Helvetica", 24)).pack(side=tkinter.TOP, anchor=tkinter.W)
tkinter.Label(Time, text="Tuesday, 19 June 2020").pack(side=tkinter.TOP, anchor=tkinter.S)
#tkinter.Label(Time, text="   ").pack(side=tkinter.TOP, anchor=tkinter.S)
##########################################################################################
#Cashier operations:######################################################################
Cashier = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
Cashier.place(relx=0.015, rely=0.48, anchor=tkinter.NW)
tkinter.Label(fen, text='Cashier operations',background="light gray").place(relx=.12, rely=0.48,anchor=tkinter.W)
#Create and pack the NoteBook.############################################################
#tkinter.Label(Cashier, text=" "*145).pack(side=tkinter.TOP, anchor=tkinter.S)
nb = ttk.Notebook(Cashier,style="Treeview.Heading")
nb.pack(fill=tkinter.BOTH, expand=tkinter.Y, padx=2, pady=10)
#Make 1st tab
f1 = tkinter.Frame(nb,background="light gray")
#Add the tab
nb.add(f1, text=" Rooms Options ")
#Make 2nd tab
f2 = tkinter.Frame(nb,background="light gray")
#Add 2nd tab 
#do print puttom for checkin in or when finish it you do print automatickly
nb.add(f2, text=" CheckIn ")
nb.select(f2)
#Add 3rd tab
f3 = tkinter.Frame(nb,background="light gray")
#do print puttom for checkout in or when finish it you do print automatickly
nb.add(f3, text=" CheckOut ")
nb.select(f3)
###########################################################################################################################
#rooms options:############################################################################################################
tkinter.Button(f1, text='new Room   ',background="light gray").grid(row=0, column=0,sticky='sw')
tkinter.Button(f1,text='save Room  ',background="light gray").grid(row=0, column=1,sticky='sw')
tkinter.Button(f1,text='delete Room',background="light gray").grid(row=0, column=2,sticky='sw')
tkinter.Label(f1,text="Room Number ",background="light gray").grid(row=1,column=0,sticky='w')
groove_entry1 = tkinter.Entry(f1, font=10,relief="groove",background="white").grid(row=1,column=1,columnspan=2,sticky='nw')
tkinter.Label(f1,text="Room Name ",background="light gray").grid(row=2,column=0,sticky='w')
groove_entry2 = tkinter.Entry(f1,font=10,relief="groove",background="white").grid(row=2,column=1,columnspan=2,sticky='nw')
tkinter.Label(f1,text="Room Type ",background="light gray").grid(row=3,column=0,sticky='w')
groove_entry3 = tkinter.Entry(f1,font=10,relief="groove",background="white").grid(row=3,column=1,columnspan=2,sticky='nw')
tkinter.Label(f1,text="Status   ",background="light gray").grid(row=1,column=3,sticky='w')
status_free = tkinter.Label(f1, text="       Free         ",background="pale green",relief="solid").grid(row=1,column=4,sticky='w')
#status_inuse = tkinter.Label(f1, text="      IN USE      ",background="tomato",relief="solid").grid(row=1,column=4)
tkinter.Label(f1,text="Remain Time ",background="light gray").grid(row=2,column=3,sticky='w')
tkinter.Label(f1, text="    1m/3d/3h    ",background="white",relief="solid").grid(row=2,column=4,sticky='w')
tkinter.Label(f1,text="Details       ",background="light gray").grid(row=3,column=3,sticky='w')
groove_entry4 = tkinter.Entry(f1,font=10,relief="groove",background="white").grid(row=3,column=4,columnspan=5,sticky='ns')
tkinter.Label(f1,text="Room Side  ",background="light gray").grid(row=4,column=0,sticky='w')
groove_entry5 = tkinter.Entry(f1,font=10,relief="groove",background="white").grid(row=4,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f1,text="Beds  ",background="light gray").grid(row=4,column=3,sticky='w')
groove_entry6 = tkinter.Entry(f1,font=10,relief="groove",background="white").grid(row=4,column=4,columnspan=5,sticky='nsw')
############################################################################################################################
#CHECK IN:
#Guest information:
###################################################################################
#buttons:
tkinter.Button(f2, text='Print',background="light gray").grid(row=0, column=0,sticky='we')
tkinter.Button(f2,text='Change Room',background="light gray").grid(row=0, column=1,sticky='we')
tkinter.Button(f2,text='Update',background="light gray").grid(row=0, column=2,sticky='we')
tkinter.Button(f2,text='Cancel',background="light gray",width=11).grid(row=0, column=3,columnspan=5,sticky='we')
###################################################################################
tkinter.Label(f2,text="Folio No: ",background="light gray").grid(row=1,column=0,sticky='w')
# w = tkinter.Text(f2, height=1,width=10,bg="white")
# w.insert(1.0,"009-098")
# w.grid(row=1,column=1,columnspan=2,sticky='nsw')
groove_entry0 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
groove_entry0.grid(row=1,column=1,columnspan=2,sticky='nsw')
groove_entry0.insert(0,"009-098")
tkinter.Label(f2,text="First name ",background="light gray").grid(row=2,column=0,sticky='w')
groove_entry1 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=2,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text="Last name ",background="light gray").grid(row=3,column=0,sticky='w')
groove_entry2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=3,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text="RCard No ",background="light gray").grid(row=4,column=0,sticky='w')
groove_entry3 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=4,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text="Country ",background="light gray").grid(row=5,column=0,sticky='w')
#country list
with open(os.path.join( os.getcwd(), 'country.txt')) as f: lineList = f.readlines()
countrylist = ttk.Combobox(f2,values=list(map(lambda x:x.strip(),lineList)),width=10)
countrylist.grid(row=5,column=1,sticky='w')
#to choose first country as first choice
#countrylist.current(1)
#print country name you choosed
#tkinter.Button(f2, text='print month',background="light gray",command=country_choice).grid(row=5, column=0,sticky='sw' )
tkinter.Label(f2,text="Adress ",background="light gray").grid(row=6,column=0,sticky='w')
groove_entry4 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=6,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text=" ID_Type ",background="light gray").grid(row=7,column=0,sticky='w')
ID_TYPE_LIST = ttk.Combobox(f2,values=["(SSN)Social Security Number","Passport number","Driver license","taxpayer ID number","patient ID number"],width=10).grid(row=7,column=1,sticky='w')
tkinter.Label(f2,text=" ID_No ",background="light gray").grid(row=8,column=0,sticky='w')
groove_entry5 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=8,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text="Car ",background="light gray").grid(row=1,column=2,sticky='w')
carlist = ttk.Combobox(f2,values=cars,width=10).grid(row=1,column=3,columnspan=5,sticky='w')
tkinter.Label(f2,text="Plate NO ",background="light gray").grid(row=2,column=2,sticky='w')
groove_entry6 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=2,column=3,columnspan=5,sticky='nsw')
tkinter.Label(f2,text="Room NO ",background="light gray").grid(row=3,column=2,sticky='w')
groove_entry7 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
groove_entry7.grid(row=3,column=3,sticky='nsw')
groove_entry7.insert(0, "12")
# Room_No = tkinter.Text(f2, height=1,width=10,bg="white")
# Room_No.insert(1.0,"009-098")
# Room_No.grid(row=1,column=1,columnspan=2,sticky='nsw')
tkinter.Label(f2,text="Date In: ",background="light gray").grid(row=4,column=2,sticky='w')
DateIn = ttk.Combobox(f2,values=date_list,width=11)
#choose the date today as first choise
DateIn.grid(row=4,column=3,columnspan=5,sticky='w')
DateIn.current(date_list.index(date.today().strftime("%Y-%m-%d")))
tkinter.Label(f2,text="Date Out: ",background="light gray").grid(row=5,column=2,sticky='w')
DateOut = ttk.Combobox(f2,values=date_list,width=11).grid(row=5,column=3,columnspan=5,sticky='w')
tkinter.Label(f2,text="No. of Days ",background="light gray").grid(row=6,column=2,sticky='w')
groove_entry8 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
groove_entry8.grid(row=6,column=3,sticky='nsw')
groove_entry8.insert(0, "7")
tkinter.Button(f2, text='⯇',background="light gray").grid(row=6, column=4,sticky='we')
tkinter.Button(f2, text='⯈',background="light gray").grid(row=6, column=5,sticky='we')
tkinter.Label(f2,text="No.of Adults",background="light gray").grid(row=7,column=2,sticky='w')
groove_entry9 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
groove_entry9.grid(row=7,column=3,sticky='nsw')
groove_entry9.insert(0, "1")
tkinter.Button(f2, text='⯇',background="light gray").grid(row=7, column=4,sticky='we')
tkinter.Button(f2, text='⯈',background="light gray").grid(row=7, column=5,sticky='we')
tkinter.Label(f2,text="No.of Childs",background="light gray").grid(row=8,column=2,sticky='w')
groove_entry10 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
groove_entry10.grid(row=8,column=3,sticky='nsw')
groove_entry10.insert(0, "0")
tkinter.Button(f2, text='⯇',background="light gray").grid(row=8, column=4,sticky='we')
tkinter.Button(f2, text='⯈',background="light gray").grid(row=8, column=5,sticky='we')
tkinter.Label(f2,text="Rate Type",background="light gray").grid(row=1,column=6,sticky='w')
Rate_Type = ttk.Combobox(f2,values=['Standard','Deluxe','Off-Season','Royal','Dopule Joint','Suite','Prepaid','Loyalty','Membership','Special','Group','Family','Package'],width=11).grid(row=1,column=7,sticky='w')


#alternate rows colors#######################################################
treeview.tag_configure('gray', background='#cccccc')
treeview.tag_configure('bb', background='light gray')
#treeview.bind('<ButtonRelease-1>', selectItem)
can.pack()
fen.mainloop()


