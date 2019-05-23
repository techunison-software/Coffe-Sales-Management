import pandas 
from tabulate import tabulate

class InventoryModuleMenu:
  def __mainMuen__(self):
    print("=======================================================")
    print(tabulate([["1", "Item List"],["2","Add Item"],["3","Update Item"],["4","Delete Item"],['5','PO Request'],['6','Report'],["7","Logout"]], headers=['ID', 'MENU']))
    
  def __itemListMenu__(self):
    print("=======================================================")
    print(tabulate([["1", "All Item List"],["2","0 Quantity Item List"]], headers=['ID', 'MENU']))

  def __poMenuList__(self):
    print('=======================================================')
    print(tabulate([['1','PO Request List'],['2','New PO Request'],['3','Update PO Request'],['4','Delete PO Request'],['5','Report']], headers=['ID','MENU']))      
  
  def __poRequestListMenu__(self):
    print("=======================================================")
    print(tabulate([['1','All PO Request List'],['2','Purchased PO Request List'],['3','Pending PO Request List']],headers=['ID','MENU']))

  

    

