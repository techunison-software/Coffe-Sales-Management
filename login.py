import pandas as pd
import sqlalchemy as sql
import SQLAlchemyCon as conn

sql_engine=conn.getConnection()

class Login:    

    def initialCall(self):
        self.user_name=input("Enter User Name :")
        self.password=input("Enter password : ")
        self.authenticate()

    def authenticate(self):
        user=self.getUserDetails()   
        if self.user_name == user["user_name"][0] and self.password == user["password"][0]:
            print("Login success!")
            self.user=user            
            self.showMainMenu()
        else:
            print("\tLogin Failed!\n\tInvalid User name or password.")
            self.user=None
            self.initialCall()

    def getUserDetails(self):
        query = 'select u.user_id, u.user_name, u.name, u.email_id, u.password, u.department_id, d.department_name, u.role_id, rt.role, u.status_id, u.created_by, u.created_on, u.updated_by, u.updated_on from users u join role_type rt on rt.role_id=u.role_id join department d on d.department_id=u.department_id where u.user_name=''"'+self.user_name+'"'
        return pd.read_sql_query(query, sql_engine)        

    def showMainMenu(self):
        if str(self.user["role"][0]).casefold()==str("Admin").casefold():
            self.moduleValue(1,1,input("1. User Module \n2. Inventory \n3. Purchase Module \n4. Sales Module \nEnter the Value :"))            
        else:
            if str(self.user["department_name"][0]).casefold()==str("HR").casefold():
                #self.moduleValue(2,1,input("1. User Module\nEnter the Value :"))
                
            elif str(self.user["department_name"][0]).casefold()==str("Inventory").casefold():
                #self.moduleValue(2,2,input("1. Inventory Module\nEnter the Value :")) 
                InventoryModule(self.user)
            elif str(self.user["department_name"][0]).casefold()==str("Purchase").casefold():
                self.moduleValue(2,3,input("1. purhase Module \n2. Inventory Module  \nEnter the Value :"))         
            elif str(self.user["department_name"][0]).casefold()==str("Sales").casefold():
                self.moduleValue(2,4,input("1. Sales Module \n2. Inventory Module \nEnter the Value :"))         
            
    def moduleValue(self,method_id,dep_type,inp_value):
        if method_id==1:
            if inp_value==1
                UserModule(self.user)
            elif
                InventoryModule(self.user)

         print("cameeeee",method_id,dep_type,inp_value)

    def callUserModule():
        UserModule(self.user)
    
    def callInventoryModule():
        InventoryModule(self.user)
       


login_check = Login()        
login_check.initialCall()
          
    