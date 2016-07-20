import math
def adddig(num):
    if num == 0:
        return 0
    else:
        temp = num % 9
        return 9 if temp is 0 else temp

print(adddig(38))