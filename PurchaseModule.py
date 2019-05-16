import pandas as pd
import sqlalchemy as sql
import SQLAlchemyCon as conn


sql_engine=conn.getConnection()


while True:


    answer = input('Please Select One Of The Values 1. Vendor 2. Purchase or type Q to quit:')

    if answer in '':
        print('Please Enter a Value')
    elif answer in 'Q' and answer in 'q' :
        break
    
    elif answer in '1':
        print(answer, 'Vendor.')
        print('You Have chosen Vendor')
        
        query = 'SELECT Vendors_Id, Vendors_Name FROM vendors WHERE Is_Active=1'
        result=pd.read_sql_query(query, sql_engine) 
        print(result)
        response = input('Select any one of the operations to process Vendor a. Add Vendor b. Edit Vendor c. Delete Vendor :')

        if response in '':
            print('Input is blank. Please Select A Menu.')

        elif response in 'a':
            
            print(response,'-You Have Opted to Add a Vendor')
            VendorsName=input('Enter The Vendor Name : ')
            if VendorsName in '':
                print('The Vendor Name is blank. So enter a value.')
                
            elif VendorsName not in '':
                    VendorsPhone=input('Enter The Vendors contact :')
            if VendorsPhone in '':
                print('The Vendor Contact is Empty. So please Enter.')
            elif VendorsName not in '':
                VendorsAddress=input('Enter The Vendors Address :')
            if VendorsAddress in '':
                print ('The Vendor Address is Empty. So Please Enter.')    
            elif VendorsAddress not in '':
                VendorsMailId=input('Enter The Vendors Mail Id :')    
            if VendorsMailId in '':
                print('The Vendor Mail Id is Empty. So Please Enter it.')

            if VendorsName not in '' and VendorsPhone not in '' and VendorsAddress not in '' and VendorsMailId not in '':

                try:
                    sql = "INSERT INTO vendors(Vendors_Name,Vendors_Phone,Vendors_Address,Vendors_Mail_Id,Is_Active)VALUES(%s, %s,%s, %s,1)"
                    val = (VendorsName,VendorsPhone,VendorsAddress,VendorsMailId)
                    sql_engine.execute(sql, val)
                    print("Success. A record has been inserted.")
                except :
                     print("Failed inserting record into python_users table ")


        elif response in 'b':
            print(response,'-You Have Opted to UPDATE a Vendor')   
            VendorID=input('Enter The VendorId You Want To Update :')     
            try:
                val = str(VendorID)
                
                if( VendorID.isdigit()):
                    print("User input is Number ")
                

                VendorId_string=str(val)
                print("The Vendor Id is: ", val)

                query = 'SELECT * FROM vendors WHERE Vendors_Id =''"'+VendorId_string+'"'
                
                result=pd.read_sql_query(query, sql_engine) 
                print(result)

                VendorsName=input('Enter The Name of The Vendor You want to Edit :')
                if VendorsName in '':
                    print('The Vendor Name is blank. So enter a value.')

                elif VendorsName not in '':
                    VendorsAddress=input('Enter The Address of The vendor You Want To Edit :')

                if VendorsAddress in '':
                    print('The Vendor Address is blank. So enter a value.')
                
                elif VendorsAddress not in '':
                    VendorsPhone=input('Enter The Contact Of The Vendor that You want to Edit :')

                if VendorsPhone in '':
                    print('The Vendor Phone is blank. So Enter a Value')    

                elif VendorsPhone not in '':
                    VendorsMailId=input('Enter The MailId of The Contact That You want to Update :')

                    if VendorsName not in '' and VendorsPhone not in '' and VendorsAddress not in '' and VendorsMailId not in '':

                        try:
                            Vendor_Update_Query= 'UPDATE vendors SET Vendors_Name = %s, Vendors_Phone=%s, Vendors_Address=%s,Vendors_Mail_Id=%s WHERE Vendors_Id = ''"'+VendorId_string+'"'
                            values = (VendorsName,VendorsPhone,VendorsAddress,VendorsMailId)
                            sql_engine.execute(Vendor_Update_Query, values)

                            print("Success. A record has been updated.")
                        except :
                            print("Failed Updating record into Vendors table ")

                else:
                    print("User input is string ")    

            except:
                print('Please Check...')            


        elif response in 'c':
            print('You Have Selected to delete a Vendor -',response)
            VendorsActive=2
            VendorID=input('Enter The VendorId You Want To DELETE :')     
            try:
                val = str(VendorID)
                if( VendorID.isdigit()):
                    print("User input is Number ")
                    Vendor_Delete_Query= 'UPDATE vendors SET Is_Active = %s WHERE Vendors_Id = ''"'+VendorID+'"'
                    values = (VendorsActive)
                    sql_engine.execute(Vendor_Delete_Query, values)
                    print("Success. A record has been deleted.")
                else:    
                    print("User input is string ")
                
            except :
                        print("Failed Deleting record into Vendors table ")

                   



        elif response in 'Q':
            print('Goodbye.')
            break   


        elif response in 'q':
            print('Goodbye.')
            break 
                            

              
            # except ValueError:
            #         print("That's not a valid input! Please Enter a Valid Input.")
                            

        else:
            print('Enter An Appropriate Value From The Menu')
            exit
                
                
                
# if answer in '2':
#         print(answer,'Purchases.')
#         print('You Have chosen Purchases')
#         response = input('Select any one of the operations to process Purchase x. Add Purchase y. Edit Purchase z. Delete Purchase :')
#         print('You have chosen', response)

# if answer in 'Q':
#     print('ABC')
#     exit         
    
        
# if answer in 'q':
#     print('XYZ')
             
    
    
      
    
    
# else:
#           print('Enter An Appropriate Value From The Menu')


