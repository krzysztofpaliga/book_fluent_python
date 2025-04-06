from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))
floats[-1]
# 0.010349146937579157
floats[1]
# 0.5033180525827335
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()
floats2[-1]
floats2 == floats
# True
