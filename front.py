#!/usr/bin/env python3
#use control+b to execute code

import tkinter
import tkinter.ttk as ttk
import tkinter.font as tkfont
import os
from datetime import timedelta, date , datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import tkinter.messagebox


'''
line: 940  CHANGE_ROOM_CHECK_IN()
line: 906 and see trace_checkin_inputs , how it works
line: 926 #costumize them all to fit with update checkin fields , not booking
adding check_in detals to booking_table
adding serial "folio number" to serial_table
get check_in details when click on table1 by choosing room number then getting details from booking_table by number
def update_state_function():
	every num of seccounds check date and time of finish booking
	if  one of rooms near end date and time:
		yellow blinking on row of room in table1
		message: room <num> is almost free try to tell guest
	if one of rooms pass end date and time:
		red blinking red  room row in table1 3 times
		message: room <num> is free , you can use it , take key from guest
		move room details from booking to unfinishing checkouts
'''


#VARS:
TABLE_HEIGHT=0
COLOR_TAG = {}
COLOR_CHOICE = 0
COLOR_TAG[0] = 'gray'
COLOR_TAG[1] = 'white'
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
first_list_Scorll_X = 562
first_list_Scorll_Y = 80
cars = ["","Abarth","Alfa Romeo","Aston Martin","Audi","Bentley","BMW","Bugatti","Cadillac","Chevrolet","Chrysler","Citroën","Dacia","Daewoo","Daihatsu","Dodge","Donkervoort","DS","Ferrari","Fiat","Fisker","Ford","Honda","Hummer","Hyundai","Infiniti","Iveco","Jaguar","Jeep","Kia","KTM","Lada","Lamborghini","Lancia","Land Rover","Landwind","Lexus","Lotus","Maserati","Maybach","Mazda","McLaren","Mercedes-Benz","MG","Mini","Mitsubishi","Morgan","Nissan","Opel","Peugeot","Porsche","Renault","Rolls-Royce","Rover","Saab","Seat","Skoda","Smart","SsangYong","Subaru","Suzuki","Tesla","Toyota","Volkswagen","Volvo"]

room_types = ['Standard','Deluxe','Off-Season','Royal','Dopule Joint','Suite','Prepaid','Loyalty','Membership','Special','Group','Family','Package']
ID_TYPES = ["(SSN)Social Security Number","Passport number","Driver license","taxpayer ID number","patient ID number"]
date_list = []

#database functions:########################################################################
def create_main_database(DATABESE_NAME):
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS table_name(
				Room_No INT PRIMARY KEY NOT NULL,
				Room_Name TEXT NOT NULL,
				Room_Type TEXT NOT NULL,
				Room_Status TEXT NOT NULL,
				Room_Side TEXT NOT NULL,
				Room_Details TEXT NOT NULL,
				Room_Beds TEXT NOT NULL  ) ''' )
	conn.commit()
	conn.close()


def create_rate_table(DATABESE_NAME):
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS rate_table(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				Rate_Type TEXT NOT NULL,
				Room_Rate REAL NOT NULL,
				Person_No TEXT NOT NULL,
				Extra_Adults_Rate TEXT NOT NULL,
				Extra_Childrens_Rate TEXT NOT NULL) ''')
	conn.commit()
	conn.close()


def create_serial_table(DATABASE_NAME):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS serial_table(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				serial_num INT NOT NULL) ''')
	conn.commit()
	conn.close()

def create_booking_table(DATABASE_NAME):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS booking_table(
				Room_No INT PRIMARY KEY NOT NULL,
				serial_num INT,
				First_name TEXT,
				Last_name TEXT,
				R_CARD_No TEXT,
				Country TEXT,
				Adress TEXT ,
				ID_Type TEXT,
				ID_No TEXT,
				Car TEXT,
				Plate_No TEXT,
				Date_In TEXT,
				TIME_IN TEXT,
				Date_Out TEXT,
				NO_OF_DAYS INT,
				NO_OF_ADULTS INT,
				NO_OF_CHILDS INT,
				Rate_Type TEXT,
				RATE_PERIOD REAL,
				TOTAL_CHARGE REAL,
				OTHER_CHARGES REAL,
				DISCOUNT REAL,
				TOTAL REAL,
				AMOUNT_PAID REAL,
				BALANCE REAL) ''')

	conn.commit()
	conn.close()


def create_new_booking_room(DATABASE_NAME,Room_No):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO booking_table(Room_No) VALUES (?)",(Room_No,))
	conn.commit()
	c.close()


def insert_to_booking_table(DATABASE_NAME,Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	#change vars:
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? ,Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_In = ? , TIME_IN = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? ,OTHER_CHARGES = ? , DISCOUNT = ?  , TOTAL = ? , AMOUNT_PAID = ? ,  BALANCE = ?  WHERE Room_No = ? ',
			(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	conn.commit()
	c.close()

def database_booking_update(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? , Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_In = ? , TIME_IN = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? , OTHER_CHARGES = ? , DISCOUNT = ? , TOTAL = ? , AMOUNT_PAID = ? , BALANCE = ? WHERE Room_No = ? ',(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	conn.commit()
	c.close()

def change_in_table_name_status(Room_No,STATUS):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute('UPDATE table_name SET Room_Status = ? WHERE Room_No = ? ',(STATUS,Room_No,))
	conn.commit()
	c.close()

def room_is_free(Room_No):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("SELECT Room_Status FROM table_name WHERE Room_No = ?",(Room_No,))
	rows = c.fetchall()
	for row in rows:
		return row[0] == 'Free'

#important:tomorrow
def book_it(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	global update_trace_checkin_inputs,trace_checkin_inputs,CHECKIN_CHOICE
	CHECKIN_CHOICE = 'BOOKING'
	update_trace_checkin_inputs = 0
	# print(Rate_Type)
	# print('1) booking .')
	# print(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE)
	if check_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type) == True:
		# print(f'check_inputs_all_right is: {True}')
		# print('all inputs are right')
		if check_if_room_in_database(Room_No) == True:
			#print(room_is_free(Room_No))
			if room_is_free(Room_No):
				BOOKING_CHOICE = tkinter.messagebox.askquestion(message="do you relly want to rent this room?")
				if BOOKING_CHOICE == 'yes':
					database_booking_update(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE)
					change_in_table_name_status(Room_No,"IN USE")
					insert_to_serial_table('__main2.db',serial_num)
					first_table_show_options(Status.get(),R_Type.get(),R_number.get())
					# print('room is rented secsassfully')
				else:
					pass
			elif not room_is_free(Room_No):
				# print('room is not free')
				pass
		elif not check_if_room_in_database(Room_No):
			# print('room not in database')
			pass
		trace_checkin_inputs = 0
	else:
		trace_checkin_inputs = 1
		# print(f'check_inputs_all_right is: {False}')
		# print('some inputs are wrong change this inputs or fill it  if its empty')
		find_and_mark_wrong_fields(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type)
		MESSAGE = ""
		for message in check_in_input_error_messages:
			MESSAGE = MESSAGE + f'\n{message}'
		# print(f'message: {MESSAGE}')
		tkinter.messagebox.showinfo(message=MESSAGE)


def red_warning_entry_borders(ENTRY,COLOR):
	if COLOR == 'RED':
		globals()[ENTRY].configure(highlightbackground="red",highlightcolor="red")
		can.after(10)
		can.update()
	elif COLOR  == 'NORMAL':
		globals()[ENTRY].configure(highlightbackground="light gray",highlightcolor="black")
		can.after(10)
		can.update()


def find_and_mark_wrong_fields(Room_No,serial_num=None,First_name=None,Last_name=None,Adress=None,ID_No=None,NO_OF_DAYS=None,Rate_Type=None):
	global check_in_input_error_messages,groove_entry7F2
	check_in_input_error_messages = []
	# print(int(Room_No) in list(zip(*select_room_numbers("__main2.db")))[0])
	if Room_No == '' or Room_No == None:
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append("room number field is empty .!")
	elif Room_No != '' or Room_No != None:
		if int(Room_No) not in list(zip(*select_room_numbers("__main2.db")))[0]:
			#print(int(Room_No) not in list(zip(*select_room_numbers("__main2.db")))[0])
			red_warning_entry_borders('groove_entry7F2','RED')
			check_in_input_error_messages.append("room number not in table name, its not exists, choose defferant room .!")
		else:
			pass
	elif serial_num != '' and  Room_No != '' and str(serial_num) == str(select_from_booking_table_where_num('__main2.db',Room_No)[0][1]).zfill(6) and view_selected_data('__main2.db','All','All',Room_No)[0][3] == 'IN USE':
		red_warning_entry_borders('groove_entry7F2','RED')
		# print('problem is here here !!!!')
		check_in_input_error_messages.append('Room with this number and this folio is still IN USE, you can use update or change room')
	elif int(Room_No) not in BOOKING_TABLE_ROOM_NUMS or int(Room_No) not in  TABLE_NAME_ROOM_NUMS:
		red_warning_entry_borders('groove_entry7F2','RED')
		if int(Room_No) not in BOOKING_TABLE_ROOM_NUMS:
			check_in_input_error_messages.append("room number not in booking table , choose defferant room .!")
		if int(Room_No) not in  TABLE_NAME_ROOM_NUMS:
			check_in_input_error_messages.append("room is not exist in table_name .!")
	elif Room_No != '':
		if int(Room_No) in BOOKING_TABLE_ROOM_NUMS and  int(Room_No) in  TABLE_NAME_ROOM_NUMS:
			# print('its right')
			red_warning_entry_borders('groove_entry7F2','NORMAL')
			Rate_Type_CHECKIN.current()
	else:
		red_warning_entry_borders('groove_entry7F2','NORMAL')
	#serial_num: groove_entry0F2
	if serial_num == '' or serial_num == None:
		red_warning_entry_borders('groove_entry0F2','RED')
		check_in_input_error_messages.append("folio number field is empty  .!")
		#generate_new_folio_numbeer(last_serial_number_in_serial_table+1)
		#pass
	elif int(serial_num) in SERIAL_TABLE or int(serial_num) in BOOKING_TABLE_SERIAL_NUMS:
		red_warning_entry_borders('groove_entry0F2','RED')
		if int(serial_num) in SERIAL_TABLE:
			check_in_input_error_messages.append("folio number is actually existed in serial table  .!")
			#generate_new_folio_numbeer(last_serial_number_in_serial_table+1)
		if int(serial_num) in BOOKING_TABLE_SERIAL_NUMS:
			check_in_input_error_messages.append("folio is really still active yet, you can use update!")
			#generate_new_folio_number(last_serial_number_in_serial_table+1)
			# pass
	elif serial_num != '' and serial_num != None:
		if int(serial_num) not in SERIAL_TABLE and int(serial_num) not in BOOKING_TABLE_SERIAL_NUMS:
			# print('its right')
			red_warning_entry_borders('groove_entry0F2','NORMAL')
	#First_name:
	if First_name == '' or First_name == None:
		red_warning_entry_borders('groove_entry1F2','RED')
		check_in_input_error_messages.append("first name field is empty  .!")
	else:
		red_warning_entry_borders('groove_entry1F2','NORMAL')
	#Last_name:
	if Last_name == '' or Last_name == None:
		red_warning_entry_borders('groove_entry2F2','RED')
		check_in_input_error_messages.append("last name field is empty  .!")
	else:
		red_warning_entry_borders('groove_entry2F2','NORMAL')
	#Adress: groove_entry4F2
	if Adress == '' or Adress == None:
		red_warning_entry_borders('groove_entry4F2','RED')
		check_in_input_error_messages.append("adress field is empty  .!")
	else:
		red_warning_entry_borders('groove_entry4F2','NORMAL')
	#ID_No:
	if ID_No == '' or ID_No == None:
		red_warning_entry_borders('groove_entry5F2','RED')
		check_in_input_error_messages.append("id number field is empty  .!")
	else:
		red_warning_entry_borders('groove_entry5F2','NORMAL')
	#NO_OF_DAYS:
	if NO_OF_DAYS == '' or NO_OF_DAYS== None or NO_OF_DAYS == 0 or NO_OF_DAYS == '0':
		red_warning_entry_borders('groove_entry8F2','RED')
		check_in_input_error_messages.append("number of days , field is empty or 0 days .!")
	else:
		red_warning_entry_borders('groove_entry8F2','NORMAL')


def check_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
	# print('1a) checking inputs all right .')
	#inputs variables:
	global SERIAL_TABLE,BOOKING_TABLE_ROOM_NUMS,BOOKING_TABLE_SERIAL_NUMS,TABLE_NAME_ROOM_NUMS
	SERIAL_TABLE = list(zip(*view_serial_table("__main2.db")))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table('__main2.db','Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table('__main2.db','serial_num')))[0]
	TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers("__main2.db")))[0]

	if Room_No != '' and Room_No != None and serial_num != '' and serial_num != None:
		if int(Room_No) in BOOKING_TABLE_ROOM_NUMS and int(Room_No) in  TABLE_NAME_ROOM_NUMS and int(serial_num) not in SERIAL_TABLE and int(serial_num) not in BOOKING_TABLE_SERIAL_NUMS:
			if First_name != None and First_name != '' and Last_name != None and Last_name != '' and  Adress != None and Adress != '' and ID_No != None and ID_No != ''and NO_OF_DAYS != '0':
				if NO_OF_DAYS != '' and Rate_Type != None and Rate_Type != '':
					return True

	else:
		if Room_No not in TABLE_NAME_ROOM_NUMS:
			tkinter.messagebox.showinfo(message="there is some problem")
		return False



def select_from_booking_table(DATABESE_NAME,column):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute("SELECT "+column+" FROM booking_table")
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list

def select_from_booking_table_where_num(DATABESE_NAME,num):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute("SELECT * FROM booking_table WHERE Room_No = "+str(num)+" ")
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list

def check_room_status():
	#loop check if used room is freed or renting time is finished or almust
	#message: room <num> is almust to finish renting time every 5 secounds
	#when it fineshess , mark its raw in table1 with red color blinking
	#message: room <num> renting time is finished , 5 times , every 2 secounds 
	#move checkout details to unfinished checkouts_table in database , and in gui 
	#free the room , delete checkout fields , delete checkin fields
	#change room in table1 and database table_name to be free
	#change row color in table1 from red to gray or whigth
	#update table view 
	can.after(100,check_room_status)
	pass
####################################################################

def insert_to_serial_table(DATABASE_NAME,SERIAL_NUM):
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO serial_table(serial_num) VALUES (?)",(SERIAL_NUM,))
	conn.commit()
	c.close()


def check_if_serial_in_database(SERIAL_NUM):
	my_list = []
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute(''' SELECT serial_num FROM serial_table ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(int(row[0]))
	return int(SERIAL_NUM) in my_list

def view_serial_table(DATABESE_NAME):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' SELECT serial_num FROM serial_table ORDER BY id ''' )
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list


def insert_to_database(Room_No,Room_Name,Room_Type,Room_Status,SIDE,DETAILS,BEDS):
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO table_name VALUES (?,?,?,?,?,?,?)"
			,(Room_No,Room_Name,Room_Type,Room_Status,SIDE,DETAILS,BEDS))
	conn.commit()
	c.close()


def insert_rate_to_database(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate):
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO rate_table(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate) VALUES (?,?,?,?,?)"
			,(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate))
	conn.commit()
	c.close()


def database_items_count():
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute(''' SELECT COUNT(*) FROM table_name ''')
	result=c.fetchone()
	return result[0]
	c.close()


def check_if_room_in_database(NUM):
	my_list = []
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute(''' SELECT * FROM table_name ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(int(row[0]))
	return int(NUM) in my_list


def check_if_rate_in_database(Rate_Type):
	my_list = []
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute(''' SELECT * FROM rate_table ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(row[1].casefold())
	return Rate_Type.casefold() in my_list


def database_room_update(NUM,NAME,TYPE,SIDE,DETAILS,BEDS):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute('UPDATE table_name SET Room_Name = ? , Room_Type = ? , Room_Side = ? , Room_Details = ? , Room_Beds = ? WHERE Room_No = ? ',(NAME,TYPE,SIDE,DETAILS,BEDS,NUM,))
	conn.commit()
	c.close()


def database_rate_update(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute('UPDATE rate_table SET  Room_Rate = ? , Person_No = ? , Extra_Adults_Rate = ? , Extra_Childrens_Rate = ? WHERE Rate_Type = ? ',(float(Room_Rate),int(float(Person_No)),float(Extra_Adults_Rate),float(Extra_Childrens_Rate),str(Rate_Type),))
	conn.commit()
	c.close()


def database_room_delete(NUM):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("DELETE from table_name where Room_No = ?",(NUM,))
	conn.commit()
	c.close()


def database_rate_delete(Rate_Type):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("DELETE from rate_table where Rate_Type = ?",(Rate_Type,))
	conn.commit()
	c.close()


def view_selected_data(DATABESE_NAME,STATUS,TYPE,NUM):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
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


def view_selected_rate(DATABESE_NAME,RATE_TYPE):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	if RATE_TYPE == 'All':
		c.execute(''' SELECT Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate FROM rate_table ''' )
	else:
		c.execute("SELECT Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate FROM rate_table WHERE Rate_Type=?", (RATE_TYPE,))
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list


def select_types(DATABESE_NAME):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' SELECT Rate_Type FROM rate_table ORDER BY id''' )
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list


def select_room_numbers(DATABESE_NAME):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' SELECT Room_No FROM table_name ORDER BY Room_No''' )
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list


##date list:#########################################################

def date_list():
	global date_list
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

def date_one_day_after(MAIN_DATE,DAYS_AFTER):
	year,month,day = MAIN_DATE.split("-")
	DATE = date(int(year),int(month),int(day))
	return DATE + timedelta(days=DAYS_AFTER)

################################################################################
####:OTHER functions:###########################################################
################################################################################
def treeview_rate_options_table(MASTER):
	f4 = MASTER
	global treeview2
	tkinter.Label(f4,text=" ",background="light gray").grid(row=2,column=1,sticky='w')
	can4 = tkinter.Canvas(f4,background="light gray",width=200,height=180)
	RATE_X = 0
	RATE_Y = 0
	can4.create_rectangle(RATE_X,RATE_Y,RATE_X+634,RATE_Y+160, fill="gray")
	can4.grid(row=6,column=0,columnspan=10,sticky='wen')
	#column names
	treeview_table_generator(f4,2,["Room Type","Room Rate","max Person",'Extra Adults Rate','Extra Children Rate'],[100,100,100,145,170],10,80,7,geometry={'grid':{'row':7,'column':1,'columnspan':10,'sticky':'sw'},'place':{'X':1,'Y':77}},COUNT='OK')
	globals()[f'treeview{2}'].bind('<<TreeviewSelect>>',selectItem2)
	Style_generator(2,None,9,'light gray')
	secound_list_Scorll_X = 569+50
	secound_list_Scorll_Y = 75
	item2 = {}
	secound_table_show_options('All')
	treeview2.tag_configure('gray', background='#cccccc')
	treeview2.tag_configure('bb', background='light gray')

def secound_table_show_options(RATE_TYPE):
	# print('func works')
	ITEMS_NO = len(view_selected_rate('__main2.db',RATE_TYPE))
	COLUMN_NO = 5
	if ITEMS_NO > 0:
		ITEMS_LIST = view_selected_rate('__main2.db',RATE_TYPE)
	elif ITEMS_NO <= 0:
		ITEMS_LIST = None
	treeview_inserts(fen,2,ITEMS_NO,ITEMS_LIST,8,COLUMN_NO)

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
	f5 = tkinter.Frame(nb,background="light gray")
	f6 = tkinter.Frame(nb,background="light gray")
	nb.add(f1, text=" Room Settings ")
	nb.add(f2, text=" CheckIn ")
	nb.add(f3, text=" CheckOut ")
	nb.add(f4, text=" Room Price OPtions ")
	nb.add(f5, text=" User's Settings ")
	nb.add(f6, text=" Database Settings ")
	nb.select(f2)
	nb.select(f3)
	nb.select(f4)
	nb.select(f1)
	rooms_options(f1)
	CHECK_IN(f2)
	CHECK_OUT(f3)
	room_price_options(f4)
	treeview_rate_options_table(f4)

####################################################################################
def clear_rate_fields():
	groove_entry38.delete(0, 'end')
	groove_entry38.insert(0,'')
	groove_entry34.delete(0, 'end')
	groove_entry34.insert(0,'')
	groove_entry35.delete(0, 'end')
	groove_entry35.insert(0,'')
	groove_entry36.delete(0, 'end')
	groove_entry36.insert(0,'')
	groove_entry37.delete(0, 'end')
	groove_entry37.insert(0,'')

def room_price_buttons(OPTION,Rate_Type,Room_Rate=0,Person_No=0,Extra_Adults_Rate=0,Extra_Childrens_Rate=0):
	global Rate_Type_CHECKIN,groove_entry3,R_Type
	try:
		if OPTION == 'new':
			if check_if_rate_in_database(Rate_Type) == False:
				insert_rate_to_database(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate)
				clear_rate_fields()
				Rate_Type_CHECKIN.config(values=select_types("__main2.db"))
				groove_entry3.config(values=select_types("__main2.db"))
				R_Type.config(values=['All']+select_types("__main2.db"))
				Rate_Type_List.config(values=['All']+select_types("__main2.db"))
			elif check_if_rate_in_database(Rate_Type) == True:
				tkinter.messagebox.showinfo(message="Editing Error Rate is exists ,add new Rate or use update current one .")
		elif OPTION == 'update':	
			if check_if_rate_in_database(Rate_Type) == True:
				Room_Rate = Room_Rate.replace(',','')
				Person_No = Person_No.replace(',','')
				Extra_Adults_Rate = Extra_Adults_Rate.replace(',','')
				Extra_Childrens_Rate = Extra_Childrens_Rate.replace(',','')
				try:
					int(float(Room_Rate))
					int(float(Person_No))
					int(float(Extra_Adults_Rate))
					int(float(Extra_Childrens_Rate))
					# print('they are all numbers')
					database_rate_update(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate)
					clear_rate_fields()
				except ValueError:
					# print(ValueError)
					tkinter.messagebox.showinfo(message="selected value is wrong  change it to numaric value .")
			elif check_if_rate_in_database(Rate_Type) == False:
				tkinter.messagebox.showinfo(message="Update Error Rate  is not exists ,add new Rate or use update current Rate .")
		elif OPTION == 'delete':
			if check_if_rate_in_database(Rate_Type) == True:
				# print('delete')
				database_rate_delete(Rate_Type)
				clear_rate_fields()
				Rate_Type_CHECKIN.config(values=select_types("__main2.db"))
				groove_entry3.config(values=select_types("__main2.db"))
				R_Type.config(values=['All']+select_types("__main2.db"))
				Rate_Type_List.config(values=['All']+select_types("__main2.db"))
			elif check_if_rate_in_database(Rate_Type) == False:
				tkinter.messagebox.showinfo(message="Delete Error , \n room  is not exists .")
		else:
			# print('rate option is wrong')
			pass
		secound_table_show_options(rate_type_choose_trigger())
	except ValueError:
		pass

def rate_type_choose_trigger(*args):
	RATE_TYPE_LIST = Rate_Type_List.get()
	return RATE_TYPE_LIST

def room_price_options(MASTER):
	global groove_entry34,groove_entry35,groove_entry36,groove_entry37,groove_entry38,Rate_Type_List
	f4 = MASTER
	#BUTTONS:
	tkinter.Button(f4,text='New Type',background="light gray",command=lambda:room_price_buttons('new',groove_entry38.get(),groove_entry34.get(),groove_entry35.get(),groove_entry36.get(),groove_entry37.get())).grid(row=1, column=1,sticky='we')
	tkinter.Button(f4,text='Update',background="light gray",command=lambda:room_price_buttons('update',groove_entry38.get(),groove_entry34.get(),groove_entry35.get(),groove_entry36.get(),groove_entry37.get())).grid(row=1, column=2,sticky='we')
	tkinter.Button(f4,text='Delete',background="light gray",command=lambda:room_price_buttons('delete',groove_entry38.get())).grid(row=1, column=3,sticky='we')
	#LABELS:
	tkinter.Label(f4,text="Rate Type",background="light gray").grid(row=1,column=0)
	tkinter.Label(f4,text=" Room Rate",background="light gray").grid(row=2,column=1)
	tkinter.Label(f4,text="No. of Person",background="light gray").grid(row=2,column=2)
	tkinter.Label(f4,text="Adult's Rate",background="light gray").grid(row=2,column=3)
	tkinter.Label(f4,text="Children's Rate",background="light gray").grid(row=2,column=4)
	tkinter.Label(f4,text=" "*45,background="light gray").grid(row=1,column=4,columnspan=7,sticky='w')
	#ENTRIES:
	groove_entry38 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry38.grid(row=3,column=0,sticky='nwe')
	groove_entry38.insert(0, "")
	groove_entry34 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry34.grid(row=3,column=1,sticky='nwe')
	groove_entry34.insert(0, "")
	groove_entry35 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry35.grid(row=3,column=2,sticky='nwe')
	groove_entry35.insert(0, "")
	groove_entry36 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry36.grid(row=3,column=3,sticky='nwe')
	groove_entry36.insert(0, "")
	groove_entry37 = tkinter.Entry(f4,font=10,relief="groove",background="white",width=10)
	groove_entry37.grid(row=3,column=4,sticky='nwe')
	groove_entry37.insert(0, "")
	tkinter.Label(f4,text=" "*45,background="light gray").grid(row=3,column=5,columnspan=7,sticky='w')
	#LISTS:
	Rate_Type_List = ttk.Combobox(f4,values=['All']+select_types("__main2.db"),width=11)
	Rate_Type_List.grid(row=2,column=0,sticky='w')
	Rate_Type_List.bind('<<ComboboxSelected>>', rate_type_choose_trigger)
	Rate_Type_List.current(0)

def CHECK_OUT(MASTER):
	f3 = MASTER
	#BUTTONS:
	tkinter.Button(f3, text='CheckOut',background="light gray").grid(row=0, column=0,sticky='we')
	tkinter.Button(f3,text='Cancel',background="light gray").grid(row=0, column=1,sticky='we')
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


def modify_paymen_numbers_2(*args):
	try:
		# print(args)
		def Extract(lst,NUM):
			return list(list(zip(*lst))[NUM])
		my_list = []
		rate = view_selected_rate('__main2.db',Rate_Type_CHECKIN.get())
		my_list.append(rate)
		for ROOM_RATE in Extract(rate,1):
			RATE_PERIOD = ROOM_RATE
		NO_OF_DAYS = groove_entry8F2.get()

		for MAX_PERSONS in Extract(rate,2): 
			MAX_PERSONS  = int(MAX_PERSONS)

		NO_OF_ADULTS = groove_entry9F2.get()

		if NO_OF_ADULTS == '':
			NO_OF_ADULTS = 0
		
		if int(NO_OF_ADULTS) > int(MAX_PERSONS):
			EXTRA_ADULTS = int(NO_OF_ADULTS) - int(MAX_PERSONS)
		else:
			EXTRA_ADULTS = 0

		if NO_OF_DAYS == 0 or NO_OF_DAYS == None or NO_OF_DAYS == '0' or  NO_OF_DAYS == '':
			  EXTRA_ADULTS = 0

		EXTRA_CHILDREN  =  groove_entry10F2.get()
		if EXTRA_CHILDREN == '' or EXTRA_CHILDREN == None or NO_OF_DAYS == '0' or NO_OF_DAYS == None or NO_OF_DAYS == 0 or NO_OF_DAYS == '':
			EXTRA_CHILDREN = 0

		for EXTRA_ADULTS_RATE in Extract(rate,3):
			EXTRA_ADULTS_RATE = float(EXTRA_ADULTS_RATE)
		for EXTRA_CHILDREN_RATE in Extract(rate,4):
			EXTRA_CHILDREN_RATE = float(EXTRA_CHILDREN_RATE)

		if NO_OF_DAYS == 0 or NO_OF_DAYS == '':
			NO_OF_DAYS = 0.00
		TOTAL_CHARGES = (RATE_PERIOD * float(int(NO_OF_DAYS))) + ( float(int(EXTRA_ADULTS)) * EXTRA_ADULTS_RATE ) +  ( float(int(EXTRA_CHILDREN)) * EXTRA_CHILDREN_RATE)

		DISCOUNT = groove_entry15F2.get()
		if DISCOUNT == '':
			DISCOUNT = 0

		OTHER_CHAGES = groove_entry14F2.get()

		if OTHER_CHAGES == '':
			OTHER_CHAGES = 0.00

		if int(float(DISCOUNT)) > 0:
			TOTAL = (((float(TOTAL_CHARGES) + float(OTHER_CHAGES))) - ((float(TOTAL_CHARGES) + float(OTHER_CHAGES)))  * (float(str(DISCOUNT))/100)) 
		elif int(float(DISCOUNT)) == 0:
			TOTAL = float(TOTAL_CHARGES) + float(OTHER_CHAGES)
		else:
			pass

		AMOUNT_PAIED = groove_entry17F2.get()
		if AMOUNT_PAIED == '':
			AMOUNT_PAIED = 0
		BALANCE = (TOTAL - float(str(AMOUNT_PAIED))) * -1
		if BALANCE == -0.0:
			BALANCE = 0.00

		groove_entry11F2.delete(0,'end') # rate/period
		groove_entry12F2.delete(0,'end') # total charges
		# # groove_entry14F2.delete() # other charges
		# # # groove_entry15F2.delete() # discount you change this 
		groove_entry16F2.delete(0,'end') # total 
		# # groove_entry17F2.delete() # amount paied
		groove_entry18F2.delete(0,'end') # balance

		groove_entry11F2.insert(0,RATE_PERIOD)#rate/period
		groove_entry12F2.insert(0,TOTAL_CHARGES) # total charges
		# groove_entry14F2.insert(0, "4,233.22") # other charges
		# # groove_entry15F2.insert(0, "0.0000") # discount you change this
		groove_entry16F2.insert(0, TOTAL) # total 
		# groove_entry17F2.insert(0, "0.00") # amount paied
		groove_entry18F2.insert(0, BALANCE) # balance
	except ValueError:
		#print('error')
		tkinter.messagebox.showinfo(message="Value Error,\nyou added wrong value , \nonly numbers please..")

			
def database_booking_update_costumized_no_time_datein_serial(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? , Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? , OTHER_CHARGES = ? , DISCOUNT = ? , TOTAL = ? , AMOUNT_PAID = ? , BALANCE = ? WHERE Room_No = ? ',(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	conn.commit()
	c.close()

	
def boolian_room_status(Room_No,STATUS):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("SELECT Room_Status FROM table_name WHERE Room_No = ?",(Room_No,))
	rows = c.fetchall()
	for row in rows:
		return row[0] == STATUS


def boolian_Room_No_same_where_serial(Room_No,serial_num):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("SELECT Room_No FROM booking_table WHERE serial_num  = ?",(int(serial_num),))
	rows = c.fetchall()
	for row in rows:
		return row[0] == Room_No


def get_Room_No_with_serial(serial_num):
	conn =None;
	conn = sqlite3.connect("__main2.db")
	c = conn.cursor()
	c.execute("SELECT Room_No FROM booking_table WHERE serial_num  = ?",(int(serial_num),))
	rows = c.fetchall()
	for row in rows:
		return row[0]


def check_if_change_room_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
	if boolian_room_status(get_Room_No_with_serial(serial_num),'IN USE'):
		if check_if_room_in_database(Room_No):
			if not boolian_Room_No_same_where_serial(Room_No,serial_num):
				if boolian_room_status(Room_No,'Free'):
					return True
	else:
		pass


def room_changing(Room_No,serial_num,First_name=None,Last_name=None,R_CARD_No=None,Country=None,Adress=None,ID_Type=None,ID_No=None,Car=None,Plate_No=None,Date_In=None,TIME_IN=None,Date_Out=None,NO_OF_DAYS=None,NO_OF_ADULTS=None,NO_OF_CHILDS=None,Rate_Type=None,RATE_PERIOD=None,TOTAL_CHARGE=None,OTHER_CHARGES=None,DISCOUNT=None,TOTAL=None,AMOUNT_PAID=None,BALANCE=None):
	#copy those details to the free room
	#free bast room
	#show all tree1 "refrish"


def CHANGE_ROOM_CHECK_IN(Room_No,serial_num,First_name=None,Last_name=None,R_CARD_No=None,Country=None,Adress=None,ID_Type=None,ID_No=None,Car=None,Plate_No=None,Date_In=None,TIME_IN=None,Date_Out=None,NO_OF_DAYS=None,NO_OF_ADULTS=None,NO_OF_CHILDS=None,Rate_Type=None,RATE_PERIOD=None,TOTAL_CHARGE=None,OTHER_CHARGES=None,DISCOUNT=None,TOTAL=None,AMOUNT_PAID=None,BALANCE=None):
	global CHECKIN_CHOICE
	CHECKIN_CHOICE = 'CHANGING'
	#print(boolian_Room_No_same_where_serial(Room_No,serial_num))
	#print(f'room with this serial {get_Room_No_with_serial(serial_num)}')
	#print(boolian_room_status(get_Room_No_with_serial(serial_num),'IN USE'))
	if check_if_change_room_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
		print(f'change room to {Room_No}')
		print(f'free room with serial {serial_num}')
		#message box with yse,no:
		room_changing(Room_No,serial_num,First_name=None,Last_name=None,R_CARD_No=None,Country=None,Adress=None,ID_Type=None,ID_No=None,Car=None,Plate_No=None,Date_In=None,TIME_IN=None,Date_Out=None,NO_OF_DAYS=None,NO_OF_ADULTS=None,NO_OF_CHILDS=None,Rate_Type=None,RATE_PERIOD=None,TOTAL_CHARGE=None,OTHER_CHARGES=None,DISCOUNT=None,TOTAL=None,AMOUNT_PAID=None,BALANCE=None)
	else:
		#show wrong fields in message box have ok , choose from 4 wrong actions in check_if_change_room_inputs_all_right() function:


def Update_CHECK_IN_DETAILS(Room_No,serial_num,First_name,Last_name=None,R_CARD_No=None,Country=None,Adress=None,ID_Type=None,ID_No=None,Car=None,Plate_No=None,Date_In=None,TIME_IN=None,Date_Out=None,NO_OF_DAYS=None,NO_OF_ADULTS=None,NO_OF_CHILDS=None,Rate_Type=None,RATE_PERIOD=None,TOTAL_CHARGE=None,OTHER_CHARGES=None,DISCOUNT=None,TOTAL=None,AMOUNT_PAID=None,BALANCE=None):
	global update_check,update_trace_checkin_inputs,CHECKIN_CHOICE
	CHECKIN_CHOICE = 'UPDATING'
	if check_if_update_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
		update_trace_checkin_inputs = 0
		UPDATE_CHECKIN_CHOICE = tkinter.messagebox.askquestion(message="do you really want to update check in details?")
		if UPDATE_CHECKIN_CHOICE == 'yes':
			database_booking_update_costumized_no_time_datein_serial(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE)
		elif UPDATE_CHECKIN_CHOICE == 'no':
			pass
	else:
		update_trace_checkin_inputs = 1
		looking_for_wrong_fields_and_mark_them(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type)
		

def check_if_update_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
	global update_trace_checkin_inputs
	update_trace_checkin_inputs = 1
	print('checking for updating.....!!!')
	normalize_all_inputs(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type)
	SERIAL_TABLE = list(zip(*view_serial_table("__main2.db")))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table('__main2.db','Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table('__main2.db','serial_num')))[0]
	#use check_if_room_in_database(Room_No) insted to:
	#TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers("__main2.db")))[0]
	if not Room_No.isspace():
		if Room_No != '' and Room_No != None and serial_num != '' and serial_num != None and check_if_room_in_database(Room_No):
			if int(serial_num) == (list(zip(*select_from_booking_table_where_num('__main2.db',Room_No)))[1][0]):
				if int(Room_No) in BOOKING_TABLE_ROOM_NUMS  and int(serial_num) in SERIAL_TABLE and int(serial_num)  in BOOKING_TABLE_SERIAL_NUMS:
					if First_name != None and First_name != '' and Last_name != None and Last_name != '' and  Adress != None and Adress != '' and ID_No != None and ID_No != ''and NO_OF_DAYS != '0':
						if Rate_Type != None and Rate_Type != '':
							if boolian_room_status(Room_No,'IN USE'):
								return True
	else:
		#tkinter.messagebox.showinfo(message="there is some problem")
		return False


def serial_is_serial_where_num(serial_num,Room_No):
	Room_No = groove_entry7F2.get()
	if Room_No != '' and not Room_No.isspace() and Room_No != None:
		if check_if_room_in_database(int(Room_No)):
			return str(serial_num) == str(select_from_booking_table_where_num('__main2.db',Room_No)[0][1]).zfill(6)
	else:
		return False


def normalize_all_inputs(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type=None):
	red_warning_entry_borders('groove_entry7F2','NORMAL')
	red_warning_entry_borders('groove_entry0F2','NORMAL')
	red_warning_entry_borders('groove_entry1F2','NORMAL')
	red_warning_entry_borders('groove_entry2F2','NORMAL')
	red_warning_entry_borders('groove_entry4F2','NORMAL')
	red_warning_entry_borders('groove_entry5F2','NORMAL')
	red_warning_entry_borders('groove_entry8F2','NORMAL')


def looking_for_wrong_fields_and_mark_them(Room_No,serial_num,First_name,Last_name=None,Adress=None,ID_No=None,NO_OF_DAYS=None,Rate_Type=None):
	# normalize_all_inputs(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS)
	SERIAL_TABLE = list(zip(*view_serial_table("__main2.db")))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table('__main2.db','Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table('__main2.db','serial_num')))[0]
	TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers("__main2.db")))[0]
	global check_in_input_error_messages,groove_entry7F2
	check_in_input_error_messages = []
	if Room_No == '' or Room_No == None or len(Room_No) == 0 or Room_No.isspace():
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append("room number field is empty .!")
	elif Room_No != '' and Room_No != None and not check_if_room_in_database(Room_No):
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append("room number not in table name, its not exists, choose defferant room .!")
	elif Room_No != '' and boolian_room_status(Room_No,'Free'):
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append("room with this number is Free , you can book it or choose  another Used room to update .!")
	elif serial_num != '' and  Room_No != '' and not serial_is_serial_where_num(serial_num,Room_No):
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append('Room number is not for folio....!')
	elif int(Room_No) not in BOOKING_TABLE_ROOM_NUMS or int(Room_No) not in  TABLE_NAME_ROOM_NUMS:
		red_warning_entry_borders('groove_entry7F2','RED')
		if int(Room_No) not in BOOKING_TABLE_ROOM_NUMS:
			check_in_input_error_messages.append("room number not in booking table , choose defferant room .!")
		if int(Room_No) not in  TABLE_NAME_ROOM_NUMS:
			check_in_input_error_messages.append("room is not exist in table_name .!")
	elif Room_No != '':
		if int(Room_No) in BOOKING_TABLE_ROOM_NUMS and check_if_room_in_database(Room_No):
			red_warning_entry_borders('groove_entry7F2','NORMAL')
			Rate_Type_CHECKIN.current()
	else:
		red_warning_entry_borders('groove_entry7F2','NORMAL')
	#serial_num: groove_entry0F2
	if serial_num == '' or serial_num == None:
		red_warning_entry_borders('groove_entry0F2','RED')
		check_in_input_error_messages.append("folio number field is empty  .!")
		#generate_new_folio_numbeer(last_serial_number_in_serial_table+1)
		#pass
	elif int(serial_num) not in SERIAL_TABLE or int(serial_num) not in BOOKING_TABLE_SERIAL_NUMS:
		red_warning_entry_borders('groove_entry0F2','RED')
		if int(serial_num) not in SERIAL_TABLE:
			check_in_input_error_messages.append("folio number is actually existed in serial table  .!")
			#generate_new_folio_numbeer(last_serial_number_in_serial_table+1)
		if int(serial_num) not in BOOKING_TABLE_SERIAL_NUMS:
			check_in_input_error_messages.append("folio is really still active yet, you can use update!")
			#generate_new_folio_number(last_serial_number_in_serial_table+1)
			# pass
	elif not serial_is_serial_where_num(serial_num,Room_No):
		red_warning_entry_borders('groove_entry0F2','RED')
		check_in_input_error_messages.append("folio is not for this room num....!")
	elif serial_num != '' and serial_num != None:
		if int(serial_num) in SERIAL_TABLE and int(serial_num) in BOOKING_TABLE_SERIAL_NUMS:
			# print('its right')
			red_warning_entry_borders('groove_entry0F2','NORMAL')
	#First_name:
	First_name = groove_entry1F2.get()
	if First_name == '' or First_name == None or len(First_name) == 0 or First_name.isspace():
		red_warning_entry_borders('groove_entry1F2','RED')
		check_in_input_error_messages.append("first name field is empty  .!")
	elif len(First_name)  !=  0 and not First_name.isspace() and len(First_name) != 0 and not First_name.isspace():
		red_warning_entry_borders('groove_entry1F2','NORMAL')
	else:
		pass
	#Last_name:
	Last_name = groove_entry2F2.get()
	if Last_name == '' or Last_name == None or len(Last_name) == 0 or Last_name.isspace():
		red_warning_entry_borders('groove_entry2F2','RED')
		check_in_input_error_messages.append("last name field is empty  .!")
	elif len(Last_name)  !=  0 and not Last_name.isspace() and Last_name != '' or Last_name != None:
		red_warning_entry_borders('groove_entry2F2','NORMAL')
	#Adress: 
	Adress = groove_entry4F2.get()
	if Adress == '' or Adress == None or len(Adress) == 0 or Adress.isspace():
		red_warning_entry_borders('groove_entry4F2','RED')
		check_in_input_error_messages.append("adress field is empty  .!")
	elif len(Adress)  !=  0 and not Adress.isspace() and Adress != '' or Adress != None:
		red_warning_entry_borders('groove_entry4F2','NORMAL')
	#ID_No:
	ID_No = groove_entry5F2.get()
	if ID_No == '' or ID_No == None or len(ID_No) == 0 or ID_No.isspace():
		red_warning_entry_borders('groove_entry5F2','RED')
		check_in_input_error_messages.append("id number field is empty  .!")
	else:
		red_warning_entry_borders('groove_entry5F2','NORMAL')
	#NO_OF_DAYS:
	NO_OF_DAYS = groove_entry8F2.get()
	if NO_OF_DAYS == '' or NO_OF_DAYS == None or NO_OF_DAYS == 0 or NO_OF_DAYS == '0':
		red_warning_entry_borders('groove_entry8F2','RED')
		check_in_input_error_messages.append("number of days , field is empty or 0 days .!")
	else:
		red_warning_entry_borders('groove_entry8F2','NORMAL')


def CHECK_IN(MASTER):
	global groove_entry0F2,groove_entry1F2,groove_entry2F2,groove_entry3F2,groove_entry4F2,groove_entry5F2,groove_entry6F2
	global groove_entry7F2,groove_entry8F2,groove_entry9F2,groove_entry10F2,groove_entry11F2,groove_entry12F2,groove_entry13F2
	global groove_entry14F2,groove_entry15F2,groove_entry16F2,groove_entry17F2,groove_entry18F2,CHECKIN_CHOICE
	global Rate_Type_CHECKIN,DateIn,DateOut,trace_checkin_inputs,countrylist,lineList,ID_TYPE_LIST,carlist,update_trace_checkin_inputs
	f2 = MASTER
	CHECKIN_CHOICE = None
	trace_checkin_inputs = 0
	update_trace_checkin_inputs = 0
	def trace_entry(ENTRY_VAR):
		def callback(sv):
			print(f'CHECKIN_CHOICE: {CHECKIN_CHOICE}')
			print(f'update_trace_checkin_inputs: {update_trace_checkin_inputs}')
			print(f'trace_checkin_inputs: {trace_checkin_inputs}')
			if groove_entry7F2.get() != '' and groove_entry7F2.get() != None:
				existed_room_numbers_list = []
				for i in view_selected_data('__main2.db','All','All','All'):
					existed_room_numbers_list.append(i[0])
				if int(groove_entry7F2.get()) in existed_room_numbers_list:
					LIST = view_selected_data('__main2.db','All','All',int(groove_entry7F2.get()))
					Rate_Type_CHECKIN.current(room_types.index(LIST[0][2]))
				else:
					pass
					# print('the number is not in existedd rooms list')
					# print(f'{int(groove_entry7F2.get())} in the list ....')
				# print(view_selected_data('__main2.db','All','All','All'))
			if Rate_Type_CHECKIN.get() != "":
				modify_paymen_numbers_2()
			# if trace_checkin_inputs == 1:
			if CHECKIN_CHOICE == 'BOOKING':
				# print('under booking process')				   
				find_and_mark_wrong_fields(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry4F2.get(),groove_entry5F2.get(),groove_entry8F2.get(),Rate_Type_CHECKIN.get())
			# if update_trace_checkin_inputs == 1:
			if CHECKIN_CHOICE == 'UPDATING':
				# print('under update process')
				looking_for_wrong_fields_and_mark_them(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry4F2.get(),groove_entry5F2.get(),groove_entry8F2)
			else:
				pass
		globals()[f'{ENTRY_VAR}_trace'] = tkinter.StringVar()
		globals()[f'{ENTRY_VAR}_trace'].trace("w", lambda name, index, mode, sv=globals()[f'{ENTRY_VAR}_trace']: callback(globals()[f'{ENTRY_VAR}_trace'])) 
	trace_entry('groove_entry7F2')
	trace_entry('groove_entry8F2')
	trace_entry('groove_entry9F2')
	trace_entry('groove_entry10F2')
	trace_entry('groove_entry14F2')
	trace_entry('groove_entry15F2')
	trace_entry('groove_entry17F2')
	trace_entry('groove_entry0F2')
	trace_entry('groove_entry1F2')
	trace_entry('groove_entry2F2')
	trace_entry('groove_entry5F2')
	trace_entry('groove_entry4F2')
	#BUTTONS:
	def TIME_NOW():
		timenow =  datetime.now().time().strftime('%H:%M:%S')
		return timenow
	tkinter.Button(f2, text='Book it',background="light gray",command=lambda:book_it(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry3F2.get(),countrylist.get(),groove_entry4F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),carlist.get(),groove_entry6F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get())).grid(row=0, column=0,sticky='we')
	tkinter.Button(f2, text='Print',background="light gray",width=11).grid(row=0, column=1,sticky='we')
	tkinter.Button(f2,text='Update',background="light gray",command=lambda:Update_CHECK_IN_DETAILS(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry3F2.get(),countrylist.get(),groove_entry4F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),carlist.get(),groove_entry6F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get())).grid(row=0, column=2,sticky='we')
	tkinter.Button(f2,text='Change Room',background="light gray",command=lambda:CHANGE_ROOM_CHECK_IN(groove_entry7F2.get(),groove_entry0F2.get())).grid(row=0, column=3,columnspan=5,sticky='w')
	tkinter.Button(f2,text='Cancel',background="light gray").grid(row=0,column=6,sticky='ew')
	def change_num(master,arithmetic,CHANGE_VARS):
		# print(CHANGE_VARS)
		for VAR in CHANGE_VARS:
			if 'tkinter.Entry' in str(globals()[VAR].info):
				# print(str(globals()[VAR].info))
				if globals()[VAR].get():
					first_val = int(globals()[VAR].get())
					# print(first_val)
				else :
					first_val = 0 	
				if arithmetic == '-':
					# print('-')
					if first_val > 0:
						last_val = int(first_val) - 1
						globals()[VAR].delete(0,'end')
						globals()[VAR].insert(0,last_val)
					else :
						pass
				if arithmetic == '+':
					# print('+')
					if first_val >= 0:
						# print(first_val)
						last_val = int(first_val) + 1
						# print(last_val)
						globals()[VAR].delete(0,'end')
						globals()[VAR].insert(0,last_val)
					elif first_val == 0:
						last_val = 0 + 1
						globals()[VAR].delete(0,'end')
						globals()[VAR].insert(0,last_val) 
			elif 'tkinter.ttk.Combobox' in str(globals()[VAR].info):
				if arithmetic == '-':
					if first_val > 0:
						for VAR in CHANGE_VARS:	
							if 'tkinter.Entry' in str(globals()[VAR].info):	  
								DAYS_NUM = int(globals()[VAR].get())
						DateOut_Change = int(date_list.index(DateIn.get()) + DAYS_NUM )
						DateOut.current(DateOut_Change)
					else :
						pass
				if arithmetic == '+':
					for VAR in CHANGE_VARS:	
						if 'tkinter.Entry' in str(globals()[VAR].info):	  
							DAYS_NUM = int(globals()[VAR].get())
						DateOut_Change = int(date_list.index(DateIn.get()) + DAYS_NUM )
						DateOut.current(DateOut_Change)
	###################################################################################################################
	tkinter.Button(f2, text='⯇',background="light gray",command=lambda:change_num(f2,'-',['groove_entry8F2','DateOut'])).grid(row=6, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray",command=lambda:change_num(f2,'+',['groove_entry8F2','DateOut'])).grid(row=6, column=5,sticky='we')
	tkinter.Button(f2, text='⯇',background="light gray",command=lambda:change_num(f2,'-',['groove_entry9F2'])).grid(row=7, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray",command=lambda:change_num(f2,'+',['groove_entry9F2'])).grid(row=7, column=5,sticky='we')
	tkinter.Button(f2, text='⯇',background="light gray",command=lambda:change_num(f2,'-',['groove_entry10F2'])).grid(row=8, column=4,sticky='we')
	tkinter.Button(f2, text='⯈',background="light gray",command=lambda:change_num(f2,'+',['groove_entry10F2'])).grid(row=8, column=5,sticky='we')
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
	ID_TYPE_LIST = ttk.Combobox(f2,values=ID_TYPES,width=10)
	ID_TYPE_LIST.grid(row=7,column=1,sticky='w')
	ID_TYPE_LIST.current(0)
	carlist = ttk.Combobox(f2,values=cars,width=10)
	carlist.grid(row=1,column=3,columnspan=5,sticky='w')
	carlist.current(0)
	DateIn = ttk.Combobox(f2,values=date_list,width=11)
	DateIn.grid(row=4,column=3,columnspan=5,sticky='w')
	DateIn.current(date_list.index(date.today().strftime("%Y-%m-%d")))
	DateIn.bind('<<ComboboxSelected>>', date_choose_checkin_trigger)
	DateOut = ttk.Combobox(f2,values=date_list,width=11)
	DateOut.current(date_list.index(str(date_one_day_after(date.today().strftime("%Y-%m-%d"),1))))
	DateOut.grid(row=5,column=3,columnspan=5,sticky='w')
	DateOut.bind('<<ComboboxSelected>>', date_choose_checkin_trigger)
	Rate_Type_CHECKIN = ttk.Combobox(f2,values=select_types("__main2.db"),width=11)
	Rate_Type_CHECKIN.grid(row=1,column=7,columnspan=8,sticky='w')
	Rate_Type_CHECKIN.bind("<<ComboboxSelected>>",lambda event:modify_paymen_numbers_2(event))
	#ENTRIES:
	groove_entry0F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry0F2_trace,text="00005") # serial folio no
	groove_entry0F2.grid(row=1,column=1,columnspan=2,sticky='nsw')
	groove_entry0F2.insert(0,f"{str(int(view_serial_table('__main2.db')[-1][0])+1).zfill(6)}")
	groove_entry0F2.config(state="readonly",readonlybackground="white")
	groove_entry1F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry1F2_trace) # first name
	groove_entry1F2.grid(row=2,column=1,columnspan=2,sticky='nsw')
	groove_entry2F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry2F2_trace) # last name
	groove_entry2F2.grid(row=3,column=1,columnspan=2,sticky='nsw')
	groove_entry3F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10) # Rcad_no
	groove_entry3F2.grid(row=4,column=1,columnspan=2,sticky='nsw')
	groove_entry4F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry4F2_trace) # adress
	groove_entry4F2.grid(row=6,column=1,columnspan=2,sticky='nsw')
	groove_entry5F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry5F2_trace)  # id_no
	groove_entry5F2.grid(row=8,column=1,columnspan=2,sticky='nsw')
	groove_entry6F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10) # plate no
	groove_entry6F2.grid(row=2,column=3,columnspan=5,sticky='nsw')
	# groove_entry6F2.insert(0,"") 
	groove_entry7F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3,textvariable=groove_entry7F2_trace) # room number
	groove_entry7F2.grid(row=3,column=3,sticky='nsw')
	# groove_entry7F2.insert(0, "") 
	groove_entry8F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3,textvariable=groove_entry8F2_trace)  # no of days
	groove_entry8F2.grid(row=6,column=3,sticky='nsw')
	groove_entry8F2.insert(0, "1")
	groove_entry9F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3,textvariable=groove_entry9F2_trace) # no of adults
	groove_entry9F2.grid(row=7,column=3,sticky='nsw')
	groove_entry9F2.insert(0, "0")	
	groove_entry10F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3,textvariable=groove_entry10F2_trace) # no of childs
	groove_entry10F2.grid(row=8,column=3,sticky='nsw')
	groove_entry10F2.insert(0, "0") 
	groove_entry11F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10) # rate/period
	groove_entry11F2.grid(row=2,column=7,columnspan=8,sticky='nsw')
	groove_entry11F2.insert(0, "0.00") 
	groove_entry12F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10) # total charge
	groove_entry12F2.grid(row=3,column=7,columnspan=8,sticky='nsw')
	groove_entry12F2.insert(0, "0.00") 
	# groove_entry13F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	# groove_entry13F2.grid(row=4,column=7,columnspan=8,sticky='nsw')
	# groove_entry13F2.insert(0, "1.11") 
	groove_entry14F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry14F2_trace)
	groove_entry14F2.grid(row=4,column=7,columnspan=8,sticky='nsw')
	groove_entry14F2.insert(0, "0.00") # other charges
	groove_entry15F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=8,textvariable=groove_entry15F2_trace)
	groove_entry15F2.grid(row=5,column=7,sticky='nsw')
	groove_entry15F2.insert(0, "0") # discount
	groove_entry16F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry16F2.grid(row=6,column=7,columnspan=8,sticky='nsw')
	groove_entry16F2.insert(0, "0.00") # total 
	groove_entry17F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry17F2_trace)
	groove_entry17F2.grid(row=7,column=7,columnspan=8,sticky='nsw')
	groove_entry17F2.insert(0, "0.00") # amount paied
	groove_entry18F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10)
	groove_entry18F2.grid(row=8,column=7,columnspan=8,sticky='nsw')
	groove_entry18F2.insert(0, "0.00") # balance


def date_choose_checkin_trigger(even):
	global DAYS_NUM
	def d(s):
	  [year,month,day] = map(int, s.split('-'))
	  return date(year, month, day)
	def days(start, end):
	  return (d(end) - d(start)).days
	if DateIn.get() and DateOut.get():
		if DateOut.get() > DateIn.get():
			DAYS_NUM = days(DateIn.get(),DateOut.get())
			groove_entry8F2.delete(0, 'end')
			groove_entry8F2.insert(0, DAYS_NUM)


def room_options_buttons(OPTION,ROOM_NO,NAME=None,TYPE=None,SIDE=None,DETAILS=None,BEDS=None):
	try:
		if OPTION == 'new':
			if check_if_room_in_database(ROOM_NO) == False:
				insert_to_database(ROOM_NO,NAME,TYPE,'Free',SIDE,DETAILS,BEDS)
				R_number.config(values=['All']+select_room_numbers('__main2.db'))
				create_new_booking_room('__main2.db',ROOM_NO)
			elif check_if_room_in_database(ROOM_NO) == True:
				tkinter.messagebox.showinfo("Editing Error", "room  is exists ,add new number or use update current room .")
		elif OPTION == 'update':	
			if check_if_room_in_database(ROOM_NO) == True:
				database_room_update(ROOM_NO,NAME,TYPE,SIDE,DETAILS,BEDS)
			elif check_if_room_in_database(ROOM_NO) == False:
				tkinter.messagebox.showinfo("Update Error", "room  is not exists ,add new number or use update current room .")
		elif OPTION == 'delete':
			if check_if_room_in_database(ROOM_NO) == True:
				database_room_delete(ROOM_NO)
				R_number.config(values=['All']+select_room_numbers('__main2.db'))
			elif check_if_room_in_database(ROOM_NO) == False:
				tkinter.messagebox.showinfo("Update Error", "room  is not exists .")
		else:
			# print('room option is wrong')
			pass
		first_table_show_options(Status.get(),R_Type.get(),R_number.get())
	except ValueError:
		pass


def rooms_options(MASTER):
	global room_status
	f1 = MASTER
	global groove_entry1,groove_entry2,groove_entry3,groove_entry4,groove_entry5,groove_entry6
	#BUTTONS:
	tkinter.Button(f1, text='  add new     ',background="light gray",command=lambda:room_options_buttons('new',groove_entry1.get(),groove_entry2.get(),groove_entry3.get(),groove_entry5.get(),groove_entry4.get(),groove_entry6.get())).grid(row=0, column=0,sticky='sw')
	tkinter.Button(f1,text='       update       ',background="light gray",command=lambda:room_options_buttons('update',groove_entry1.get(),groove_entry2.get(),groove_entry3.get(),groove_entry5.get(),groove_entry4.get(),groove_entry6.get())).grid(row=0, column=1,sticky='sw')
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
	room_status = tkinter.Label(f1, text="       Free         ",background="pale green",relief="solid")
	room_status.grid(row=1,column=4,sticky='w')
	#LIST:
	groove_entry3 = ttk.Combobox(f1,values=select_types("__main2.db"),width=11)
	groove_entry3.grid(row=3,column=1,columnspan=2,sticky='nw')
	groove_entry3.current(0)
	#ENTRIES:
	groove_entry1 = tkinter.Entry(f1, font=10,relief="groove",background="white")
	groove_entry1.grid(row=1,column=1,columnspan=2,sticky='nw')
	groove_entry1.insert(0, "")
	ROOM_NO = groove_entry1.get() 
	groove_entry2 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry2.grid(row=2,column=1,columnspan=2,sticky='nw')
	groove_entry2.insert(0, "")
	ROOM_NAME = groove_entry2.get()
	groove_entry5 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry5.grid(row=4,column=1,columnspan=2,sticky='nsw')
	groove_entry5.insert(0, "")
	groove_entry4 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry4.grid(row=5,column=1,columnspan=2,sticky='nsw')
	groove_entry4.insert(0, "")
	groove_entry6 = tkinter.Entry(f1,font=10,relief="groove",background="white")
	groove_entry6.grid(row=6,column=1,columnspan=2,sticky='nsw')
	groove_entry6.insert(0, "")


def first_table_show_options(STATUS,TYPE,NUM):
	ITEMS_NO = len(view_selected_data('__main2.db',STATUS,TYPE,NUM))
	# print(ITEMS_NO)
	ITEMS_LIST = view_selected_data('__main2.db',STATUS,TYPE,NUM)
	if ITEMS_NO > 0: 
		COLUMN_NO = len(view_selected_data('__main2.db',STATUS,TYPE,NUM)[0])
	treeview_inserts(fen,1,ITEMS_NO,ITEMS_LIST,8,4)		
##############################################################################

def treeview_inserts(MASTER,TABLE_NUM,ITEMS_NO,ITEMS_LIST,MAX_ROWS,COLUMN_NO):
	global COLOR_CHOICE
	COLOR_CHOICE = 0
	globals()[f'treeview{TABLE_NUM}'].delete(*globals()[f'treeview{TABLE_NUM}'].get_children())
	database_Table_view_Height(MASTER,first_list_Scorll_X,first_list_Scorll_Y,ITEMS_NO,TABLE_NUM,MAX_ROWS)
	if ITEMS_NO > 0:
		for TABLE in ITEMS_LIST:
			if COLOR_CHOICE == 0:
				COLOR_CHOICE = COLOR_CHOICE + 1
			elif COLOR_CHOICE == 1:
				COLOR_CHOICE = COLOR_CHOICE - 1
			else:
				pass
				# print('error')
				# print(f'COLOR_CHOICE: {COLOR_CHOICE}')
			globals()[f'treeview{TABLE_NUM}'].insert("" , "end" , text = f"{TABLE[0]}", values = TABLE[1:COLUMN_NO] ,tag=f"{COLOR_TAG[COLOR_CHOICE]}")


def database_Table_view_Height(master,X,Y,ITEMS_NO,TABLE_NUM,MAX_ROWS):
	# global vsb
	# global TABLE_HEIGHT
	if ITEMS_NO <= MAX_ROWS :
		globals()['TABLE{TABLE_NUM}_HEIGHT'] =  ITEMS_NO
	elif ITEMS_NO >= MAX_ROWS:
		globals()['TABLE{TABLE_NUM}_HEIGHT'] = MAX_ROWS
	globals()[f'treeview{TABLE_NUM}'].configure(height=globals()['TABLE{TABLE_NUM}_HEIGHT'])
	if ITEMS_NO > MAX_ROWS:
		globals()[f'vbs{TABLE_NUM}'] = ttk.Scrollbar(master, orient="vertical", command=globals()[f'treeview{TABLE_NUM}'].yview)
		globals()[f'vbs{TABLE_NUM}'].place(x=X, y=Y, height=180)
	if ITEMS_NO <= MAX_ROWS:
		if f'vbs{TABLE_NUM}' in globals():
			globals()[f'vbs{TABLE_NUM}'].place_forget()
		if f'vbs{TABLE_NUM}' in locals():
			locals()[f'vbs{TABLE_NUM}'].place_forget()


def setup_background(BACKGROUND_COLOR,FONT_COLOR):
	global __font
	global canv
	global canv_text
	__font = tkfont.Font()
	canv = tkinter.Canvas(treeview1,background=BACKGROUND_COLOR,borderwidth=0,highlightthickness=0)
	canv_text = canv.create_text(0, 0,fill=FONT_COLOR,anchor='w')

def treeview_table_generator(MASTER,TREE_NUM,COLUMNS,WIDTHS,X,Y,TABLE_HEIGHT,geometry,COUNT):
	LEN = len(COLUMNS)
	if COUNT == 'OK':
		columns = COLUMNS[1:LEN]
	if COUNT == 'NO':
		columns = COLUMNS
	globals()[f'treeview{TREE_NUM}'] =  ttk.Treeview(MASTER,columns=(columns) ,height=TABLE_HEIGHT)
	COLUMN_NUM = 0
	for COLUMN in COLUMNS:
		if COUNT == 'OK':
			TEXT = "{}".format(COLUMN) 
		if COUNT == 'NO':
			TEXT = ""
		globals()[f'treeview{TREE_NUM}'].heading("#{}".format(COLUMN_NUM), text=TEXT, anchor = "w")
		globals()[f'treeview{TREE_NUM}'].column("#{}".format(COLUMN_NUM), width = WIDTHS[COLUMN_NUM], anchor = "w")
		COLUMN_NUM = COLUMN_NUM + 1
	
	if 'pack' in geometry:
		globals()[f'treeview{TREE_NUM}'].pack(fill=geometry['pack']['fill'],expand=geometry['pack']['expand'])
	if 'grid' in geometry:
		# print('grid is ok')
		globals()[f'treeview{TREE_NUM}'].grid(row=geometry['grid']['row'],column=geometry['grid']['column'],columnspan=geometry['grid']['columnspan'],sticky=geometry['grid']['sticky'])
	if 'place' in geometry:
		globals()[f'treeview{TREE_NUM}'].place(x=geometry['place']['X'],y=geometry['place']['Y'])


def table1():
	treeview_table_generator(fen,1,["Room No","Room Name","Room Type","Room Status"],[72,187,187,104],10,80,TABLE_HEIGHT,geometry={'place':{'X':10 , 'Y':80},'pack':{'fill': tkinter.BOTH ,'expand':1}},COUNT='OK')
	Style_generator(1,None,9,'light gray')
	globals()['treeview1'].bind('<<TreeviewSelect>>',selectItem)
	first_table_show_options('All','All','All')

def Style_generator(STYLE_NUM,FONT,FONT_SIZE,BG_COLOR):
	globals()[f'style{STYLE_NUM}'] = ttk.Style()
	globals()[f'style{STYLE_NUM}'].configure(f"treeview{STYLE_NUM}.Heading", font=(FONT, FONT_SIZE,'bold'),background=BG_COLOR)
	globals()[f'treeview{STYLE_NUM}'].tag_configure('gray', background=BG_COLOR)


def selectItem2(a):
	curItem = treeview2.focus()
	# print(curItem)
	LIST = view_selected_rate('__main2.db',str(treeview2.item(curItem)['text']))
	# print(LIST)
	groove_entry35.delete(0,'end')
	groove_entry35.insert(0, LIST[0][2])
	#update name:
	groove_entry36.delete(0,'end')
	groove_entry36.insert(0, LIST[0][3])
	#update type:
	#groove_entry3.current(room_types.index(LIST[0][2]))
	#update side
	groove_entry37.delete(0,'end')
	groove_entry37.insert(0, LIST[0][4])
	# #update beds
	groove_entry38.delete(0,'end')
	groove_entry38.insert(0, LIST[0][0])
	#update details:
	groove_entry34.delete(0,'end')
	groove_entry34.insert(0, LIST[0][1])


def update_all_check_in(num,STATUS):
	# global trace_checkin_inputs
	if STATUS == "IN USE":
		# trace_checkin_inputs = 1
		groove_entry0F2.config(state="normal",readonlybackground="white")
		groove_entry0F2.delete(0,'end')     #   serial folio no
		groove_entry0F2.insert(0,str(select_from_booking_table_where_num('__main2.db',num)[0][1]).zfill(6))#   serial folio no
		groove_entry0F2.config(state="readonly",readonlybackground="white")
		groove_entry1F2.delete(0,'end')     #   first name
		groove_entry1F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][2])     #   first name
		groove_entry2F2.delete(0,'end')     #   last name
		groove_entry2F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][3])     #   last name
		groove_entry3F2.delete(0,'end')     #   Rcad_no 
		groove_entry3F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][4])     #   Rcad_no 
		countrylist.current(list(map(lambda x:x.strip(),lineList)).index(str(select_from_booking_table_where_num('__main2.db',num)[0][5])))         #   country  "LIST"
		groove_entry4F2.delete(0,'end')     #   adress
		groove_entry4F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][6])          #   adress
		ID_TYPE_LIST.current(ID_TYPES.index(str(select_from_booking_table_where_num('__main2.db',num)[0][7])))        #   id type "LIST"
		groove_entry5F2.delete(0,'end')     #   id_no 
		groove_entry5F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][8])     #   id_no 
		carlist.current(cars.index(str(select_from_booking_table_where_num('__main2.db',num)[0][9])))             #   "LIST"
		groove_entry6F2.delete(0,'end')     #   plate no
		groove_entry6F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][10])     #   plate no
		groove_entry7F2.delete(0,'end')     #   room number
		groove_entry7F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][0])     #   room number
		DateIn.current(date_list.index(str(select_from_booking_table_where_num('__main2.db',num)[0][11])))              #   "list"
		DateOut.current(date_list.index(str(select_from_booking_table_where_num('__main2.db',num)[0][13])))             #   "LIST"
		groove_entry8F2.delete(0,'end')     #   no of days
		groove_entry8F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][14])     #   no of days
		groove_entry9F2.delete(0,'end')     #   no of adults
		groove_entry9F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][15])     #   no of adults
		groove_entry10F2.delete(0,'end')    #   no of childs
		groove_entry10F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][16])    #   no of childs
		groove_entry11F2.delete(0,'end')    #   rate/period
		groove_entry11F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][18])    #   rate/period
		groove_entry12F2.delete(0,'end')    #   total/charge
		groove_entry12F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][19])    #   total/charge
		groove_entry14F2.delete(0,'end')    #   other charges
		groove_entry14F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][20])    #   other charges
		groove_entry15F2.delete(0,'end')    #   discount
		groove_entry15F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][21])    #   discount
		groove_entry16F2.delete(0,'end')    #   total
		groove_entry16F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][22])    #   total
		groove_entry17F2.delete(0,'end')    #   amount paied
		groove_entry17F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][23])    #   amount paied
		groove_entry18F2.delete(0,'end')    #   balance
		groove_entry18F2.insert(0,select_from_booking_table_where_num('__main2.db',num)[0][24])    #   balance
	if STATUS == "Free":
		# trace_checkin_inputs = 0
		groove_entry0F2.config(state="normal",readonlybackground="white")
		groove_entry0F2.delete(0,'end')     #   serial folio no
		groove_entry0F2.insert(0,f"{str(int(view_serial_table('__main2.db')[-1][0])+1).zfill(6)}")     #   serial folio no
		groove_entry0F2.config(state="readonly",readonlybackground="white")
		groove_entry1F2.delete(0,'end')     #   first name
		groove_entry2F2.delete(0,'end')     #   last name
		groove_entry3F2.delete(0,'end')     #   Rcad_no 
		countrylist.current(0)              #   country  "LIST"
		groove_entry4F2.delete(0,'end')     #   adress
		ID_TYPE_LIST.current(0)             #   id type "LIST"
		groove_entry5F2.delete(0,'end')     #   id_no 
		carlist.current(0)             #   "LIST"
		groove_entry6F2.delete(0,'end')     #   plate no
		DateIn.current(date_list.index(date.today().strftime("%Y-%m-%d")))          #   "list"
		DateOut.current(date_list.index(date.today().strftime("%Y-%m-%d")))             #   "LIST"
		groove_entry8F2.delete(0,'end')     #   no of days
		groove_entry8F2.insert(0,0)     #   no of days
		groove_entry9F2.delete(0,'end')     #   no of adults
		groove_entry9F2.insert(0,0)     #   no of adults
		groove_entry10F2.delete(0,'end')    #   no of childs
		groove_entry10F2.insert(0,0)    #   no of childs

def normalize_checkin_fileds():
	red_warning_entry_borders('groove_entry7F2','NORMAL')
	red_warning_entry_borders('groove_entry0F2','NORMAL')
	red_warning_entry_borders('groove_entry1F2','NORMAL')
	red_warning_entry_borders('groove_entry2F2','NORMAL')
	red_warning_entry_borders('groove_entry4F2','NORMAL')
	red_warning_entry_borders('groove_entry5F2','NORMAL')
	red_warning_entry_borders('groove_entry8F2','NORMAL')

def selectItem(a):
	global trace_checkin_inputs,update_trace_checkin_inputs,CHECKIN_CHOICE
	CHECKIN_CHOICE = None
	trace_checkin_inputs = 0
	update_trace_checkin_inputs = 0
	normalize_checkin_fileds()
	curItem = treeview1.focus()
	# print(curItem)
	LIST = view_selected_data('__main2.db','All','All',int(treeview1.item(curItem)['text']))
	#print(LIST)
	groove_entry1.delete(0,'end')
	groove_entry1.insert(0, LIST[0][0])
	#update name:
	groove_entry2.delete(0,'end')
	groove_entry2.insert(0, LIST[0][1])
	#update type:
	groove_entry3.current(room_types.index(LIST[0][2]))
	#update side
	groove_entry5.delete(0,'end')
	groove_entry5.insert(0, LIST[0][4])
	#update beds
	groove_entry6.delete(0,'end')
	groove_entry6.insert(0, LIST[0][6])
	#update details:
	groove_entry4.delete(0,'end')
	groove_entry4.insert(0, LIST[0][5])
	if LIST[0][3] == 'Free':
		room_status.configure(text="       Free         ",background="pale green",relief="solid")
	elif LIST[0][3] == 'IN USE':
		room_status.configure(text="      IN USE      ",background="tomato",relief="solid")
	else:
		pass
		# print('error')
	#update room number:
	groove_entry7F2.delete(0,'end')
	groove_entry7F2.insert(0,LIST[0][0])
	#update Room Type:
	Rate_Type_CHECKIN.current(room_types.index(LIST[0][2]))
	modify_paymen_numbers_2()
	if LIST[0][3] == "IN USE":
		update_all_check_in(LIST[0][0],"IN USE")
	elif LIST[0][3] == "Free":
		update_all_check_in(LIST[0][0],"Free")
	


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
	R_Type = ttk.Combobox(Room_View,values=['All']+select_types("__main2.db"),width=11)
	R_number = ttk.Combobox(Room_View,values=['All']+select_room_numbers('__main2.db'),width=3)
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
	def live_time_change():
		timenow =  datetime.now().time().strftime('%H:%M:%S')
		datenow = datetime.now().strftime('%A,%d %B %Y')
		clock.config(text=timenow)
		DATE.config(text=datenow,width=23)
		fen.after(200, live_time_change)
	datenow = datetime.now().strftime('%A,%d %B %Y')
	timenow =  datetime.now().time().strftime('%H:%M:%S')
	Time = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Time.place(relx=0.74, rely=0.108, anchor=tkinter.NW)
	tkinter.Label(fen, text='Time',bg="light gray").place(relx=.77, rely=0.108,anchor=tkinter.W)
	clock = tkinter.Label(Time, text=f'{timenow}',font=("Helvetica", 24),bg="light gray")
	clock.pack(side=tkinter.TOP, anchor=tkinter.N)
	DATE = tkinter.Label(Time, text=f'{datenow}',bg="light gray")
	DATE.pack(side=tkinter.TOP, anchor=tkinter.W)
	live_time_change()


def main():
	date_list()
	clock_date()
	Room_View_Options()
	create_main_database("__main2.db")
	create_rate_table("__main2.db")
	create_serial_table("__main2.db")
	# create_type_table("__main2.db")
	#insert_to_database(1,'single bed','Standard','Free','west','2xtoilets','2xsingle')
	view_selected_data('__main2.db','All','All','All')
	table1()
	Cashier_operations()
	# print(f'types: {select_types("__main2.db")}')
	# date_one_day_after("2020-04-14",1)
	create_booking_table('__main2.db')
	create_new_booking_room('__main2.db',1)
	create_new_booking_room('__main2.db',2)
	# update_all_check_in()

#widget:
fen = tkinter.Tk()

fen.title('Hotel')

can = tkinter.Canvas(fen , height=570,width=800,bg="light gray")
can.create_text(85,45,fill="black",font="albattar 20 bold",text="Hotel Name",tags="NAME")

can.create_rectangle(9, 80, 578, 261, outline="white", fill="grey")
main()
can.pack()
fen.mainloop()



