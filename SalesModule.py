def checkpositiveinteger(pint):
    if( pint.isdigit()== False):
        pint  = input("the number u have entered is not positive number,Enter your number")
        checkpositiveinteger(pint)
    else:
        print("proceed with the next one")
    return pint

dup_user_number  = input("Enter your number")
user_number = checkpositiveinteger(dup_user_number)
print(user_number, end='')
print(" next number")

lst = [user_number,165]

for item in range(len(lst)):
    print (lst[item])

def check(strng):
    if(strng == ''):
        strng = 0 
    return strng

lst = []

item_id = input("enter item id")
item_name = input("enter item name")
quantity = input("enter quantity")
discount = input("enter discount")
discount = check(discount)
unitprice = input("enter unit price")

lst.append({'itemid':item_id, 'itemname':item_name,'qty':quantity,'discount':discount,'uprice':unitprice})
lst.append({'itemid':'2', 'itemname':'coffee','qty':2,'discount':3,'uprice':4})

for elem in lst:
    print (elem['itemid'], elem['itemname'],elem['qty'],elem['uprice'],elem('discount'))

y_n = input()