import pandas as pd
import sqlalchemy as sql
import SQLAlchemyCon as conn


sql_engine=conn.getConnection()

class PurchaseModule:

    
        # while True:

            # Statement()


            def ShowVendor(self):
                query = 'SELECT Vendors_Id, Vendors_Name FROM vendors WHERE Is_Active=1'
                result=pd.read_sql_query(query, sql_engine) 
                print(result)
                return result

            def AddVendor(self):
                Msg="Success. A record has been inserted."
                print('You Have Opted to Add a Vendor')
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

                    return Msg     


            def UpdateVendor(self):
                Message="Success. A record has been updated."
                i=1
                while i==1:
                    
                    VendorID=input('Enter The VendorId You Want To Update :')
                    try:
                        val = str(VendorID)
                        if( VendorID.isdigit()):
                            print("User input is Number ")
                                                
                        VendorId_string=str(val)
                        print("The Vendor Id is: ", val)
                        query = 'SELECT * FROM vendors WHERE Is_Active=1 AND Vendors_Id =''"'+VendorId_string+'"'
                        result=pd.read_sql_query(query, sql_engine) 
                        print(result)

                        

                        df = pd.DataFrame(result, columns = ['Vendors_Id'])
                        print(df['Vendors_Id'])
                        POVendorsId=int(df['Vendors_Id'][0])
                        
                        Vendor=int(VendorID)
                        
                        if Vendor == POVendorsId:
                            i=2
                            while i==2:
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

                                    except:
                                        print('Failed Updating record into Vendors table...')
                        else:
                            print('Id does not exist. So Please Enter Correct ID.')                                               
                            i==2
                        

                    except :
                        print('The entered ID is not active. So enter an Active ID from the list.')
                        i==1

                return Message  


            def DeleteVendor(self):
                DelMsg="Success. A record has been deleted."
                VendorsActive=2
                VendorID=input('Enter The VendorId You Want To DELETE :')     
                try:
                    #val = str(VendorID)
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
                    return DelMsg      


            def ShowPurchaseList(self):
                Po_Requestquery = 'SELECT po_request_id, inv_item_id,po_request_quantity,Po_request_Status FROM po_request WHERE Po_request_Status=4'
                result=pd.read_sql_query(Po_Requestquery, sql_engine) 
                print(result)
                return result


            def CreatePurchaseList(self,Vendors_Id):
                try:
                    Vendor_val = int(Vendors_Id)
                    print("Input number value is: ", Vendor_val)
                    VendorId_Check='SELECT po_request_id FROM po_request WHERE po_request_id=''"'+str(Vendor_val)+'"'
                    result=pd.read_sql_query(VendorId_Check, sql_engine) 
                    print(VendorId_Check)

                    df = pd.DataFrame(result, columns = ['po_request_id'])
                    print(df['po_request_id'])
                    PORequestId=int(df['po_request_id'])

                    if Vendor_val == PORequestId:
                        print('The Request Id Is Present In The Purchase Request. So continue.')
                        totalamount=input('Enter The Total amount of The Purchase :')
                        Totalamt=totalamount
                        paymentId=input('Enter The Payment Id Of the Purchase :')
                        Payment=paymentId

                        RequestDetails_Query='SELECT po_request_id,inv_item_id,po_request_quantity FROM po_request WHERE po_request_id=''"'+str(Vendor_val)+'"'
                        Requestresult=pd.read_sql_query(RequestDetails_Query, sql_engine) 
                        print(Requestresult)

                        df=pd.DataFrame(Requestresult,columns=['po_request_id'])
                        po_request_id=df['po_request_id']
                        print(po_request_id)

                        df=pd.DataFrame(Requestresult,columns=['inv_item_id'])
                        inv_item_id=(df['inv_item_id'][0])
                        print(df['inv_item_id'])

                        df=pd.DataFrame(Requestresult,columns=['po_request_quantity'])
                        po_request_quantity=(df['po_request_quantity'][0]) 
                        print(df['po_request_quantity'])    

                        print('Check->',df['po_request_quantity'])                                                    
                        vendorsitemid_Query='SELECT Vendors_item_id FROM vendors_item WHERE inv_item_id='+str(inv_item_id)           #and vendors_id=''"'+str(Vendor_val)+'"'
                        print(vendorsitemid_Query)
                        getvendorsitemid=pd.read_sql_query(vendorsitemid_Query,sql_engine)
                            

                        df=pd.DataFrame(getvendorsitemid,columns=['Vendors_item_id'])
                        Vendors_item_id=(df['Vendors_item_id'][0])
                            
                            
                        Inv_Quantity_Query='SELECT item_quantity FROM inv_item WHERE inv_item_id='+str(inv_item_id)
                        results=pd.read_sql_query(Inv_Quantity_Query,sql_engine)
                        df=pd.DataFrame(results,columns=['item_quantity'])
                        itemquantity=(df['item_quantity'][0])
                           
                        ActualQuantity=po_request_quantity+itemquantity
                        Currentdate=pd.to_datetime('now')
                        
                        try:                                
                            Po_Request_Insert="INSERT INTO po_purchase(created_by,updated_by,order_no,total_amount,Payment_type_id,created_on,updated_on,po_request_id,vendors_item_id)VALUES(1, NULL,NULL, %s,%s, %s,%s,%s,%s)"
                            vals = (Totalamt,Payment,Currentdate,Currentdate,PORequestId,Vendors_item_id)   
                            sql_engine.execute(Po_Request_Insert, vals)
                            print(Po_Request_Insert)                                   
                            print("Success. A record has been inserted.")

                        except:
                            print(Po_Request_Insert)                                
                            print('Insert went wrong in Purchase Department! Please Check')

                            try:
                                UpdateQty_Query='UPDATE inv_item SET item_quantity=%s WHERE inv_item_id=''"'+str(inv_item_id)+'"'
                                values = (ActualQuantity)
                                print(UpdateQty_Query)
                                sql_engine.execute(UpdateQty_Query,values)
                                print("Success. Quantity has been updated.")

                        
                            except:
                                print("Error while updating Inventory.")


                                try:
                                    requestStatus='Update po_request SET Po_Request_Status=5 WHERE inv_item_id=''"'+str(inv_item_id)+'"'
                                    sql_engine.execute(requestStatus)
                                    print('purchase Request Status Has been Updated...')

                                except:
                                    print('Error while updating the status...')    
                            #i=0 
                    else:
                        print('Enter The Correct Purchase Request From The Above List.')
                            

                except ValueError:
                    print("That's not an int! So Enter an int value.")
                    return


            def EditPurchase(self):
                i = 3
                while i == 3:
                    Vendors_Id=input('Enter The Purchase ID You Want To Edit : ')
                    
                    if Vendors_Id in '':
                        print('The Purchase ID is blank. So enter a value.')
                        i=3

                    elif Vendors_Id not in '' and Vendors_Id.isdigit():
                        try:
                            h=1
                            while h==1:
                                Vendor_val = int(Vendors_Id)                        
                                print("Input number value is: ", Vendor_val)

                                PurchaseId_Check='SELECT * FROM Po_Purchase WHERE po_purchase_Id=''"'+str(Vendor_val)+'"'
                                PurchaseId_result=pd.read_sql_query(PurchaseId_Check, sql_engine) 
                                print(PurchaseId_result)
                                df = pd.DataFrame(PurchaseId_result, columns = ['po_purchase_Id','po_request_id'])
                                POPurchaseId=int(df['po_purchase_Id'][0])                                
                                print('RequestID')
                                RequestID=int(df['po_request_id'])
                                print('RequestID',RequestID)

                                                                
                                if Vendor_val == POPurchaseId:
                                    print('The Purchase Request Id Is Present In The Purchase Request. So continue.')

                                    #invItemID='SELECT inv_item_id FROM po_request WHERE po_request_id=''"'+str(RequestID)+'"'

                                    PurchaseTotalAmount=input('Enter The Total Amount :')
                                    
                                    if PurchaseTotalAmount in '' :
                                        e=1
                                        while e==1:
                                            print('Total Amount is blank...')
                                            e=1
                                        
                                    elif PurchaseTotalAmount not in '' and PurchaseTotalAmount.isdigit():
                                        PurchasePayment=input('Enter The Payment Id :')
                                        if PurchasePayment in '':
                                            s=1
                                            while s==1:
                                                print('Enter the payment as it is blank...')
                                                s=1

                                        elif PurchasePayment not in '' and PurchasePayment.isdigit():
                                            PurchaseItemMrpPrice=input('Enter The MRP Price :')
                                            if PurchaseItemMrpPrice in '':
                                                print('MRP Price is blank.')

                                            elif PurchaseItemMrpPrice not in '' and PurchaseItemMrpPrice.isdigit():
                                                PurchaseItemQuantity=input('Enter The Quantity :')            
                                                if PurchaseItemQuantity in '':
                                                    print('Item Quantity is blank...')

                                                elif PurchaseItemQuantity not in '' and PurchaseItemQuantity.isdigit():
                                                    PurchaseMaxDiscount=input('Enter The Max Discount :')
                                                    if PurchaseMaxDiscount is '':
                                                        print('Max Discount is empty :')

                                                    elif PurchaseMaxDiscount not in '' and PurchaseMaxDiscount.isdigit():
                                                        PurchaseWeight=input('Enter the Weight :')
                                                        if PurchaseWeight is '':
                                                            print('Weight is blank...')

                                                        elif PurchaseWeight not in '' and PurchaseWeight.isdigit():
                                                            try:
                                                                print('a',PurchaseTotalAmount)
                                                                print('b',PurchasePayment)
                                                                Purchase_Update_Query= 'UPDATE Po_Purchase SET total_amount = %s, Payment_type_id=%s WHERE po_purchase_id = ''"'+str(POPurchaseId)+'"'
                                                                values = (PurchaseTotalAmount,PurchasePayment)
                                                                sql_engine.execute(Purchase_Update_Query, values)
                                                                print("Success. Purchase has been updated.")
                                                            except:
                                                                print('Failed Updating record into Purchase table...') 
                                                                                                                                           

                                                            try:
                                                                print('c',PurchaseItemMrpPrice)
                                                                print('d',PurchaseItemQuantity)
                                                                print('e',PurchaseMaxDiscount)
                                                                print('f',PurchaseWeight)
                                                                inv_Update_Query='Update inv_item SET item_mrp_price=%s,item_quantity=%s,item_max_discount=%s,weight=%s WHERE inv_item_id=''"'+str(RequestID)+'"'
                                                                values=(PurchaseItemMrpPrice,PurchaseItemQuantity,PurchaseMaxDiscount,PurchaseWeight)
                                                                sql_engine.execute(inv_Update_Query,values)
                                                                print("Success. Inventory has been updated.")

                                                            except:
                                                                print('Failed to update Inventory Table...!')



                                else:
                                    print('Enter The Correct Purchase Request From The Above List.')
                                    h=1                   

                        except:
                            print('Check')        
                            i = 3
                            return


                                                       
                    
            """def DeletePurchase(self):
                Vendors_Id=input('Enter The Purchase ID You Want To Edit : ')
                if Vendors_Id in '':
                    print('The Purchase ID is blank. So enter a value.')
                    i=3
                elif Vendors_Id not in '' and Vendors_Id.isdigit():
                    try:
                        h=1
                        while h==1:
                            Vendor_val = int(Vendors_Id)                        
                            print("Input number value is: ", Vendor_val)
                            PurchaseId_Check='SELECT * FROM Po_Purchase WHERE po_purchase_Id=''"'+str(Vendor_val)+'"'
                            PurchaseId_result=pd.read_sql_query(PurchaseId_Check, sql_engine) 
                            print(PurchaseId_result)
                            df = pd.DataFrame(PurchaseId_result, columns = ['po_purchase_Id','po_request_id'])
                            POPurchaseId=int(df['po_purchase_Id'][0])                                
                            print('RequestID')
                            RequestID=int(df['po_request_id'])
                            print('RequestID',RequestID)
                            if Vendor_val == POPurchaseId:
                                print('The Purchase Request Id Is Present In The Purchase Request. So continue.')
                                return"""


            def initCall(self,user):
                self.user=user
                self.Statement()

            def Statement(self):
                print("Statement")
                try:
                    i=0
                    while i==0:
                        answer = input('Please Select One Of The Values 1. Vendor 2. Purchase or type Q to quit:')
                        if answer in '':
                            print('Please Enter a Value')
                            i=0
                        elif answer in 'Q' and answer in 'q' :
                            exit     

                        elif answer in '1':
                            print(answer, 'Vendor.')
                            print('You Have chosen Vendor')
                            PurchaseModule().ShowVendor()

                            response = input('Select any one of the operations to process Vendor a. Add Vendor b. Edit Vendor c. Delete Vendor :')

                            if response in '':
                                print('Input is blank. Please Select A Menu.')
                                i=0

                            elif response in 'a':
                                PurchaseModule().AddVendor()

                            elif response in 'b':
                                print('You Have Opted to UPDATE a Vendor')   
                                PurchaseModule().UpdateVendor()                         


                            elif response in 'c':
                                print('You Have Selected to delete a Vendor -',response)
                                PurchaseModule().DeleteVendor()
                
                            elif response in 'Q':
                                print('Goodbye.')
                                exit   


                            elif response in 'q':
                                print('Goodbye.')
                                exit 
            

                        else:
                            print('Enter An Appropriate Value From The Menu')
                            i=0
                            #exit
                
                
                        if answer in '2':
                            a = 4
                            while a == 4:
                                print(answer,'Purchases.')
                                print('You Have chosen Purchases')
                                print('Below Is The List Of Purchase Request')
                                PurchaseModule().ShowPurchaseList()
                                response = input('Select any one of the operations to process Purchase x. Add Purchase y. Edit Purchase z. Delete Purchase :')
                                print('You have chosen : ', response)                       
                                if response in '':
                                    print('User has not entered any Input. Please Choose A Menu.')
                                elif response in 'x':
                                    i=6
                                    while i==6:
                                        print(response,'-You Have Opted to Create a Purchase')
                                        Vendors_Id=input('Enter The Purchase Request ID You Want To Manipulate : ')
                                        if Vendors_Id in '':
                                            print('The Vendor ID is blank. So enter a value.')
                                            i=6

                                        elif Vendors_Id not in '':
                                            PurchaseModule().CreatePurchaseList(Vendors_Id)

                                elif response in 'y':
                                    print('You Have Selected To Edit A Purchase ')

                                    PurchaseModule().EditPurchase()


                                elif response in'c':
                                    print('You Have Selected To Delete A Purchase ')    
                                    PurchaseModule.DeletePurchase()


                        else:
                            print('Enter appropriate input')
                            a=4


                except:
                    print('Something went wrong in Initial call..!')           

                    if answer in 'Q' or answer in 'q':
                        print('Exiting...')
                        exit
    
              
