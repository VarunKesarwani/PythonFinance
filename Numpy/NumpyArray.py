import numpy as np

#Creating Numpy Array
lst1 = [1,2,3]
x= np.array(lst1)
print(type(x))
print(x)

#multi dimension array
my_matrix = [[1,2,3],[4,5,6],[7,8,9]]
y = np.array(my_matrix)
print(y)

#Arange
z= list(range(0,5))
print(type(z))
print(np.arange(0,5))
#print in gaps of 3: outPut [ 1  4  7 10]
print(np.arange(1,11,3))

#Zeros. it create float array with 0.0 as value
a = np.zeros(4)
print(a)
b = np.zeros((5,5))#rows and column
c = np.zeros((3,5))
print(c)

#once. it create float array with 1.0 as value
d = np.ones(5)
e = np.ones((3,5))
print(d)
print(e)

#linespace
#this give equally space value between start and stope
#0 is start and 10 is end value
#21 will give 20 equally spaced value between 0 and 10 since indexinf starts at 0
f = np.linspace(0,10,21)
print(f)

#has same number of rows and colume, and dialogs are 1.0
g = np.eye(4)
print(g)

#Random. there are lot of option in random; rand is just one of them
#rand uses uniform distribution over [0,1]
#uniform distribution says all number between 0 and 1 have probablity to be picked.
h = np.random.rand(5,4)
print(h)

#standard normal distribution
i = np.random.randn(5)
j = np.random.randn(5,4)
print(i)
print(j)

print(np.random.randint(1,100,6))

#Reshape
arr = np.arange(25)
print(arr)
print(arr.reshape(5,5))
#print(arr.reshape(3,5)) this will show error
print(arr.shape)
print(arr.reshape(25,1).shape)

#data type
print(arr.dtype)

arrm = np.random.randint(1,100,10)
print(arrm)
print(arrm.max())
print(arrm.argmax())
print(arrm.min())
print(arrm.argmin())
