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
        try:
            a=1
            while a==1:
                VendorsName=input('Enter The Vendor Name : ')
                if VendorsName in '':
                    print('The Vendor Name is blank. So enter a value.')
                    a=1
                    
                elif VendorsName not in '':
                    b=1
                    while b==1:
                        VendorsPhone=input('Enter The Vendors contact :')
                        

                        if VendorsPhone in '' :
                           print('The Vendor Contact is Empty. So please Enter.')
                           b=1
                                
                        elif VendorsPhone not in '' and VendorsPhone.isdigit():
                            d=1
                            while d==1:
                                VendorsAddress=input('Enter The Vendors Address :')
                                
                                if VendorsAddress in '':
                                    print ('The Vendor Address is Empty. So Please Enter.')                    
                                    d=1                        

                                elif VendorsAddress not in '':
                                    f=1
                                    while f==1:
                                        VendorsMailId=input('Enter The Vendors Mail Id :')  
                                                                            
                                        if VendorsMailId in '' :                                            
                                            print('The Vendor Mail Id is Empty. So Please Enter it.')            
                                            f=1
                                                                                    
                                        elif VendorsMailId not in '':
                                            #if VendorsName not in '' and VendorsPhone not in '' and VendorsAddress not in '' and VendorsMailId not in '':
                                            try:
                                                sql = "INSERT INTO vendors(Vendors_Name,Vendors_Phone,Vendors_Address,Vendors_Mail_Id,Is_Active)VALUES(%s, %s,%s, %s,1)"
                                                val = (VendorsName,VendorsPhone,VendorsAddress,VendorsMailId)
                                                sql_engine.execute(sql, val)
                                                print("Success. A record has been inserted.")
                                                PurchaseModule().Statement()
                                            except :
                                                print("Failed inserting record into python_users table ")

                                        else :
                                            print('')

                                else:
                                    print('')

        except:
            print('Inputs must not be blank...')
            a=1
            return Msg     


    def UpdateVendor(self):
        Message="Success. A record has been updated."
        try:
            i=1
            while i==1:
                VendorID=input('Enter The VendorId You Want To Update :')
                val = str(VendorID)
                if VendorID is '':
                    print('Id does not exist. So Please Enter Correct ID.')
                    i=1 
                elif (VendorID.isdigit()):
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
                        i=1
                        while i==1:
                            VendorsName=input('Enter The Name of The Vendor You want to Edit :')
                            if VendorsName in '':
                                print('The Vendor Name is blank. So enter a value.')
                                i=1
                            elif VendorsName not in '':
                                a=1
                                while a==1:
                                    VendorsAddress=input('Enter The Address of The vendor You Want To Edit :')

                                    if VendorsAddress in '':
                                        print('The Vendor Address is blank. So enter a value.')
                                        a=1

                                    elif VendorsAddress not in '':
                                        b=1
                                        while b==1:
                                            VendorsPhone=input('Enter The Contact Of The Vendor that You want to Edit :')
                                                                                    
                                            if VendorsPhone in '':
                                                print('The Vendor Phone is blank. So Enter a Value')    
                                                b=1

                                            elif VendorsPhone not in '' and VendorsPhone.isdigit():
                                                VendorsMailId=input('Enter The MailId of The Contact That You want to Update :')
                                                if VendorsName not in '' and VendorsPhone not in '' and VendorsAddress not in '' and VendorsMailId not in '':
                                                    try:
                                                        Vendor_Update_Query= 'UPDATE vendors SET Vendors_Name = %s, Vendors_Phone=%s, Vendors_Address=%s,Vendors_Mail_Id=%s WHERE Vendors_Id = ''"'+VendorId_string+'"'
                                                        values = (VendorsName,VendorsPhone,VendorsAddress,VendorsMailId)
                                                        sql_engine.execute(Vendor_Update_Query, values)
                                                        print("Success. A record has been updated.")
                                                        PurchaseModule().Statement()
                                                    except:
                                                        print('Failed Updating record into Vendors table...')
                                                else:
                                                    print('')

                                    else:
                                        print('Invalid Mail Input...')
                                        b=1
                    else:
                        print('Application Cannot Proceed further...')
                else:
                    print('Id is a Number... So Please Enter Correct ID...')                                               
                    i==1
                        

        except :
            print('The entered ID is not active. So enter an Active ID from the list.')
            i==1
            return Message  


    def DeleteVendor(self):
        DelMsg="Success. A record has been deleted."
        VendorsActive=2
        i=1
        while i==1:
            try:
                a=1
                while a==1:
                    VendorID=input('Enter The VendorId You Want To DELETE :')
                                    
                    if VendorID is '':
                        print('Vendor ID cannot be empty...')
                        a=1
                        
                    elif VendorID not in '' and VendorID.isdigit():
                        CheckVendorExists='SELECT Vendors_Id FROM vendors WHERE Is_Active =1 and Vendors_Id=''"'+str(VendorID)+'"'
                        result=pd.read_sql_query(CheckVendorExists, sql_engine)
                        print(result)
                        #df = pd.DataFrame(result, columns = ['Vendors_Id'])

                        #POVendorsId=int(df['Vendors_Id'][0])
                        
                        #if len(df.index) =='[]':
                            #print('No such ID exists...')
                            #i=1
                        
                        #elif len(df.index)!='[]':
                            #PORequestId=int(df['Vendors_Id'])
                            
                        try:
                            if( VendorID.isdigit()):                                    
                                print("User input is Number ")
                                Vendor_Delete_Query= 'UPDATE vendors SET Is_Active = %s WHERE Vendors_Id = ''"'+str(VendorID)+'"'
                                values = (VendorsActive)
                                sql_engine.execute(Vendor_Delete_Query, values)
                                print("Success. A record has been deleted.")
                                PurchaseModule().Statement()
                            else: 
                                print("User input is string ")
                                #s=1
                                
                        except :
                            print("Failed Deleting record into Vendors table... Check Your Input... ") 

                    else:
                        print('Enter Valid Input...')
                        a=1
                      
            except:
                print('Enter Proper ID which is in the database...')                   
                i=1
                return DelMsg


    def ShowPurchaseList(self):
        try:
            Po_Requestquery = 'SELECT po_request_id, inv_item_id,po_request_quantity,status_id FROM po_request WHERE status_id=4'
            result=pd.read_sql_query(Po_Requestquery, sql_engine) 
            print('There are no requests to be found...')
            print(result)
            return result
        except:
            print('')


    def CreatePurchaseList(self):
        try:
            i=6
            while i==6:
                print('-You Have Opted to Create a Purchase')
                Vendors_Id=input('Enter The Purchase Request ID You Want To Manipulate : ')
                if Vendors_Id in '':
                    print('The Vendor ID is blank. So enter a value.')
                    i=6
                elif Vendors_Id not in '' and Vendors_Id.isdigit():
                    Vendor_val = int(Vendors_Id)
                    #print(Vendor_val)
                    print("Input number value is: ", Vendor_val)
                    VendorId_Check='SELECT po_request_id FROM po_request WHERE status_id = 4 and po_request_id=''"'+str(Vendor_val)+'"'
                    result=pd.read_sql_query(VendorId_Check, sql_engine) 
                                
                    df = pd.DataFrame(result, columns = ['po_request_id'])
                    print(df['po_request_id'])
                    PORequestId=int(df['po_request_id'])
                    
                    if Vendor_val == PORequestId:
                        print('The Request Id Is Present In The Purchase Request. So continue.')
                        a=1
                        while a==1:
                            totalamount=input('Enter The Total amount of The Purchase :')
                            if totalamount in '':
                                print('Total Amount cannot be blank... Please check it')
                                a=1
                            elif totalamount not in '' and totalamount.isdigit():
                                Totalamt=totalamount

                                b=1
                                while b==1:
                                    paymentId=input('Enter The Payment Id Of the Purchase :')

                                    if paymentId in '':
                                        print('Payment ID cannot be blank... Please check it...')
                                        b=1

                                    elif paymentId not in '' and paymentId.isdigit():
                                        Payment=paymentId

                                        RequestDetails_Query='SELECT po_request_id,inv_item_id,po_request_quantity FROM po_request WHERE po_request_id=''"'+str(Vendor_val)+'"'
                                        Requestresult=pd.read_sql_query(RequestDetails_Query, sql_engine) 
                                        print(Requestresult)

                                        df=pd.DataFrame(Requestresult,columns=['po_request_id'])
                                        po_request_id=int(df['po_request_id'][0])
                
                                        df=pd.DataFrame(Requestresult,columns=['inv_item_id'])
                                        inv_item_id=(df['inv_item_id'][0])
                                        #print(df['inv_item_id'])

                                        df=pd.DataFrame(Requestresult,columns=['po_request_quantity'])
                                        po_request_quantity=(df['po_request_quantity'][0]) 
                                        #print(df['po_request_quantity'])    

                                        print('CheckassSasAS->',inv_item_id)                                                    
                                        vendorsitemid_Query='SELECT Vendors_item_id FROM vendors_item WHERE vendors_id=''"'+str(Vendor_val)+'"'             #inv_item_id='+str(inv_item_id)           #and vendors_id=''"'+str(Vendor_val)+'"'
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
                                            Po_Request_Insert="INSERT INTO po_purchase(created_by,updated_by,order_no,total_amount,Payment_type_id,created_on,updated_on,po_request_id,vendors_item_id,Purchase_Status)VALUES(1, NULL,NULL, %s,%s, %s,%s,%s,%s,1)"
                                            vals = (Totalamt,Payment,Currentdate,Currentdate,PORequestId,Vendors_item_id)   
                                            sql_engine.execute(Po_Request_Insert, vals)
                                                      
                                            print("Success. A Purchase record has been inserted.")

                                        except:
                                            print('Insert went wrong in Purchase Department! Please Check')

                                        try:
                                            UpdateQty_Query='UPDATE inv_item SET item_quantity=%s WHERE inv_item_id=''"'+str(inv_item_id)+'"'
                                            values = (ActualQuantity)
                                            print(UpdateQty_Query)
                                            sql_engine.execute(UpdateQty_Query,values)
                                            print("Success. Purchase Quantity has been updated.")
                                            
                                        except:
                                            print("Error while updating Purchase Quantity in Inventory.")


                                        try:
                                            Request_Status=5
                                            RequestStatus_str=str(Request_Status)
                                            print('dAd',po_request_id)
                                            requestStatus='Update po_request SET status_id=%s WHERE po_request_id=''"'+str(po_request_id)+'"'
                                            values=(RequestStatus_str)
                                            sql_engine.execute(requestStatus,values)
                                            print('purchase Request Status Has been Updated...')
                                            PurchaseModule().Statement()

                                        except:
                                            print('Error while updating the status...')    
                                            #i=0 

                    else:
                        print('Entered ID does not exist.., So Re-enter...')
                        i=1

                else:
                    print('Enter The Correct Purchase Request From The Above List.')
                    i=6

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
                        PurchaseId_Check='SELECT * FROM Po_Purchase WHERE Purchase_Status=1 AND po_purchase_Id=''"'+str(Vendor_val)+'"'
                        PurchaseId_result=pd.read_sql_query(PurchaseId_Check, sql_engine) 
                        print(PurchaseId_result)
                        df = pd.DataFrame(PurchaseId_result, columns = ['po_purchase_Id','po_request_id'])
                        POPurchaseId=int(df['po_purchase_Id'][0])                                
                        RequestID=int(df['po_request_id'])                        

                        if Vendor_val == POPurchaseId:
                            print('The Purchase Request Id Is Present In The Purchase Request. So continue.')
                            e=1
                            while e==1:
                                PurchaseTotalAmount=input('Enter The Total Amount :')

                                if PurchaseTotalAmount in '' :
                                    print('Total Amount is blank...')
                                    e=1

                                elif PurchaseTotalAmount not in '' and PurchaseTotalAmount.isdigit():
                                    s=1
                                    while s==1:
                                        PurchasePayment=input('Enter The Payment Id :')
                                        if PurchasePayment in '':
                                            print('Enter the payment as it is blank...')
                                            s=1

                                        elif PurchasePayment not in '' and PurchasePayment.isdigit():
                                            m=1
                                            while m==1:
                                                PurchaseItemMrpPrice=input('Enter The MRP Price :')

                                                if PurchaseItemMrpPrice in '':
                                                    print('MRP Price is blank.')
                                                    m=1

                                                elif PurchaseItemMrpPrice not in '' and PurchaseItemMrpPrice.isdigit():
                                                    n=1
                                                    while n==1:
                                                        PurchaseItemQuantity=input('Enter The Quantity :')            
                                                        if PurchaseItemQuantity in '':
                                                            print('Item Quantity is blank...')
                                                            n=1

                                                        elif PurchaseItemQuantity not in '' and PurchaseItemQuantity.isdigit():
                                                            o=1
                                                            while o==1:
                                                                PurchaseMaxDiscount=input('Enter The Max Discount :')
                                                                if PurchaseMaxDiscount is '':
                                                                    print('Max Discount is empty :')
                                                                    o=1
                                
                                                                elif PurchaseMaxDiscount not in '' and PurchaseMaxDiscount.isdigit():
                                                                    p=1
                                                                    while p==1:
                                                                        PurchaseWeight=input('Enter the Weight :')

                                                                        if PurchaseWeight is '':
                                                                            print('Weight is blank...')
                                                                            p=1

                                                                        elif PurchaseWeight not in '' and PurchaseWeight.isdigit():
                                                                            
                                                                            try:
                                                                                Purchase_Update_Query= 'UPDATE Po_Purchase SET total_amount = %s, Payment_type_id=%s WHERE po_purchase_id = ''"'+str(POPurchaseId)+'"'
                                                                                values = (PurchaseTotalAmount,PurchasePayment)
                                                                                sql_engine.execute(Purchase_Update_Query, values)
                                                                                print("Success. Purchase has been updated.")
                                                                            except:
                                                                                print('Failed Updating record into Purchase table...') 

                                                                            try:
                                                                                inv_Update_Query='Update inv_item SET item_mrp_price=%s,item_quantity=%s,item_max_discount=%s,weight=%s WHERE inv_item_id=''"'+str(RequestID)+'"'
                                                                                values=(PurchaseItemMrpPrice,PurchaseItemQuantity,PurchaseMaxDiscount,PurchaseWeight)
                                                                                sql_engine.execute(inv_Update_Query,values)
                                                                                print("Success. Inventory has been updated.")
                                                                                PurchaseModule().Statement()

                                                                            except:
                                                                                print('Failed to update Inventory Table...!')

                                                                        else:
                                                                            print('abcdefghijklmnop')

                        else:
                            print('Cannot Proceed Further...')


                except:
                    print('Enter The Correct Purchase ID From The List TO Edit...')
                    i = 3

            else:
                print('Enter The Correct Purchase Request From The Above List.')
                h=1   
                return
                                                      
                    
    def DeletePurchase(self):
        PurchaseDelMsg="Success. A record has been deleted."
        q=1
        while q==1:
            Purchases_Id=input('Enter The Purchase ID You Want To Delete : ')    


            if Purchases_Id in '':
                print('The Purchase ID is blank. So enter a value.')
                q=1

            elif Purchases_Id not in '' and Purchases_Id.isdigit():
                try:
                    Purchase_val = int(Purchases_Id)                        
                    print("Input number value is: ", Purchase_val)
                    PurchaseId_Check='SELECT * FROM Po_Purchase WHERE Purchase_Status =1 AND po_purchase_Id=''"'+str(Purchase_val)+'"'
                    PurchaseId_result=pd.read_sql_query(PurchaseId_Check, sql_engine) 
                    print(PurchaseId_result)
                    df = pd.DataFrame(PurchaseId_result, columns = ['po_purchase_Id','po_request_id'])
                    POPurchaseId=int(df['po_purchase_Id'][0])                                                                
                    RequestID=int(df['po_request_id'])

                    # Obtaining the Inventory ID and Po Request Qty from Purchase Request Table.
                    PurchaseRequest='SELECT * FROM po_request WHERE po_request_id=''"'+str(RequestID)+'"'
                    PurchaseRequest_result=pd.read_sql_query(PurchaseRequest, sql_engine)
                    print(PurchaseRequest_result)

                    df=pd.DataFrame(PurchaseRequest_result,columns=['inv_item_id','po_request_quantity'])
                    InvId=int(df['inv_item_id'])
                    RequestQty=int(df['po_request_quantity'])                        

                    # Minus the Quantity from Inventory Table With Inventory ID
                    print('Minus the Quantity from Inventory Table With Inventory ID')
                    InvQty='SELECT item_quantity from inv_item WHERE inv_item_id=''"'+str(InvId)+'"'
                    InvQty_Result=pd.read_sql_query(InvQty,sql_engine)

                    df=pd.DataFrame(InvQty_Result,columns=['item_quantity'])
                    InvQuantity=int(df['item_quantity'])
                    Quantity=InvQuantity-RequestQty       

                    if Purchase_val == POPurchaseId:
                        try:
                            zero=0
                            status=str(zero)
                            print('The Purchase Request Id to delete Is Present. So Delete.')
                            PurchaseTblUpd_Query='UPDATE po_purchase SET Purchase_Status = %s WHERE po_purchase_Id = ''"'+str(Purchase_val)+'"'
                            values=(status)
                            sql_engine.execute(PurchaseTblUpd_Query,values)
                            QuantityUpdate='Update inv_item SET item_quantity=%s WHERE inv_item_id=''"'+str(InvId)+'"'
                            values=(Quantity)
                            sql_engine.execute(QuantityUpdate,values)
                            print("Success. The Purchase ID has been deleted :",str(Purchase_val))
                            PurchaseModule().Statement()

                        except:
                            print('Error in Deleting Purchase...')
                except:
                    print('Enter Valid Purchase ID from the list...')
                    #h=1

            else:
                print('Failed in Deleting the Purchase ID : ',str(Purchase_val))                                    
                return PurchaseDelMsg

    def initCall(self,user):
        self.user=user
        self.Statement()

    def Statement(self):
        self.user=[{'role_id':1,'department_id':2}]
        #print(self.user)
        #print(self.user[0]["role_id"])
        try:
            answer = input('Please Select One Of The Values 1. Vendor 2. Purchase or type Q to quit:')
            i=0
            while i==0:
                if answer in '':
                    print('Please Enter a Value 1. Vendor 2. Purchase or type Q to quit')
                    i=0
                elif answer in 'Q' and answer in 'q' :
                    exit   

                elif answer in '1':
                    print(answer, 'Vendor.')
                    print('You Have chosen Vendor')
                    PurchaseModule().ShowVendor()
                    prompt="Select any one of the operations to process Vendor a. Add Vendor b. Edit Vendor c. Delete Vendor : " if self.user[0]["role_id"]!=3 else "Select any one of the operations to process Vendor a. Add Vendor b. Edit Vendor"
                    response = input(prompt)

                    if response in '':
                        print('Input is blank. Please Select A Menu.')
                        i=0

                    elif response in 'a':
                        PurchaseModule().AddVendor()

                    elif response in 'b':
                        print('You Have Opted to UPDATE a Vendor')   
                        PurchaseModule().UpdateVendor()                         

                    elif response in 'c' and self.user[0]["role_id"]!=3:
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

                elif answer in '2':
                    a = 4
                    while a == 4:
                        print(answer,'Purchases.')
                        print('You Have chosen Purchases')
                        print('Below Is The List Of Purchase Request')
                        PurchaseModule().ShowPurchaseList()
                        #response = input('Select any one of the operations to process Purchase x. Add Purchase y. Edit Purchase z. Delete Purchase :')
                        #print('You have chosen : ', response)  

                        prompt="Select any one of the operations to process Purchase x. Add Purchase y. Edit Purchase z. Delete Purchase : " if self.user[0]["role_id"]!=3 else "Select any one of the operations to process Purchase x. Add Purchase y. Edit Purchase :"
                        response = input(prompt)
                        
                        if response in '':
                            print('User has not entered any Input. Please Choose A Menu.')
                        elif response in 'x':
                            PurchaseModule().CreatePurchaseList()                            

                        elif response in 'y':
                            print('You Have Selected To Edit A Purchase ')
                            PurchaseModule().EditPurchase()

                        elif response in'z' and self.user[0]["role_id"]!=3:
                            print('You Have Selected To Delete A Purchase ')    
                            PurchaseModule().DeletePurchase()

                        else:
                            print('Check Credentials and Input...')
                            a=4

                elif answer in 'Q' or answer in 'q':
                    print('Exiting...')
                    exit


        except:
            print('Check Your Input..!')           
            return

PurchaseModule().Statement() 

