import pandas 
from tabulate import tabulate

class InventoryModuleMenu:
  def __mainMuen__(self):
    print("=======================================================")
    print(tabulate([["1", "Item List"],["2","Add Item"],["3","Update Item"],["4","Delete Item"],["5","Logout"]], headers=['Id', 'Menu']))
    
  def __itemListMenu__(self):
    print("=======================================================")
    print(tabulate([["1", "All Item List"],["2","0 Quantity Item List"]], headers=['Id', 'Menu']))      
     

  

    

