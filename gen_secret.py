import os
import getpass
from random import randint

if __name__ == "__main__":
    x = getpass.getpass("Password:")
    x = list(map(ord, x))
    xn = reduce(lambda ac, x: (ac<<8) + x, x)
    
    # gen dir
    os.system("mkdir -p secret")
    #os.system("touch secret/__init__.py")

    # gen key
    y = randint(0, (256**len(x))-1)
    f = open("secret/_secret.py", "w")
    f.writelines(["__key = %d"%(y,)])
    f.close()


    # gen cipher
    f = open("secret/_secret2.py", "w")
    f.writelines(["__cipher = %d"%(xn^y,)])
    f.close()

    # gen usage code
    f = open("secret/__init__.py", "w")
    f.write("""
from _secret import __key
from _secret2 import __cipher
def getPass():
    x = __key ^ __cipher
    arr = []
    while x:
        arr += [x&255]
        x >>= 8
    return "".join(map(chr, arr))[::-1]
        """)



