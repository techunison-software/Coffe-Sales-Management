import mysql.connector
#import Login as login
from mysql.connector import Error
connection = mysql.connector.connect(host='192.168.1.128',port='3307',database='coffee',user='application',password='abc123!@#')
user_bean="ssds"
# Class Name
class Inventory: 
    # Inventory menu start
   def __init__(user_bean):
      # if not user_bean:
      #   login.LoginInitial().initialCall()             

       print("id    Menu")
       print("1     View item list")
       print("2     Add item")
       print("3     Update item")
       print("4     Delete item")     
       print("Enter Id")               
       id = int(input())
       print(id)
       Inventory.__menuMethod__(id,user_bean)

   def __menuMethod__(id,user_bean):   
       if id==1:
           print("Item List")
           Inventory.__listItem__(id,user_bean)
       elif id==2:
           print(" New Item")
           Inventory.__addItem__(id,user_bean)
  # 
   def __listItem__(id,user_bean):            
      try:
        cursor = connection.cursor()
        sql="SELECT ii.inv_item_id,ii.item_name,ii.item_quantity,ii.item_mrp_price,ii.item_max_discount FROM inv_item as ii where ii.item_quantity > 0"
        print(pandas.read_sql_query(sql))
        cursor.execute()
        lst = cursor.fetchall()
        print(lst);
        print("Item Id" , "Item Name","Created by")
        for row in lst:
                print(row[0],row[1],row[2])
            #  print("ItemId= ", row[0]," Name= ",row[1]," Qty= ", row[2]," MRP= ", row[3] ," Discount= ",row[4])
      except mysql.connector.Error as error :
           print("Failed inserting record into python_users table {}".format(error))
              
      finally:
           if(connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")         
            
        
   def __addItem__(id,user_bean):      
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
            print ("Record inserted successfully into python_users table")
       except mysql.connector.Error as error :
                connection.rollback() #rollback if any exception occured
                print("Failed inserting record into python_users table {}".format(error))
       finally:
                #closing database connection.
                if(connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")



print ("Inventory.__init__:", Inventory.__init__(user_bean))
