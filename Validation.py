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

