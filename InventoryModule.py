import mysql.connector
import pandas
import InventoryModuleMenu as menu
import Validation as valid
import InventoryDAO as dao
import Login as login
from tabulate import tabulate
from texttable import Texttable

# Class Name
class InventoryModule: 
    # Inventory menu start
    def initCall(self, user):
        user_bean=[]
        self.user=user
        user_bean.insert(0,user['user_id'][0])
        user_bean.insert(1,user['role_id'][0])
        menu.InventoryModuleMenu().__mainMuen__() 
        id=valid.Validataion().__inputIdValidataion__(6)               
        self.__menuMethod__(id,user_bean)

    def __menuMethod__(self,id,user_bean): 
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
            if user_bean[1]!=3:
                print("----------------------- Delete Item -------------------")
                dao.InventoryDAO().__allItemList__(1)
                #we don't detete the itme. we just update the item_status =0 
                item_id=dao.InventoryDAO().__selectUpdateItemId__()
                dao.InventoryDAO().__updateItem__(item_id,user_bean,2)
            else:
                print("Error : You can't able to delete.")
        elif int(id)==5:
            print("-----------------------PO Request ---------------------------------")
            menu.InventoryModuleMenu().__poMenuList__()
            InventoryModule().__poRequest__(user_bean)
        elif int(id)==6:
            print("---------------------- Main Menu ----------------------------------")
            login.Login().initialCall(self.user)        
        
        self.initCall(self.user)
                        

    def __poRequest__(self,user_bean):
        id=valid.Validataion().__inputIdValidataion__(6)
        if int(id)==1:
            menu.InventoryModuleMenu().__poRequestListMenu__()
            id=valid.Validataion().__inputIdValidataion__(4)
            if int(id)==1:
                dao.InventoryDAO().__poRequestList__(1,1)
            elif int(id)==2:
                dao.InventoryDAO().__poRequestList__(1,2)             
            elif int(id)==3:
                dao.InventoryDAO().__poRequestList__(1,3)
            elif int(id)==4:
                InventoryModule().__menuMethod__(5,user_bean)

        elif int(id)==2:
            dao.InventoryDAO().__addPORequest__(user_bean)
        elif int(id)==3:
            dao.InventoryDAO().__poRequestList__(1,1)
            poRequestId=dao.InventoryDAO().__selectUpdatePORequestId__()            
            dao.InventoryDAO().__updatePORequest__(poRequestId,user_bean,1)
        elif int(id)==4:
            if user_bean[1]!=3:
                dao.InventoryDAO().__poRequestList__(1,1)
                poRequestId=dao.InventoryDAO().__selectUpdatePORequestId__()
                dao.InventoryDAO().__updatePORequest__(poRequestId,user_bean,2)
            else:
                print("Error : You can't able to delete.")

        elif int(id)==5:
            print("========")
        elif int(id)==6:
            InventoryModule().initCall(user_bean)
        menu.InventoryModuleMenu().__poMenuList__()
        InventoryModule().__poRequest__(user_bean)

            


    
