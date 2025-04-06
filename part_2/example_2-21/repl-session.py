from array import array
numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
len(memv)
# 5
memv[0]
# -2
memv_oct = memv.cast('B')
memv_oct.tolist()
# [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
memv_oct[5] = 4
numbers
# array('h', [-2, -1, 1024, 1, 2])
memv_oct.tolist()
# [254, 255, 255, 255, 0, 4, 1, 0, 2, 0]
