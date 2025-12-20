SCORE = 0
def add_score(amount):
    global SCORE
    SCORE += amount
def compress(a): 
    sub=[0,0,0,0]
    i=0 
    for x in a: 
        if (x!=0):
             sub[i]=x 
             i+=1 
    return sub
def merge(a):
    for i in range(3):
        if a[i] == a[i + 1] and a[i] != 0:
            a[i] = a[i] * 2          
            add_score(a[i])          
            a[i + 1] = 0             
    return compress(a)
def combin(a):
    return merge(compress(a))
