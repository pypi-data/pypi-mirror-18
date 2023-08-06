#function
"""print each element of the list,whether it has list"""
def print_lol(lists,level = 0):
    for l in lists:
        if isinstance(l,list):
            print_lol(l,level + 1)
        else:
            for tab_stop in range(level):
                print '\t',
            print l
listss = [1,2,[3,4],[5,6,[7,8]],9]

print print_lol(listss,0)
