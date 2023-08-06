'''simple test module to decend a multi level list
    user indicates if they require indentation by supplying True value'''

def procList(alist,indent=False,level=0):
    for item in alist:
        if isinstance(item,list):
            procList(item,True,level+1)
        else:
            if indent:
                for i in range(level):
                    print('\t',end=' ')
                print(item)




                    


            
     
            
