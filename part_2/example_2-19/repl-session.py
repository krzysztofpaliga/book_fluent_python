import bisect
import random
SIZE = 7
random.seed(1729)
my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)
#
# 10 -> [10]
#  0 -> [0, 10]
#  6 -> [0, 6, 10]
#  8 -> [0, 6, 8, 10]
#  7 -> [0, 6, 7, 8, 10]
#  2 -> [0, 2, 6, 7, 8, 10]
# 10 -> [0, 2, 6, 7, 8, 10, 10]
