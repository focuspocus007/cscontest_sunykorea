from time import time

s = time()
while(True):
    if (time() - s >= 1):
        s = time()
        print(s)