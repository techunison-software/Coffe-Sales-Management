import mysql.connector
from mysql.connector import Error


conn = mysql.connector.connect(host='192.168.1.128',port='3307',database='coffee',user='application',password='abc123!@#')
mycursor = conn.cursor()


class SalesModule:

    def initCall(self):
        self.dup_crud = input("1.Create Sales Order \t 2.Update Sales Order \t 3.Delete Sales Order \n Press number 1 or 2 or 3 \t")
        self.crud = self.checkpositiveinteger(self.dup_crud)
        if self.crud == 1:
            cso = CreateSO()
            cso.initCall()
        elif self.crud == 2:
            uso.initCall(self)
        elif self.crud == 3:
            dso.initCall(self)
        else:
            print("Please choose number from 1 to 3 \n")
            self.initCall()

    def checkpositiveinteger(self,posint):
        self.pint = posint
        if( self.pint.isdigit()== False):
            self.pint  = input("Not a number,Please enter number!!! \t")
            self.checkpositiveinteger(self.pint)
        return int(self.pint)
    
class CreateSO:
    
    def initCall(self):
        print("Welcome to Create Sales order Screen: \n")
        self.listitems()


    def listitems(self):
        mycursor.execute("SELECT ii.inv_item_id,ii.item_name,ii.item_quantity,ii.item_mrp_price,ii.item_max_discount FROM inv_item as ii where ii.item_quantity > 0 and ii.item_status = 1")
        lst = mycursor.fetchall()
        for row in lst:
            print("ItemId= ", row[0]," Name= ",row[1]," Qty= ", row[2]," MRP= ", row[3] ," Discount= ",row[4])
        self.createsalesorder(lst)
        
            
    def createsalesorder(self,lst):
        itemlist = lst
        itemid = self.getitemid(itemlist)
        qty = self.getquantity(itemlist,itemid)
        discount = self.getdiscount(itemlist,itemid)
        print(type(discount))

    def getitemid(self,lst):
        itemlist = lst
        dup_itemid = input("Choose ItemId from the list:\t")
        itemid1 = SalesModule.checkpositiveinteger(self,dup_itemid)
        itemid = self.checkiteminv(itemlist,itemid1)
        return itemid

    def getdiscount(self,lst,itemid):
        itemid = itemid
        itemlist = lst
        for row in itemlist:
            if itemid == row[0]:
                if row[4] == 0 or row[4] == None:
                    print("Your item has no discount!!!\t")
                    return 0

    def getquantity(self,lst,itemid):
        itemid = itemid
        itemlist = lst
        dup_quantity = input("Choose Quantity:\t")
        quantity1 = SalesModule.checkpositiveinteger(self,dup_quantity)
        quantity = self.checkquantity(itemlist,itemid,quantity1)
        return quantity

    def checkiteminv(self,lst,itemid):
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

    def checkquantity(self,lst,itemid,qty):
        ls = lst
        iid = itemid
        qty = qty

        for row in ls:
            if iid == row[0]:
                if qty < row[2] :
                    return qty
                else:
                    print("Quantity is Greater than available quantity!!!, ",end="")
                    return self.getquantity(ls,iid)
    
    #def checkdiscount(self,lst,itemid):
        





class UpdateSO:
    def initCall(self):
        print("Update so",end="")

class DeleteSO:
    def initCall(self):
        print("Delete SO",end="")

sm = SalesModule()
sm.initCall()


       
