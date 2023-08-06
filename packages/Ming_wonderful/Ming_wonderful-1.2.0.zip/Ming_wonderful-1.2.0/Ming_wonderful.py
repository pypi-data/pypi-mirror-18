def print_a (self,indent = False,level = 0):
    for i in self:
        if isinstance(i,list):
            print_a(i,indent,level+1)
        else:
            if indent:
                for b in range(level):
                    print("\t", end='')
            print (i)
