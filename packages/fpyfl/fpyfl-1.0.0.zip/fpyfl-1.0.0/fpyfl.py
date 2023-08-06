def get_oushu():
    a=range(1,101)
    for x in a:
        if x % 2 == 1:
             a.remove(x)
    return a 
print get_oushu()