
def fizBuzz(x):
    if x % 15 == 0:
            return x , "fizbuzz"
    elif x % 3 == 0:
         return x, "fiz"
    elif x % 5 == 0:
        return x, "buz"
    else:
        return x, str(x)
def second_element(x):
     return x[1]
x = 0 
list = []
while x <101:
    x = x + 1 
    list.append (fizBuzz(x))
#list.sort(key=lambda x: x[1])
list.sort(key=second_element)
for a in list:
     print (a)