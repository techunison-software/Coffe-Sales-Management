import mysql.connector
from mysql.connector import Error
import pandas as pd

conn = mysql.connector.connect(host='192.168.1.128',port='3307',database='coffee',user='application',password='abc123!@#')
mycursor = conn.cursor()

global soitemlst
soitemlst = []

class SalesModule:
    def initCall(self):
        self.dup_crud = input("1.Create Sales Order \t 2.Update Sales Order \t 3.Delete Sales Order 4.View Sales Orders 0.Exit \n Press number 1 or 2 or 3 or 4 or 0:\t")
        self.crud = self.checkpositiveinteger(self.dup_crud)
        if self.crud == 1:
            cso = CreateSO()
            cso.initCall()
        elif self.crud == 2:
            uso = UpdateSO()
            uso.initCall(self)

        elif self.crud == 3:
            dso= DeleteSO()
            dso.initCall(self)

        elif self.crud==4:
            vso = ViewSO()
            vso.initCall(self)
        #elif self.crud == 0:

        else:
            print("Please choose correct number!!!\n")
            self.initCall()

    def checkpositiveinteger(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveinteger(self.pint)
        return int(self.pint)
    
class CreateSO:

    def initCall(self):
        print("Welcome to Create Sales order Screen: \n")
        self.listitems()
        #SalesModule.initCall()

    def checkpositiveint(self,posint):
        self.pint = posint
        if self.pint.isdigit()== False:
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveint(self.pint)
        return int(self.pint)

    def listitems(self):
        mycursor.execute("SELECT ii.inv_item_id,ii.item_name,ii.item_quantity,ii.item_mrp_price,ii.item_max_discount FROM inv_item as ii where ii.item_quantity > 0 and ii.item_status = 1")
        lst = mycursor.fetchall()
        for row in lst:
            print("ItemId= ", row[0]," Name= ",row[1]," Qty= ", row[2]," MRP= ", row[3] ," Discount= ",row[4])
        self.createsalesorder(lst,0)


    def additem(self,lst):
        itemlist = lst
        invitem= []
        itemid = self.getitemid(itemlist)
        quantity = self.getquantity(itemlist,itemid)
        discount = self.getdiscount(itemlist,itemid)
        unitprice = self.getuprice(itemlist,itemid)
        totalprice = self.gettprice(itemid,discount,unitprice,quantity)
        print("Item "+ str(itemid) + " is added")
        invitem.append({'inv_item_id':itemid,'quantity':quantity,'discount':discount,'unit_price':unitprice,'total_price':totalprice})
        return invitem

    def paymenttransaction(self,lst):
        dup_totalamount = 0
        dup_payid = input("Welcome to Payment screen.. 1.Cash 2.Credit/Debit Card 3.UPI 0.Go back \n Press number 1 or 2 or 3 or 0:\t")
        payid1 = self.checkpositiveint(dup_payid)
        payid = self.checkpayid(payid1,lst)
    
        for elem in soitemlst:
            dup_totalamount += elem['total_price']
        totalamount = dup_totalamount
        print(type(totalamount))
        
        sql_insert_query = 'insert into so_header(created_by,total_amount,payment_mode_id,created_on) values (1,'+ str(totalamount) +','+ str(payid) +',now())'
        print(sql_insert_query)
        cursor = conn.cursor()
        result  = cursor.execute(sql_insert_query)
        conn.commit()
        print ("Record inserted successfully into python_users table")
        return result

    def createsalesorder(self,ls,mode):
        lst = ls
        cond = 1

        if mode == 0:
            te= self.additem(lst)
            soitemlst.append({'inv_item_id':te[0]['inv_item_id'],'quantity':te[0]['quantity'],'discount':te[0]['discount'],'unit_price':te[0]['unit_price'],'total_price':te[0]['total_price']})

        if mode == 1:
            print("Items in your cart!!!")
            print(pd.DataFrame(soitemlst))
            
        while True:
            dup_ifs = input("1.Add Item \t 2.Delete existing Item \t 3.Proceed for payment 4.View Items in cart \t 0.Exit \n Press number 1 or 2 or 3 or 0:\t")
            ifs = self.checkpositiveint(dup_ifs)

            if ifs == 1 :
                te= self.additem(lst)
                soitemlst.append({'inv_item_id':te[0]['inv_item_id'],'quantity':te[0]['quantity'],'discount':te[0]['discount'],'unit_price':te[0]['unit_price'],'total_price':te[0]['total_price']})
                

            elif ifs == 2:
                self.deletesoitem()

            elif ifs == 3:
                parent = self.paymenttransaction(lst)
                
            elif ifs == 4:
                self.getcartitems()

            elif ifs == 0:
                SalesModule().initCall()
                

            #else:
                #cond = 0
    
    def deletesoitem(self):
        itemlist = soitemlst
        dup_item_id = input("Choose the ItemId to delete:\t")
        itemid1 = self.checkpositiveint(dup_item_id)
        itemid = self.checkdeleteitem(itemlist,itemid1) 


    def getcartitems(self):
        print("Items in your cart!!!")
        df= pd.DataFrame(soitemlst)
        df.columns = ['ItemId','Qty.','UnitPrice','Discount','TotalPrice']
        print(df[['ItemId','Qty.','UnitPrice','Discount','TotalPrice']])

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

    def getitemid(self,lst):
        itemlist = lst
        dup_itemid = input("Choose ItemId:\t")
        itemid1 = self.checkpositiveint(dup_itemid)
        itemid = self.checkitem(itemlist,itemid1)
        return itemid

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

    def checkitem(self,lst,itemid):
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
            return self.getitemid(ls)
        
    def checkpayid(self,pid,ls):
        lst = ls
        payid = pid
        if payid == 1 or payid == 2 or payid == 3:
            return int(payid)
        elif payid == 0:
            return self.createsalesorder(lst,1)
        else: 
            print("Payment ID is Wrong!!!, ",end="") 
            return self.getitemid(payid,lst)         

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
        


class UpdateSO:
    def initCall(self):
        print("Update so",end="")

class DeleteSO:
    def initCall(self):
        print("Delete SO",end="")

class ViewSO:
    def initCall(self):
        print("List of Sales orders",end="")

sm = SalesModule()
sm.initCall()


       
