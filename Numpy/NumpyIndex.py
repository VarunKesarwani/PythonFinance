import numpy as np

arr = np.arange(0,11)

print(arr)
print(arr[2])
print(arr[2:5]) #Output: [2 3 4]

print(arr[:4]) #Output: [0 1 2 3]
print(arr[5:]) #Output: [ 5  6  7  8  9 10]

#boardcast
arr[0:4] = 50
print(arr) #Output : [50 50 50 50  4  5  6  7  8  9 10]

arr2 = np.arange(0,11)
slice_of_arr = arr2[0:6]
print(slice_of_arr)
slice_of_arr[:] = 99
print(slice_of_arr)
print(arr2)

arr_copy = arr2.copy()
arr_copy[:] = 200
print(arr_copy)
print(arr2)

#matrix index
#mat[row,col]
#mat[row][col]
mat = np.array([[23,54,76],[52,12,65],[67,34,48]])
print(mat)
print(mat[0])#get all elememt in row 0
print(mat[2])#get all elememt in row 2
print(mat[2][2])#get all elememt in row 0 and col 2
print(mat[2,2])#get all elememt in row 0 and col 2

#Slice mat
mat_slice = mat[:2,1:]
print(mat_slice)
mat_slice2 = mat[1:,:2]
print(mat_slice2)

#conditional selection
arr3 = np.arange(0,11)
print(arr3 > 4)
#output [False False False False False  True  True  True  True  True  True]

bool_arr = arr3 > 4
print(arr3[bool_arr])# return all value when index is true
#output [ 5  6  7  8  9 10]

print(arr3[arr3>4])
#output [ 5  6  7  8  9 10]