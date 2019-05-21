import mysql.connector
import pandas 
from tabulate import tabulate
from texttable import Texttable
connection = mysql.connector.connect(host='1.22.137.204',port='3307',database='coffee',user='application',password='abc123!@#')

class InventoryDAO:    
    def __allItemList__(self):
        try:
            cursor = connection.cursor()
            sql="select item.inv_item_id, item.item_name,item.item_quantity,item.item_mrp_price,item.item_status,item.item_max_discount,item.created_on,cb.name as created_by,item.updated_on,ub.name as  updated_by from inv_item item inner join users cb on item.created_by=cb.user_id left join users ub on item.updated_by=ub.user_id order by  item.inv_item_id"
            cursor.execute(sql) 
            lst = cursor.fetchall()         
            print(tabulate(lst, headers=['Item Id', 'Item Name','Quantity', 'Item MRP Price', 'Item Status', 'Discount','Created On', 'Created By', 'Updated On', 'Updated By']))        
        except mysql.connector.Error as error :
            print("Error :".format(error))              
        finally:
            if(connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")   
                          

    def __isCount0ItemList__(self):        
        try:
            cursor = connection.cursor()
            sql="select item.inv_item_id, item.item_name,item.item_quantity,item.item_mrp_price,item.item_status,item.item_max_discount,item.created_on,cb.name as created_by,item.updated_on,ub.name as  updated_by from inv_item item inner join users cb on item.created_by=cb.user_id left join users ub on item.updated_by=ub.user_id  where  item.item_quantity=0 or item.item_quantity is null order by  item.inv_item_id"
            cursor.execute(sql)
            lst=cursor.fetchall()
            print(tabulate(lst, headers=['Item Id', 'Item Name','Quantity', 'Item MRP Price', 'Item Status', 'Discount','Created On', 'Created By', 'Updated On', 'Updated By']))
        except mysql.connector.Error as error:
            print("Failed".format(error))  
        finally:
             if(connection.is_connected()):
                cursor.close()
                connection.close()
                 

    def __addItem__(self,user_bean):
       i = 0
       while i == 0:
        print("Enter item name :")
        item_name=input()          
        print(item_name) 
        if not item_name:
            print("Enter valid item name")
            i=0            
        else:
            break 
       try:
            sql_insert_query = 'insert into inv_item(item_name,item_status,created_by,created_on) values("'+item_name+'",2,1,now())'
            print(sql_insert_query)
            cursor = connection.cursor()
            result  = cursor.execute(sql_insert_query)
            connection.commit()
            print ("Record inserted successfully into inventory table")
       except mysql.connector.Error as error :
                connection.rollback() #rollback if any exception occured
                print("Failed inserting record into inventory table {}".format(error))
       finally:
                #closing database connection.
                if(connection.is_connected()):
                    cursor.close()
                    connection.close()
                     
         
        
