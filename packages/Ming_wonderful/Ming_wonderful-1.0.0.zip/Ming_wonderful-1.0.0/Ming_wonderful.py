def print_a (self,level=0):
    for i in self:
        if isinstance(i,list):
            print_a(i,level+1)
        else:
            for b in range(level):
                print("\t", end='')
            print (i)
