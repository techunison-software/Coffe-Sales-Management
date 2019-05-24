import InventoryDAO as dao
from array import array
class Validataion:
    def __representsInt__(id):
        try:
            int(id)
            return True
        except ValueError as error:
            return False

    def __inputIdValidataion__(self,menu): 
        i=0 
        while i==0:     
            print("========================================================")       
            print("Enter Id")
            id=input()
            status=Validataion.__representsInt__(id)
            if status==True:
                if int(id)<=int(menu):                   
                    break;            
                else:
                    print("Enter input from 0 to "+str(menu))                    
            else:
                print("Enter valid ID")

        return id

    def __addItemValidation__(self):
        item =[]
        i = 0
        while i == 0:  
            item.insert(0,input("Enter Item Name : "))           
            #item[0]=input("Enter Item Name : ")            
            if not item[0]:
                print("Enter valid item name")
                i=0            
            else:
                break 
        while i==0 :
            item.insert(1,input("Enter Item Description : "))           
            if not item[1]:
                print('Enter valid item description')
            else:
                break          
        return item
    
    def __selectUpdateItem__(self):
        item_id=""
        i = 0
        while i == 0:  
            item_id=input("Enter Item Id : ")           
            if not item_id:
                print("Enter valid item Id")                           
            else:
                break
        return item_id

    def __addPORequestValidation__(self):
        po =[]
        i = 0        
        while i == 0:  
            po.insert(0,input("Enter Item id : "))  
            status=Validataion.__representsInt__(po[0])  
            if status==True:                       
                if not po[0]:
                    print("Error : Enter valid item id ")                              
                else:
                    break 
            else:
                print('Enter valid item id' )
        while i == 0:  
            po.insert(1,input("Enter quantity : "))  
            status=Validataion.__representsInt__(po[1])  
            if status==True:                       
               break 
            else:
                print('Enter valid quantity' )            
        return po

    def __enterUpdatePORequest__(self):
        poRequestId=""
        i=0
        while i==0:            
            poRequestId=input("Enter PO Request Id :")          
            status=Validataion.__representsInt__(poRequestId)  
            if status==True:                       
                if not poRequestId:
                    print("Error : Enter valid PO Request Id  ")                              
                else:
                    break
        return poRequestId 
                


