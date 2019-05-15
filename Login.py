import pandas as pd
import sqlalchemy as sql
import SQLAlchemyCon as conn

import UserModule as userMod
import PurchaseModule as purchaseMod
import SalesModule as salesMod
"""import InventoryModule as inventoryMod   """

sql_engine=conn.getConnection()

class Login:    

    def initialCall(self):
        self.user_name=input("Enter User Name :")
        self.password=input("Enter password  :")
        self.authenticate()

    def authenticate(self):
        user=self.getUserDetails()
        if not user.empty:
            if self.user_name == user["user_name"][0] and self.password == user["password"][0]:
                print("\tSuccessfully LogedIn!\n")
                self.user=user            
                self.showMainMenu()
            else:
                print("\tLogin Failed!\n\tInvalid User name or password.")
                self.user=None
                self.initialCall()
        else:
            print("\tLogin Failed!\n\tUser Does not Exist.Please enter a valid user.\n")
            self.initialCall()

    def getUserDetails(self):
        result=None
        try:
            query = 'select u.user_id, u.user_name, u.name, u.email_id, u.password, u.department_id, d.department_name, u.role_id, rt.role, u.status_id, u.created_by, u.created_on, u.updated_by, u.updated_on from users u join role_type rt on rt.role_id=u.role_id join department d on d.department_id=u.department_id where u.user_name=''"'+self.user_name+'"'
            result=pd.read_sql_query(query, sql_engine) 
        except :
            print('An error occured.')       
        return result     

    def showMainMenu(self):
        if str(self.user["role"][0]).casefold()==str("Admin").casefold():
            val=input("\t1. User Module \n\t2. Inventory \n\t3. Purchase Module \n\t4. Sales Module \n\nEnter the Value :")
            self.moduleValue(val)            
        else:
            if str(self.user["department_name"][0]).casefold()==str("HR").casefold():
                self.callUserModule()                
            elif str(self.user["department_name"][0]).casefold()==str("Inventory").casefold():
                self.callInventoryModule()
            elif str(self.user["department_name"][0]).casefold()==str("Purchase").casefold():
                user_input=self.checkIntValue(input("\t1. Purhase Module \n\t2. Inventory Module  \nEnter the Value :"))
                if user_input ==1:
                    self.callPurchaseModule()
                elif user_input ==2 :
                    self.callInventoryModule()
                else :
                    print("\tPlease enter a valid input!\n")
                    self.showMainMenu()
            elif str(self.user["department_name"][0]).casefold()==str("Sales").casefold():
                user_input = self.checkIntValue(input("\t1. Sales Module \n\t2. Inventory Module \nEnter the Value :"))                 
                if user_input==1:
                    self.callPurchaseModule()
                elif user_input==2 :
                    self.callInventoryModule()
                else:
                    print("\tPlease enter a valid input!\n")
                    self.showMainMenu()

    def moduleValue(self,user_input):
        inp_value = self.checkIntValue(user_input) 
        if inp_value == 1:
            self.callUserModule()
        elif inp_value==2:
            self.callInventoryModule()
        elif inp_value==3:
            self.callPurchaseModule()
        elif inp_value==4:
            self.callSalesModule()
        else:
            print("\tPlease enter a valid input!\n")
            self.showMainMenu()
        
    def checkIntValue(self,user_input):
        try:
            val = int(user_input)
            return val
        except ValueError:
            print("\tInput value is not an Integer. Please enter Integer value alone!\n")
            self.showMainMenu()  
            
    def callUserModule(self):
        try:
            us_mod=userMod.UserModule()
            us_mod.initCall(self.user)
        except :
            print("\tNo file named UserModule is found!\n")
            self.showMainMenu()

    def callInventoryModule(self):
        try:
            inv_mod=inventoryMod.InventoryModule()
            inv_mod.initCall(self.user)
        except :
            print("\tNo file named InventoryModule is found!\n")
            self.showMainMenu()
            
    def callPurchaseModule(self):
        try:
            pur_mod=purchaseMod.PurchaseModule()
            pur_mod.initCall(self.user)
        except :
            print("\tNo file named PurchaseModule is found!\n")
            self.showMainMenu()
            
    def callSalesModule(self):
        try:
            sales_mod=salesMod.SalesModule()
            sales_mod.initCall(self.user)
        except :
            print("\tNo file named SalesModule is found!\n")
            self.showMainMenu()
            
login_check = Login()        
login_check.initialCall()
          
    
