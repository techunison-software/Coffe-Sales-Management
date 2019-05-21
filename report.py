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
#Main Class
class Report:

	def initCall(self,user_bean):
		self.getIDDetails(user_bean["role_id"][0],user_bean["department_id"][0])
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

	#//roleId = int(input("Enter your role Id: "))
	#print("\n\nChoose an option")
	#if roleId == 1 or roleId == 2:
		
	#else:
	#	print("1. Sales")

	def adminReport(self):
		print("1.Sales\n2.Purchase\n3.Inventory")
		catOption = int(input())
		if catOption == 1:
			reportTable = "inv_item"
		elif catOption == 2:
			reportTable = "inv_item"
		elif catOption == 3:
			reportTable = "inv_item"


		if catOption == 1 or catOption == 2 or catOption == 3:
			print("\n\nSales Report: Filters")
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

		queryDate ='select * from '+reportTable+' where created_on between \'' + startdate + '\' and \'' + endDate + '\''
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

	def inventoryReport(self):
		print("1.Inventory")
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
	def salesReport(self):
		print("1.salesReport")
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
	def purchaseReport(self):
		print("1.purchaseReport")
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





