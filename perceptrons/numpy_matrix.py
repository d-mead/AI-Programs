import numpy as np

x = np.matrix([[1, 2],
               [3, 4]])
y = np.matrix([[2, 3],
               [4, 5]])

print(x + y)               # adds each element together
print(x * y)               # math matrix multiplication
print(np.multiply(x, y) + 1)   # multiplies each corresponding elements
print(np.multiply(x, y))
print(4*x)                 # mutliplies each element by 4
print(x.transpose())       # makes the cols rows and visa-versa
print(x[0, 1])             # prints the 0th row, 1st col
print(y[1, 1])             # prints 1st row, 1st col

def ex_f(x):
    return x**2 + 1

vec_f = np.vectorize(ex_f)

print(vec_f(x))

print(np.linalg.norm(np.matrix([[1, -1]])))
print(np.linalg.norm(np.matrix([[-3, 4]])))