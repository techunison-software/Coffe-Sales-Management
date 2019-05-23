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
        id=valid.Validataion().__inputIdValidataion__(7)               
        InventoryModule.__menuMethod__(id,user_bean)

    def __menuMethod__(id,user_bean):         
        if int(id)==1:    
            menu.InventoryModuleMenu().__itemListMenu__() 
            id=valid.Validataion().__inputIdValidataion__(2)             
            if int(id)==1:
                dao.InventoryDAO().__allItemList__(1)
            else:
                dao.InventoryDAO().__isCount0ItemList__()
        elif int(id)==2:
            print("---------------------- New Item  ---------------------")
            dao.InventoryDAO().__addItem__(user_bean)
        elif int(id)==3:
            print("---------------------- Update Item -------------------")
            dao.InventoryDAO().__allItemList__(2)
            item_id=dao.InventoryDAO().__selectUpdateItemId__()
            dao.InventoryDAO().__updateItem__(item_id,user_bean,1)
        elif int(id)==4:
            print("----------------------- Delete Item -------------------")
            dao.InventoryDAO().__allItemList__(1)
            #we don't detete the itme. we just update the item_status =0 
            item_id=dao.InventoryDAO().__selectUpdateItemId__()
            dao.InventoryDAO().__updateItem__(item_id,user_bean,2)
        elif int(id)==5:
            print("--------------------------------------------------------")
            menu.InventoryModuleMenu().__poMenuList__()
            InventoryModule.__poRequest__(user_bean)
        InventoryModule.__init__(user_bean)
                        

    def __poRequest__(user_bean):
        id=valid.Validataion().__inputIdValidataion__(5)
        if int(id)==1:
            menu.InventoryModuleMenu().__poRequestListMenu__()
            id=valid.Validataion().__inputIdValidataion__(3)
            if int(id)==1:
                dao.InventoryDAO().__poRequestList__(1,1)
            elif int(id)==2:
                dao.InventoryDAO().__poRequestList__(1,2)             
            elif int(id)==3:
                dao.InventoryDAO().__poRequestList__(1,3)
        elif int(id)==2:
            dao.InventoryDAO().__addPORequest__(user_bean)
        elif int(id)==3:
            dao.InventoryDAO().__poRequestList__(1,1)
            poRequestId=dao.InventoryDAO().__selectUpdatePORequestId__()
            


    

            
         

                    
        
   



print ("Inventory.__init__:", InventoryModule.__init__(user_bean))
