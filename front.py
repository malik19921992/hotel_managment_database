#!/usr/bin/env python3

import tkinter
import tkinter.ttk as ttk
import tkinter.font as tkfont
import os
from datetime import timedelta, date , datetime
from dateutil.relativedelta import relativedelta
import sqlite3

#VARS:
TABLE_HEIGHT=0
COLOR_TAG = {}
COLOR_CHOICE = 0
COLOR_TAG[0] = 'gray'
COLOR_TAG[1] = 'white'
######COLORS:
LGREEN        =    "light green"
GREEN         =    "green"
RED           =    "red"
BLACK         =    "black"
WHITE         =    "white"
FIREBRICK1    =    "firebrick1"
LIGHTPINK1    =    "lightpink1"
PINK1         =    "pink1"
BROWN1        =    "brown1"
first_list_Scorll_X = 562
first_list_Scorll_Y = 80
cars = ["Abarth","Alfa Romeo","Aston Martin","Audi","Bentley","BMW","Bugatti","Cadillac","Chevrolet","Chrysler","Citroën","Dacia","Daewoo","Daihatsu","Dodge","Donkervoort","DS","Ferrari","Fiat","Fisker","Ford","Honda","Hummer","Hyundai","Infiniti","Iveco","Jaguar","Jeep","Kia","KTM","Lada","Lamborghini","Lancia","Land Rover","Landwind","Lexus","Lotus","Maserati","Maybach","Mazda","McLaren","Mercedes-Benz","MG","Mini","Mitsubishi","Morgan","Nissan","Opel","Peugeot","Porsche","Renault","Rolls-Royce","Rover","Saab","Seat","Skoda","Smart","SsangYong","Subaru","Suzuki","Tesla","Toyota","Volkswagen","Volvo"]
date_list = []

#database functions:########################################################################
def create_main_database():
    conn = sqlite3.connect('__main.db')
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS table_name(
                Room_No INT PRIMARY KEY NOT NULL,
                Room_Name TEXT NOT NULL,
                Room_Type TEXT NOT NULL,
                Room_Status TEXT NOT NULL ) ''' )
    conn.commit()
    conn.close()

def insert_to_database(Room_No,Room_Name,Room_Type,Room_Status):
    conn = sqlite3.connect("__main.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO table_name VALUES (?,?,?,?)"
            ,(Room_No,Room_Name,Room_Type,Room_Status))
    conn.commit()
    c.close()

def database_items_count():
	conn =None;
	conn = sqlite3.connect("__main.db")
	c = conn.cursor()
	c.execute(''' SELECT COUNT(*) FROM table_name ''')
	result=c.fetchone()
	return result[0]
	# rows = c.fetchall()
	# return len(rows)+1
	c.close()

def check_if_room_in_database(NUM):
	my_list = []
	# print('check started')
	conn =None;
	conn = sqlite3.connect("__main.db")
	c = conn.cursor()
	c.execute(''' SELECT * FROM table_name ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(int(row[0]))
	return int(NUM) in my_list

def database_room_update(NUM,NAME,TYPE):
	#print(NUM,NAME,TYPE)
	conn =None;
	conn = sqlite3.connect("__main.db")
	c = conn.cursor()
	c.execute('UPDATE table_name SET Room_Name = ? , Room_Type = ? WHERE Room_No = ? ',(NAME,TYPE,NUM))
	conn.commit()
	c.close()


def database_room_delete(NUM):
	conn =None;
	conn = sqlite3.connect("__main.db")
	c = conn.cursor()
	c.execute("DELETE from table_name where Room_No = ?",(NUM,))
	conn.commit()
	c.close()

def databse_inserts():
	insert_to_database(3,'Dobule Room','two besds','Free')
	insert_to_database(4,'Dobule Room','two besds','Free')
	insert_to_database(5,'Dobule Room','two besds','Free')
	insert_to_database(6,'Dobule Room','two besds','Free')
	insert_to_database(7,'Dobule Room','two besds','Free')
	insert_to_database(8,'Dobule Room','two besds','Free')
	insert_to_database(9,'Dobule Room','two besds','Free')

def view_selected_data(STATUS,TYPE,NUM):
	my_list = []
	conn = sqlite3.connect('__main.db')
	c = conn.cursor()
	if NUM == 'All' and TYPE == 'All' and STATUS == 'All':
		c.execute(''' SELECT * FROM table_name ORDER BY Room_No ''' )
	elif NUM != 'All':
		c.execute("SELECT * FROM table_name WHERE Room_No=? ", (NUM,))
	elif TYPE != 'All':
		c.execute(" SELECT * FROM table_name WHERE Room_Type LIKE ? ORDER BY Room_No ", (TYPE,) )
	elif STATUS != 'All':
		c.execute('SELECT * FROM table_name WHERE Room_Status LIKE ? ORDER BY Room_No',(STATUS,))
	elif TYPE != 'All' and STATUS != 'All':
		c.execute('SELECT * FROM table_name WHERE Room_Status LIKE ? and Room_Type LIKE ? ORDER BY Room_No',(STATUS,TYPE,))
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list

#################################################################################
##################
#OTHER functions:#
##################

def treeview_rate_options_table(MASTER):
	f4 = MASTER
	global treeview2
	tkinter.Label(f4,text=" ",background="light gray").grid(row=2,column=1,sticky='w')
	can4 = tkinter.Canvas(f4,background="light gray",width=200,height=180)
	RATE_X = 0
	RATE_Y = 0
	can4.create_rectangle(RATE_X,RATE_Y,RATE_X+634,RATE_Y+181, fill="gray")
	can4.grid(row=3,column=1,columnspan=10,sticky='wesn')
	#column names
	# treeview_table_generator(f4,2,["Room Type","Room Rate","max Person",'Extra Adults Rate','Extra Children Rate'],[65,84,84,95,134,153],10,80,TABLE_HEIGHT)
	# Style_generator(2,None,9,'light gray')

	treeview2 = ttk.Treeview(f4,columns=("Room Type","Room Rate","No. of Person",'Extra Adults Rate','Extra Children Rate') ,height=8)
	#headings:
	treeview2.heading("#0", text="Room No", anchor = "w")
	treeview2.heading("#1", text=" Room Type",anchor = "w")
	treeview2.heading("#2", text=" Room Rate",anchor = "w")
	treeview2.heading("#3", text="No. of Person",anchor = "w")
	treeview2.heading("#4", text="Extra Adults's Rate",anchor = "c")
	treeview2.heading("#5", text="Extra Children's Rate",anchor = "c")
	#columns:
	treeview2.column("#0", width = 65, anchor = "w")
	treeview2.column("#1", width = 84, anchor = "w")
	treeview2.column("#2", width = 84, anchor = "w")
	treeview2.column("#3",width=95,anchor = "w")
	treeview2.column("#4",width=134,anchor = "w")
	treeview2.column("#5",width=153,anchor = "w")
	# geomitry:
	treeview2.grid(row=3,column=1,columnspan=10,sticky='wesn')
	treeview2.place(x=1,y=74)
	################################
	secound_list_Scorll_X = 569+50
	secound_list_Scorll_Y = 75
	item2 = {}
	item2[0] = treeview2.insert("" , "end" , text = "1", values = ('Standard','1,458.00','2','351.00','0.00'))
	item2[0] = treeview2.insert("" , "end" , text = "1", values = ('Standard','1,458.00','2','351.00','0.00'),tag='bb')
	# Table_Height(f4,secound_list_Scorll_X,secound_list_Scorll_Y)
	treeview2.tag_configure('gray', background='#cccccc')
	treeview2.tag_configure('bb', background='light gray')


def Cashier_operations():
	# global f1
	Cashier = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Cashier.place(relx=0.015, rely=0.48, anchor=tkinter.NW)
	tkinter.Label(fen, text='Cashier operations',background="light gray").place(relx=.12, rely=0.48,anchor=tkinter.W)
	nb = ttk.Notebook(Cashier,style="Treeview.Heading")
	nb.pack(fill=tkinter.BOTH, expand=tkinter.Y, padx=2, pady=10)
	f1 = tkinter.Frame(nb,background="light gray")
	f2 = tkinter.Frame(nb,background="light gray")	
	f3 = tkinter.Frame(nb,background="light gray")
	f4 = tkinter.Frame(nb,background="light gray")
	nb.add(f1, text=" Room Settings ")
	nb.add(f2, text=" CheckIn ")
	nb.add(f3, text=" CheckOut ")
	nb.add(f4, text=" Room Price OPtions ")
	nb.select(f2)
	nb.select(f3)
	nb.select(f4)
	nb.select(f1)
	rooms_options(f1)
	CHECK_IN(f2)
	CHECK_OUT(f3)
	room_price_options(f4)
	treeview_rate_options_table(f4)

def room_price_options(MASTER):
	f4 = MASTER
	#BUTTONS:
	tkinter.Button(f4, text='Update',background="light gray").grid(row=1, column=6,sticky='we')
	tkinter.Button(f4, text='Update All',background="light gray").grid(row=1, column=7,sticky='we')
	#LABELS:
	tkinter.Label(f4,text="Rate Type",background="light gray").grid(row=0,column=1,sticky='w')
	tkinter.Label(f4,text="Room Rate",background="light gray").grid(row=0,column=2,sticky='w')
	tkinter.Label(f4,text="No. of Person",background="light gray").grid(row=0,column=3,sticky='w')
	tkinter.Label(f4,text="Adult's Rate",background="light gray").grid(row=0,column=4,sticky='w')
	tkinter.Label(f4,text="Children's Rate",background="light gray").grid(row=0,column=5,sticky='w')
	#ENTRIES:
	groove_entry34 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry34.grid(row=1,column=2,sticky='nsw')
	groove_entry34.insert(0, " ")
	groove_entry35 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry35.grid(row=1,column=3,sticky='nsw')
	groove_entry35.insert(0, " ")
	groove_entry36 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry36.grid(row=1,column=4,sticky='nsw')
	groove_entry36.insert(0, " ")
	groove_entry37 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry37.grid(row=1,column=5,sticky='ns')
	groove_entry37.insert(0, " ")
	#LISTS:
	Rate_Type = ttk.Combobox(f4,values=['Standard','Deluxe','Off-Season','Royal','Dopule Joint','Suite','Prepaid','Loyalty','Membership','Special','Group','Family','Package'],width=11)
	Rate_Type.grid(row=1,column=1,sticky='w')
	Rate_Type.current(1)


def CHECK_OUT(MASTER):
	f3 = MASTER
	#BUTTONS:
	tkinter.Button(f3, text='CheckOut',background="light gray").grid(row=0, column=0,sticky='we')
	tkinter.Button(f3,text='Cancel',background="light gray").grid(row=0, column=1,sticky='we')
	#tkinter.Button(f3, text='⯇',background="light gray").grid(row=4, column=4,sticky='w')
	#tkinter.Button(f3, text='⯈',background="light gray").grid(row=4, column=5,sticky='w')
	#tkinter.Button(f3, text='⯇',background="light gray").grid(row=2, column=4,sticky='w')
	#tkinter.Button(f3, text='⯈',background="light gray").grid(row=2, column=5,sticky='w')
	#tkinter.Button(f3, text='⯇',background="light gray").grid(row=3, column=4,sticky='w')
	#tkinter.Button(f3, text='⯈',background="light gray").grid(row=3, column=5,sticky='w')
	#LABELS:
	tkinter.Label(f3,text="Guest Name ",background="light gray").grid(row=1,column=0,sticky='w')
	tkinter.Label(f3,text="Folio No ",background="light gray").grid(row=2,column=0,sticky='w')
	tkinter.Label(f3,text="Room No",background="light gray").grid(row=3,column=0,sticky='w')
	tkinter.Label(f3,text="Date In",background="light gray").grid(row=4,column=0,sticky='w')
	tkinter.Label(f3,text="Date Out",background="light gray").grid(row=5,column=0,sticky='w')
	tkinter.Label(f3,text="Rate Type",background="light gray").grid(row=6,column=0,sticky='w')
	tkinter.Label(f3,text="Rate/Piriod",background="light gray").grid(row=7,column=0,sticky='w')
	tkinter.Label(f3,text="No. of Days",background="light gray").grid(row=2,column=2,sticky='w')
	tkinter.Label(f3,text="No.of Adults",background="light gray").grid(row=3,column=2,sticky='w')
	tkinter.Label(f3,text="No.of Children",background="light gray").grid(row=4,column=2,sticky='w')
	tkinter.Label(f3,text="Other Charges",background="light gray").grid(row=5,column=2,sticky='w')
	tkinter.Label(f3,text="Sub Total",background="light gray").grid(row=6,column=2,sticky='w')
	tkinter.Label(f3,text="Dicount",background="light gray").grid(row=7,column=2,sticky='w')
	tkinter.Label(f3,text="%",background="light gray").grid(row=7,column=5,sticky='w')
	tkinter.Label(f3,text="Total",background="light gray").grid(row=1,column=6,sticky='w')
	tkinter.Label(f3,text="Amount Paid",background="light gray").grid(row=2,column=6,sticky='w')
	tkinter.Label(f3,text="Balance",background="light gray").grid(row=3,column=6,sticky='w')
	#ENTRIES:
	groove_entry20 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=32)
	groove_entry20.grid(row=1,column=1,columnspan=5,sticky='nsw')
	groove_entry20.insert(0, "abdul-malek mohammed aladeen")
	groove_entry19 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry19.grid(row=2,column=1,sticky='nsw')
	groove_entry19.insert(0, "009-098")
	groove_entry21 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry21.grid(row=3,column=1,sticky='nsw')
	groove_entry21.insert(0, "12")
	groove_entry22 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry22.grid(row=4,column=1,sticky='nsw')
	groove_entry22.insert(0, "2020-03-30")
	groove_entry22 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry22.grid(row=5,column=1,sticky='nsw')
	groove_entry22.insert(0, "2020-04-30")
	groove_entry23 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry23.grid(row=6,column=1,sticky='nsw')
	groove_entry23.insert(0, "Double")
	groove_entry24 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry24.grid(row=7,column=1,sticky='nsw')
	groove_entry24.insert(0, "998.00")
	groove_entry25 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry25.grid(row=2,column=3,sticky='w')
	groove_entry25.insert(0, "30")
	groove_entry26 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry26.grid(row=3,column=3,sticky='w')
	groove_entry26.insert(0, "2")
	groove_entry27 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry27.grid(row=4,column=3,sticky='w')
	groove_entry27.insert(0, "0")
	groove_entry28 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=9)
	groove_entry28.grid(row=5,column=3,columnspan=5,sticky='nsw')
	groove_entry28.insert(0, "0.00")
	groove_entry29 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=9)
	groove_entry29.grid(row=6,column=3,columnspan=5,sticky='nsw')
	groove_entry29.insert(0, "2,916.00")
	groove_entry30 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=6)
	groove_entry30.grid(row=7,column=3,columnspan=4,sticky='nsw')
	groove_entry30.insert(0, "0.00")
	groove_entry31 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry31.grid(row=1,column=8,sticky='nsw')
	groove_entry31.insert(0, "2,916.00")
	groove_entry32 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry32.grid(row=2,column=8,sticky='nsw')
	groove_entry32.insert(0, "0.00")
	groove_entry33 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry33.grid(row=3,column=8,sticky='nsw')
	groove_entry33.insert(0, "2,916.00")

def CHECK_IN(MASTER):
	f2 = MASTER
	#BUTTONS:
	tkinter.Button(f2, text='Print',background="light gray").grid(row=0, column=0,sticky='we')
	tkinter.Button(f2,text='Change Room',background="light gray").grid(row=0, column=1,sticky='we')
	tkinter.Button(f2,text='Update',background="light gray").grid(row=0, column=2,sticky='we')
	tkinter.Button(f2,text='Cancel',background="light gray",width=11).grid(row=0, column=3,columnspan=3,sticky='we')
	tkinter.Button(f2, text='⯇',background="light gray").grid(row=6, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray").grid(row=6, column=5,sticky='we')
	tkinter.Button(f2, text='⯇',background="light gray").grid(row=7, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray").grid(row=7, column=5,sticky='we')
	tkinter.Button(f2, text='⯇',background="light gray").grid(row=8, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray").grid(row=8, column=5,sticky='we')
	#LABELS:
	tkinter.Label(f2,text="Folio No: ",background="light gray").grid(row=1,column=0,sticky='w')
	tkinter.Label(f2,text="First name ",background="light gray").grid(row=2,column=0,sticky='w')
	tkinter.Label(f2,text="Last name ",background="light gray").grid(row=3,column=0,sticky='w')
	tkinter.Label(f2,text="RCard No ",background="light gray").grid(row=4,column=0,sticky='w')
	tkinter.Label(f2,text="Country ",background="light gray").grid(row=5,column=0,sticky='w')
	tkinter.Label(f2,text="Adress ",background="light gray").grid(row=6,column=0,sticky='w')
	tkinter.Label(f2,text=" ID_Type ",background="light gray").grid(row=7,column=0,sticky='w')
	tkinter.Label(f2,text=" ID_No ",background="light gray").grid(row=8,column=0,sticky='w')
	tkinter.Label(f2,text="Car ",background="light gray").grid(row=1,column=2,sticky='w')
	tkinter.Label(f2,text="Plate NO ",background="light gray").grid(row=2,column=2,sticky='w')
	tkinter.Label(f2,text="Room NO ",background="light gray").grid(row=3,column=2,sticky='w')
	tkinter.Label(f2,text="Date In: ",background="light gray").grid(row=4,column=2,sticky='w')
	tkinter.Label(f2,text="Date Out: ",background="light gray").grid(row=5,column=2,sticky='w')
	tkinter.Label(f2,text="No. of Days ",background="light gray").grid(row=6,column=2,sticky='w')
	tkinter.Label(f2,text="No.of Adults",background="light gray").grid(row=7,column=2,sticky='w')
	tkinter.Label(f2,text="No.of Childs",background="light gray").grid(row=8,column=2,sticky='w')
	tkinter.Label(f2,text="Rate Type",background="light gray").grid(row=1,column=6,sticky='w')
	tkinter.Label(f2,text="Rate/Period",background="light gray").grid(row=2,column=6,sticky='w')
	tkinter.Label(f2,text="Total Charge",background="light gray").grid(row=3,column=6,sticky='w')
	tkinter.Label(f2,text="Other Charges",background="light gray").grid(row=4,column=6,sticky='w')
	tkinter.Label(f2,text="Sub Total",background="light gray").grid(row=5,column=6,sticky='w')
	tkinter.Label(f2,text="Discount",background="light gray").grid(row=5,column=6,sticky='w')
	tkinter.Label(f2,text="%",background="light gray").grid(row=5,column=8,sticky='e')
	tkinter.Label(f2,text="Total",background="light gray").grid(row=6,column=6,sticky='w')
	tkinter.Label(f2,text="Amount Paid",background="light gray").grid(row=7,column=6,sticky='w')
	tkinter.Label(f2,text="Balance",background="light gray").grid(row=8,column=6,sticky='w')
	#LISTS:
	with open(os.path.join( os.getcwd(), 'country.txt')) as f: lineList = f.readlines()
	countrylist = ttk.Combobox(f2,values=list(map(lambda x:x.strip(),lineList)),width=10)
	countrylist.grid(row=5,column=1,sticky='w')
	countrylist.current(1)
	ID_TYPE_LIST = ttk.Combobox(f2,values=["(SSN)Social Security Number","Passport number","Driver license","taxpayer ID number","patient ID number"],width=10).grid(row=7,column=1,sticky='w')
	carlist = ttk.Combobox(f2,values=cars,width=10).grid(row=1,column=3,columnspan=5,sticky='w')
	DateIn = ttk.Combobox(f2,values=date_list,width=11)
	DateIn.grid(row=4,column=3,columnspan=5,sticky='w')
	# DateIn.current(date_list.index(date.today().strftime("%Y-%m-%d")))
	DateOut = ttk.Combobox(f2,values=date_list,width=11).grid(row=5,column=3,columnspan=5,sticky='w')
	Rate_Type = ttk.Combobox(f2,values=['Standard','Deluxe','Off-Season','Royal','Dopule Joint','Suite','Prepaid','Loyalty','Membership','Special','Group','Family','Package'],width=11).grid(row=1,column=7,columnspan=8,sticky='w')
	#ENTRIES:
	groove_entry0 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry0.grid(row=1,column=1,columnspan=2,sticky='nsw')
	groove_entry0.insert(0,"009-098")
	groove_entry1 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=2,column=1,columnspan=2,sticky='nsw')
	groove_entry2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=3,column=1,columnspan=2,sticky='nsw')
	groove_entry3 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=4,column=1,columnspan=2,sticky='nsw')
	groove_entry4 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=6,column=1,columnspan=2,sticky='nsw')
	groove_entry5 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=8,column=1,columnspan=2,sticky='nsw')
	groove_entry6 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10).grid(row=2,column=3,columnspan=5,sticky='nsw')
	groove_entry7 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
	groove_entry7.grid(row=3,column=3,sticky='nsw')
	groove_entry7.insert(0, "12")
	groove_entry8 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
	groove_entry8.grid(row=6,column=3,sticky='nsw')
	groove_entry8.insert(0, "7")	
	groove_entry9 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
	groove_entry9.grid(row=7,column=3,sticky='nsw')
	groove_entry9.insert(0, "1")	
	groove_entry10 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3)
	groove_entry10.grid(row=8,column=3,sticky='nsw')
	groove_entry10.insert(0, "0")
	groove_entry11 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry11.grid(row=2,column=7,columnspan=8,sticky='nsw')
	groove_entry11.insert(0, "998.00")
	groove_entry12 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry12.grid(row=3,column=7,columnspan=8,sticky='nsw')
	groove_entry12.insert(0, "4,233.00")
	groove_entry13 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry13.grid(row=4,column=7,columnspan=8,sticky='nsw')
	groove_entry13.insert(0, "0.00")
	groove_entry14 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry14.grid(row=4,column=7,columnspan=8,sticky='nsw')
	groove_entry14.insert(0, "4,233.00")
	groove_entry15 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=8)
	groove_entry15.grid(row=5,column=7,sticky='nsw')
	groove_entry15.insert(0, "0.0000")
	groove_entry16 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry16.grid(row=6,column=7,columnspan=8,sticky='nsw')
	groove_entry16.insert(0, "4,233.00")
	groove_entry17 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry17.grid(row=7,column=7,columnspan=8,sticky='nsw')
	groove_entry17.insert(0, "0.00")
	groove_entry18 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry18.grid(row=8,column=7,columnspan=8,sticky='nsw')
	groove_entry18.insert(0, "4,233.00")


def room_options_buttons(OPTION,ROOM_NO,NAME,TYPE):
	try:
   		if OPTION == 'new':
   			if check_if_room_in_database(ROOM_NO) == False:
   				insert_to_database(ROOM_NO,NAME,TYPE,'Free')
   			elif check_if_room_in_database(ROOM_NO) == True:
   				# print(my_list)
   				#tkinter.new widget message:
   				print('room  is exists ,add new number or use update current room')
   				#ok button:
   		elif OPTION == 'update':	
   			if check_if_room_in_database(ROOM_NO) == True:
   				database_room_update(ROOM_NO,NAME,TYPE)
   			elif check_if_room_in_database(ROOM_NO) == False:
   				#tkinter.new widget message:
   				print('room  is not exists ,add new number or use update current room')
   				#ok button:
   		elif OPTION == 'delete':
   			if check_if_room_in_database(ROOM_NO) == True:
   				database_room_delete(ROOM_NO)
   			elif check_if_room_in_database(ROOM_NO) == False:
   				#tkinter.new widget message:
   				print('room  is not exists')
   				#ok button:
   		else:
   			print('room option is wrong')

   		first_table_show_options(Status.get(),R_Type.get(),R_number.get())

	except ValueError:
		pass


def rooms_options(MASTER):
	f1 = MASTER
	#BUTTONS:
	tkinter.Button(f1, text='  add new     ',background="light gray",command=lambda:room_options_buttons('new',groove_entry1.get(),groove_entry2.get(),groove_entry3.get())).grid(row=0, column=0,sticky='sw')
	tkinter.Button(f1,text='       update       ',background="light gray",command=lambda:room_options_buttons('update',groove_entry1.get(),groove_entry2.get(),groove_entry3.get())).grid(row=0, column=1,sticky='sw')
	tkinter.Button(f1,text='delete   ',background="light gray",command=lambda:room_options_buttons('delete',groove_entry1.get())).grid(row=0, column=2,sticky='sw')
	#LABELS:
	tkinter.Label(f1,text="Room Number ",background="light gray").grid(row=1,column=0,sticky='w')
	tkinter.Label(f1,text="Room Name ",background="light gray").grid(row=2,column=0,sticky='w')
	tkinter.Label(f1,text="Room Type ",background="light gray").grid(row=3,column=0,sticky='w')
	tkinter.Label(f1,text="Status   ",background="light gray").grid(row=1,column=3,sticky='w')
	tkinter.Label(f1,text="Remain Time ",background="light gray").grid(row=2,column=3,sticky='w')
	tkinter.Label(f1, text="    1m/3d/3h    ",background="white",relief="solid").grid(row=2,column=4,sticky='w')
	tkinter.Label(f1,text="Room Side  ",background="light gray").grid(row=4,column=0,sticky='w')
	tkinter.Label(f1,text="Details       ",background="light gray").grid(row=5,column=0,sticky='w')
	tkinter.Label(f1,text="Beds  ",background="light gray").grid(row=6,column=0,sticky='w')
	status_free = tkinter.Label(f1, text="       Free         ",background="pale green",relief="solid").grid(row=1,column=4,sticky='w')
	#ENTRIES:
	groove_entry1 = tkinter.Entry(f1, font=10,relief="groove",background="white")
	groove_entry1.grid(row=1,column=1,columnspan=2,sticky='nw')
	groove_entry1.insert(0, "room number")
	ROOM_NO = groove_entry1.get() 

	groove_entry2 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry2.grid(row=2,column=1,columnspan=2,sticky='nw')
	groove_entry2.insert(0, "NAME")
	ROOM_NAME = groove_entry2.get()

	groove_entry3 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry3.grid(row=3,column=1,columnspan=2,sticky='nw')
	groove_entry3.insert(0, "TYPE")
	ROOM_TYPE = groove_entry3.get()

	groove_entry5 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry5.grid(row=4,column=1,columnspan=2,sticky='nsw')
	groove_entry5.insert(0, "SIDE")

	groove_entry4 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry4.grid(row=5,column=1,columnspan=2,sticky='nsw')
	groove_entry4.insert(0, "details")

	groove_entry6 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry6.grid(row=6,column=1,columnspan=2,sticky='nsw')
	groove_entry6.insert(0, "max beds")

def first_table_show_options(STATUS,TYPE,NUM):
	ITEMS_NO = len(view_selected_data(STATUS,TYPE,NUM))
	ITEMS_LIST = view_selected_data(STATUS,TYPE,NUM)
	treeview1_inserts(ITEMS_NO,ITEMS_LIST)
		
def treeview1_inserts(ITEMS_NO,ITEMS_LIST):
	global COLOR_CHOICE
	global TABLE_HEIGHT
	COLOR_CHOICE = 0
	treeview1.delete(*treeview1.get_children())
	database_Table_view_Height(fen,first_list_Scorll_X,first_list_Scorll_Y,ITEMS_NO)
	for TABLE in ITEMS_LIST:
		if COLOR_CHOICE == 0:
			COLOR_CHOICE = COLOR_CHOICE + 1
		elif COLOR_CHOICE == 1:
			COLOR_CHOICE = COLOR_CHOICE - 1
		else:
			print('error')
			print(f'COLOR_CHOICE: {COLOR_CHOICE}')
		treeview1.insert("" , "end" , text = f"{TABLE[0]}", values = TABLE[1:4] ,tag=f"{COLOR_TAG[COLOR_CHOICE]}")

def database_Table_view_Height(master,X,Y,ITEMS_NO):
	global vsb
	global TABLE_HEIGHT
	if ITEMS_NO <= 8 :
		TABLE_HEIGHT =  ITEMS_NO
	elif ITEMS_NO >= 8:
		TABLE_HEIGHT = 8
	treeview1.configure(height=TABLE_HEIGHT)
	if ITEMS_NO > 8:
		vsb = ttk.Scrollbar(master, orient="vertical", command=treeview1.yview)
		vsb.place(x=X, y=Y, height=180)
	if ITEMS_NO <= 8:
		if 'vsb' in globals():
			vsb.place_forget()
		if 'vsb' in locals():
			vsb.place_forget()


def setup_background(BACKGROUND_COLOR,FONT_COLOR):
    global __font
    global canv
    global canv_text
    __font = tkfont.Font()
    canv = tkinter.Canvas(treeview1,background=BACKGROUND_COLOR,borderwidth=0,highlightthickness=0)
    canv_text = canv.create_text(0, 0,fill=FONT_COLOR,anchor='w')

def treeview_table_generator(MASTER,TREE_NUM,COLUMNS,WIDTHS,X,Y,TABLE_HEIGHT):
	LEN = len(COLUMNS)
	globals()[f'treeview{TREE_NUM}'] =  ttk.Treeview(MASTER,columns=(COLUMNS[1:LEN]) ,height=TABLE_HEIGHT)
	COLUMN_NUM = 0
	for COLUMN in COLUMNS:
		# print("#{}".format(COLUMN_NUM),"{}".format(COLUMN))
		globals()[f'treeview{TREE_NUM}'].heading("#{}".format(COLUMN_NUM), text="{}".format(COLUMN), anchor = "w")
		globals()[f'treeview{TREE_NUM}'].column("#{}".format(COLUMN_NUM), width = WIDTHS[COLUMN_NUM], anchor = "w")
		COLUMN_NUM = COLUMN_NUM + 1
	globals()[f'treeview{TREE_NUM}'].pack(fill=tkinter.BOTH,expand=1)
	globals()[f'treeview{TREE_NUM}'].place(x=X,y=Y)


def table1():
	treeview_table_generator(fen,1,["Room No","Room Name","Room Type","Room Status"],[72,187,187,104],10,80,TABLE_HEIGHT)
	Style_generator(1,None,9,'light gray')
	first_table_show_options('All','All','All')

def Style_generator(STYLE_NUM,FONT,FONT_SIZE,BG_COLOR):
	globals()[f'style{STYLE_NUM}'] = ttk.Style()
	globals()[f'style{STYLE_NUM}'].configure(f"treeview{STYLE_NUM}.Heading", font=(FONT, FONT_SIZE,'bold'),background=BG_COLOR)
	globals()[f'treeview{STYLE_NUM}'].tag_configure('gray', background=BG_COLOR)

def Room_View_Options():
	#globals:
	global Status,R_Type,R_number
	#main frame:
	Room_View = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Room_View.place(relx=0.74, rely=0.260, anchor=tkinter.NW)
	#Labels:
	tkinter.Label(fen, text='Rooms Show Options',background="light gray").place(relx=.77, rely=0.260,anchor=tkinter.W)
	tkinter.Label(Room_View, text="   ",background="light gray").grid(row=0,column=0,sticky='w')
	tkinter.Label(Room_View,text="Room Status",background="light gray").grid(row=2,column=0,sticky='w')
	tkinter.Label(Room_View,text="Room Type",background="light gray").grid(row=3,column=0,sticky='w')
	tkinter.Label(Room_View,text="Room .NO",background="light gray").grid(row=4,column=0,sticky='w')
	tkinter.Label(Room_View,text=" ",background="light gray").grid(row=5,column=0,sticky='w')
	#lists:
	Status = ttk.Combobox(Room_View,values=['All','Free','In Use'],width=5)
	R_Type = ttk.Combobox(Room_View,values=['All','Standard','Deluxe','Off-Season','Royal','Dopule Joint','Suite','Prepaid','Loyalty','Membership','Special','Group','Family','Package'],width=11)
	R_number = ttk.Combobox(Room_View,values=['All',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],width=3)
	#geometry:
	Status.grid(row=2,column=1,sticky='w')
	R_Type.grid(row=3,column=1,sticky='w')
	R_number.grid(row=4,column=1,sticky='w')
	#first choice:
	Status.current(0)
	R_Type.current(0)
	R_number.current(0)
	#bindings:
	Status.bind('<<ComboboxSelected>>', room_view_callback)
	R_Type.bind('<<ComboboxSelected>>', room_view_callback)
	R_number.bind('<<ComboboxSelected>>', room_view_callback)

def room_view_callback(event):
	STATUS  =   Status.get()
	TYPE    =   R_Type.get()
	NUM     =	R_number.get()
	first_table_show_options(STATUS,TYPE,NUM)


def clock_date():
	global clock
	global DATE
	datenow = datetime.now().strftime('%A,%d %B %Y')
	timenow =  datetime.now().time().strftime('%H:%M:%S')
	Time = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Time.place(relx=0.74, rely=0.108, anchor=tkinter.NW)
	tkinter.Label(fen, text='Time',bg="light gray").place(relx=.77, rely=0.108,anchor=tkinter.W)
	clock = tkinter.Label(Time, text=f'            {timenow}          ',font=("Helvetica", 24),bg="light gray")
	clock.pack(side=tkinter.TOP, anchor=tkinter.N)
	DATE = tkinter.Label(Time, text=f'          {datenow}              ',bg="light gray")
	DATE.pack(side=tkinter.TOP, anchor=tkinter.W)
	live_time_change()

def live_time_change():
	timenow =  datetime.now().time().strftime('%H:%M:%S')
	datenow = datetime.now().strftime('%A,%d %B %Y')
	clock.config(text=timenow)
	DATE.config(text=f'      {datenow}        ')
	fen.after(200, live_time_change)

def main():
	clock_date()
	Room_View_Options()
	create_main_database()
	table1()
	Cashier_operations()

################################################################################

#widget:
fen = tkinter.Tk()

fen.title('Hotel')

can = tkinter.Canvas(fen , height=570,width=800,bg="light gray")
can.create_text(85,45,fill="black",font="albattar 20 bold",text="Hotel Name",tags="NAME")

can.create_rectangle(9, 80, 578, 261, outline="white", fill="grey")
main()
can.pack()
fen.mainloop()


