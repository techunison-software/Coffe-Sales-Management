import pandas as pd
import sqlalchemy as sql
import SQLAlchemyCon as conn
from tabulate import tabulate
from passlib.hash import sha256_crypt

import UserModule as userMod
import PurchaseModule as purchaseMod
import SalesModule as salesMod
import InventoryModule as inventoryMod
import report 

sql_engine=conn.getConnection()

class LoginInitial:

    def initialCall(self):
        self.user_name=input("=======================================================\nEnter User Name :")
        self.password=input("Enter password  :")
        self.authenticate()

    def authenticate(self):
        user=self.getUserDetails()
        if not user.empty:
            if self.user_name == user["user_name"][0] and sha256_crypt.verify(self.password , user["password"][0]):
                print("\n\tSuccessfully LogedIn!")
                Login().initialCall(user)
            else:
                print("\n\tLogin Failed!\n\tInvalid User name or password.")
                user=None
                self.initialCall()
        else:
            print("\n\tLogin Failed!\n\tUser Does not Exist.Please enter a valid user.")
            self.initialCall()

    def getUserDetails(self):
        result=None
        try:
            #connection = conn.getConnection()
            query = 'select u.user_id, u.user_name, u.name, u.email_id, u.password, u.department_id, d.department_name, u.role_id, rt.role, u.status_id, u.created_by, u.created_on, u.updated_by, u.updated_on from users u join role_type rt on rt.role_id=u.role_id join department d on d.department_id=u.department_id where u.status_id=1 and u.user_name=''"'+self.user_name+'"'
            result=pd.read_sql_query(query, sql_engine) 
        except Exception as e:
            print('\n\tAn error occured.',e)
        finally:
            sql_engine.dispose()      
        return result  


class Login:         
    def initialCall(self,user):
        self.user=user
        self.showMainMenu()

    def showMainMenu(self):
        print("=======================================================")
        if str(self.user["role"][0]).casefold()==str("Admin").casefold():
            print(tabulate([["1", "User"],["2","Inventory"],["3","Purchase"],["4","Sales"],["5","Reports"],["6","Logout"]], headers=['Id', 'Menu']))    
            val=input("=======================================================\nEnter the Value :")
            self.moduleValue(val)            
        else:
            if str(self.user["department_name"][0]).casefold()==str("HR").casefold():
                self.callUserModule()                
            elif str(self.user["department_name"][0]).casefold()==str("Inventory").casefold():
                self.callInventoryModule()
            elif str(self.user["department_name"][0]).casefold()==str("Purchase").casefold():                                                                                                                
                print(tabulate([["1", "Purchase"],["2","Inventory"],["3","User"],["4","Report"],["5","Logout"]], headers=['Id', 'Menu'])) if str(self.user["role"][0]).casefold()==str("manager").casefold() else print(tabulate([["1", "Purchase"],["2","Inventory"],["3","Report"],["4","Logout"]], headers=['Id', 'Menu']))
                user_input=self.checkIntValue(input("=======================================================\n\nEnter the Value :"))
                if user_input ==1:
                    self.callPurchaseModule()
                elif user_input ==2 :
                    self.callInventoryModule()
                elif (user_input ==3 and str(self.user["role"][0]).casefold()==str("associate").casefold()) or ((user_input ==4 and str(self.user["role"][0]).casefold()==str("manager").casefold())):
                    self.callReportModule()
                elif (user_input ==4 and str(self.user["role"][0]).casefold()==str("associate").casefold()) or ((user_input ==5 and str(self.user["role"][0]).casefold()==str("manager").casefold())):
                    self.logout()
                elif user_input ==3 and str(self.user["role"][0]).casefold()==str("manager").casefold():
                    self.callUserModule()
                else :
                    print("\n\tPlease enter a valid input!")
                    self.showMainMenu()
            elif str(self.user["department_name"][0]).casefold()==str("Sales").casefold():
                user_input = self.checkIntValue(input("\n\t1. Sales Module \n\t2. Inventory Module \n\t3. Logout \nEnter the Value :"))                 
                if user_input==1:
                    self.callPurchaseModule()
                elif user_input==2 :
                    self.callInventoryModule()
                elif user_input ==3 :
                    self.logout()
                else:
                    print("\n\tPlease enter a valid input!")
                    self.showMainMenu()
            else:
                print("error")

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
        elif inp_value==5:
            self.callReportModule()
        elif inp_value==6:
            self.logout()
        else:
            print("\n\tPlease enter a valid input!")
            self.showMainMenu()
    
    def logout(self):
        self.user=None
        print("\n\tLogged Out Successfully!")
        sql_engine.dispose()
        LoginInitial().initialCall()

    def checkIntValue(self,user_input):
        try:
            val = int(user_input)
            return val
        except ValueError:
            print("\n\tInput value is not an Integer. Please enter Integer value alone!")
            self.showMainMenu()  

    def callReportModule(self):
        try:
            rp_mod=report.Report()
            rp_mod.initCall(self.user)
        except :
            print("\tNo file named Report Module is found!\n",e)
            self.showMainMenu()

    def callUserModule(self):       
        try:
            us_mod=userMod.UserModule()
            us_mod.initCall(self.user)
        except :
            print("\tNo file named UserModule is found!\n",e)
            self.showMainMenu()

    def callInventoryModule(self):
        try:
            inv_mod=inventoryMod.InventoryModule()
            inv_mod.initCall(self.user)
        except Exception as e:
            print("\n\tNo file named InventoryModule is found!",e)
            self.showMainMenu()
            
    def callPurchaseModule(self):
        try:
            pur_mod=purchaseMod.PurchaseModule()
            pur_mod.initCall(self.user)
        except Exception as e:
            print("\n\tNo file named PurchaseModule is found!",e)
            self.showMainMenu()
            
    def callSalesModule(self):
        try:
            sales_mod=salesMod.SalesModule()
            sales_mod.initCall(self.user)
        except Exception as e:
            print("\n\tNo file named SalesModule is found!",e)
            self.showMainMenu()
            
          
    
