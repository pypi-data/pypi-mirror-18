#function
"""print each element of the list,whether it has list"""
def print_lol(lists):
    for l in lists:
        if isinstance(l,list):
            print_lol(l)
        else:
            print l
