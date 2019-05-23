import pandas as pd
import pdfkit as pdf
import datetime
import os
import glob
import csv
import sqlalchemy as sql
import SQLAlchemyCon as conn
from xlsxwriter.workbook import Workbook
#Establish the database connection
sql_engine = conn.getConnection()
userRole = None
#Main Class
class Report:

	def initCall(self,user_bean):
	#def initCall(self):
		# roleId = int(input("Enter the roleId: "))
		# deptId = int(input(" Enter the deptId: "))
		self.getIDDetails(user_bean["role_id"][0],user_bean["department_id"][0])
		userRole = user_bean["role_id"][0]
		print("user role",userRole)
		#self.getIDDetails(roleId,deptId)
		#print("User role not defined")

	#def getUserID(rId,deptId):
	def getIDDetails(self,roleId,deptId):
		#roleId = int(input("Enter the roleId: "))
		#deptId = int(input(" Enter the deptId: "))
		#print(roleId)
		#roleId=rId
		if roleId == 1:
			self.adminReport()
		elif roleId == 2:
			if deptId == 2:
				self.inventoryReport()
			elif deptId == 3:
				self.purchaseReport()
			elif deptId == 4:
				self.salesReport()
		elif roleId == 3:
			self.userReport()


	def adminReport(self):
		print("1.Sales\n2.Purchase\n3.Inventory")
		catOption = int(input())
		if catOption == 1:
			# reportTable = "inv_item"
			self.salesReport()
		elif catOption == 2:
			self.purchaseReport()
		elif catOption == 3:
			# reportTable = "inv_item"
			self.inventoryReport()
		else:
			print("Select type of report")
			self.adminReport()

	def inventoryReport(self):
		queryInventory = None
		print("Inventory Report")
		print("------------------------------")
		print("\n Choose Filter")
		print("1. Date")
		print("2. Item")
		print("3. Discount")
		print("4. Price")
		print("5. Quantity")
		filter = int(input("which filter? "))
		if filter == 1:
			stdt = input("enter start date (yyyy-mm-dd hh:mm:ss) : ")
			enddt = input("enter end date (yyyy-mm-dd hh:mm:ss) : ")
			startdate = stdt
			endDate = enddt
			queryInventory ='select * from inv_item where created_on between \'' + startdate + '\' and \'' + endDate + '\''
		elif filter ==2:
			print("1.3 Roses\n2.AVT Tea\n3.Brooke Bond Taaza\n4.Lipton Tea\n5.Marvel Tea\n6.Pataka Tea\n7.ociety Tea\n8.Tata tea\n9.Chakra Gold\n10.Sunrise")
			itemOption = int(input("Select an item  "))
			queryInventory = 'select * from inv_item  WHERE inv_item_id ='+str(itemOption) 
		elif filter == 3:
			itemOption = int(input("Enter the discount amount "))
			queryInventory = 'select * from inv_item  WHERE item_max_discount <='+str(itemOption) 
		elif filter == 4:
			itemOption = int(input("Enter the price"))
			queryInventory = 'select * from inv_item  WHERE item_mrp_price <='+str(itemOption)
		elif filter == 5:
			itemOption = int(input("Enter the Quantity"))
			queryInventory = 'select * from inv_item  WHERE item_quantity <='+str(itemOption)
		else:
			print("Choose any filter")
			self.inventoryReport()
		
		result=pd.read_sql_query(queryInventory, sql_engine) 
		inventryCount = len(result)
		if inventryCount > 0:
			print(result)
			print('\n-----------------------------------------------------------------')
			print('|Item Id\t|Item Name\t|Price\t\t|Quantity\t|')
			print('\n-----------------------------------------------------------------')
			for index, row in result.iterrows():
				print('|'+str(row['inv_item_id'])+'\t\t|'+row['item_name']+'\t\t|'+str(row['item_mrp_price'])+'\t\t|'+str(row['item_quantity'])+'\t\t|')
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
			self.inventoryReport()
		else:
			print("No data found in selected filter")
			self.inventoryReport()
	def salesReport(self):
		querySales=None
		print("-----------Sales Report--------------")
		try:
			print("\nChoose Filters")
			print("1. Date")
			print("2. Item")
			print("3. Discount")
			print("4. Selling Price")
			print("-------------------------------")
			filter = int(input("Choose filter? "))
			if filter == 1:
				stdt = input("enter start date (yyyy-mm-dd hh:mm:ss) : ")
				enddt = input("enter end date (yyyy-mm-dd hh:mm:ss) : ")
				startdate = stdt
				endDate = enddt
				querySales ='select * from so_header_details where created_on between \'' + startdate + '\' and \'' + endDate + '\''
			elif filter == 2:
				print("1.3 Roses\n2.AVT Tea\n3.Brooke Bond Taaza\n4.Lipton Tea\n5.Marvel Tea\n6.Pataka Tea\n7.ociety Tea\n8.Tata tea\n9.Chakra Gold\n10.Sunrise")
				itemOption = int(input("Select an item  "))
				querySales = 'select * from so_header_details  WHERE inv_item_id ='+str(itemOption) 
			elif filter == 3:
				itemOption = int(input("Enter the discount amount "))
				querySales = 'select * from so_header_details  WHERE discount <='+str(itemOption) 
			elif filter == 4:
				itemOption = int(input("Enter the total seeling amount"))
				querySales = 'select * from so_header_details  WHERE total_price <='+str(itemOption) 
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
				print('\n------------------------------------------------------------------------------------')
				print('|Item Id\t\t|Item Quantity\t\t|Discount\t\t|Unit_price\t\t|Total_price\t\t|created_by\t\t|created_on|')
				print('\n-------------------------------------------------------------------------------------')
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
				self.salesReport()
			else:
				print("No data found in selected filter")
				# if userRole == 1:
				# 	self.adminReport()
				# else:
				self.salesReport()
		except Exception as e:
			print("Select valid data: ")

	#def salesReportGenerate(self,queryString)
				

	def purchaseReport(self):
		queryPurchase = None
		print("----------------purchaseReport-----------")
		print("\nChoose Filters")
		print("1. Date")
		print("2. Vendor")
		filter = int(input("Choose filter? "))
		if filter == 1:
			stdt = input("enter start date (yyyy-mm-dd hh:mm:ss) : ")
			enddt = input("enter end date (yyyy-mm-dd hh:mm:ss) : ")
			startdate = stdt
			endDate = enddt
			queryPurchase ='select * from po_purchase where created_on between \'' + startdate + '\' and \'' + endDate + '\''
		elif filter == 2:
			print("1.Tata\n2.Chakra Gold\n3.Sunrise\n4.Lipton\n5.3 Roses\n6.Society\n7.Marvel\n8.Brooke Bond\n9.Pataka\n10.Taj Mahal")
			itemOption = int(input("Select an item  "))
			queryPurchase = 'select * from po_purchase  WHERE vendors_item_id = '+str(itemOption) 
		else:
			print("Choose any filter")
			self.purchaseReport()

		result=pd.read_sql_query(queryPurchase, sql_engine) 
		print(result)
		purchaseCount = len(result)
		if purchaseCount > 0:
			print('\n-----------------------------------------------------------------')
			print('|Purchase Id\t|Total Amount\t|Payment Type\t\t|Vendors ID\t|\t\t|Created On\t|')
			print('\n-----------------------------------------------------------------')
			for index, row in result.iterrows():
				print('|'+str(row['po_purchase_Id'])+'\t\t|'+str(row['total_amount'])+'\t\t|'+str(row['Payment_type_id'])+'\t\t|'+str(row['vendors_item_id'])+'\t\t|'+str(row['created_on'])+'\t\t|')
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
			self.purchaseReport()
		else:
			print("No data found in selected filter")
			self.purchaseReport()
	def userReport(self):
		print("1.userReport")
		catOption = int(input())
		if catOption == 1:
			print("\n\Inventory Report: Filters")
			print("1. date")
			print("2. item")
		filter = int(input("which filter? "))
		if filter == 1:
			stdt = input("enter start date (yyyy-mm-dd hh:mm:ss) : ")
			enddt = input("enter end date (yyyy-mm-dd hh:mm:ss) : ")

		#startdate = datetime.date(2019,5,15).strftime('%Y-%m-%d %H:%M:%S')
		#endDate = datetime.date(2019,5,16).strftime('%Y-%m-%d %H:%M:%S')
		startdate = stdt
		endDate = enddt

		queryDate ='select * from inv_item where created_on between \'' + startdate + '\' and \'' + endDate + '\''
		result=pd.read_sql_query(queryDate, sql_engine) 
		print('\n-----------------------------------------------------------------')
		print('|Item Id\t|Item Name\t|Price\t\t|Quantity\t|')
		print('\n-----------------------------------------------------------------')
		for index, row in result.iterrows():
			print('|'+str(row['inv_item_id'])+'\t\t|'+row['item_name']+'\t\t|'+str(row['item_mrp_price'])+'\t\t|'+str(row['item_quantity'])+'\t\t|')
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



# rp = Report()
# rp.initCall()


