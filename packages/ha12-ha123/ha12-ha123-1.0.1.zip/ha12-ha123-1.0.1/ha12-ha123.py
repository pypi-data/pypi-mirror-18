def smart(haha,level):
    for x in haha:
            if isinstance(x,list):
                smart(x,level+1)
            else:
                for y in range(level):
                    print("\t",end='')
                print(x)
