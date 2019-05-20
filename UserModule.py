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

    def createUser(self):
        print("\n\tNew User Creation")
        newUser={}
        newUser["name"]=self.sanitised_input("\nEnter the Name  : ", str,len_=(3,100))
        newUser["email"]=self.checkEmailValid()     
        newUser["user_name"]=self.checkUserNameValid()
        newUser["password"]=self.sanitised_input("Enter Password  : ", str,len_=(6,50))
        print("\nLIST OF DEPARTMENT :\n",self.getDepartmrnt())
        newUser["department"]=self.sanitised_input("\nEnter  Department Id : ", int, 1, 4)
        print("\nLIST OF ROLE :\n",self.getRole())
        newUser["role"]=self.sanitised_input("\nEnter Role Id : ", int, 2, 3)        
        self.insertUser(newUser)

    def insertUser(self,newUser):
        try:                                                       #created on -pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")
            query = 'insert into users (name, email_id,user_name, password, department_id, role_id, status_id, created_by,created_on) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'             
            insert_tuple = (newUser["name"], newUser["email"], newUser["user_name"], newUser["password"],newUser["department"],newUser["role"],int(1),self.user["user_id"][0],pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
            with sql_engine.begin() as conn:
                df=conn.execute(query,insert_tuple)
            print("\nUser Created Successfully!")
        except Exception as e:
            print("Error in Inserting New User!",e)
        finally:            
            self.menuList()

    def editUser(self):
        while True:
            user=self.getEditUser(self.sanitised_input("\nEnter user Id to Edit : ", int)) 
            print(user)
            if not user.empty:
                break
            else :
                print("Invalid user Id! enter a valid ID")                
        self.getEditInput(user)
    
    def getEditInput(self,user):
        print("Enter the Value to Edit or Press Enter To skip.")
        newUser={}
        n_name=self.sanitised_input('\nName [''"'+user["name"][0]+'"''] -> ', str,len_=(3,100),type_id=2)
        newUser["name"]=n_name if n_name!="" else user["name"][0]
        n_email=self.checkEmailValid(type_id=2,email=user["email_id"][0])  
        newUser["email"]= n_email  if n_email!="" else user["email_id"][0]
        n_userName=self.checkUserNameValid(type_id=2,user_name=user["user_name"][0])
        newUser["user_name"]=n_userName if n_userName!="" else user["user_name"][0]
        print("\nLIST OF DEPARTMENT :\n",self.getDepartmrnt())
        n_dep=self.sanitised_input('\nDepartment Id ['+str(user["department_id"][0])+'] -> ', int, 1, 4)
        newUser["department"]=n_dep if n_dep!="" else user["department_id"][0]
        print("\nLIST OF ROLE :\n",self.getRole())
        n_role=self.sanitised_input('\nRole Id ['+str(user["role_id"][0])+'] -> ', int, 2, 3) 
        newUser["role"]=n_role if n_role!="" else user["role_id"][0]
        self.updateOrdeleteUser(newUser,status_id=1,user_id=user["user_id"][0])

    def updateOrdeleteUser(self,newUser,status_id=1,user_id=None):
        try:                                                     #created on -pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")
            query = 'update users set name=''"'+newUser["name"]+'"'', email_id=''"'+newUser["email"]+'"'',user_name=''"'+newUser["user_name"]+'"'', department_id='+str(newUser["department"])+', role_id='+str(newUser["role"])+', status_id='+str(status_id)+', updated_by='+str(self.user["user_id"][0])+',updated_on=''"'+pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")+'"'' where user_id='+str(user_id)
            with sql_engine.begin() as conn:
                df=conn.execute(query)
            print("\nUser Updated Successfully!")
        except Exception as e:
            print("Error in Updating User!",e)
        finally:            
            self.menuList()

    def checkUserNameValid(self,type_id=1,user_name=None):
        while True:
            prompt="User Name : " if type_id==1 else 'User Name [''"'+user_name+'"''] -> '
            inp=self.sanitised_input(prompt, str,len_=(3,100),type_id=type_id)
            if self.checkUserExist(inp,"user_name")==True:
                break
            else :
                print("\n\tUser Name Already Exist!")
        return inp

    def checkEmailValid(self,type_id=1,email=None):
        while True:
            prompt="Enter Email     : " if type_id==1 else 'Email [''"'+email+'"''] -> '
            inp=self.sanitised_input(prompt, str,len_=(3,100),type_id=type_id) 
            if self.checkUserExist(inp,"email_id")==True:
                break
            else :
                print("\n\tEmail Already Exists!")
        return inp

    def checkUserExist(self,inpName,colName):    
        result=None 
        ret=True   
        try:
            if not inpName :
                query = 'select * from users where '+colName+'=''"'+inpName+'"'
                result=pd.read_sql_query(query, sql_engine) 
                ret=False if not result.empty else True
        except Exception as e:
            print("\nError in checking user exist !",e)
        return ret

    def getEditUser(self,userId):
        result=None    
        try:
            query = 'select * from users where user_id='+str(userId)
            result=pd.read_sql_query(query, sql_engine)            
        except Exception as e:
            print("\nError in getting user details for Edit!",e)
        return result

    def getRole(self):
        result=None
        try:
            query = 'select role_id as RoleID ,role as Role from role_type where type_id=1'
            result=pd.read_sql_query(query, sql_engine) 
        except Exception as e:
            print('\n\tError : In getting Role List.',e)
        return result

    def getDepartmrnt(self):
        result=None
        try:
            query = 'select department_id as DepartmentID ,department_name as DepartmentName from department'
            result=pd.read_sql_query(query, sql_engine) 
        except Exception as e:
            print('\n\tError : In getting Department List.',e)
        return result

    def sanitised_input(self,prompt, type_=None, min_=None, max_=None,len_=None,type_id=1):
        if min_ is not None and max_ is not None and max_ < min_:
            raise ValueError("\n\tmin_ value must be less than or equal to max_ value.")
        while True:
            ui = input(prompt)
            if type_ is not None and (type_id ==2 and ui.strip() != "") :
                try:
                    ui = type_(ui)
                except ValueError:
                    print("\n\tInput type must be {0}.".format(type_.__name__))
                    continue
            if max_ is not None and (type_id ==2 and ui.strip() != ""):
                if ui > max_ :
                    print("\n\tInput must be less than or equal to {0}.".format(max_))
            elif min_ is not None and (type_id ==2 and ui.strip() != ""):
                if ui < min_ :
                    print("\n\tInput must be greater than or equal to {0}.".format(min_))
            elif len_ is not None and (type_id ==2 and ui.strip() != ""):
                length=len(ui)
                if length in range(len_[0],len_[1]+1) :
                    break
                else:
                    print("\n\tPlease Enter a input of length minimum of ",len_[0], "and maximum of ",len_[1]," charcters.")
                    #continue
            else:
                break
        return ui

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


