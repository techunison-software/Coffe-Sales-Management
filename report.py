import pandas as pd
import pdfkit as pdf
import datetime
from datetime import datetime
import os
import glob
import csv
import Login 
import sqlalchemy as sql
import SQLAlchemyCon as conn
from xlsxwriter.workbook import Workbook
from tabulate import tabulate
#Establish the database connection
sql_engine = conn.getConnection()
global userRole 
#userRole = 0
global userID 
global userData
#Main Class
class Report:

	def initCall(self,user_bean):
	# def initCall(self):
		# roleId = int(input("Enter the roleId: "))
		# deptId = int(input(" Enter the deptId: "))
		global userID
		userID = user_bean["user_id"][0]
		print("user ID",userID)
		global userRole 
		# userRole = roleId
		userRole = user_bean["role_id"][0]
		global userData
		userData = user_bean
		self.getIDDetails(user_bean["role_id"][0],user_bean["department_id"][0])

		# print("userRole------",userRole)
		# self.getIDDetails(roleId,deptId)
		#print("User role not defined")
	def callLoginModule(self):
		try:
			loginModule = Login.Login()
			loginModule.initialCall(userData)
		except:
			print("\n Function call error")
			self.initCall(userData)
           
	#def getUserID(rId,deptId):
	def getIDDetails(self,roleId,deptId):
		#roleId = int(input("Enter the roleId: "))
		#deptId = int(input(" Enter the deptId: "))
		#print(roleId)
		#roleId=rId
		try:
			if roleId == 1:
				self.adminReport()
			elif roleId == 2:
				if deptId == 2:
					self.inventryManager()
				elif deptId == 3:
					self.purchaseManager()
				elif deptId == 4:
					self.salesManager()
			elif roleId == 3:
				self.userMethod()
		except Exception as e:
			print("Error:----",e)
		finally:
			print("Valid user data")		


	def adminReport(self):
		print(tabulate([["1", "Sales Report"],["2","Purchase Report"],["3","Inventory Report"],["4","Back To Main Menu"]], headers=['Id', 'Menu'])) 
		try:
			adminOption = input("\n----Select the report type----\n")
			if adminOption.isdigit():
				catOption = int(adminOption)
				if catOption == 1:
					# reportTable = "inv_item"
					self.salesReport()
				elif catOption == 2:
					self.purchaseReport()
				elif catOption == 3:
					# reportTable = "inv_item"
					self.inventoryReport()
				elif catOption == 4:
					# reportTable = "inv_item"
					self.callLoginModule()
				else:
					print("Select the report")
					self.adminReport()
			else:
				print("Enter valid input number")
				self.adminReport()
		except Exception as e:
			print("Error:-----",e)
		finally:
			print("Select Valid report")
	def salesManager(self):
		print(tabulate([["1", "Sales Report"],["2","Back To Main Menu"]], headers=['Id', 'Menu']))
		UserOption = input("\n----Select the report type ----\n")
		try:
			if UserOption.isdigit():
				selectionOption = int(UserOption)
				if selectionOption == 1:
					self.salesReport()
				elif selectionOption ==2:
					self.callLoginModule()
				else:
					print("Select valid item")
					self.salesManager()
			else:
				print("Enter valid input number")
				self.salesManager()
		except Exception as e:
			print("Error-----",e)
			
		finally:
			print("Valid input")
			self.salesManager()
	def purchaseManager(self):
		print(tabulate([["1", "Purchase Report"],["2","Back To Main Menu"]], headers=['Id', 'Menu']))
		userselection = input("\n----Select the report type ----\n")
		try:
			if userselection.isdigit():
				selectionOption = int(userselection)
				if selectionOption == 1:
					self.purchaseReport()
				elif selectionOption ==2:
					self.callLoginModule()
				else:
					print("Select valid item")
			else:
				print("Enter valid input number")
				self.purchaseManager()
		except Exception as e:
			print("Error:----",e)
		finally:
			print("Enter valid input number")
			self.purchaseManager()
	def inventryManager(self):
		print(tabulate([["1","Inventry Report"],["2","Back To Main Menu"]], headers=['Id', 'Menu']))
		userInventory = input("\n----Select the report type ----\n")
		try:
			if userInventory.isdigit():
				selectionOption = int(userInventory)
				if selectionOption == 1:
					self.inventoryReport()
				elif selectionOption ==2:
					self.callLoginModule()
				else:
					print("Select valid item")
			else:
				print("")
				self.inventryManager("Enter valid input number")
		except Exception as e:
			print("Error:----",e)
		finally:
			print("Valid input")
			self.inventryManager()

	def userMethod(self):
		print(tabulate([["1", "User Report"],["2","Back To Main Menu"]], headers=['Id', 'Menu']))
		userselection = input("\n----Select the report type ----\n")
		try:
			if userselection.isdigit():
				selectionOption = int(userselection)
				if selectionOption == 1:
					self.userReport()
				elif selectionOption ==2:
					self.callLoginModule()
				else:
					print("Select valid item")
			else:
				print("Enter valid input number")
				self.userMethod()
		except Exception as e:
			print("Error:----",e)
		finally:
			print("Enter valid input number")
			self.userMethod()
	def inventoryReport(self):
		queryInventory = None
		print("------------------Inventory Report---------------\n")

		print(tabulate([["1","Date"],["2","Item"],["3","Discount"],["4","Price"],["5","Quantity"],["6","Back To Main Menu"]], headers=['Id', 'Menu'])) 
		inventType = input("Choose filter type?")
		try:
			if inventType.isdigit():
				filter = int(inventType)
				if filter == 1:
					stdt = input("enter start date (yyyy-mm-dd) : ")
					startdate = stdt
					if self.validateDate(startdate) is False:
						self.inventoryReport()
					enddt = input("enter end date (yyyy-mm-dd hh:mm:ss) : ")
					endDate = enddt
					if self.validateDate(endDate) is False:
						self.inventoryReport()
					queryInventory ='select * from inv_item where created_on between \'' + startdate + '\' and \'' + endDate + '\''
				elif filter ==2:
					print(tabulate([["1","3 Roses"],["2","AVT Tea"],["3","Brooke Bond Taaza"],["4","Lipton Tea"],["5","Marvel Tea"],["6","Pataka Tea"],["7","Society Tea"]], headers=['Id', 'Menu'])) 
					itemOption = input("Select an item  ")
					if itemOption.isdigit():
						queryInventory = 'select * from inv_item  WHERE inv_item_id ='+itemOption
					else:
						print("Enter valid number")	 
						self.inventoryReport()
				elif filter == 3:
					itemOption = input("Enter the discount price ")
					if itemOption.isdigit():
						queryInventory = 'select * from inv_item  WHERE item_max_discount <='+itemOption 
					else:
						print("Enter valid price")	 
						self.inventoryReport()
				elif filter == 4:
					itemOption = input("Enter the price")
					if itemOption.isdigit():
						queryInventory = 'select * from inv_item  WHERE item_mrp_price <='+itemOption
					else:
						print("Enter valid price")	 
						self.inventoryReport()
				elif filter == 5:
					itemOption = input("Enter the Quantity")
					if itemOption.isdigit():
						queryInventory = 'select * from inv_item  WHERE item_quantity <='+str(itemOption)
					else:
						print("Enter valid number")	 
						self.inventoryReport()
				elif filter == 6:
					rId =  userRole
					if rId == 1:
						self.adminReport()
					else:	
						self.inventryManager()
				else:
					print("Choose any filter")			
					self.inventoryReport()
				result=pd.read_sql_query(queryInventory, sql_engine) 
				inventryCount = len(result)
				if inventryCount > 0:
					# print(result)
					print('\n--------------------------------------------------------------------------------------------------------------------------------------\n')					
					print(tabulate(result, headers=['Item Id','Item Name','Item Description','Item MRP Price','Quantity','Item Status','Discount','Created By','Created On','Updated By','Updated On','Weight','Active','Delete Date']))
					#Converting CSV File
					result.to_csv("report.csv", index=False)
					#Converting Excel File
					for csvfile in glob.glob(os.path.join('.', '*.csv')):
					    workbook = Workbook(csvfile[:-4] + '.xlsx')
					    worksheet = workbook.add_worksheet()
					    with open(csvfile, 'rt', encoding='utf8') as f:
					        reader = csv.reader(f)
					        for r, row in enumerate(reader):
					            for c, col in enumerate(row):
					                worksheet.write(r, c, col)
					    workbook.close() 
					#Converting PDF File        
					csv_file = 'report.csv'
					html_file = csv_file[:-3]+'html'
					pdf_file = csv_file[:-3]+'pdf'
					df = pd.read_csv(csv_file, sep=',')
					df.to_html(html_file)
					pdf.from_file(html_file, pdf_file)
					self.inventoryReport()
				else:
					print("No data found in selected filter")
					self.inventoryReport()
			else:
				print("Enter valid input number")
				self.inventoryReport()
		except Exception as e:
			print("Error:----",e)
		
		finally:
			print('\n\tError : Input.',e)
			self.inventoryReport()
	def salesReport(self):
		querySales=None
		print("-----------Sales Report--------------\n")
		print(tabulate([["1","Date"],["2","Item"],["3","Discount"],["4","Selling Price"],["5","Back To Main Menu"]], headers=['Id', 'Menu']))
		salesIDValue = input("Choose filter type? ")
		try:
			if salesIDValue.isdigit():
				filter = int(salesIDValue)
				if filter == 1:
					stdt = input("enter start date (yyyy-mm-dd) : ")
					startdate = stdt
					if self.validateDate(startdate) is False:
						self.salesReport()
					enddt = input("enter end date (yyyy-mm-dd ) : ")
					endDate = enddt
					if self.validateDate(endDate) is False:
						self.salesReport()
					querySales ='select * from so_header_details where created_on between \'' + startdate + '\' and \'' + endDate + '\''
				elif filter == 2:
					print(tabulate([["1","3 Roses"],["2","AVT Tea"],["3","Brooke Bond Taaza"],["4","Lipton Tea"],["5","Marvel Tea"],["6","Pataka Tea"],["7","Society Tea"]], headers=['Id', 'Menu'])) 
					itemOption = input("Select an item  ")
					if itemOption.isdigit():
						querySales = 'select * from so_header_details  WHERE inv_item_id ='+itemOption 
					else:
						print("Enter valid number")
						self.salesReport()	 	
				elif filter == 3:
					itemOption = input("Enter the discount price ")
					if itemOption.isdigit():
						querySales = 'select * from so_header_details  WHERE discount <='+itemOption 
					else:
						print("Enter valid price")
						self.salesReport()
				elif filter == 4:
					itemOption = input("Enter the total seeling price ")
					if itemOption.isdigit():
						querySales = 'select * from so_header_details  WHERE total_price <='+itemOption 
					else:
						print("Enter valid seeling price")
						self.salesReport()
				elif filter == 5:
					rId =  userRole
					if rId == 1:
						self.adminReport()
					else:	
						self.salesManager()
				else:
					print("Choose any filter")
					self.salesReport()
				#queryDate ='select * from inv_item where created_on between \'' + startdate + '\' and \'' + endDate + '\''
				# queryDate = 'select * from so_header_details  WHERE inv_item_id ='+str(itemOption) 
				result=pd.read_sql_query(querySales, sql_engine) 
				totalcount = len(result)
				print("totalcount",totalcount)
				if totalcount > 0:
					# print(result)
					print('\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
					print(tabulate(result, headers=['Header Details ID','Item ID','Quantity','Discount','Unit Price','Total Price','Created By','Created On','Updated By','Updated On','Header ID','Delete Date']))
					#Converting CSV File
					result.to_csv("report.csv", index=False)
					#Converting Excel File
					for csvfile in glob.glob(os.path.join('.', '*.csv')):
					    workbook = Workbook(csvfile[:-4] + '.xlsx')
					    worksheet = workbook.add_worksheet()
					    with open(csvfile, 'rt', encoding='utf8') as f:
					        reader = csv.reader(f)
					        for r, row in enumerate(reader):
					            for c, col in enumerate(row):
					                worksheet.write(r, c, col)
					    workbook.close() 
					#Converting PDF File        
					csv_file = 'report.csv'
					html_file = csv_file[:-3]+'html'
					pdf_file = csv_file[:-3]+'pdf'
					df = pd.read_csv(csv_file, sep=',')
					df.to_html(html_file)
					pdf.from_file(html_file, pdf_file)
					self.salesReport()
				else:
					print("No data found in selected filter")
					# if userRole == 1:
					# 	self.adminReport()
					# else:
					self.salesReport()
			else:
				print("Enter valid input number")
				self.salesReport()
		except Exception as e:
			print("Select valid data: ")
		finally:
			print("Input error")
			self.salesReport()

	#def salesReportGenerate(self,queryString)
				

	def purchaseReport(self):
		queryPurchase = None
		print("----------------purchaseReport-----------\n")
		print(tabulate([["1","Date"],["2","Vendor"],["3","Back To Main Menu"]], headers=['Id', 'Menu']))
		purchaseIDvalue = input("Choose filter? ")
		try:
			if purchaseIDvalue.isdigit():
				filter = int(purchaseIDvalue)
				if filter == 1:
					stdt = input("enter start date (yyyy-mm-dd) : ")
					startdate = stdt
					if self.validateDate(startdate) is False:
						self.purchaseReport()
					enddt = input("enter end date (yyyy-mm-dd) : ")
					endDate = enddt
					if self.validateDate(endDate) is False:
						self.purchaseReport()
					queryPurchase ='select * from po_purchase where created_on between \'' + startdate + '\' and \'' + endDate + '\''
				elif filter == 2:
					print(tabulate([["1","Tata"],["2","Chakra Gold"],["3","Sunrise"],["4","Lipton"],["5","3 Roses"],["6","Society"],["6","Marvel"]], headers=['Id', 'Menu'])) 
					itemOption = input("Select an item  ")
					if itemOption.isdigit():
						queryPurchase = 'select * from po_purchase  WHERE vendors_item_id = '+itemOption
					else:
						print("Enter valid number")
						self.purchaseReport() 
				elif filter == 3:
					rId =  userRole
					if rId == 1:
						self.adminReport()
					else:	
						self.purchaseManager()
				else:
					print("Choose any filter")
					self.purchaseReport()

				result=pd.read_sql_query(queryPurchase, sql_engine) 
				#print(result)
				purchaseCount = len(result)
				if purchaseCount > 0:
	
					print('\n-----------------------------------------------------------------------------------------------------------------------------------------------------\n')
					print(tabulate(result, headers=['Purchase ID','Created By','Updated By','Order No','Total Amount','Payment Type','Created On','Updated On','PO Req ID','Vendors Item ID','Status']))
					#Converting CSV File
					result.to_csv("report.csv", index=False)
					#Converting Excel File 
					for csvfile in glob.glob(os.path.join('.', '*.csv')):
					    workbook = Workbook(csvfile[:-4] + '.xlsx')
					    worksheet = workbook.add_worksheet()
					    with open(csvfile, 'rt', encoding='utf8') as f:
					        reader = csv.reader(f)
					        for r, row in enumerate(reader):
					            for c, col in enumerate(row):
					                worksheet.write(r, c, col)
					    workbook.close() 
					#Converting PDF File        
					csv_file = 'report.csv'
					html_file = csv_file[:-3]+'html'
					pdf_file = csv_file[:-3]+'pdf'
					df = pd.read_csv(csv_file, sep=',')
					df.to_html(html_file)
					pdf.from_file(html_file, pdf_file)
					self.purchaseReport()
				else:
					print("No data found in selected filter")
					self.purchaseReport()
			else:
				print("Enter valid input number")
				self.purchaseReport()
		except Exception as e:
			print("Error: ----",e)
		finally:
			print("Purchase report input error")
			self.purchaseReport()
	def userReport(self):
		queryUser = None
		print("-------------------userReport----------------------\n")
		print(tabulate([["1","Date"],["2","Consolidate"],["3","Back To Main Menu"]], headers=['Id', 'Menu']))
		userIDValue = input("which filter? ")

		try:
			if userIDValue.isdigit():
				filter = int(userIDValue)
				if filter == 1:
					stdt = input("enter start date (yyyy-mm-dd) : ")
					startdate = stdt
					if self.validateDate(startdate) is False:
						self.userReport()
					enddt = input("enter end date (yyyy-mm-dd) : ")
					endDate = enddt
					if self.validateDate(endDate) is False:
						self.userReport()
					itemOPS = userID
					queryUser ='select * from so_header_details  WHERE  created_on between \'' + startdate + '\' and \'' + endDate + '\'  and  created_by = '+str(itemOPS)
				elif filter == 2:
					#querySales = 'select * from so_header_details  WHERE created_by ='+str(itemOption) 
					itemOPS = userID
					# itemOPS = 1
					queryUser = 'select * from so_header_details  WHERE created_by = '+str(itemOPS) 
				elif filter == 3:
					self.userMethod()
				else:
					self.userReport()

				result=pd.read_sql_query(queryUser, sql_engine) 
				totalcount = len(result)
				print("totalcount",totalcount)
				if totalcount > 0:
					
					print('\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
					print(tabulate(result, headers=['Header Details ID','Item ID','Quantity','Discount','Unit Price','Total Price','Created By','Created On','Updated By','Updated On','Header ID','Delete Date']))
					for index, row in result.iterrows():
						#print('|'+str(row['inv_item_id'])+'\t\t|'+row['item_name']+'\t\t|'+str(row['item_mrp_price'])+'\t\t|'+str(row['item_quantity'])+'\t\t|')
						print('|'+str(row['inv_item_id'])+'\t\t|'+str(row['quantity'])+'\t\t|'+str(row['discount'])+'\t\t|'+str(row['unit_price'])+'\t\t|'+'\t\t|'+str(row['total_price'])+'\t\t|'+'\t\t|'+str(row['created_by'])+'\t\t|'+str(row['created_on'])+'\t\t|')
						#print('|'+str(row['inv_item_id'])+'\t\t|'+str(row['quantity'])+'\t\t|'+str(row['discount'])+'\t\t|'+str(row['unit_price'])+'\t\t|'+str(row['total_price'])+'\t\t|'+row['created_by']+'\t\t'+row['created_on']+'\t\t|')
						print('\n-----------------------------------------------------------------\n')
						#Converting CSV File
						result.to_csv("report.csv", index=False)
						#Converting Excel File
						for csvfile in glob.glob(os.path.join('.', '*.csv')):
						    workbook = Workbook(csvfile[:-4] + '.xlsx')
						    worksheet = workbook.add_worksheet()
						    with open(csvfile, 'rt', encoding='utf8') as f:
						        reader = csv.reader(f)
						        for r, row in enumerate(reader):
						            for c, col in enumerate(row):
						                worksheet.write(r, c, col)
						    workbook.close() 
						#Converting PDF File        
						csv_file = 'report.csv'
						html_file = csv_file[:-3]+'html'
						pdf_file = csv_file[:-3]+'pdf'
						df = pd.read_csv(csv_file, sep=',')
						df.to_html(html_file)
						pdf.from_file(html_file, pdf_file)
						self.userReport()
				else:
					print("No data found in selected filter")
					# if userRole == 1:
					# 	self.adminReport()
					# else:
					self.userReport()
			else:
				print("")
				self.userReport()
		except Exception as e:
			print("Error:--------",e)
		finally:
			print("Invalid Syntax")
			self.userReport()

	def validateDate(self,dateString):
		try:
			datetime.strptime(dateString, '%Y-%m-%d')
			print('The date {} is valid.'.format(dateString))
			return True
		except ValueError:
			print('The date {} is invalid'.format(dateString))
			return False
						
					
						
						






# rp = Report()
# rp.initCall()


