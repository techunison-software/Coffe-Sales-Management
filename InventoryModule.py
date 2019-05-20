import mysql.connector
import pandas
import InventoryModuleMenu as menu
import Validation as valid
import InventoryDAO as dao
from tabulate import tabulate
from texttable import Texttable
#import Login as login
from mysql.connector import Error
connection = mysql.connector.connect(host='192.168.1.128',port='3307',database='coffee',user='application',password='abc123!@#')
user_bean=""
# Class Name
class InventoryModule: 
    # Inventory menu start
    def __init__(user_bean):
        # if not user_bean:
      #   login.LoginInitial().initialCall() 
        menu.InventoryModuleMenu().__mainMuen__() 
        id=valid.Validataion().__inputIdValidataion__(4)               
        InventoryModule.__menuMethod__(id,user_bean)

    def __menuMethod__(id,user_bean):         
        if int(id)==1:    
            menu.InventoryModuleMenu().__itemListMenu__() 
            id=valid.Validataion().__inputIdValidataion__(2)             
            if int(id)==1:
                dao.InventoryDAO().__allItemList__()
            else:
                dao.InventoryDAO().__isCount0ItemList__()
        elif int(id)==2:
            print("---------------------- New Item  ---------------------")
            dao.InventoryDAO().__addItem__(id,user_bean)
        InventoryModule.__init__(user_bean)            
        
   



print ("Inventory.__init__:", InventoryModule.__init__(user_bean))
