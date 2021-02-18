#!/usr/bin/python

# The purpose of this program is to create a ticket selling service that runs in a terminal. This ticket selling service will contain a front end for users to purchase and sell tickets from. It will also create a back end which will store user, ticket, event and transaction information.
# please read the attached README file to see how the program runs.

from array import *
import sys

userLines = []
userInfo  = []
AvailableTicketsLines = []
sellerandTix = []
events = []
eventInfo = []
transactions = []
result = open(sys.argv[2],"w+")
dailytransactions = open("DailyTransactions.txt", "w+")
inputs = []

#UserAccounts text file is read into the program and contents of the file is added into userInfo
with open("./Database/UserAccounts.txt") as fp:
   line = fp.readline()
   cnt = 1
   while line:
       userLines.append(line.strip())
       line = fp.readline()
       cnt += 1
for line in userLines:
	tempUserName = line[0:15].replace(" ","").lower()
	tempUserType = line[16:18]
	tempUserCredit = float(line[-9:])
	userInfo.append([tempUserName,tempUserType,tempUserCredit])


#AvailableTickets text file is read into the program and contents of the file is added into the eventInfo list
with open("./Database/AvailableTickets.txt") as fp:
   line = fp.readline()
   cnt = 1
   while line:
       AvailableTicketsLines.append(line.strip())
       line = fp.readline()
       cnt += 1
for line in AvailableTicketsLines:
	tempEvent = line[:19].replace(" ","")
	tempSeller = line[20:33].replace(" ","")
	tempTix = int(line[34:37])
	tempPrice = float(line[-6:])
	events.append(tempEvent)
	eventInfo.append([tempEvent,tempSeller,tempTix,tempPrice])
events = list(dict.fromkeys(events))

#Store input values into a string Array
with open(sys.argv[1]) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       inputs.append(line.strip())
       line = fp.readline()
       cnt += 1


#initial login screen
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("  Welcome to the Batty Boys Movie Ticket System")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
result.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
result.write("\n  Welcome to the Batty Boys Movie Ticket System")
result.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
exit = 0
login = 0
admin = 0
buyer = 0
seller = 0
loggeduser =[]

# Performs user login, and necessary logic
def LoginUser():
	global login
	global admin
	global seller
	global buyer
	global loggeduser
	if login == 1:
		print("\n  Already Logged in")
		result.write("\n  Already Logged in")

	#when login is 0
	else:
		print("\n  Enter User Name:\n")
		result.write("\n  Enter User Name:\n")
		username = inputs.pop(0)
		print(username)
		result.write(username)
		for user in userInfo:
			if user[0] == username:
				login = 1
				loggeduser = user
				result.write("\n  Logged in Successfully")
				if user[1] == "AA":
					admin = 1
					buyer = 1
					seller= 1
					print("Admin logged in")
				if user[1] == "BS":
					buyer = 1
					admin = 0
					seller= 0
				if user[1] == "FS":
					buyer = 1
					seller= 1
					admin = 0
				if user[1] == "SS":
					seller =1
					buyer = 0
					admin = 0
			
		if login == 0:
			print("\n  User not found on System")  
			result.write("\n  User not found on System")  
	return

# Buy function where a buyer account may buy tickets to an event.
def Buy():
	print("\n  What event do you want to buy tickets for?\n")
	result.write("\n  What event do you want to buy tickets for?\n")
	for eventname in events:
		print("   - ", eventname)
		result.write(eventname)
	event = inputs.pop(0)
	print(event)
	result.write(event)
	found = 0
	#for loop that iterates through current events and checks to see if user's input matches a current event title
	for eventname in events:
		if eventname == event:
			found = 1
			print("\n  How many tickets will you like to buy? (Max 4 tickets per Sale)\n") #Max tickets constraint applied (4 tickets per sale)
			result.write("\n  How many tickets will you like to buy? (Max 4 tickets per Sale)\n")
			numoftix = inputs.pop(0)
			print(numoftix)
			result.write(numoftix)
			while int(numoftix) > 4:
				print("\n  Sorry that's too many tickets, try again:\n")
				result.write("\n  Sorry that's too many tickets, try again:\n")
				numoftix = inputs.pop(0) #loops back until user enters a number less than 4
				print(numoftix)
				result.write(numoftix)
			print("\n  Enter the username of the seller:\n")
			result.write("\n  Enter the username of the seller:\n")
			buyerfound = 0
			buyerName  =""
			buyerTix = 0
			sellername = inputs.pop(0)
			print(sellername)
			result.write(sellername)
			sellerLine = 0
			foundseller = 0
			for seller in eventInfo: #for loop that checks to see if seller username and valid number of tickets exists. IF both are found continue; else end transaction;
				if seller[0] == event and seller[1] == sellername:
					if seller[2] > int(numoftix):
						buyerfound = 1
						buyerName = seller[1]
						buyerTix  = seller[2]
						price = seller[3]
						foundseller = sellerLine
				sellerLine+=1
			if buyerfound == 1:
				print("\n  '" + buyerName + "' has tickets for this price: " + str(price) + " \n  Would u like to purchase \n  (type yes or no):\n")
				result.write("\n  '" + buyerName + "' has tickets for this price: " + str(price) + " \n  Would u like to purchase \n  (type yes or no):\n")

				buy = inputs.pop(0)
				print(buy)
				result.write(buy)
				#user inputs if they want to proceed with the transaction or not after looking at the total price.
				if buy == "yes":
					eventInfo[foundseller][2] = eventInfo[foundseller][2] - int(numoftix)
					updateAvailableTickets()
					buyAndSellTransaction("buy",eventInfo[foundseller])
					print("\n  You have successfully purchased the tickets")
					result.write("\n  You have successfully purchased the tickets")
				else:
					print("\n  Transaction cancelled")
					result.write("\n  Transaction cancelled")
			else:
				print("\n  Buyer was not found \n  Transaction Cancelled")
				result.write("\n  Buyer was not found \n  Transaction Cancelled")
					   
		   
	if found == 0:
		print("\n  Sorry that event isn't happening right now")
		result.write("\n  Sorry that event isn't happening right now")


# Sell function where a seller account may sell tickets to an event.
def Sell():
	print("\n  What event do u want to sell Tickets for\n  ")
	result.write("\n  What event do u want to sell Tickets for\n  ")
	event = inputs.pop(0)
	print(event)
	result.write(event)
	while len(event) > 25:
		print("\n  Event title cannot exceed 25 characters, try again:\n")
		result.write("\n  Event title cannot exceed 25 characters, try again:\n")
		event = inputs.pop(0) #loops back until user enters a title less than 25 chars
		print(event)
		result.write(event)

	print("\n  Under what name should the tickets be sold from\n  ")
	result.write("\n  Under what name should the tickets be sold from\n  ")
	name = inputs.pop(0)
	print(name)
	result.write(name)

	print("\n  What is the sale price for the tickets?\n  ")
	result.write("\n  What is the sale price for the tickets?\n  ")
	ticketPrice = float(inputs.pop(0))
	print(ticketPrice)
	result.write(str(ticketPrice))
	while ticketPrice > 999:
		print("\n  Sorry the ticket price must be under $999, try again:\n")
		result.write("\n  Sorry the ticket price must be under $999, try again:\n")
		ticketPrice = int(inputs.pop(0)) #loops back until user enters a number less than 999
		print(ticketPrice)
		result.write(str(ticketPrice))

	print("\n  How many tickets do u have avaiable for sale\n  ")
	result.write("\n  How many tickets do u have avaiable for sale\n  ")
	numoftix = int(inputs.pop(0))
	print(numoftix)
	result.write(str(numoftix))
	result.write(str(ticketPrice))
	while numoftix > 100:
		print("\n  Sorry the max amount of tickets allowed to sell is 100, try again:\n")
		result.write("\n  Sorry the max amount of tickets allowed to sell is 100, try again:\n")
		numoftix = int(inputs.pop(0)) #loops back until user enters a number less than 100
		print(numoftix)
		result.write(str(numoftix))

	events.append(event)
	eventInfo.append([event,name,numoftix,ticketPrice])
	updateAvailableTickets()
	#Added Seller's username, number of tickets, and event to Event and SellerAndTix Array. 
	print("\n  Tickets are now Officially on Sale\n  ")
	result.write("\n  Tickets are now Officially on Sale\n  ")
	buyAndSellTransaction("sell",[event,name,numoftix,ticketPrice])


#Refund function that allows the admin to add funds back into a buyers account from a seller's account.
def Refund():
	print("\n  Enter buyer for refund\n  ")
	result.write("\n  Enter buyer for refund\n  ")
	buyer = inputs.pop(0)
	print(buyer)
	result.write(buyer)
	print ("\n  Enter seller for refund\n  ")
	result.write ("\n  Enter seller for refund\n  ")
	seller = inputs.pop(0)
	print(seller)
	result.write(seller)
	buyerAccount =[]
	buyerfound = 0
	sellerfound = 0
	for user in userInfo: #search for valid buyer username
		if user[0] == buyer:
			if user[1] != "SS":
				buyerAccount = user
				buyerfound = 1
	for sell in eventInfo: #search for valid seller username
			if sell[1] == seller:
				sellerfound = 1
	if buyerfound == 0:
		print("\n  User was not found\n ") 
		result.write("\n  User was not found\n ") 
	if sellerfound == 0:
		print("\n  Seller was not found\n ")
		result.write("\n  Seller was not found\n ")
	if sellerfound == 1 and buyerfound == 1: #if both are found then refund the amount to buyer.
		print ("\n How many credits to refund?\n ")
		result.write("\n How many credits to refund?\n ")
		refund = inputs.pop(0)
		print(refund)
		result.write(refund)
		newCredit = buyerAccount[2]+ float(refund)
		userInfo.append([buyerAccount[0],buyerAccount[1],newCredit])
		userInfo.remove(buyerAccount)
		print ("\n  " + buyer + " was refunded " + refund + " credits from " + seller + "\n")
		result.write ("\n  " + buyer + " was refunded " + refund + " credits from " + seller + "\n")
		updateUserAccounts()
		refundTransaction(buyer,seller,float(refund))
		

#Addcredit function that will allow admin account to add credit to any valid account.
def addCredit():
	print("\n  Enter username to add credits to\n")
	result.write("\n  Enter username to add credits to\n")
	oldbalance = []
	newCredit =0.00
	username = inputs.pop(0)
	print(username)
	result.write(username)
	userfound = 0
	for user in userInfo: #search for valid username within data
		if user[0] == username:
			userfound = 1
			oldbalance= user
	if userfound == 1: #if found ask how many credits to add
		print("\n  Enter number of credits to add\n")
		result.write("\n  Enter number of credits to add\n")
		credit = inputs.pop(0) #add credits
		print(credit)
		result.write(credit)
		if credit > 1000 or (oldbalance[2] + credit) > 1000:
			print("Credit Value too high")
			result.write("Credit Value too high")
			
		else:
			newCredit = oldbalance[2] + credit
			userInfo.remove(oldbalance)
			userInfo.append([oldbalance[0],oldbalance[1],newCredit])
			updateUserAccounts()
			otherTransaction("addCredit")
			print(username + " has been creditted " + credit + " dollars")
			result.write(username + " has been creditted " + credit + " dollars")
		
	else:
		print("\n  User has not been found")
		result.write("\n  User has not been found")
			
#Create Fucntion that allows admin to create new buyer, seller, or admin accounts.
def Create():
	exit = 0
	userfound = 0
	while exit != 1:
		userfound = 0
		print("\n  Enter the new account's username:\n")
		result.write("\n  Enter the new account's username:\n")
		username = inputs.pop(0)
		print(username)
		result.write(username)
		if len(username)>15:
			print("Username is too long")
			result.write("Username is too long")
		else:
			for user in userInfo: #search for valid username within data
				if user[0] == username:
					userfound = 1
			if userfound == 1:
				print("Username already exists")
			else:	
				print("\n  What type of user is this (AA,FS,BS,SS):\n")
				result.write("\n  What type of user is this (AA,FS,BS,SS):\n")
				accountType = inputs.pop(0)
				print(accountType)
				result.write(accountType)
				print("\n  How much credit is in this account?:\n")
				result.write("\n  How much credit is in this account?:\n")
				credit = inputs.pop(0)
				print(credit)
				result.write(credit)
				if float(credit) > 999.99:
					print("Max Credit is 999.99")
				else:
					userInfo.append([username,accountType,float(credit)]) #add new account to loginTemp Array.
					updateUserAccounts()
					otherTransaction("create")
					print("\n  Successfully created new user: '" + username + "' of Type: '" + accountType + "' with Credit: '" + credit +"'")
					result.write("\n  Successfully created new user: '" + username + "' of Type: '" + accountType + "' with Credit: '" + credit +"'")
					exit = 1	
#Delete function that allows admin to delete an existing account from the database(array).
def Delete():
	userfound = 0
	print("\n  Enter the account's username that you wish to delete:\n")
	result.write("\n  Enter the account's username that you wish to delete:\n")
	username = inputs.pop(0)
	print(username)
	result.write(username)
	for user in userInfo:
		if user[0] == username:
			if username != loggeduser[0]:
				userfound = 1
				userInfo.remove(user)
			elif username == loggeduser[0]:
				print("Cannot Delete logged User")
				result.write("Cannot Delete logged User")	
	#if input account exists then delete user (remove user from loginTemp array).
	if userfound == 1:
		updateUserAccounts()
		otherTransaction("delete")
		print("\n  Successfully deleted user!")
		result.write("\n  Successfully deleted user!")
	else:
		print("\n  User not found")
		result.write("\n  User not found")

# Displays avaiable commands for users
def help():
	print("\n  Ask and ye shall receive!:\n")
	result.write("\n  Ask and ye shall receive!:\n")
	if login == 0:
		nonbuyer = 1
		print("  login = login to the system")
		result.write("  login = login to the system")
		print("  exit = exit the system")
		result.write("  exit = exit the system")
	else:
		print("  logout = logout of the system ")
		print("  buy = buy movie tickets ")
		print("  sell = sell movie tickets ")
		print("  refund = refund a user credits (admin only)")
		print("  add credit = add credit to a users account (admin only)")
		print("  create = creates a new user (admin only)")
		print("  delete = deletes a user's account (admin only)")
		result.write("  logout = logout of the system ")
		result.write("  buy = buy movie tickets ")
		result.write("  sell = sell movie tickets ")
		result.write("  refund = refund a user credits (admin only)")
		result.write("  add credit = add credit to a users account (admin only)")
		result.write("  create = creates a new user (admin only)")
		result.write("  delete = deletes a user's account (admin only)")
	return


# Prints out the array of daily transactions for the current session
def printtransactions():
	for trans in transactions:
		dailytransactions.write(trans  + "\n")
	return

# Adds the transaction line for a buy/sell action to the transactions array
def buyAndSellTransaction(transType, info):
	code = ""
	if transType == "sell":
		code = "03"
	elif transType == "buy":
		code = "04"
	eventName = info[0]
	if len(eventName) < 19:
		oldLength = len(eventName)
		remainingChars = 19 - oldLength
		for i in range(remainingChars):
			eventName += " "
	seller = info[1]
	if len(seller) < 4:
		oldLength = len(seller)
		remainingChars = 14 - oldLength
		for i in range(remainingChars):
			seller += " "
	numoftix = str(info[2])
	if len(numoftix) < 3:
		oldLength = len(numoftix)
		remainingChars = 3 - oldLength
		for i in range(remainingChars):
			numoftix += " "
	price = str(info[3])
	if len(price) < 6:
		oldLength = len(price)
		remainingChars = 6 - oldLength
		for i in range(remainingChars):
			price += "0"

	line = code + " " + eventName + " " + seller + " " + numoftix + " " + price
	transactions.append(line)
	return

# Adds the transaction line for a refund action to the transactions array
def refundTransaction(buyer, seller, refundFloat):
	code = "05"
	if len(buyer) < 15:
		oldLength = len(buyer)
		remainingChars = 15 - oldLength
		for i in range(remainingChars):
			buyer += " "
	if len(seller) < 15:
		oldLength = len(seller)
		remainingChars = 15 - oldLength
		for i in range(remainingChars):
			seller += " "
	refund = str(refundFloat)
	if len(refund) < 9:
		oldLength = len(refund)
		remainingChars = 9 - oldLength
		for i in range(remainingChars):
			refund += "0"

	line = code + " " + buyer + " " + seller + " " + refund
	transactions.append(line)
	return
	
# Adds the transaction line for a create/delete/addcredit action to the transactions array
def otherTransaction(transType):
	code = ""
	if transType == "create":
		code = "01"
	elif transType == "delete":
		code = "02"
	elif transType == "addCredit":
		code = "06"
	elif transType == "exit":
		code = "00"
	userName = loggeduser[0]
	if len(userName) < 15:
		oldLength = len(userName)
		remainingChars = 15 - oldLength
		for i in range(remainingChars):
			userName += " "
	userType = loggeduser[1]
	if len(userType) < 2:
		oldLength = len(userType)
		remainingChars = 13 - oldLength
		for i in range(remainingChars):
			userType += " "
	credit = str(loggeduser[2])
	if len(credit) < 9:
		oldLength = len(credit)
		remainingChars = 9 - oldLength
		for i in range(remainingChars):
			credit += "0"

	line = code + " " + userName + " " + userType + " " + credit
	transactions.append(line)
	return

#Updates the UserAccounts text file (database) with new data
def updateUserAccounts():
	newfile = open("./Database/UserAccounts.txt", "w+")
	for info in userInfo:
		userName = info[0]
		if len(userName) < 15:
			oldLength = len(userName)
			remainingChars = 15 - oldLength
			for i in range(remainingChars):
				userName += " "
		userType = info[1]
		if len(userType) < 2:
			oldLength = len(userType)
			remainingChars = 13 - oldLength
			for i in range(remainingChars):
				userType += " "
		credit = str(info[2])
		if len(credit) < 9:
			oldLength = len(credit)
			remainingChars = 9 - oldLength
			for i in range(remainingChars):
				credit += "0"

		line = userName + " " + userType + " " + credit
		newfile.write(line + "\n")
	newfile.close 
	return

#Updates the AvailableTickets text file (database) with new data
def updateAvailableTickets():
	newfile = open("./Database/AvailableTickets.txt", "w+")
	for info in eventInfo:
		eventName = info[0]
		if len(eventName) < 19:
			oldLength = len(eventName)
			remainingChars = 19 - oldLength
			for i in range(remainingChars):
				eventName += " "
		sellerName = info[1]
		if len(sellerName) < 13:
			oldLength = len(sellerName)
			remainingChars = 13 - oldLength
			for i in range(remainingChars):
				sellerName += " "
		numoftix = str(info[2])
		if len(numoftix) < 3:
			oldLength = len(numoftix)
			remainingChars = 3 - oldLength
			for i in range(remainingChars):
				numoftix += " "
		price = str(info[3])
		if len(price) < 6:
			oldLength = len(price)
			remainingChars = 6 - oldLength
			for i in range(remainingChars):
				price += "0"

		line = eventName + " " + sellerName + " " + numoftix + " " + price
		newfile.write(line + "\n")
	newfile.close 
	return


#while loop for commands (Main Function)
while exit != 1:
	print("\n  Please Enter Command (type help for info)  \n")
	result.write("\n  Please Enter Command (type help for info)  \n")
	command = inputs.pop(0).lower()
	print(command)
	result.write(command)
	
	if command =="exit":
		printtransactions()
		exit = 1

	elif command == "help":
		help()

	elif command == "login":
		LoginUser()

	elif command == "logout":
		#login check
		if login == 0:
			print("\n  Unable to logout due to no account being logged in")
			result.write("\n  Unable to logout due to no account being logged in")
		elif login ==1:
			otherTransaction("exit")
			print("\n  Logged Out Successfully")
			result.write("\n  Logged Out Successfully")
			login =0
			loggeduser =[]
	
	elif command == "buy":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and buyer == 0: 
			print("\n  Cannot Buy on Seller Account")
			result.write("\n  Cannot Buy on Seller Account")
		else:
			Buy()

	elif command == "sell":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and seller == 0:
			print("\n  You sneaky fool, only sellers allowed!")
			result.write("\n  You sneaky fool, only sellers allowed!")
		else:
			Sell()

	elif command == "refund":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and admin == 1:
			Refund()
		else:
			print("\n  You sneaky fool, only admins allowed!")

	elif command == "add":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and admin == 1:
			addCredit()
		else:
			print("\n  You sneaky fool, only admins allowed!")
			result.write("\n  You sneaky fool, only admins allowed!")

	elif command == "create":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and admin == 1:
			Create()
		else:
			print("\n  You sneaky fool, only admins allowed!")
			result.write("\n  You sneaky fool, only admins allowed!")    

	elif command == "delete":
		#login check
		if login == 0:
			print("\n  Not logged in yet")
			result.write("\n  Not logged in yet")
		elif login == 1 and admin == 1:
			Delete()
		else:
			print("\n  You sneaky fool, only admins allowed!")
			result.write("\n  You sneaky fool, only admins allowed!")

	else:
		print("\n  Invalid Command!")

dailytransactions.close()
result.close()
