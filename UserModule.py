import pandas as pd
import Login as login
import SQLAlchemyCon as conn

sql_engine=conn.getConnection()
class UserModule:
    
    def initCall(self,user):
        self.user=user
        if not self.user.empty :
            self.menuList()
        else:
            print("\n\tSession Invalid Login Again.") 
            self.sesInvalid()

    def menuList(self):
        if str(self.user["role"][0]).casefold()==str("Admin").casefold() or str(self.user["department_name"][0]).casefold()==str("HR").casefold():
            self.menuValue(self.checkIntValue(input("\n\t1. User List View \n\t2. Create User \n\t3. Edit User \n\t4. Delete User \n\t5. Back to main Menu \n\nEnter the Value :")))
        elif str(self.user["role"][0]).casefold()==str("Manager").casefold() :
            x=self.checkIntValue(input("\n\t1. User List View\n\t2. Back to main Menu \n\nEnter the Value :"))
            if x==1:
                self.userListView(2)
            elif x==2:
                self.backMainMenu()  
            else:
                print("\n\tPlease enter a valid input!")
                self.menuList()
        else:
            print("\nUnauthorized Entry!")
            self.sesInvalid()
    
    def menuValue(self,inp_value): 
        if inp_value == 1:
            self.userListView(1)
        elif inp_value==2:
            self.createUser()
        elif inp_value==3:
            self.editUser()
        elif inp_value==4:
            self.deleteUser()
        elif inp_value==5:
            self.backMainMenu()
        else:
            print("\n\tPlease enter a valid input!")
            self.menuList()

    def userListView(self,methodId):
        query=None
        try:
            if methodId==1:
                query = 'select u.user_id as UserId, u.name as Name, u.user_name as UserName ,u.email_id as Email,d.department_name as Department, rt.role as Role, u.status_id as StatusId, u.created_on as CreatedOn from users u join role_type rt on rt.role_id=u.role_id join department d on d.department_id=u.department_id where u.status_id=1 '
            else :
                query = 'select u.user_id as UserId, u.name as Name, u.user_name as UserName ,u.email_id as Email,d.department_name as Department, rt.role as Role, u.status_id as StatusId, u.created_on as CreatedOn from users u join role_type rt on rt.role_id=u.role_id join department d on d.department_id=u.department_id where u.status_id=1 and u.department_id='+str(self.user["department_id"][0])
            result=pd.read_sql_query(query, sql_engine) 
            print("\nLIST OF USER :\n",result)
        except Exception as e:
            print('\n\tError : In getting User List View.',e)
        finally :
            self.menuList()
    def checkIntValue(self,user_input):
        try:
            val = int(user_input)
            return val
        except ValueError:
            print("\n\tInput value is not an Integer. Please enter Integer value alone!")
            self.menuList() 

    def backMainMenu(self):
        log=login.Login()
        log.initialCall(self.user)

    def sesInvalid(self):
        log=login.LoginInitial()
        log.initialCall()
