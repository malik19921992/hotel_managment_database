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
sublime select multi-same word select-->"alt+f3"
728: use the function to change variable and look for way in the web page which describe the way
714: write this 
	#LAST_DATABASE_LINK
make admin user undeletable , cant change privilages , only can change password for admin
line: 772 update_users_table(DATABASE_NAME)
user's settings window
auto_checking_free_rooms(): 852
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

def read_from_config(file_path,section,key):
	from configparser import ConfigParser
	#Read config.ini file
	config_object = ConfigParser()
	config_object.read(file_path)
	#Get valueconfig
	SECTION = config_object[section]
	return SECTION[key]

#VARS:
LAST_DATABASE_LINK = read_from_config("config.ini","DATABASE_INFO","LAST_DATABASE_LINK")
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
def create_past_checkouts_table(DATABESE_NAME):
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS past_checkouts_table(
				Room_No INT,
				Guest_Name TEXT,
				Room_Type TEXT,
				serial_num INT,
				ID_Type TEXT,
				ID_No TEXT,
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
	# insert_to_serial_table(LAST_DATABASE_LINK,"000001")



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
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? , Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_In = ? , TIME_IN = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? , OTHER_CHARGES = ? , DISCOUNT = ? , TOTAL = ? , AMOUNT_PAID = ? , BALANCE = ? WHERE Room_No = ? ',(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	conn.commit()
	c.close()


def change_in_table_name_status(Room_No,STATUS):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE table_name SET Room_Status = ? WHERE Room_No = ? ',(STATUS,Room_No,))
	conn.commit()
	c.close()


def room_is_free(Room_No):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("SELECT Room_Status FROM table_name WHERE Room_No = ?",(Room_No,))
	rows = c.fetchall()
	for row in rows:
		return row[0] == 'Free'


def book_it(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	global update_trace_checkin_inputs,trace_checkin_inputs,CHECKIN_CHOICE
	CHECKIN_CHOICE = 'BOOKING'
	update_trace_checkin_inputs = 0
	#print(Rate_Type)
	#print('1) booking .')
	#print(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE)
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
					insert_to_serial_table(LAST_DATABASE_LINK,serial_num)
					first_table_show_options(Status.get(),R_Type.get(),R_number.get())
					update_auto_free_room(LAST_DATABASE_LINK,Room_No,'IN USE')
					#print('room is rented secsassfully')
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
	# print(int(Room_No) in list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0])
	if Room_No == '' or Room_No == None:
		red_warning_entry_borders('groove_entry7F2','RED')
		check_in_input_error_messages.append("room number field is empty .!")
	elif Room_No != '' or Room_No != None:
		if int(Room_No) not in list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0]:
			#print(int(Room_No) not in list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0])
			red_warning_entry_borders('groove_entry7F2','RED')
			check_in_input_error_messages.append("room number not in table name, its not exists, choose defferant room .!")
		else:
			pass
	elif serial_num != '' and  Room_No != '' and str(serial_num) == str(select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1]).zfill(6) and view_selected_data(LAST_DATABASE_LINK,'All','All',Room_No)[0][3] == 'IN USE':
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
	SERIAL_TABLE = list(zip(*view_serial_table(LAST_DATABASE_LINK)))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'serial_num')))[0]
	TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0]

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


def insert_to_serial_table(DATABASE_NAME,SERIAL_NUM):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO serial_table(serial_num) VALUES (?)",(SERIAL_NUM,))
	conn.commit()
	c.close()


def check_if_serial_in_database(SERIAL_NUM):
	my_list = []
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
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
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO table_name VALUES (?,?,?,?,?,?,?)"
			,(Room_No,Room_Name,Room_Type,Room_Status,SIDE,DETAILS,BEDS))
	conn.commit()
	c.close()



def insert_rate_to_database(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate):
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO rate_table(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate) VALUES (?,?,?,?,?)"
			,(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate))
	conn.commit()
	c.close()



def database_items_count():
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute(''' SELECT COUNT(*) FROM table_name ''')
	result=c.fetchone()
	return result[0]
	c.close()



def check_if_room_in_database(NUM):
	my_list = []
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute(''' SELECT * FROM table_name ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(int(row[0]))
	return int(NUM) in my_list



def check_if_rate_in_database(Rate_Type):
	my_list = []
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute(''' SELECT * FROM rate_table ''')
	rows = c.fetchall()
	for row in rows:
		my_list.append(row[1].casefold())
	return Rate_Type.casefold() in my_list



def database_room_update(NUM,NAME,TYPE,SIDE,DETAILS,BEDS):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE table_name SET Room_Name = ? , Room_Type = ? , Room_Side = ? , Room_Details = ? , Room_Beds = ? WHERE Room_No = ? ',(NAME,TYPE,SIDE,DETAILS,BEDS,NUM,))
	conn.commit()
	c.close()



def database_rate_update(Rate_Type,Room_Rate,Person_No,Extra_Adults_Rate,Extra_Childrens_Rate):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE rate_table SET  Room_Rate = ? , Person_No = ? , Extra_Adults_Rate = ? , Extra_Childrens_Rate = ? WHERE Rate_Type = ? ',(float(Room_Rate),int(float(Person_No)),float(Extra_Adults_Rate),float(Extra_Childrens_Rate),str(Rate_Type),))
	conn.commit()
	c.close()



def database_room_delete(NUM):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("DELETE from table_name where Room_No = ?",(NUM,))
	conn.commit()
	c.close()



def database_rate_delete(Rate_Type):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
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
	ITEMS_NO = len(view_selected_rate(LAST_DATABASE_LINK,RATE_TYPE))
	COLUMN_NO = 5
	if ITEMS_NO > 0:
		ITEMS_LIST = view_selected_rate(LAST_DATABASE_LINK,RATE_TYPE)
	elif ITEMS_NO <= 0:
		ITEMS_LIST = None
	treeview_inserts(fen,2,ITEMS_NO,ITEMS_LIST,8,COLUMN_NO)


def Cashier_operations(*args):
	Cashier = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Cashier.place(relx=0.015, rely=0.48, anchor=tkinter.NW)
	tkinter.Label(fen, text='Cashier operations',background="light gray").place(relx=.12, rely=0.48,anchor=tkinter.W)

	nb = ttk.Notebook(Cashier,style="Treeview.Heading")
	nb.pack(fill=tkinter.BOTH, expand=tkinter.Y, padx=2, pady=10)
	
	if args[0][0] == 'On' and args[0][1] == 'Off':
		f1 = tkinter.Frame(nb,background="light gray")
		nb.add(f1, text=" Room Settings ")
		rooms_options(f1,'read')
	elif args[0][1] == 'On':
		f1 = tkinter.Frame(nb,background="light gray")
		nb.add(f1, text=" Room Settings ")
		rooms_options(f1,'read|write')

	if args[0][0] == 'Off' and args[0][1] == 'Off':
		print('rooms_option dissabled......!')


	f2 = tkinter.Frame(nb,background="light gray")	
	f3 = tkinter.Frame(nb,background="light gray")	
	nb.add(f2, text=" CheckIn ")
	nb.add(f3, text=" CheckOut ")
	nb.select(f1)

	if args[0][2] == 'On': #discount On:
		CHECK_IN(f2,'On')
		CHECK_OUT(f3,'On')
	elif args[0][2] == 'Off': #discount off:
		CHECK_IN(f2,'Off')
		CHECK_OUT(f3,'Off')	
	
	if args[0][3] == 'On' and args[0][4] == 'Off':
		f4 = tkinter.Frame(nb,background="light gray")
		nb.add(f4, text=" Room Price OPtions ")
		room_price_options(f4,'read')
		treeview_rate_options_table(f4)
	elif args[0][4] == 'On':
		f4 = tkinter.Frame(nb,background="light gray")
		nb.add(f4, text=" Room Price OPtions ")
		room_price_options(f4,'read|write')
		treeview_rate_options_table(f4)
	if args[0][3] == 'Off' and args[0][4] == 'Off':
		print('rooms_option dissabled......!')
	
	if args[0][5] == 'On': 
		f5 = tkinter.Frame(nb,background="light gray")
		nb.add(f5, text=" User Settings ")
		USER_SETTINGS(f5)	
	elif args[0][5] == 'Off': 
		print('user settings is off for this user')

	if args[0][6] == 'On': 
		f6 = tkinter.Frame(nb,background="light gray")
		nb.add(f6, text=" Database Settings ")
		DATABASE_SETTINGS(f6)
	elif args[0][6] == 'Off': 
		print('database settings is off for this user')



def set_value_in_property_file(file_path, section, key, value):
	import configparser
	config = configparser.RawConfigParser()
	config.read(file_path)
	config.set(section,key,value)                         
	cfgfile = open(file_path,'w')
	config.write(cfgfile, space_around_delimiters=False)  # use flag in case case you need to avoid white space.
	cfgfile.close()


def create_config_if_not_exists():
	from configparser import ConfigParser
	#Get the configparser object
	config_object = ConfigParser()
	#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
	config_object["DATABASE_INFO"] = {
	    "LAST_DATABASE_LINK": "/home/mal/Templates/learnpy/projects/hotel_database/__main.db",
	    "loginid": "chankeypathak",
	    "password": "tutswiki"
	}
	config_object["SERVERCONFIG"] = {
	    "host": "tutswiki.com",
	    "port": "8080",
	    "ipaddr": "8.8.8.8"
	}
	#Write the above sections to config.ini file
	with open('config.ini', 'w') as conf:
	    config_object.write(conf)





def boolian_check_file_exists(path):
	return os.path.isfile(path)


def open_database_file():
	global groove_entry1m
	import os
	from tkinter import filedialog
	can.filename =  filedialog.askopenfilename(initialdir = f"{os.path.dirname(os.path.abspath(__file__))}",title = "Select file",filetypes = (("database file","*.db "),("all files","*.*")))
	groove_entry1m.delete(0,"end")
	groove_entry1m.insert(0,f"{can.filename}")

	if boolian_check_file_exists("config.ini"):
		set_value_in_property_file("config.ini", "DATABASE_INFO" , "LAST_DATABASE_LINK" , can.filename)
	elif not boolian_check_file_exists("config.ini"):
		create_config_if_not_exists()

	# write this on  first line of script
	# LAST_DATABASE_LINK
	# set_value_in_property_file(file_path, section, key, value)


def  create_new_database():
	from tkinter.filedialog import asksaveasfile 
	files = [('SQLite Database file', "*.db"),]
	types = ['.db',]
	file = asksaveasfile(mode = "w",filetypes = files, defaultextension = types ) 


def save_database():
	from tkinter.filedialog import asksaveasfile 
	files = [('SQLite Database file', "*.db"),]
	types = ['.db',]
	file = asksaveasfile(mode = "w",filetypes = files, defaultextension = types )


def DATABASE_SETTINGS(MASTER):
	global groove_entry1m
	f6 = MASTER
	groove_entry1m = tkinter.Entry(f6,font=10,relief="groove",background="white",width=55)
	groove_entry1m.grid(row=1,column=0,columnspan=7,sticky='we')
	groove_entry1m.insert(0,"")
	if boolian_check_file_exists("config.ini"):
		groove_entry1m.insert(0,read_from_config("config.ini","DATABASE_INFO","LAST_DATABASE_LINK"))
	tkinter.Button(f6,text='open database ',background="light gray",command=open_database_file).grid(row=0,column=0,sticky='we')
	tkinter.Button(f6,text='new database ',background="light gray",command=create_new_database).grid(row=0,column=1,sticky='we')
	tkinter.Button(f6,text='over network',background="light gray",command=print("nigit")).grid(row=0,column=2,sticky='we')
	tkinter.Button(f6,text='save as',background="light gray",command=save_database).grid(row=0,column=3,sticky='we')


def column_from_users_table(column):
	n = 0
	LIST = []
	for i in read_from_users_table(LAST_DATABASE_LINK,'All'):
		LIST.append(read_from_users_table(LAST_DATABASE_LINK,'All')[n][column])
		n += 1
	return LIST

def create_new_user(user_name,password,confirm_password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings):
	global List_of_users
	if password != confirm_password:
		print('password not the same as cinfirm password...')
	if confirm_password.isspace():
		print('confirm password is empty')
	if password.isspace():
		print('password is empty...')
	if  user_name in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
		print('this user is exist , try to use new user')
	if user_name.isspace():
		print('user name is empty....')	
	#check if username not empty field
	if not user_name.isspace():
		#check if username not in database
		if user_name not in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
			#check if password not empty
			if not password.isspace():
				#check if confirm password not empty
				if not confirm_password.isspace():
					#check if password == confirm_password
					if password == confirm_password:
						#if all right:
						insert_to_users_table(LAST_DATABASE_LINK,user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings)
						#free three fields
						if 'groove_entry1d' in globals():
							groove_entry1d.delete(0,'end')
						if 'groove_entry2d' in globals():
							groove_entry2d.delete(0,'end')
						if 'groove_entry3d' in globals():
							groove_entry3d.delete(0,'end')
						#refresh list of users
						if 'List_of_users' in globals():
							List_of_users['values'] = ['All']+column_from_users_table(0)
							for i in range(1,8):
								butons[i]["label"] = "off"
								butons[i].set(0)

def USER_SETTINGS(MASTER):
	#add admin  user , undeletble , update only password , no privliages update , no change name.
	global groove_entry1d,groove_entry2d,groove_entry3d,List_of_users
	
	def update_user_details(user_name,password,confirm_password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings):
		# print(read_from_users_table(LAST_DATABASE_LINK,user_name)[0][1])
		if user_name.isspace():
			print('user name is empty field , choose user')
		if user_name not in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
			print('user name not exists')
		if not user_name.isspace():
			#check if username not in database
			if user_name in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
				if not password.isspace():
					if password == read_from_users_table(LAST_DATABASE_LINK,user_name)[0][1]:
						update_users_table(LAST_DATABASE_LINK,user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings)
					elif password != read_from_users_table(LAST_DATABASE_LINK,user_name)[0][1]:
						if not confirm_password.isspace():
							if confirm_password == password:
								print('change password')
								update_users_table(LAST_DATABASE_LINK,user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings)
							elif confirm_password != password:
								print('password not the same as confirm')
						if confirm_password.isspace():
							print('type confirm password.....!to change')
				elif password.isspace():
					print('password is empty field....!')
	
	def delete_user(user_name):
		#if user_name exists in databas":
		if user_name in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
			#if user_name != 'admin':
			if user_name != 'admin':
				pass
				# tkinter.ask question yes ? , no
				DELETE_USER = tkinter.messagebox.askquestion(message="do you really want to delete this user?")
				if DELETE_USER  == 'yes':
					# choose All
					List_of_users.current(0)
					# delete user from database
					delete_user_from_users_table(LAST_DATABASE_LINK,user_name)
					# free fields
					groove_entry1d.delete(0,'end')
					groove_entry2d.delete(0,'end')
					groove_entry3d.delete(0,'end')
					for i in range(1,8):
						butons[i]["label"] = "off"
						butons[i].set(0)

				elif DELETE_USER == 'no':
					pass
			elif user_name == 'admin':
				print('admin user is indeletable....!')
		elif user_name not in read_column_from_users_table(LAST_DATABASE_LINK,"user_name"):
			print('user name not exists...!')
	f5 = MASTER
	#BUTTONS:
	tkinter.Button(f5,text='new user ',background="light gray",command=lambda:create_new_user(groove_entry1d.get(),groove_entry2d.get(),groove_entry3d.get(),butons[1]["label"],butons[2]["label"],butons[3]["label"],butons[4]["label"],butons[5]["label"],butons[6]["label"],butons[7]["label"])).grid(row=0, column=2,sticky='we')
	tkinter.Button(f5,text='update user ',background="light gray",command=lambda:update_user_details(groove_entry1d.get(),groove_entry2d.get(),groove_entry3d.get(),butons[1]["label"],butons[2]["label"],butons[3]["label"],butons[4]["label"],butons[5]["label"],butons[6]["label"],butons[7]["label"])).grid(row=0, column=3,sticky='we')
	tkinter.Button(f5,text='delete user ',background="light gray",command=lambda:delete_user(groove_entry1d.get())).grid(row=0, column=4,sticky='we')
	#LABELS:
	tkinter.Label(f5,text="username",background="light gray").grid(row=1,column=0,sticky='w')
	tkinter.Label(f5,text="password",background="light gray").grid(row=1,column=2,sticky='w')
	tkinter.Label(f5,text="confirm password",background="light gray").grid(row=1,column=4,sticky='w')
	tkinter.Label(f5,text="list of users",background="light gray").grid(row=0,column=0,sticky='w')
	#ENTRIES:
	groove_entry1d = tkinter.Entry(f5,font=10,relief="groove",background="white",width=13)
	groove_entry1d.grid(row=1,column=1,sticky='nwe')
	groove_entry1d.insert(0, "")
	groove_entry2d = tkinter.Entry(f5,font=10,relief="groove",background="white",width=13)
	groove_entry2d.grid(row=1,column=3,sticky='nwe')
	groove_entry2d.insert(0, "")
	groove_entry3d = tkinter.Entry(f5,font=10,relief="groove",background="white",width=13)
	groove_entry3d.grid(row=1,column=5,sticky='nwe')
	groove_entry3d.insert(0, "") 
	#LISTS:
	#change users list and and function related to:
	def users_choose_trigger(args):
		if List_of_users.get() == 'All':
			#free fields:
			#free username
			#free password
			#free confirm password
			groove_entry1d.delete(0,'end')
			groove_entry2d.delete(0,'end')
			groove_entry3d.delete(0,'end')
			#off all user privilages
			for i in range(1,8):
				butons[i]["label"] = "off"
				butons[i].set(0)
				# butons[i]["state"] = "disabled"
		else:
			# print(read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0])
			#fill the fields:
			#fill username
			groove_entry1d.delete(0,'end')
			groove_entry1d.insert(0,read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][0])
			#fill password
			groove_entry2d.delete(0,'end')
			groove_entry2d.insert(0,read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][1])
			#free confirm password
			groove_entry3d.delete(0,'end')
			#chnge user privilages:
			for i in range(1,8):
				butons[i]["label"] = read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][i+1]
				if read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][i+1] == "Off":
					# butons[i]["to"] = 0
					butons[i].set(0)
				elif read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][i+1] == "On":
					# butons[i]["to"] = 1
					butons[i].set(50)

				else:
					print('something else.....!')
					print(read_from_users_table(LAST_DATABASE_LINK,List_of_users.get())[0][i+1])

	List_of_users = ttk.Combobox(f5,values=['All']+column_from_users_table(0),width=13)
	List_of_users.grid(row=0,column=1,sticky='w')
	List_of_users.bind('<<ComboboxSelected>>', users_choose_trigger)
	List_of_users.current(0) # list of users
	#Frame:
	prev = tkinter.Frame(f5, relief=tkinter.GROOVE,borderwidth=2,background="light gray")
	prev.place(relx=0.01, rely=0.250, anchor=tkinter.NW)
	tkinter.Label(f5, text='User Privileges',background="light gray").place(relx=.09, rely=0.250,anchor=tkinter.W)
	tkinter.Label(prev,text=" "*25,background="light gray").grid(row=0,column=0,columnspan=7,sticky='w')
	global buton
	butons = {}
	for i in range(1,8):
		butons[i] = {}

	def degis(*args):
		if(args[0] == "1"):
			butons[int(args[1])]["label"] = "On"
		else:
			butons[int(args[1])]["label"] = "Off"

	tkinter.Label(prev,text=" "*25,background="light gray").grid(row=0,column=0,columnspan=7,sticky='w')
	butons[1] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "off" ,bg="light gray",command =lambda event:degis(event,'1'))
	butons[1].grid(row=1,column=1,sticky='nwe')
	butons[2] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'2'))
	butons[2].grid(row=2,column=1,sticky='nwe')
	butons[3] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'3'))
	butons[3].grid(row=3,column=1,sticky='nwe')
	butons[4] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'4'))
	butons[4].grid(row=1,column=3,sticky='nwe')
	butons[5] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'5'))
	butons[5].grid(row=2,column=3,sticky='nwe')
	butons[6] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'6'))
	butons[6].grid(row=3,column=3,sticky='nwe')
	butons[7] = tkinter.Scale(prev , orient=tkinter.HORIZONTAL,width=15,length = 50,to = 1,showvalue = False,sliderlength = 25,label = "Off",bg="light gray",command =lambda event:degis(event,'7'))
	butons[7].grid(row=1,column=5,sticky='nwe')
	tkinter.Label(prev,text="Read room settings",background="light gray").grid(row=1,column=0,sticky='ws')
	tkinter.Label(prev,text="Write room settings",background="light gray").grid(row=2,column=0,sticky='ws')
	tkinter.Label(prev,text="Disccount",background="light gray").grid(row=3,column=0,sticky='ws')
	tkinter.Label(prev,text="read room prices",background="light gray").grid(row=1,column=2,sticky='ws')
	tkinter.Label(prev,text="write room prices",background="light gray").grid(row=2,column=2,sticky='ws')
	tkinter.Label(prev,text="allow user settings",background="light gray").grid(row=3,column=2,sticky='ws')
	tkinter.Label(prev,text="allow database settings",background="light gray").grid(row=1,column=4,sticky='ws')
	#add_new user
	#change password
	#change privilages what can open ,example: normal user cant open user's settings field and not allow to change discount 
	#root user , unchangble only one user
	#you change root password  
	#admin user, you can gave admin privaligaes for more than one user
	#privilages as radio buttons swtitch on/off 
	#save settings button to save in database
	#increpted passwords in database


def create_users_table(DATABESE_NAME):
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS users_table(
				user_name TEXT,
				password TEXT,
				read_room_settings INT,
				write_room_settings INT,
				Discount INT,
				read_room_price INT,
				write_room_price INT,
				allow_user_settings INT,
				allow_database_settings INT) ''')
	conn.commit()
	conn.close()


def insert_to_users_table(DATABASE_NAME,user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO users_table(user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings) VALUES (?,?,?,?,?,?,?,?,?)",(user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings,))
	conn.commit()
	c.close()


def update_users_table(DATABASE_NAME,user_name,password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute('UPDATE users_table SET password = ? , read_room_settings = ? , write_room_settings = ? , Discount = ? , read_room_price = ? , write_room_price = ? , allow_user_settings = ? , allow_database_settings = ?  WHERE user_name = ? ',
			(password,read_room_settings,write_room_settings,Discount,read_room_price,write_room_price,allow_user_settings,allow_database_settings,user_name,))
	conn.commit()
	c.close()


def read_from_users_table(DATABASE_NAME,user_name):
	my_list = []
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	if user_name == 'All':
		c.execute("SELECT * FROM users_table")
	else:
		c.execute('SELECT * FROM users_table WHERE user_name = ? ',(user_name,))
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list

def delete_user_from_users_table(DATABASE_NAME,user_name):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("DELETE FROM users_table WHERE user_name = ?",(user_name,))
	conn.commit()
	c.close()


def read_column_from_users_table(DATABASE_NAME,column_name):
	my_list = []
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("SELECT "+column_name+" FROM users_table")
	rows = c.fetchall()
	for row in rows:
		my_list.append(row[0])
	return my_list


# def DATABASE_SETTINGS(MASTER):
# 	pass


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
				Rate_Type_CHECKIN.config(values=select_types(LAST_DATABASE_LINK))
				groove_entry3.config(values=select_types(LAST_DATABASE_LINK))
				R_Type.config(values=['All']+select_types(LAST_DATABASE_LINK))
				Rate_Type_List.config(values=['All']+select_types(LAST_DATABASE_LINK))
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
				Rate_Type_CHECKIN.config(values=select_types(LAST_DATABASE_LINK))
				groove_entry3.config(values=select_types(LAST_DATABASE_LINK))
				R_Type.config(values=['All']+select_types(LAST_DATABASE_LINK))
				Rate_Type_List.config(values=['All']+select_types(LAST_DATABASE_LINK))
			elif check_if_rate_in_database(Rate_Type) == False:
				tkinter.messagebox.showinfo(message="Delete Error , \n room  is not exists .")
		else:
			# print('rate option is wrong')
			pass
		secound_table_show_options(rate_type_choose_trigger())
	except ValueError:
		pass
	secound_table_show_options('All')


def rate_type_choose_trigger(*args):
	secound_table_show_options(Rate_Type_List.get())


def room_price_options(MASTER,PRIV):

	if PRIV == 'read':
		print('buttons dissabled')
		STATE = "disabled"
	elif PRIV == 'read|write':
		print('buttons open')
		STATE = "normal"
	
	global groove_entry34,groove_entry35,groove_entry36,groove_entry37,groove_entry38,Rate_Type_List
	f4 = MASTER
	#BUTTONS:
	tkinter.Button(f4,text='New Type',background="light gray",state=STATE,command=lambda:room_price_buttons('new',groove_entry38.get(),groove_entry34.get(),groove_entry35.get(),groove_entry36.get(),groove_entry37.get())).grid(row=1, column=1,sticky='we')
	tkinter.Button(f4,text='Update',background="light gray",state=STATE,command=lambda:room_price_buttons('update',groove_entry38.get(),groove_entry34.get(),groove_entry35.get(),groove_entry36.get(),groove_entry37.get())).grid(row=1, column=2,sticky='we')
	tkinter.Button(f4,text='Delete',background="light gray",state=STATE,command=lambda:room_price_buttons('delete',groove_entry38.get())).grid(row=1, column=3,sticky='we')
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
	Rate_Type_List = ttk.Combobox(f4,values=['All']+select_types(LAST_DATABASE_LINK),width=11)
	Rate_Type_List.grid(row=2,column=0,sticky='w')
	Rate_Type_List.bind('<<ComboboxSelected>>', rate_type_choose_trigger)
	Rate_Type_List.current(0)


def insert_to_past_checkouts(DATABASE_NAME,Room_No):
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("INSERT INTO past_checkouts_table(Room_No,Guest_Name,Room_Type,serial_num,ID_Type,ID_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
			,(Room_No,groove_entry20.get(),groove_entry23.get(),groove_entry0F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get()))
	conn.commit()
	c.close()


def boolian_remain_time(s1,s2):
	import datetime
	format = '%d-%m-%Y %H:%M:%S'
	remain_time = datetime.datetime.strptime(str(s1),format) - datetime.datetime.strptime(str(s2),format)
	if int(remain_time.total_seconds()) > 0:
		return True
	elif int(remain_time.total_seconds()) <= 0:
		return False


def now_datetime():
	from datetime import datetime
	now = datetime.now()
	timenow = now.strftime("%d-%m-%Y %H:%M:%S")
	return timenow


def booking_end_datetime(Room_No):
	year,month,day = select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][13].split("-")
	time = select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][12]
	last_timedate = f"{day}-{month}-{year} {time}"
	return last_timedate


def create_auto_free_table(DATABASE_NAME):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute(''' CREATE TABLE IF NOT EXISTS auto_free_table(
		Room_No INT PRIMARY KEY NOT NULL,
		Status TEXT NOT NULL) ''')
	conn.commit()
	conn.close()


def insert_auto_free_room(DATABASE_NAME,Room_No,STATUS):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("INSERT OR IGNORE INTO auto_free_table(Room_No,Status) VALUES (?,?)"
		,(Room_No,STATUS))
	conn.commit()
	conn.close()


def update_auto_free_room(DATABASE_NAME,Room_No,STATUS):
	conn = sqlite3.connect(DATABASE_NAME)
	c = conn.cursor()
	c.execute("UPDATE auto_free_table SET Status = ? WHERE Room_No =  ? ",(STATUS,Room_No,))
	conn.commit()
	conn.close()


def auto_create_list_of_auto_free_rooms():
	TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0]
	for room in TABLE_NAME_ROOM_NUMS:
		insert_auto_free_room(LAST_DATABASE_LINK,room,'Free')


def get_auto_free_status(DATABASE_NAME,Room_No,STATUS):
	pass


def auto_free_room(Room_No):
	pass


def checkout_print():
	pass


def auto_checking_free_rooms():
	pass
	#for room in table_name rooms:
		#if check_if_auto-free mode:
			#if remain time <= 0:
				#free the room
				#blinking mark room with green color in list1 for 30 min or until booking again if less
		#elif not check_if_auto_free_mode:
			#if remain time <= 0:
				#blinking red until checkout order
		#if remain time closer to 0:
			#keep blinking yellow until 0 time
	#change: room status in Room settings
	#change: remain time in Room settings
	#fen.after(200, live_time_change)



def checkout_order(Room_No):
	global checkout_status
	if boolian_room_status(Room_No,'IN USE'):
		insert_to_past_checkouts(LAST_DATABASE_LINK,Room_No)
		print('room is in use...!!')
		if boolian_remain_time(booking_end_datetime(Room_No),now_datetime()):
			update_auto_free_room(LAST_DATABASE_LINK,Room_No,'autoFree')
			free_checkout_fields(Room_No)
			checkout_status.config(text="Amount Paid",background="sky blue")
		elif not boolian_remain_time(booking_end_datetime(Room_No),now_datetime()):
			delete_feilds_in_booking_table(Room_No)
			change_table_name_room_status(Room_No,'Free')
			free_checkout_fields(Room_No)
			clear_check_in_fields()
			checkout_status.config(text="Amount closed",background="yellow")
			first_table_show_options('All','All','All')

		
def CHECK_OUT(MASTER,DISCOUNT):
	
	if DISCOUNT == 'Off':
		STATE = "disabled"
	elif DISCOUNT == 'On':
		STATE = "normal"

	global groove_entry21,groove_entry19,groove_entry20,groove_entry22,groove_entry22b,groove_entry19b,groove_entry19c,checkout_status
	global CHECKOUT_BUTTON,groove_entry23,groove_entry24,groove_entry25,groove_entry26,groove_entry27,groove_entry28,groove_entry29,groove_entry30,groove_entry31,groove_entry32,groove_entry33
	f3 = MASTER
	#BUTTONS:
	CHECKOUT_BUTTON = tkinter.Button(f3, text='CheckOut',background="light gray",command=lambda:checkout_order(groove_entry21.get()))
	CHECKOUT_BUTTON.grid(row=0, column=0,sticky='we')
	tkinter.Button(f3,text='Print',background="light gray",command=lambda:checkout_print()).grid(row=0, column=1,sticky='we')
	#LABELS:
	checkout_status = tkinter.Label(f3, text="Amount Free",background="pale green",relief="solid",width=13,height=1)
	checkout_status.grid(row=0,column=2,sticky='w')
	tkinter.Label(f3,text="Guest Name ",background="light gray").grid(row=1,column=0,sticky='w')
	tkinter.Label(f3,text="ID_Type",background="light gray").grid(row=2,column=0,sticky='w')
	tkinter.Label(f3,text="ID_No",background="light gray").grid(row=3,column=0,sticky='w')
	tkinter.Label(f3,text="Folio No ",background="light gray").grid(row=4,column=0,sticky='w')
	tkinter.Label(f3,text="Room No",background="light gray").grid(row=5,column=0,sticky='w')
	tkinter.Label(f3,text="Date In",background="light gray").grid(row=6,column=0,sticky='w')
	tkinter.Label(f3,text="Date Out",background="light gray").grid(row=7,column=0,sticky='w')
	tkinter.Label(f3,text="Rate Type",background="light gray").grid(row=8,column=0,sticky='w')
	tkinter.Label(f3,text="Rate/Piriod",background="light gray").grid(row=2,column=2,sticky='w')
	tkinter.Label(f3,text="No. of Days",background="light gray").grid(row=3,column=2,sticky='w')
	tkinter.Label(f3,text="No.of Adults",background="light gray").grid(row=4,column=2,sticky='w')
	tkinter.Label(f3,text="No.of Children",background="light gray").grid(row=5,column=2,sticky='w')
	tkinter.Label(f3,text="Other Charges",background="light gray").grid(row=6,column=2,sticky='w')
	tkinter.Label(f3,text="Sub Total",background="light gray").grid(row=7,column=2,sticky='w')
	tkinter.Label(f3,text="Dicount",background="light gray").grid(row=8,column=2,sticky='w')
	tkinter.Label(f3,text="%",background="light gray").grid(row=8,column=5,sticky='w')
	tkinter.Label(f3,text="Total",background="light gray").grid(row=1,column=6,sticky='w')
	tkinter.Label(f3,text="Amount Paid",background="light gray").grid(row=2,column=6,sticky='w')
	tkinter.Label(f3,text="Balance",background="light gray").grid(row=3,column=6,sticky='w')
	#ENTRIES:
	groove_entry20 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=32)
	groove_entry20.grid(row=1,column=1,columnspan=5,sticky='nsw')
	groove_entry20.insert(0, "") #guest name
	groove_entry19b = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry19b.grid(row=2,column=1,sticky='nsw')
	groove_entry19b.insert(0,ID_TYPE_LIST.get())
	groove_entry19c = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry19c.grid(row=3,column=1,sticky='nsw')
	groove_entry19c.insert(0,groove_entry5F2.get())
	groove_entry19 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry19.grid(row=4,column=1,sticky='nsw')
	groove_entry19.insert(0, "") # serial number folio
	groove_entry21 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry21.grid(row=5,column=1,sticky='nsw')
	groove_entry21.insert(0, "") #room num
	groove_entry22 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry22.grid(row=6,column=1,sticky='nsw')
	groove_entry22.insert(0, "")
	groove_entry22b = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry22b.grid(row=7,column=1,sticky='nsw')
	groove_entry22b.insert(0, "")
	groove_entry23 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry23.grid(row=8,column=1,sticky='nsw')
	groove_entry23.insert(0, "") #Double
	groove_entry24 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=9)
	groove_entry24.grid(row=2,column=3,columnspan=4,sticky='nsw')
	groove_entry24.insert(0, "")
	groove_entry25 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry25.grid(row=3,column=3,sticky='w')
	groove_entry25.insert(0, "")
	groove_entry26 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry26.grid(row=4,column=3,sticky='w')
	groove_entry26.insert(0, "")
	groove_entry27 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=3)
	groove_entry27.grid(row=5,column=3,sticky='w')
	groove_entry27.insert(0, "")
	groove_entry28 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=9)
	groove_entry28.grid(row=6,column=3,columnspan=5,sticky='nsw')
	groove_entry28.insert(0, "")
	groove_entry29 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=9)
	groove_entry29.grid(row=7,column=3,columnspan=5,sticky='nsw')
	groove_entry29.insert(0, "")
	groove_entry30 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=6,state=STATE,disabledbackground="red")
	groove_entry30.grid(row=8,column=3,columnspan=4,sticky='nsw')
	groove_entry30.insert(0, "")
	groove_entry31 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry31.grid(row=1,column=8,sticky='nsw')
	groove_entry31.insert(0, "")
	groove_entry32 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry32.grid(row=2,column=8,sticky='nsw')
	groove_entry32.insert(0, "")
	groove_entry33 = tkinter.Entry(f3,font=10,relief="groove",background="white",width=10)
	groove_entry33.grid(row=3,column=8,sticky='nsw')
	groove_entry33.insert(0, "")


def modify_paymen_numbers_2(*args):
	try:
		# print(args)
		def Extract(lst,NUM):
			return list(list(zip(*lst))[NUM])
		my_list = []
		rate = view_selected_rate(LAST_DATABASE_LINK,Rate_Type_CHECKIN.get())
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
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? , Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? , OTHER_CHARGES = ? , DISCOUNT = ? , TOTAL = ? , AMOUNT_PAID = ? , BALANCE = ? WHERE Room_No = ? ',(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	conn.commit()
	c.close()


	
def boolian_room_status(Room_No,STATUS):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("SELECT Room_Status FROM table_name WHERE Room_No = ?",(Room_No,))
	rows = c.fetchall()
	for row in rows:
		return row[0] == STATUS


def boolian_Room_No_same_where_serial(Room_No,serial_num):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("SELECT Room_No FROM booking_table WHERE serial_num  = ?",(int(serial_num),))
	rows = c.fetchall()
	for row in rows:
		return row[0] == Room_No


def get_Room_No_with_serial(serial_num):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
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



def copy_between_rooms_booking_table(serial_num):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("SELECT * FROM booking_table WHERE serial_num  = ?",(int(serial_num),))
	rows = c.fetchall()
	for row in rows:
		return row


def paste_details_to_free_room(Room_No,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,serial_num):
	details = copy_between_rooms_booking_table(serial_num)
	First_Room_No = details[0]
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = ? , First_name = ? , Last_name = ? , R_CARD_No = ? , Country = ? , Adress = ? , ID_Type = ? , ID_No = ? , Car = ? , Plate_No = ? , Date_In = ? , TIME_IN = ? , Date_Out = ? , NO_OF_DAYS = ? , NO_OF_ADULTS = ? , NO_OF_CHILDS = ? , Rate_Type = ? , RATE_PERIOD = ? , TOTAL_CHARGE = ? , OTHER_CHARGES = ? , DISCOUNT = ? , TOTAL = ? , AMOUNT_PAID = ? , BALANCE = ? WHERE Room_No = ? ',(serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE,Room_No,))
	c.execute('UPDATE booking_table SET serial_num = NULL , First_name = NULL , Last_name = NULL , R_CARD_No = NULL , Country = NULL , Adress = NULL , ID_Type = NULL , ID_No = NULL , Car = NULL , Plate_No = NULL , Date_In = NULL , TIME_IN = NULL , Date_Out = NULL , NO_OF_DAYS = NULL , NO_OF_ADULTS = NULL , NO_OF_CHILDS = NULL , Rate_Type = NULL , RATE_PERIOD = NULL , TOTAL_CHARGE = NULL , OTHER_CHARGES = NULL , DISCOUNT = NULL , TOTAL = NULL , AMOUNT_PAID = NULL , BALANCE = NULL WHERE Room_No = ? ',(First_Room_No,))
	conn.commit()
	c.close()


def change_in_room_tabe_status(First_Room_No,Secound_Room_No):
	#change statuses in tabele_name:
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("UPDATE table_name SET Room_Status = 'Free' WHERE Room_No = ?",(First_Room_No,))
	c.execute("UPDATE table_name SET Room_Status = 'IN USE' WHERE Room_No = ?",(Secound_Room_No,))
	conn.commit()
	c.close()


def room_changing(serial_num,Room_No):
	details_list = copy_between_rooms_booking_table(serial_num)
	First_Room_No = details_list[0]
	Secound_Room_No =  Room_No
	paste_details_to_free_room(Room_No,details_list[2],details_list[3],details_list[4],details_list[5],details_list[6],details_list[7],details_list[8],details_list[9],details_list[10],details_list[11],details_list[12],details_list[13],details_list[14],details_list[15],details_list[16],details_list[17],details_list[18],details_list[19],details_list[20],details_list[21],details_list[22],details_list[23],details_list[24],details_list[1])
	change_in_room_tabe_status(First_Room_No,Secound_Room_No)
	first_table_show_options('All','All','All')
	pass


def check_wrong_fields_and_show_them(Room_No,serial_num):
	global change_room_wrong_messages_list
	change_room_wrong_messages_list = []
	#check what is the problem by prnting two fields bellow 
	if str(Room_No) == str(copy_between_rooms_booking_table(serial_num)[0]):
		change_room_wrong_messages_list.append("room is same number main room , try to change for defferant number....!")
	if not boolian_room_status(get_Room_No_with_serial(serial_num),'IN USE'):
		change_room_wrong_messages_list.append("your room you choosed is free, try to choose used room to change....!")
	if not check_if_room_in_database(Room_No):
		change_room_wrong_messages_list.append("room not in database....!")
	if boolian_room_status(get_Room_No_with_serial(serial_num),'IN USE'):
		if boolian_Room_No_same_where_serial(Room_No,serial_num):
			change_room_wrong_messages_list.append("this serial not for that number....!")
	if not boolian_room_status(Room_No,'Free'):
		change_room_wrong_messages_list.append("Room you want to change to is not Free....!")
	MESSAGE = ""
	for message in change_room_wrong_messages_list:
			MESSAGE = MESSAGE + f'\n{message}'
	tkinter.messagebox.showinfo(message=MESSAGE)


def CHANGE_ROOM_CHECK_IN(Room_No,serial_num,First_name,Last_name,R_CARD_No,Country,Adress,ID_Type,ID_No,Car,Plate_No,Date_In,TIME_IN,Date_Out,NO_OF_DAYS,NO_OF_ADULTS,NO_OF_CHILDS,Rate_Type,RATE_PERIOD,TOTAL_CHARGE,OTHER_CHARGES,DISCOUNT,TOTAL,AMOUNT_PAID,BALANCE):
	global CHECKIN_CHOICE
	CHECKIN_CHOICE = 'CHANGING'
	print(f' copy: {copy_between_rooms_booking_table(serial_num)[0]}')
	print(f'Room No: {Room_No}')
	if check_if_change_room_inputs_all_right(Room_No,serial_num,First_name,Last_name,Adress,ID_No,NO_OF_DAYS,Rate_Type):
		print(f'change room to {Room_No}')
		print(f'free room with serial {serial_num}')
		#message box with yse,no:
		CHANGE_ROOM_CHECKIN_CHOICE = tkinter.messagebox.askquestion(message="do you really want to change room?")
		if CHANGE_ROOM_CHECKIN_CHOICE  == 'yes':
			room_changing(serial_num,Room_No)
		elif CHANGE_ROOM_CHECKIN_CHOICE == 'no':
			pass
	else:
		check_wrong_fields_and_show_them(Room_No,serial_num)
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
	SERIAL_TABLE = list(zip(*view_serial_table(LAST_DATABASE_LINK)))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'serial_num')))[0]
	#use check_if_room_in_database(Room_No) insted to:
	#TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0]
	if not Room_No.isspace():
		if Room_No != '' and Room_No != None and serial_num != '' and serial_num != None and check_if_room_in_database(Room_No):
			if int(serial_num) == (list(zip(*select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)))[1][0]):
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
			return str(serial_num) == str(select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1]).zfill(6)
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
	SERIAL_TABLE = list(zip(*view_serial_table(LAST_DATABASE_LINK)))[0]
	BOOKING_TABLE_ROOM_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'Room_No')))[0]
	BOOKING_TABLE_SERIAL_NUMS = list(zip(*select_from_booking_table(LAST_DATABASE_LINK,'serial_num')))[0]
	TABLE_NAME_ROOM_NUMS = list(zip(*select_room_numbers(LAST_DATABASE_LINK)))[0]
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


def delete_feilds_in_booking_table(Room_No):
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute('UPDATE booking_table SET serial_num = NULL , First_name = NULL , Last_name = NULL , R_CARD_No = NULL , Country = NULL , Adress = NULL , ID_Type = NULL , ID_No = NULL , Car = NULL , Plate_No = NULL , Date_In = NULL , TIME_IN = NULL , Date_Out = NULL , NO_OF_DAYS = NULL , NO_OF_ADULTS = NULL , NO_OF_CHILDS = NULL , Rate_Type = NULL , RATE_PERIOD = NULL , TOTAL_CHARGE = NULL , OTHER_CHARGES = NULL , DISCOUNT = NULL , TOTAL = NULL , AMOUNT_PAID = NULL , BALANCE = NULL WHERE Room_No = ? ',(Room_No,))
	conn.commit()
	c.close()


def change_table_name_room_status(Room_No,STATUS):
	#change statuses in tabele_name:
	conn =None;
	conn = sqlite3.connect(LAST_DATABASE_LINK)
	c = conn.cursor()
	c.execute("UPDATE table_name SET Room_Status = ? WHERE Room_No = ?",(STATUS,Room_No,))
	conn.commit()
	c.close()


def clear_check_in_fields():
	groove_entry0F2.config(state="normal",readonlybackground="white")
	groove_entry0F2.delete(0,'end')     #   serial folio no
	groove_entry0F2.insert(0,f"{str(int(view_serial_table(LAST_DATABASE_LINK)[-1][0])+1).zfill(6)}")     #   serial folio no
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
	groove_entry8F2.insert(0,0)         #   no of days
	groove_entry9F2.delete(0,'end')     #   no of adults
	groove_entry9F2.insert(0,0)         #   no of adults
	groove_entry10F2.delete(0,'end')    #   no of childs
	groove_entry10F2.insert(0,0)        #   no of childs


def CANCEL_CHECK_IN_BOOING(Room_No,serial_num):
	print(f'serial_num: {serial_num}')
	if Room_No != '' and Room_No != 0 and not Room_No.isspace():
		if check_if_room_in_database(Room_No):
			if boolian_room_status(Room_No,'IN USE'):
				if boolian_Room_No_same_where_serial(int(Room_No),int(serial_num)):
					CANCEL_CHECK_MESSAGE = tkinter.messagebox.askquestion(message="do you want to cancel this booking ?")
					if CANCEL_CHECK_MESSAGE == 'yes':
						print('cancel')
						delete_feilds_in_booking_table(Room_No)
						change_table_name_room_status(Room_No,'Free')
						clear_check_in_fields()
						update_auto_free_room(LAST_DATABASE_LINK,Room_No,'Free')
						first_table_show_options('All','All','All')
					elif CANCEL_CHECK_MESSAGE == 'no':
						print('there is wrong thing....!')
				else:
					print('room num not same with serial in booking table....!')
			else:
				print('room is free')
		else:
			print('room with this number not in database')
	else:
		print('room number is empty')


def TIME_NOW():
	timenow =  datetime.now().time().strftime('%H:%M:%S')
	return timenow

def CHECK_IN(MASTER,DISCOUNT):
	
	if DISCOUNT == 'Off':
		STATE = "disabled"
	elif DISCOUNT == 'On':
		STATE = "normal"

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
				for i in view_selected_data(LAST_DATABASE_LINK,'All','All','All'):
					existed_room_numbers_list.append(i[0])
				if int(groove_entry7F2.get()) in existed_room_numbers_list:
					LIST = view_selected_data(LAST_DATABASE_LINK,'All','All',int(groove_entry7F2.get()))
					Rate_Type_CHECKIN.current(room_types.index(LIST[0][2]))
				else:
					pass
					# print('the number is not in existedd rooms list')
					# print(f'{int(groove_entry7F2.get())} in the list ....')
				# print(view_selected_data(LAST_DATABASE_LINK,'All','All','All'))
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
	tkinter.Button(f2,text='Book it',background="light gray",command=lambda:book_it(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry3F2.get(),countrylist.get(),groove_entry4F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),carlist.get(),groove_entry6F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get())).grid(row=0, column=0,sticky='we')
	tkinter.Button(f2,text='Print',background="light gray",width=11).grid(row=0, column=1,sticky='we')
	tkinter.Button(f2,text='Update',background="light gray",command=lambda:Update_CHECK_IN_DETAILS(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry3F2.get(),countrylist.get(),groove_entry4F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),carlist.get(),groove_entry6F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get())).grid(row=0, column=2,sticky='we')
	tkinter.Button(f2,text='Change Room',background="light gray",command=lambda:CHANGE_ROOM_CHECK_IN(groove_entry7F2.get(),groove_entry0F2.get(),groove_entry1F2.get(),groove_entry2F2.get(),groove_entry3F2.get(),countrylist.get(),groove_entry4F2.get(),ID_TYPE_LIST.get(),groove_entry5F2.get(),carlist.get(),groove_entry6F2.get(),DateIn.get(),TIME_NOW(),DateOut.get(),groove_entry8F2.get(),groove_entry9F2.get(),groove_entry10F2.get(),Rate_Type_CHECKIN.get(),groove_entry11F2.get(),groove_entry12F2.get(),groove_entry14F2.get(),groove_entry15F2.get(),groove_entry16F2.get(),groove_entry17F2.get(),groove_entry18F2.get())).grid(row=0, column=3,columnspan=5,sticky='w')
	tkinter.Button(f2,text='Cancel',background="light gray",command=lambda:CANCEL_CHECK_IN_BOOING(groove_entry7F2.get(),groove_entry0F2.get())).grid(row=0,column=6,sticky='ew')
	
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
	# LISTS:
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
	Rate_Type_CHECKIN = ttk.Combobox(f2,values=select_types(LAST_DATABASE_LINK),width=11)
	Rate_Type_CHECKIN.grid(row=1,column=7,columnspan=8,sticky='w')
	Rate_Type_CHECKIN.bind("<<ComboboxSelected>>",lambda event:modify_paymen_numbers_2(event))
	#ENTRIES:
	groove_entry0F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry0F2_trace,text="00005") # serial folio no
	groove_entry0F2.grid(row=1,column=1,columnspan=2,sticky='nsw')
	groove_entry0F2.insert(0,f"{str(int(view_serial_table(LAST_DATABASE_LINK)[-1][0])+1).zfill(6)}")
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
	groove_entry8F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=3,textvariable=groove_entry8F2_trace)  #no of days
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
	groove_entry14F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=10,textvariable=groove_entry14F2_trace)
	groove_entry14F2.grid(row=4,column=7,columnspan=8,sticky='nsw')
	groove_entry14F2.insert(0, "0.00") # other charges
	groove_entry15F2 = tkinter.Entry(f2,font=10,relief="groove",background="white",width=8,textvariable=groove_entry15F2_trace,state=STATE,disabledbackground="red")
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
				R_number.config(values=['All']+select_room_numbers(LAST_DATABASE_LINK))
				create_new_booking_room(LAST_DATABASE_LINK,ROOM_NO)
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
				R_number.config(values=['All']+select_room_numbers(LAST_DATABASE_LINK))
			elif check_if_room_in_database(ROOM_NO) == False:
				tkinter.messagebox.showinfo("Update Error", "room  is not exists .")
		else:
			# print('room option is wrong')
			pass
		first_table_show_options(Status.get(),R_Type.get(),R_number.get())
	except ValueError:
		pass

def switch_rooms_options_buttons(STATUS):
	global add_new_room,update_room,delete_room
	add_new_room["state"] == STATUS
	update_room["state"] == STATUS
	delete_room["state"] == STATUS

def rooms_options(MASTER,PRIV):
	global room_status
	f1 = MASTER
	global groove_entry1,groove_entry2,groove_entry3,groove_entry4,groove_entry5,groove_entry6,add_new_room,update_room,delete_room
	
	if PRIV == 'read':
		print('buttons dissabled')
		# switch_rooms_options_buttons("disabled")
		STATE = "disabled"
	elif PRIV == 'read|write':
		print('buttons open')
		# switch_rooms_options_buttons("normal")
		STATE = "normal"
	
	#BUTTONS:
	add_new_room  =  tkinter.Button(f1, text='  add new     ',background="light gray",state=STATE ,command=lambda:room_options_buttons('new',groove_entry1.get(),groove_entry2.get(),groove_entry3.get(),groove_entry5.get(),groove_entry4.get(),groove_entry6.get()))
	add_new_room.grid(row=0, column=0,sticky='sw')
	update_room   =  tkinter.Button(f1,text='       update       ',background="light gray",state=STATE ,command=lambda:room_options_buttons('update',groove_entry1.get(),groove_entry2.get(),groove_entry3.get(),groove_entry5.get(),groove_entry4.get(),groove_entry6.get()))
	update_room.grid(row=0, column=1,sticky='sw')
	delete_room   =  tkinter.Button(f1,text='delete   ',background="light gray",state=STATE,command=lambda:room_options_buttons('delete',groove_entry1.get()))
	delete_room .grid(row=0, column=2,sticky='sw')
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
	groove_entry3 = ttk.Combobox(f1,values=select_types(LAST_DATABASE_LINK),width=11)
	groove_entry3.grid(row=3,column=1,columnspan=2,sticky='nw')
	if select_types(LAST_DATABASE_LINK):
		groove_entry3.current(0)
	elif not select_types(LAST_DATABASE_LINK):
		pass
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
	ITEMS_NO = len(view_selected_data(LAST_DATABASE_LINK,STATUS,TYPE,NUM))
	# print(ITEMS_NO)
	ITEMS_LIST = view_selected_data(LAST_DATABASE_LINK,STATUS,TYPE,NUM)
	if ITEMS_NO > 0: 
		COLUMN_NO = len(view_selected_data(LAST_DATABASE_LINK,STATUS,TYPE,NUM)[0])
	treeview_inserts(fen,1,ITEMS_NO,ITEMS_LIST,8,4)		



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
			globals()[f'treeview{TABLE_NUM}'].insert("" , "end" , text = f"{TABLE[0]}", values = TABLE[1:COLUMN_NO] ,tag=f"{COLOR_TAG[COLOR_CHOICE]}")


def database_Table_view_Height(master,X,Y,ITEMS_NO,TABLE_NUM,MAX_ROWS):
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
	LIST = view_selected_rate(LAST_DATABASE_LINK,str(treeview2.item(curItem)['text']))
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
		groove_entry0F2.insert(0,str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][1]).zfill(6))#   serial folio no
		groove_entry0F2.config(state="readonly",readonlybackground="white")
		groove_entry1F2.delete(0,'end')     #   first name
		groove_entry1F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][2])     #   first name
		groove_entry2F2.delete(0,'end')     #   last name
		groove_entry2F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][3])     #   last name
		groove_entry3F2.delete(0,'end')     #   Rcad_no 
		groove_entry3F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][4])     #   Rcad_no 
		countrylist.current(list(map(lambda x:x.strip(),lineList)).index(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][5])))         #   country  "LIST"
		groove_entry4F2.delete(0,'end')     #   adress
		groove_entry4F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][6])          #   adress
		ID_TYPE_LIST.current(ID_TYPES.index(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][7])))        #   id type "LIST"
		groove_entry5F2.delete(0,'end')     #   id_no 
		groove_entry5F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][8])     #   id_no 
		carlist.current(cars.index(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][9])))             #   "LIST"
		groove_entry6F2.delete(0,'end')     #   plate no
		groove_entry6F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][10])     #   plate no
		groove_entry7F2.delete(0,'end')     #   room number
		groove_entry7F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][0])     #   room number
		DateIn.current(date_list.index(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][11])))              #   "list"
		DateOut.current(date_list.index(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][13])))             #   "LIST"
		groove_entry8F2.delete(0,'end')     #   no of days
		groove_entry8F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][14])     #   no of days
		groove_entry9F2.delete(0,'end')     #   no of adults
		groove_entry9F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][15])     #   no of adults
		groove_entry10F2.delete(0,'end')    #   no of childs
		groove_entry10F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][16])    #   no of childs
		groove_entry11F2.delete(0,'end')    #   rate/period
		groove_entry11F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][18])    #   rate/period
		groove_entry12F2.delete(0,'end')    #   total/charge
		groove_entry12F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][19])    #   total/charge
		groove_entry14F2.delete(0,'end')    #   other charges
		groove_entry14F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][20])    #   other charges
		groove_entry15F2.delete(0,'end')    #   discount
		groove_entry15F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][21])    #   discount
		groove_entry16F2.delete(0,'end')    #   total
		groove_entry16F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][22])    #   total
		groove_entry17F2.delete(0,'end')    #   amount paied
		groove_entry17F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][23])    #   amount paied
		groove_entry18F2.delete(0,'end')    #   balance
		groove_entry18F2.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,num)[0][24])    #   balance
	if STATUS == "Free":
		# trace_checkin_inputs = 0
		groove_entry0F2.config(state="normal",readonlybackground="white")
		groove_entry0F2.delete(0,'end')     #   serial folio no
		groove_entry0F2.insert(0,f"{str(int(view_serial_table(LAST_DATABASE_LINK)[-1][0])+1).zfill(6)}")     #   serial folio no
		groove_entry0F2.config(state="readonly",readonlybackground="white")
		groove_entry1F2.delete(0,'end')                                             #   first name
		groove_entry2F2.delete(0,'end')                                             #   last name
		groove_entry3F2.delete(0,'end')                                             #   Rcad_no 
		countrylist.current(0)                                                      #   country  "LIST"
		groove_entry4F2.delete(0,'end')                                             #   adress
		ID_TYPE_LIST.current(0)                                                     #   id type "LIST"
		groove_entry5F2.delete(0,'end')                                             #   id_no 
		carlist.current(0)                                                          #   "LIST"
		groove_entry6F2.delete(0,'end')                                             #   plate no
		DateIn.current(date_list.index(date.today().strftime("%Y-%m-%d")))          #   "list"
		DateOut.current(date_list.index(date.today().strftime("%Y-%m-%d")))         #   "LIST"
		groove_entry8F2.delete(0,'end')                                             #   no of days
		groove_entry8F2.insert(0,0)                                                 #   no of days
		groove_entry9F2.delete(0,'end')                                             #   no of adults
		groove_entry9F2.insert(0,0)                                                 #   no of adults
		groove_entry10F2.delete(0,'end')                                            #   no of childs
		groove_entry10F2.insert(0,0)                                                #   no of childs


def normalize_checkin_fileds():
	red_warning_entry_borders('groove_entry7F2','NORMAL')
	red_warning_entry_borders('groove_entry0F2','NORMAL')
	red_warning_entry_borders('groove_entry1F2','NORMAL')
	red_warning_entry_borders('groove_entry2F2','NORMAL')
	red_warning_entry_borders('groove_entry4F2','NORMAL')
	red_warning_entry_borders('groove_entry5F2','NORMAL')
	red_warning_entry_borders('groove_entry8F2','NORMAL')


def select_from_auto_free_table_where_num(DATABESE_NAME,Room_No):
	my_list = []
	conn = sqlite3.connect(DATABESE_NAME)
	c = conn.cursor()
	c.execute("SELECT * FROM auto_free_table WHERE Room_No = "+str(Room_No)+" ")
	rows = c.fetchall()
	for row in rows:
		my_list.append(row)
	return my_list


def switch_checkout_button(STATUS):
	#lock/unlock checkout putton
	global CHECKOUT_BUTTON
	CHECKOUT_BUTTON.configure(state=STATUS)


def update_check_out_fields(Room_No):
	global checkout_status
	print('update checkout fields ......!')
	# print(select_from_auto_free_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1])
	if boolian_room_status(Room_No,'IN USE'):
		if select_from_auto_free_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1] != 'autoFree':
			checkout_full_in_use_mode(Room_No)
			checkout_status.config(text="Amount open",background="pale green")
			switch_checkout_button('normal')
		elif select_from_auto_free_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1] == 'autoFree':
			free_checkout_fields(Room_No)
			checkout_status.config(text="Amount Paid",background="sky blue")
			switch_checkout_button('disabled')
	elif boolian_room_status(Room_No,'Free'):
		free_checkout_fields(Room_No)
		checkout_status.config(text="Amount closed",background="yellow")
		switch_checkout_button('disabled')


def checkout_full_in_use_mode(Room_No):
	#print(str(select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][1]).zfill(6))
	first_name = select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][2]
	last_name  = select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][3]
	groove_entry20.delete(0,'end')
	groove_entry20.insert(0,f"{first_name} {last_name}")
	groove_entry19.delete(0,'end')
	groove_entry19.insert(0,groove_entry0F2.get())
	groove_entry19b.delete(0,'end')
	groove_entry19b.insert(0,ID_TYPE_LIST.get()) #id type:
	groove_entry19c.delete(0,'end')
	groove_entry19c.insert(0,groove_entry5F2.get()) #id number:
	groove_entry21.delete(0,'end')
	groove_entry21.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][0])
	groove_entry22.delete(0,'end')
	groove_entry22.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][11])
	groove_entry22b.delete(0,'end')
	groove_entry22b.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][13])
	groove_entry23.delete(0,'end')
	groove_entry23.insert(0,view_selected_data(LAST_DATABASE_LINK,'All','All',Room_No)[0][2])
	groove_entry24.delete(0,'end')
	groove_entry24.insert(0,groove_entry11F2.get())
	groove_entry25.delete(0,'end')
	groove_entry25.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][14])
	groove_entry26.delete(0,'end')
	groove_entry26.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][15])
	groove_entry27.delete(0,'end')
	groove_entry27.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][16])
	groove_entry28.delete(0,'end')
	groove_entry28.insert(0,groove_entry14F2.get()) #other charges.
	groove_entry29.delete(0,'end')
	groove_entry29.insert(0,groove_entry12F2.get())
	groove_entry30.delete(0,'end')
	groove_entry30.insert(0,groove_entry15F2.get())
	groove_entry31.delete(0,'end')
	groove_entry31.insert(0,groove_entry16F2.get())
	groove_entry32.delete(0,'end')
	groove_entry32.insert(0,groove_entry17F2.get())
	groove_entry33.delete(0,'end')
	groove_entry33.insert(0,groove_entry18F2.get())

def free_checkout_fields(Room_No):
	groove_entry19b.delete(0,'end')
	groove_entry19c.delete(0,'end')
	groove_entry20.delete(0,'end')
	groove_entry19.delete(0,'end')
	groove_entry21.delete(0,'end')
	groove_entry21.insert(0,select_from_booking_table_where_num(LAST_DATABASE_LINK,Room_No)[0][0])
	groove_entry22.delete(0,'end')
	groove_entry22b.delete(0,'end')
	groove_entry23.delete(0,'end')#rate type
	groove_entry23.insert(0,view_selected_data(LAST_DATABASE_LINK,'All','All',Room_No)[0][2])
	groove_entry24.delete(0,'end')
	groove_entry24.insert(0,groove_entry11F2.get())
	groove_entry25.delete(0,'end')
	groove_entry25.insert(0,'0')
	groove_entry26.delete(0,'end')
	groove_entry26.insert(0,'0')
	groove_entry27.delete(0,'end')
	groove_entry27.insert(0,'0')
	groove_entry28.delete(0,'end')
	groove_entry28.insert(0,groove_entry14F2.get()) #other charges.
	groove_entry29.delete(0,'end')
	groove_entry29.insert(0,'0.0') # sub total
	groove_entry30.delete(0,'end')
	groove_entry30.insert(0,'0.0') # discount
	groove_entry31.delete(0,'end')
	groove_entry31.insert(0,'0.0')
	groove_entry32.delete(0,'end')
	groove_entry32.insert(0,'0.0')
	groove_entry33.delete(0,'end')
	groove_entry33.insert(0,'0.0')


def selectItem(a):
	global trace_checkin_inputs,update_trace_checkin_inputs,CHECKIN_CHOICE
	CHECKIN_CHOICE = None
	trace_checkin_inputs = 0
	update_trace_checkin_inputs = 0
	normalize_checkin_fileds()
	curItem = treeview1.focus()
	# print(curItem)
	LIST = view_selected_data(LAST_DATABASE_LINK,'All','All',int(treeview1.item(curItem)['text']))
	#print(LIST[0][0])
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
	update_check_out_fields(LIST[0][0])


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
	R_Type = ttk.Combobox(Room_View,values=['All']+select_types(LAST_DATABASE_LINK),width=11)
	R_number = ttk.Combobox(Room_View,values=['All']+select_room_numbers(LAST_DATABASE_LINK),width=3)
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
	Time.place(relx=0.74, rely=0.13, anchor=tkinter.NW)
	tkinter.Label(fen, text='Time',bg="light gray").place(relx=.77, rely=0.13,anchor=tkinter.W)
	clock = tkinter.Label(Time, text=f'{timenow}',font=("Helvetica", 24),bg="light gray")
	clock.pack(side=tkinter.TOP, anchor=tkinter.N)
	DATE = tkinter.Label(Time, text=f'{datenow}',bg="light gray")
	DATE.pack(side=tkinter.TOP, anchor=tkinter.W)
	live_time_change()


def current_user(username):
	Current_User = tkinter.Frame(fen, relief=tkinter.GROOVE, borderwidth=2,background="light gray")
	Current_User.place(relx=0.74, rely=0.04, anchor=tkinter.NW)
	tkinter.Label(fen, text='Current User',bg="light gray").place(relx=.77, rely=0.04,anchor=tkinter.W)
	tkinter.Label(Current_User, text=f' ',font=("Helvetica", 2),bg="light gray").pack(side=tkinter.TOP, anchor=tkinter.N)
	user_name = tkinter.Label(Current_User, text=f'        {username}        ',font=("Helvetica", 15),bg="light gray",fg='blue')
	user_name.pack(side=tkinter.TOP, anchor=tkinter.N)


def main_functions(*args):
	if not boolian_check_file_exists("config.ini"):
		create_config_if_not_exists()
	create_main_database(LAST_DATABASE_LINK)	
	create_rate_table(LAST_DATABASE_LINK)
	create_serial_table(LAST_DATABASE_LINK)
	create_past_checkouts_table(LAST_DATABASE_LINK)
	create_booking_table(LAST_DATABASE_LINK)
	create_new_booking_room(LAST_DATABASE_LINK,1)
	create_auto_free_table(LAST_DATABASE_LINK)
	if not select_room_numbers(LAST_DATABASE_LINK):
		print("list is empty")
	else:
		print("list is not empty.....!")
		auto_create_list_of_auto_free_rooms()
	create_users_table(LAST_DATABASE_LINK)
	clock_date()
	date_list()
	view_selected_data(LAST_DATABASE_LINK,'All','All','All')
	table1()
	Room_View_Options()
	current_user(args[0][0])
	Cashier_operations(args[0][1])

	#print(f'types: {select_types(LAST_DATABASE_LINK)}')
	#date_one_day_after("2020-04-14",1)
	#insert_auto_free_room(LAST_DATABASE_LINK,2,'Free')
	#create_list_of_auto_free_rooms()
	#update_all_check_in()


def login():
	global fen1,can1
	create_main_database(LAST_DATABASE_LINK)	
	create_rate_table(LAST_DATABASE_LINK)
	create_serial_table(LAST_DATABASE_LINK)
	if view_serial_table(LAST_DATABASE_LINK) :
		print("list  exists")
	else:
		print("list  is not exits")
		insert_to_serial_table(LAST_DATABASE_LINK,1)
	#print(select_room_numbers(LAST_DATABASE_LINK))
	if not select_room_numbers(LAST_DATABASE_LINK):
		print("list is empty")
	else:
		print("list is not empty.....!")
		auto_create_list_of_auto_free_rooms()
	create_past_checkouts_table(LAST_DATABASE_LINK)
	create_booking_table(LAST_DATABASE_LINK)
	create_new_booking_room(LAST_DATABASE_LINK,1)
	create_auto_free_table(LAST_DATABASE_LINK)
	
	create_users_table(LAST_DATABASE_LINK)
	create_new_user('admin','123456','123456','On','On','On','On','On','On','On')
	fen1 = tkinter.Tk()
	fen1.title("User's Login")
	combostyle = ttk.Style()
	combostyle.theme_create('combostyle', parent='alt',
	                         settings = {'TCombobox':
	                                     {'configure':
	                                      {'selectbackground': 'blue',
	                                       'fieldbackground': 'white',
	                                       'background': 'green'
	                                       }}})
	combostyle.theme_use('combostyle') 
	can1 = tkinter.Canvas(fen1 , height=150,width=300)
	#labels:
	tkinter.Label(can1,text="User Name",background="light gray",font="albattar 12 normal").grid(row=0,column=0,sticky='w')
	tkinter.Label(can1,text="Password",background="light gray",font="albattar 12 normal").grid(row=1,column=0,sticky='w')
	#entry:
	password_entry = tkinter.Entry(can1,font=10,relief="groove",background="white",width=14) # password
	password_entry.grid(row=1,column=1,sticky='nsw')
	password_entry.insert(0, "")
	#lists:
	users_list = ttk.Combobox(can1,values=[""]+column_from_users_table(0),width=15,state="readonly")
	users_list.grid(row=0,column=1)
	users_list.current(0)
	#buttons:
	tkinter.Button(can1,text='Login',background="light gray",command=lambda:prestart(users_list,password_entry),width=10).grid(row=2, column=0,sticky='we')
	tkinter.Button(can1,text='Cancel',background="light gray",command=lambda:print("cancel"),width=10).grid(row=2, column=1,sticky='we')
	can1.grid()
	fen1.mainloop()


def prestart(users_list,password_entry):
	user_privs = read_from_users_table(LAST_DATABASE_LINK,users_list.get())[0][2:9]
	print(read_from_users_table(LAST_DATABASE_LINK,users_list.get())[0][2:9])
	if not users_list.get().isspace() and users_list.get() != None and users_list.get() != '':
		print('user name is not empty')
		#check if user_name exists in database:
		if users_list.get() in column_from_users_table(0):
			print('user name in list')
			if not password_entry.get().isspace() and password_entry.get() != None and password_entry.get() != '':
				print('password is not empty')
				if str(password_entry.get()) == str(read_from_users_table(LAST_DATABASE_LINK,users_list.get())[0][1]):
					print('password is same password')
					main(users_list.get(),user_privs)
					fen1.destroy()
				elif str(password_entry.get()) != str(read_from_users_table(LAST_DATABASE_LINK,users_list.get())[0][1]):
					print('password is not the same as password you entered .')
			elif password_entry.get().isspace() or password_entry.get() == None or password_entry.get() == '':
				print('password is empty')
		elif users_list.get() not in column_from_users_table(0):
			print('user name not in list')
	elif users_list.get().isspace() or users_list.get() == None or users_list.get() == '':
		print('username field is empty , choose user name')
	

def main(*args):
	global fen,can
	fen1.destroy()
	fen = tkinter.Tk()
	fen.title('Hotel')
	can = tkinter.Canvas(fen , height=570,width=800,bg="light gray")
	can.create_text(85,45,fill="black",font="albattar 20 bold",text="Hotel Name",tags="NAME")
	can.create_rectangle(9, 80, 578, 261, outline="white", fill="grey")
	main_functions(args)
	can.pack()
	fen.mainloop()


#widget:
if __name__ == '__main__':
	login()








