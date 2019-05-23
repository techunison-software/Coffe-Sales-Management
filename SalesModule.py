import mysql.connector
from mysql.connector import Error
import pandas as pd

conn = mysql.connector.connect(host='1.22.137.204',port='3307',database='coffee',user='application',password='abc123!@#')

global soitemlst
soitemlst = []
global user

class SalesModule:
    def initCall(self,user):
        user = user
        self.userid = user['user_id'][0]
        self.roleid = user['role_id'][0]
        
        if self.roleid == 1 or self.roleid == 2:
            self.dup_crud = input("1.Create Sales Order \t 2.Update Sales Order \t 3.Delete Sales Order \t 4.View Sales Orders \t 5.OverAll Itemwise Sales 0.GoBack \n Enter number 1 or 2 or 3 or 4 or 5 or 0:\t")
            self.crud = self.checkpositiveinteger(self.dup_crud)
            self.conditioncheck(self.roleid,user)

        elif self.roleid == 3:
            self.dup_crud = input("1.Create Sales Order \t 2.Update Sales Order \t 3.View Sales Orders \t 4.Overall Itemwise Sales  0.GoBack \n Enter number 1 or 2 or 3 or 4 or 0:\t")
            self.crud = self.checkpositiveinteger(self.dup_crud)
            self.conditioncheck(self.roleid,user)

    def conditioncheck(self,roleid,user):
        self.roleid = roleid
        if self.roleid == 1 or self.roleid == 2:
            if self.crud == 1:
                cso = CreateSO()
                cso.initCall(user)

            elif self.crud == 2:
                uso = UpdateSO()
                uso.initCall(user)

            elif self.crud == 3:
                dso= DeleteSO()
                dso.initCall(user)

            elif self.crud==4:
                vso = ViewSO()
                vso.initCall(user)
            
            elif self.crud  == 5:
                iws = ItemwiseSales()
                iws.initCall(user)

            elif self.crud ==0:
                return

            else:
                print("Please choose correct number!!!\n")
                self.initCall(user)
        
        elif self.roleid == 3:
            if self.crud == 1:
                cso = CreateSO()
                cso.initCall(user)
            
            elif self.crud == 2:
                uso = UpdateSO()
                uso.initCall(user)
            
            elif self.crud==3:
                vso = ViewSO()
                vso.initCall(user)

            elif self.crud == 4:
                iws = ItemwiseSales()
                iws.initCall(user)

            elif self.crud ==0:
                return

            else:
                print("Please choose correct number!!!\n")
                self.initCall(user)
        else:
            print("Role Id is undefined.Please contact admin!!!")
            return

    def checkpositiveinteger(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveinteger(self.pint)
        return int(self.pint)


class CreateSO:

    def initCall(self,user):
        print("Welcome to Create Sales order Screen: \n")
        self.listitems(user)

    def checkpositiveint(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveint(self.pint)
        return int(self.pint)

    def listitems(self,user):
        mycursor = conn.cursor()
        mycursor.execute("SELECT ii.inv_item_id,ii.item_name,ii.item_quantity,ii.item_mrp_price,ii.item_max_discount FROM inv_item as ii where ii.item_quantity > 0 and ii.item_status = 1")
        lst = mycursor.fetchall()
        if len(lst)== 0:
                print("No list..Sorry!!!")
                return SalesModule().initCall(user)

        else:
            df= pd.DataFrame(lst)
            mycursor.close()
            df.columns = ['ItemId','ItemName','Qty.','MRP','Discount']
            print(df)
            self.createsalesorder(lst,0,user,soitemlst)

    def additem(self,lst,soitemlst):
        itemlist = lst
        invitem= []
        itemid = self.getitemid(itemlist,soitemlst)
        itemname = self.getitemname(itemlist,itemid)
        quantity = self.getquantity(itemlist,itemid)
        discount = self.getdiscount(itemlist,itemid)
        unitprice = self.getuprice(itemlist,itemid)
        totalprice = self.gettprice(itemid,discount,unitprice,quantity)
        invitem.append({'inv_item_id':itemid,'itemname':itemname,'quantity':quantity,'discount':discount,'unit_price':unitprice,'total_price':totalprice})
        return invitem

    def paymenttransaction(self,lst,user,soitemlst):
        dup_totalamount = 0
        count = 0
        dup_payid = input("Welcome to Payment screen.. 1.Cash 2.Credit/Debit Card 3.UPI 0.Go back \n Enter number 1 or 2 or 3 or 0:\t")
        payid1 = self.checkpositiveint(dup_payid)
        payid = self.checkpayid(payid1,lst,user,soitemlst)
    
        for elem in soitemlst:
            dup_totalamount += elem['total_price']
        totalamount = dup_totalamount

        try:
            cursor = conn.cursor()
            sql_insert_query = 'insert into so_header(total_amount,payment_mode_id,created_on,created_by,delete_status) values ( '+ str(totalamount) +','+ str(payid) +',now(),'+str(user['user_id'][0]) +',1)'
            result = cursor.execute(sql_insert_query)
            so_header_id = cursor.lastrowid
            conn.commit()
        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed inserting record into so_header table {}".format(error))
            return SalesModule().initCall(user)
        finally:
            if conn.is_connected() :
                cursor.close()
        #print ("Record inserted successfully!!!")

        if so_header_id != 0:
            for row in soitemlst:
                try:
                    cursor = conn.cursor()
                    query2 = 'insert into so_header_details(inv_item_id,quantity,discount,unit_price,total_price,created_by,created_on,so_header_id,delete_status) values('+str(row['inv_item_id'])+','+ str(row['quantity'])+','+str(row['discount'])+','+str(row['unit_price'])+','+str(row['total_price'])+', '+ str(user['user_id'][0])+' ,now(),'+str(so_header_id)+' ,1)'
                    result  = cursor.execute(query2)
                    so_header_details_id = cursor.lastrowid
                    conn.commit()
                except mysql.connector.Error as error:
                    conn.rollback()
                    print("Failed inserting record into so_header table {}".format(error))
                    return SalesModule().initCall(user)
                finally:
                    if conn.is_connected() :
                        cursor.close()
                
        if so_header_details_id != 0:
            for row in soitemlst:
                for row2 in lst:
                    
                    if row['inv_item_id'] == row2[0] :
                        try:
                            fqty = row2[2] - row['quantity']
                            cursor = conn.cursor()
                            query3 = 'update inv_item set item_quantity =' + str(fqty) +', updated_by = '+ str(user['user_id'][0]) +' , updated_on = now() where inv_item_id = ' + str(row2[0])
                            result  = cursor.execute(query3)
                            conn.commit()
                        except mysql.connector.Error as error:
                            conn.rollback()
                            print("Failed updating record into inv_item table {}".format(error))
                            return SalesModule().initCall(user)
                        finally:
                            if conn.is_connected() :
                                cursor.close()
                count = count + 1                

        if count == len(soitemlst):
            print("Records inserted successfully!!!")
            soitemlst.clear()
            return self.createsalesorder(lst,1,user,soitemlst)
        else:
            print("Error in inserting!!!")     
            return SalesModule().initCall(user)

    def createsalesorder(self,ls,mode,user,soitemlst):
        lst = ls
        cond = 1

        if mode == 0:
            if len(soitemlst) > 0:
                soitemlst.clear()

            te= self.additem(lst,soitemlst)
            soitemlst.append({'inv_item_id':te[0]['inv_item_id'],'itemname':te[0]['itemname'],'quantity':te[0]['quantity'],'discount':te[0]['discount'],'unit_price':te[0]['unit_price'],'total_price':te[0]['total_price']})
            self.getcartitems(soitemlst)

        while True:
            dup_ifs = input("\n 1.Add Item \t 2.Delete existing Item \t 3.Proceed for payment 4.View Items in SO \t 0.Go Back \n Enter number 1 or 2 or 3 or 4 or 0:\t")
            ifs = self.checkpositiveint(dup_ifs)

            if ifs == 1 :
                te= self.additem(lst,soitemlst)
                soitemlst.append({'inv_item_id':te[0]['inv_item_id'],'itemname':te[0]['itemname'],'quantity':te[0]['quantity'],'discount':te[0]['discount'],'unit_price':te[0]['unit_price'],'total_price':te[0]['total_price']})
                self.getcartitems(soitemlst)

            elif ifs == 2:
                if len(soitemlst) == 0:
                    print("Your sales order item list is empty!!!")    
                
                else:
                    li = self.deletesoitem(soitemlst)
                    if li == 0:
                        soitemlst.clear()
                    else:
                        soitemlst = li
                
                self.getcartitems(soitemlst)
                
            elif ifs == 3:
                if len(soitemlst)> 0 : 
                    return self.paymenttransaction(lst,user,soitemlst)
                else:
                    print("Your sales item list is empty!!!Please add items to proceed")

            elif ifs == 4:
                self.getcartitems(soitemlst)

            elif ifs == 0:
                return SalesModule().initCall(user)
    
    def deletesoitem(self,soitemlst):
        if len(soitemlst) < 0:
            print("Your Sales item list is empty!!!")
        
        dup_item_id = input("Choose the ItemId to delete:\t")
        itemid1 = self.checkpositiveint(dup_item_id)
        itemid = self.checkdeleteitem(itemid1,soitemlst)

        if len(soitemlst) == 1 and soitemlst[0]['inv_item_id'] == itemid:
            soitemlst.clear()
        else:
            soitemlst = [ x for x in soitemlst if x['inv_item_id'] != itemid]
        
        return soitemlst 

    def getcartitems(self,soitemlst):
        if len(soitemlst) == 0:
            print("No items in sales order list")
        
        else:
            print("Items in SalesOrder")
            df= pd.DataFrame(soitemlst)
            df.rename(columns={'inv_item_id':'ItemId','itemname':'ItemName','quantity':'Quantity','unit_price':'UnitPrice','discount':'Discount','total_price':'TotalPrice'},inplace=True)
            #df.columns = ['ItemId','Qty.','UnitPrice','Discount','TotalPrice']
            print(df[['ItemId','ItemName','Quantity','UnitPrice','Discount','TotalPrice']])

    def gettprice(self,iid,disc,uprice,qty):
        itemid = iid
        discount = disc
        unitprice = uprice
        quantity = qty
        totalprice = unitprice*quantity

        if discount == 0:
            return totalprice

        else:
            discount = discount/100
            dup_totalprice = totalprice * discount
            totalprice = totalprice - dup_totalprice
            return totalprice

    def getuprice(self,lst,iid):
        itemlist = lst
        itemid = iid
        for row in itemlist:
            if itemid == row[0]:
                return row[3]

    def getitemid(self,lst,soitemlst):
        itemlist = lst
        dup_itemid = input("Choose ItemId:\t")
        itemid1 = self.checkpositiveint(dup_itemid)
        itemid = self.checkitemid(itemlist,itemid1,soitemlst)
        
        if len(soitemlst) > 0:
            for row in soitemlst:
                if row['inv_item_id'] == itemid:
                    print("Item is already is in list!!!Please choose different item")
                    return self.getitemid(lst,soitemlst)

        return itemid
    
    def getitemname(self,lst,iid):
        itemlist = lst
        for row in itemlist:
            if iid == row[0]:
                return row[1]

    def getdiscount(self,lst,iid):
        itemid = iid
        itemlist = lst
        
        for row in itemlist:
            if itemid == row[0]:
                if row[4] == 0 or row[4] == None:
                    print("Your item has no discount!!!\t")
                    return 0
        
        dup_disc = input("Enter Discount:\t")
        disc1 = self.checkpositiveint(dup_disc)
        disc = self.checkdiscount(itemlist,itemid,disc1)
        return disc
    
    def getquantity(self,lst,iid):
        itemid = iid
        itemlist = lst
        dup_quantity = input("Choose Quantity:")
        quantity1 = self.checkpositiveint(dup_quantity)
        quantity = self.checkquantity(itemlist,itemid,quantity1)
        return quantity

    def checkitemid(self,lst,itemid,soitemlst):
        ls = lst
        iid = itemid
        increment = 0

        for row in ls:
            if iid == row[0]:
                return iid
            else:
                increment += 1

        if len(ls) == increment:
            print("Item ID is Wrong!!!, ",end="")
            return self.getitemid(ls,soitemlst)
        
    def checkpayid(self,pid,ls,user,soitemlst):
        lst = ls
        payid = pid
        if payid == 1 or payid == 2 or payid == 3:
            return int(payid)
        elif payid == 0:
            return self.createsalesorder(lst,1,user,soitemlst)
        else: 
            print("Payment ID is Wrong!!!, ",end="")
            return self.paymenttransaction(lst,user,soitemlst)

    def checkquantity(self,lst,itemid,qty):
        ls = lst
        iid = itemid
        qty = qty

        for row in ls:
            if iid == row[0]:
                if qty <= row[2] :
                    return qty
                else:
                    print("Quantity is Greater than available quantity!!!, ",end="")
                    return self.getquantity(ls,iid)
    
    def checkdiscount(self,lst,itemid,disc):
        ls = lst
        iid = itemid
        dis = disc

        for row in ls:
            if iid == row[0]:
                if dis <= row[4] :
                    return dis
                else:
                    print("Discount is Greater than given discount !!!,",end="")
                    return self.getdiscount(ls,iid)
    
    def checkdeleteitem(self,iid,soitemlst):
        itemid = iid
        increment = 0
        lengthcartitems = len(soitemlst)

        if lengthcartitems > 0:
            for row in soitemlst:
                if itemid == row['inv_item_id']:
                    return int(itemid)
                else:
                    increment += 1
        
        if lengthcartitems == increment:
            print("Item ID is Wrong!!!, ",end="")
            return self.deletesoitem(soitemlst)
        
class UpdateSO:
    def initCall(self,user):
        self.listofso(user)
    
    def checkpositiveint(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveint(self.pint)
        return int(self.pint)

    def listofso(self,user):
        self.userid = user['user_id'][0]
        self.roleid = user['role_id'][0]
        if self.roleid == 1 or self.roleid == 2:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1"
        else:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1 and soh.created_by = "+ str(self.userid)
        try:
            cursor = conn.cursor()
            cursor.execute(str1)
            lst = cursor.fetchall()
            conn.commit()

            if len(lst)== 0:
                print("Sales Order List is empty!!!")
                return SalesModule().initCall(user)

            else:
                df= pd.DataFrame(lst)
                df.columns = ['SO_Id','SalesPerson','PaymentType','TotalAmount','BillDate']
                print(df)
                dup_sodetailedid = input('Enter SO_Id to see the detailed view of sales Order or 0.Go Back \t')
                so_detailedid1 = self.checkpositiveint(dup_sodetailedid)
                if so_detailedid1 == 0:
                    return SalesModule().initCall(user)
                else:
                    return self.detailedso(so_detailedid1,user)

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header table {}".format(error))
            return SalesModule.initCall(user)
        finally:
            if conn.is_connected() :
                cursor.close()

    def detailedso(self,so_id,user):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT sohd.inv_item_id,ii.item_name,sohd.quantity,sohd.discount,sohd.unit_price,ii.item_quantity,sohd.total_price,u.user_name,sohd.created_on FROM so_header_details sohd join users u on sohd.created_by = u.user_id join inv_item ii on ii.inv_item_id = sohd.inv_item_id  where sohd.delete_status = 1 and sohd.so_header_id = "+str(so_id))
            itemlst = cursor.fetchall()
            conn.commit()
            if len(itemlst)==0:
                print("This sales order has no item!!!")
                self.listofso(user)
            else:
                df= pd.DataFrame(itemlst)
                df.columns = ['ItemId','ItemName','Qty.','Discount(%)','UnitPrice','InventoryQty','TotalPrice','SalesPerson','CreatedDate']
                print(df)
                dup_yn = input("press 1 to continue or 0 to go back!!! ")
                yn = self.checkpositiveint(dup_yn)
                if yn == 0:
                    return self.listofso(user)
                elif yn == 1:
                    return self.selectitem(so_id,user,itemlst)
                else:
                    return self.detailedso(so_id,user)

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header_details table {}".format(error))
            return self.listofso(user)
        
        finally:
            if conn.is_connected() :
                cursor.close()

    def updateitem(self,itemdetails,so_id,user,itemlst):
        try:
            cursor = conn.cursor()
            sql_update_query = 'update so_header_details set quantity = '+ str(itemdetails[3])+' ,discount = '+ str(itemdetails[4])+' ,total_price = '+ str(itemdetails[5]) + ' ,updated_by ='+ str(user['user_id'][0])  + ' ,updated_on = now() where inv_item_id = '+str(itemdetails[0])+' and so_header_id = ' + str(so_id)
            result = cursor.execute(sql_update_query)
            conn.commit()
        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed updating record into so_header_details table {}".format(error))
            return detailedso(so_id,user)
        finally:
            if conn.is_connected() :
                cursor.close()

        try:
            cursor = conn.cursor()
            sql_update_query2 = 'update inv_item set item_quantity = '+  str(itemdetails[6]) + ' ,updated_by ='+ str(user['user_id'][0])  + ' ,updated_on = now() where inv_item_id ='+str(itemdetails[0])
            result = cursor.execute(sql_update_query2)
            conn.commit()
        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed updating record into inv_item table {}".format(error))
            return detailedso(so_id,user)
        finally:
            if conn.is_connected() :
                cursor.close()

        try:

            cursor = conn.cursor()
            sql_update_query2 = 'update so_header set total_amount = total_amount + ('+  str(itemdetails[7]) +') ,updated_by ='+ str(user['user_id'][0])  + ' ,updated_on = now() where so_header_id ='+str(so_id)
            result = cursor.execute(sql_update_query2)
            conn.commit()
        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed updating record into so_header table {}".format(error))
            return detailedso(so_id,user)
        finally:
            if conn.is_connected() :
                cursor.close()
                print("Updated Successfully!!!")
                return self.listofso(user)

    def selectitem(self,so_id,user,itemlst):
        itemid = self.getitemid(itemlst)
        itemname = self.getitemname(itemlst,itemid)
        unitprice = self.getuprice(itemlst,itemid)
        quantity = self.getquantity(itemlst,itemid)
        discount = self.getdiscount(itemlst,itemid)
        totalprice = self.gettprice(itemid,discount,unitprice,quantity)
        print("ItemId: "+str(itemid)+",ItemName: "+ itemname+",Qty: "+str(quantity)+",Discount: "+str(discount)+",TotalPrice: "+str(totalprice))
        
        for row in itemlst:
            if itemid == row[0]:
                invqty = row[5] + row[2] - quantity
                tamount = totalprice - row[6] 
                
        itemdetails = [itemid,itemname,unitprice,quantity,discount,totalprice,invqty,tamount]
        return self.updateitem(itemdetails,so_id,user,itemlst)
        
    def getitemid(self,itemlst):
        dup_itemid = input("Enter ItemId to update:\t")
        itemid1 = self.checkpositiveint(dup_itemid)
        itemid = self.checkitemid(itemlst,itemid1)
        return itemid

    def getitemname(self,itemlst,itemid):
        for row in itemlst:
            if itemid == row[0]:
                return row[1]
    
    def getuprice(self,itemlst,itemid):
        for row in itemlst:
            if itemid == row[0]:
                return row[4]

    def gettprice(self,iid,disc,uprice,qty):
        itemid = iid
        discount = disc
        unitprice = uprice
        quantity = qty
        totalprice = unitprice*quantity

        if discount == 0:
            return totalprice

        else:
            discount = discount/100
            dup_totalprice = totalprice * discount
            totalprice = totalprice - dup_totalprice
            return totalprice

    def getquantity(self,itemlst,itemid):
        dup_quantity = input("Enter quantity to update:")
        quantity1 = self.checkpositiveint(dup_quantity)
        quantity = self.checkquantity(itemlst,itemid,quantity1)
        return quantity

    def getdiscount(self,itemlst,itemid):
        for row in itemlst:
            if itemid == row[0]:
                if row[3] == 0 or row[3] == None:
                    print("Your item has no discount!!!\t")
                    return 0
        
        dup_disc = input("Enter Discount:\t")
        disc1 = self.checkpositiveint(dup_disc)
        disc = self.checkdiscount(itemlst,itemid,disc1)
        return disc

    def checkitemid(self,itemlst,itemid):
        increment = 0

        for row in itemlst:
            if itemid == row[0]:
                return itemid
            else:
                increment += 1

        if len(itemlst) == increment:
            print("Item ID is Wrong!!!, ",end="")
            return self.getitemid(itemlst)

    def checkquantity(self,itemlst,itemid,qty):
        for row in itemlst:
            if itemid == row[0]:
                if qty <= row[2] :
                    return qty
                elif qty > row[2]:
                    qty1 = qty-row[2]
                    if row[5] < qty1:
                        print("Quantity is Greater than available quantity!!!, ",end="")
                        return self.getquantity(itemlst,itemid)
                    else:
                        return qty

    def checkdiscount(self,itemlst,itemid,disc):
        for row in itemlst:
            if itemid == row[0]:
                if disc <= row[3] :
                    return disc
                else:
                    print("Discount is Greater than given discount !!!,",end="")
                    return self.getdiscount(itemlst,itemid)


class DeleteSO:
    def initCall(self,user):
        print("List of Sales Orders, Select id to delete the sales order list")
        self.listofso(user)

    def checkpositiveint(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveint(self.pint)
        return int(self.pint)


    def listofso(self,user):
        self.userid = user['user_id'][0]
        self.roleid = user['role_id'][0]
        if self.roleid == 1 or self.roleid == 2:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1"
        else:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1 and soh.created_by = "+ str(self.userid)
        try:
            cursor = conn.cursor()
            cursor.execute(str1)
            lst = cursor.fetchall()
            conn.commit()
            if len(lst)== 0:
                print("SO list is empty!!!")
                SalesModule().initCall(user)
            else:
                df= pd.DataFrame(lst)
                df.columns = ['SO_Id','SalesPerson','PaymentType','TotalAmount','BillDate']
                print(df)
                dup_sodetailedid = input('Enter SO_Id to delete the sales Order or 0.Go Back: \t')
                so_detailedid1 = self.checkpositiveint(dup_sodetailedid)
                if so_detailedid1 == 0:
                    SalesModule().initCall(user)
                else:
                    self.deleteso(so_detailedid1,user)
                    
                    

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header table {}".format(error))
            return SalesModule.initCall(user)
        finally:
            if conn.is_connected() :
                cursor.close()

    def deleteso(self,so_id,user):
        
        cursor = conn.cursor()
        cursor.execute("SELECT sohd.so_header_details_id,sohd.so_header_id,sohd.delete_status,sohd.quantity,sohd.inv_item_id FROM so_header_details sohd join users u on sohd.created_by = u.user_id where sohd.delete_status = 1 and sohd.so_header_id = "+str(so_id))
        lst = cursor.fetchall()
        conn.commit()
        cursor.close()
                        
        try:
            cursor = conn.cursor()
            query3 = 'update so_header set delete_status = 2 , updated_by = '+ str(user['user_id'][0]) +' , updated_on = now() where so_header_id = ' + str(so_id)
            cursor.execute(query3)
            conn.commit()
        
        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed updating record into inv_item table {}".format(error))
            return SalesModule().initCall(user)
        
        finally:
            if conn.is_connected() :
                cursor.close()
        
        if len(lst) > 0:
            for row in lst: 
                try:
                    cursor = conn.cursor()
                    query2 = 'update so_header_details set delete_status = 2 , updated_by = '+ str(user['user_id'][0]) +' , updated_on = now() where so_header_details_id = ' + str(row[0])
                    cursor.execute(query2)
                    conn.commit()
        
                except mysql.connector.Error as error:
                    conn.rollback()
                    print("Failed updating record into so_header_details table {}".format(error))
                    return SalesModule().initCall(user)
        
                finally:
                    if conn.is_connected() :
                        cursor.close()

                try:
                    cursor = conn.cursor()
                    query23 = 'update inv_item set item_quantity = (item_quantity + '+ str(row[3]) +' ), updated_by = '+ str(user['user_id'][0]) +' , updated_on = now() where inv_item_id = ' + str(row[4])
                    cursor.execute(query23)
                    conn.commit()
                except mysql.connector.Error as error:
                    conn.rollback()
                    print("Failed updating record into so_header_details table {}".format(error))
                    return SalesModule().initCall(user)
        
                finally:
                    if conn.is_connected() :
                        cursor.close()

            print("Deleted Successfully")
            return SalesModule().initCall(user)


class ViewSO:
    def initCall(self,user):
        print("List of Sales orders")
        self.listofso(user)
    
    def checkpositiveint(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveint(self.pint)
        return int(self.pint)
    
    def listofso(self,user):
        self.userid = user['user_id'][0]
        self.roleid = user['role_id'][0]
        if self.roleid == 1 or self.roleid == 2:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1"
        else:
            str1 = "SELECT soh.so_header_id,u.user_name,p.payment_mode_name,soh.total_amount,soh.created_on FROM so_header soh join users u on soh.created_by = u.user_id join payment_mode p on p.payment_mode_id = soh.payment_mode_id  where soh.delete_status = 1 and soh.created_by = "+ str(self.userid)
        try:
            cursor = conn.cursor()
            cursor.execute(str1)
            lst = cursor.fetchall()
            conn.commit()

            if len(lst)== 0:
                print("Sales order list is empty...")
                return SalesModule().initCall(user)

            else:
                df= pd.DataFrame(lst)
                df.columns = ['SO_Id','SalesPerson','PaymentType','TotalAmount','BillDate']
                print(df)
                dup_sodetailedid = input('Enter SO_Id to see the detailed view of sales Order or 0.Exit \t')
                so_detailedid1 = self.checkpositiveint(dup_sodetailedid)
                if so_detailedid1 == 0:
                    return SalesModule().initCall(user)
                else:
                    self.detailedso(so_detailedid1,user)

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header table {}".format(error))
            SalesModule.initCall(user)
        finally:
            if conn.is_connected() :
                cursor.close()

    def detailedso(self,so_id,user):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ii.item_name,sohd.quantity,sohd.discount,sohd.unit_price,sohd.total_price,u.user_name,sohd.created_on FROM so_header_details sohd join users u on sohd.created_by = u.user_id join inv_item ii on ii.inv_item_id = sohd.inv_item_id  where sohd.delete_status = 1 and sohd.so_header_id = "+str(so_id))
            lst = cursor.fetchall()
            conn.commit()
            if len(lst)==0:
                print("This sales order has no item!!!")
                self.listofso(user)
            else:
                df= pd.DataFrame(lst)
                df.columns = ['ItemName','Qty.','Discount(%)','UnitPrice','TotalPrice','SalesPerson','CreatedDate']
                print("List Of sales items!!!")
                print(df)
                print('\n')
                self.listofso(user)

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header_details table {}".format(error))
            self.listofso(user)
        
        finally:
            if conn.is_connected() :
                cursor.close()


class ItemwiseSales:
    def initCall(self,user):
        self.listofso(user)
    
    def listofso(self,user):
        try:
            cursor = conn.cursor()
            cursor.execute("select ii.inv_item_id,ii.item_name,sum(sohd.quantity) from so_header_details sohd join inv_item ii on ii.inv_item_id = sohd.inv_item_id group by ii.inv_item_id")
            lst = cursor.fetchall()
            conn.commit()
            if len(lst)==0:
                print("No Item has been sold!!!")
                self.listofso(user)
            else:
                df= pd.DataFrame(lst)
                df.columns = ['ItemId','ItemName','No.ofItemsSold']
                print("Item Wise Sales")
                print(df)
                return SalesModule().initCall(user)

        except mysql.connector.Error as error:
            conn.rollback()
            print("Failed Selecting record from so_header_details table {}".format(error))
            self.listofso(user)
        
        finally:
            if conn.is_connected() :
                cursor.close()


#user1 = {'user_id':{0:1,"type":"int"},'user_name':{0:"admin1","type":"string"},'role_id':{0:1,"type":"int"},'role_name':{0:"administrator","type":"string"}}
#user2 = {'user_id':{0:2,"type":"int"},'user_name':{0:"manager1","type":"string"},'role_id':{0:2,"type":"int"},'role_name':{0:"manager","type":"string"}}
#user3 = {'user_id':{0:3,"type":"int"},'user_name':{0:"user1","type":"string"},'role_id':{0:3,"type":"int"},'role_name':{0:"user","type":"string"}}

#sm = SalesModule()
#sm.initCall(user1)


       
