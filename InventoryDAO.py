import mysql.connector
import pandas 
import Validation as vaild
import copy
from tabulate import tabulate
from texttable import Texttable
connection = mysql.connector.connect(host='192.168.1.128',port='3307',database='coffee',user='application',password='abc123!@#')

class InventoryDAO:    
    def __allItemList__(self,id):        
        try:            
            cursor = connection.cursor()
            sql="select item.inv_item_id, item.item_name,item.item_description,item.item_quantity,item.item_mrp_price,item.item_status,item.item_max_discount,item.created_on,cb.name as created_by,item.updated_on,ub.name as  updated_by from inv_item item inner join users cb on item.created_by=cb.user_id left join users ub on item.updated_by=ub.user_id where item.is_active=1 order by  item.inv_item_id"
            cursor.execute(sql) 
            lst = cursor.fetchall()
            itm=[]            
            if int(id)==1:         
                print(tabulate(lst, headers=['Item Id', 'Item Name','Item Description','Quantity', 'Item MRP Price', 'Item Status', 'Discount','Created On', 'Created By', 'Updated On', 'Updated By']))
            elif int(id)==2:                                       
                for i in lst:
                    itm1=[]
                    itm1.insert(0,i[0])
                    itm1.insert(1,i[1])
                    itm1.insert(2,i[2])
                    itm.append(itm1)                                                           
                print(tabulate(itm, headers=['Item Id','Item Name','Item Description']))  
        except mysql.connector.Error as error :
            print("Failed {} :".format(error))              
        finally:
            if(connection.is_connected()):
                cursor.close()                          
                          

    def __isCount0ItemList__(self):        
        try:
            cursor = connection.cursor()
            sql="select item.inv_item_id, item.item_name,item.item_description,item.item_quantity,item.item_mrp_price,item.item_status,item.item_max_discount,item.created_on,cb.name as created_by,item.updated_on,ub.name as  updated_by from inv_item item inner join users cb on item.created_by=cb.user_id left join users ub on item.updated_by=ub.user_id  where  (item.item_quantity=0 or item.item_quantity is null) and item.is_active=1 order by  item.inv_item_id"
            cursor.execute(sql)
            lst=cursor.fetchall()
            print(tabulate(lst, headers=['Item Id', 'Item Name','Item Description','Quantity', 'Item MRP Price', 'Item Status', 'Discount','Created On', 'Created By', 'Updated On', 'Updated By']))
        except mysql.connector.Error as error:
            print("Failed {}".format(error))  
        finally:
             if(connection.is_connected()):
                cursor.close()
                 

    def __addItem__(self,user_bean):        
        try:
            item= vaild.Validataion().__addItemValidation__()   
            insert_query = 'insert into inv_item(item_name,item_description,item_status,created_by,created_on) values("'+str(item[0])+'","'+str(item[1])+'",2,"'+str(user_bean[0])+'",now())'             
            cursor = connection.cursor()
            result  = cursor.execute(insert_query)
            connection.commit()
            print ("\nRecord inserted successfully into inventory table")
        except Exception as error :
            print("Failed inserting record into inventory table ",error)
            connection.rollback() #rollback if any exception occured    
        finally:
            #closing database connection.
            if(connection.is_connected()):
                cursor.close()

    def __selectUpdateItemId__(self) :
        item_id=""        
        i=0        
        while i==0: 
            item_id=vaild.Validataion().__selectUpdateItem__()           
            lst=""
            try:
                cursor = connection.cursor()
                sql="select inv_item_id,item_name,item_description from inv_item where is_active=1 and inv_item_id="+str(item_id)
                cursor.execute(sql)
                lst=cursor.fetchall()
                print(tabulate(lst, headers=['Item Id', 'Item Name','Item Description']))
            except Exception as error:
                print("Failed {}".format(error))  
            finally:
                if(connection.is_connected()):
                    cursor.close()             
            if len(lst)==0:
                print("Enter valid id")
            else:
                break
        return item_id

    def __updateItem__(self,id,user_bean,methodId):
        item= []      
        try:
            insert_query=""
            if int(methodId)==1:
                item=vaild.Validataion().__addItemValidation__() 
                insert_query = 'update inv_item set item_name="'+item[0]+'" ,item_description="'+item[1]+'",updated_on=now(), updated_by="'+str(user_bean[0])+'" where inv_item_id="'+str(id)+'"'   
            else :
                insert_query = 'update inv_item set is_active=0 ,updated_on=now(),updated_by="'+str(user_bean[0])+'" where inv_item_id="'+str(id)+'"' 
            
            cursor = connection.cursor()
            result  = cursor.execute(insert_query)
            connection.commit()
            print ("Record updated successfully into inventory table")
        except mysql.connector.Error as error :
                connection.rollback() #rollback if any exception occured
                print("Failed updating record into inventory table {}".format(error))
        finally:
                #closing database connection.
                if(connection.is_connected()):
                    cursor.close()

    def __poRequestList__(self,id,methodId):        
        try:     
            sql=""       
            
            if int(methodId)==1:
                sql="select po.po_request_id,itm.item_name,po.po_request_quantity,s.status,cb.name as created_by,po.created_on,ub.name as updated_by, po.updated_on  from po_request po inner join inv_item itm on itm.inv_item_id=po.inv_item_id  inner join  users cb on cb.user_id=itm.created_by left join users ub on ub.user_id=itm.updated_by inner join status s on s.status_id=po.status_id  where po.is_active=1"
            elif int(methodId)==2:
                sql="select po.po_request_id,itm.item_name,po.po_request_quantity,s.status,cb.name as created_by,po.created_on,ub.name as updated_by, po.updated_on  from po_request po inner join inv_item itm on itm.inv_item_id=po.inv_item_id  inner join  users cb on cb.user_id=itm.created_by left join users ub on ub.user_id=itm.updated_by inner join status s on s.status_id=po.status_id  where po.is_active=1 and po.status_id=4 "
            elif int(methodId)==3:
                sql="select po.po_request_id,itm.item_name,po.po_request_quantity,s.status,cb.name as created_by,po.created_on,ub.name as updated_by, po.updated_on  from po_request po inner join inv_item itm on itm.inv_item_id=po.inv_item_id  inner join  users cb on cb.user_id=itm.created_by left join users ub on ub.user_id=itm.updated_by inner join status s on s.status_id=po.status_id  where po.is_active=1 and po.status_id=5"

            cursor = connection.cursor()
            cursor.execute(sql) 
            lst = cursor.fetchall()
            itm=[]            
            if int(id)==1:                        
                print(tabulate(lst, headers=['PO Request Id','Item Name', 'PO Request Quantity','Status','Created By','Created On', 'Updated By',  'Updated On']))
            elif int(id)==2:                                       
                for i in lst:
                    itm1=[]
                    itm1.insert(0,i[0])
                    itm1.insert(1,i[1])
                    itm1.insert(2,i[2])
                    itm.append(itm1)                                                           
                print(tabulate(itm, headers=['Item Id','Item Name','Item Description']))            
        except mysql.connector.Error as error :
            print("Failed {} :".format(error))              
        finally:
            if(connection.is_connected()):
                cursor.close()                                  


    def __addPORequest__(self,user_bean): 
        i=0
        InventoryDAO.__allItemList__(self,2)
        while i==0:       
            po= vaild.Validataion().__addPORequestValidation__()       
            try:
                insert_query = ' insert into po_request(inv_item_id,po_request_quantity,created_by,created_on) values("'+po[0]+'","'+po[1]+'","'+str(user_bean[0])+'",now())'            
                cursor = connection.cursor()
                result  = cursor.execute(insert_query)
                connection.commit()
                print ("Record inserted successfully into PO table")
                i=1
            except Exception as error :
                    connection.rollback() #rollback if any exception occured
                    print('Error :Enter correct item id',error)
            finally:
                    #closing database connection.
                    if(connection.is_connected()):
                        cursor.close()
                    if i==1:
                        break                 
    
    def __selectUpdatePORequestId__(self) :
        poRequestId=""        
        i=0        
        while i==0: 
            poRequestId=vaild.Validataion().__enterUpdatePORequest__()           
            lst=""
            try:
                cursor = connection.cursor()
                sql="select po.po_request_id,itm.inv_item_id,itm.item_name,po.po_request_quantity,s.status,cb.name as created_by,po.created_on,ub.name as updated_by, po.updated_on  from po_request po inner join inv_item itm on itm.inv_item_id=po.inv_item_id  inner join  users cb on cb.user_id=itm.created_by left join users ub on ub.user_id=itm.updated_by inner join status s on s.status_id=po.status_id  where po.is_active=1 and po.po_request_id="+str(poRequestId)
                
                cursor.execute(sql)
                lst=cursor.fetchall()
                print(tabulate(lst, headers=['PO Request Id','Item Id','Item Name', 'PO Request Quantity','Status','Created By','Created On', 'Updated By',  'Updated On']))
            except mysql.connector.Error as error:
                print("Failed {}".format(error))  
            finally:
                if(connection.is_connected()):
                    cursor.close()             
            if len(lst)==0:
                print("Enter valid id")
            else:
                break
        return poRequestId

    def __updatePORequest__(self,id,user_bean,methodId):   
              
        try:
            query=""
            if methodId==1:
                po= vaild.Validataion().__addPORequestValidation__() 
                query = ' update po_request set inv_item_id="'+po[0]+'",po_request_quantity="'+po[1]+'" , updated_by="'+str(user_bean[0])+'",updated_on=now() where po_request_id='+str(id) 
            else:
                query = 'update po_request set updated_by="'+str(user_bean[0])+'",updated_on=now(),is_active=0 where po_request_id='+str(id) 
                      
            cursor = connection.cursor()
            result  = cursor.execute(query)
            connection.commit()
            print ("Record updated successfully into PO table")
        except mysql.connector.Error as error :
                connection.rollback() #rollback if any exception occured
                print("Failed updated record into PO table {}".format(error))
        finally:
                #closing database connection.
                if(connection.is_connected()):
                    cursor.close()   
        

                     
         
        
