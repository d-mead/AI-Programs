import numpy as np
import math


def sig(i):
    return 1/(1+math.e**(-1*i))


def dsig(i):
    return (math.e**(-1*i))/((1+math.e**(-1*i) )**2)


def step(i):
    if i > 0:
        return 1
    else:
        return 0


A = np.vectorize(sig)

dA = np.vectorize(dsig)

w0 = np.matrix([[-1, -.5],
               [1, .5]])
b1 = np.matrix([[1, -1]])

w1 = np.matrix([[1, 2],
               [-1, -2]])
b2 = np.matrix([[-.5, .5]])

x = np.matrix([[2, 3]])
y = np.matrix([[.8, 1]])

# w0 = np.matrix([[1, -3],
#                [2, -1]])
# b1 = np.matrix([[-2, 5]])
#
# w1 = np.matrix([[1, -1],
#                [-2, 3]])
# b2 = np.matrix([[3, -1]])
#
# x = np.matrix([[0.8, 1]])
# y = np.matrix([[0, 1]])

# c1 = np.matrix([1, 1])
# c2 = np.matrix([1, 0])
# c3 = np.matrix([0, 1])
# c4 = np.matrix([0, 0])
#
# w0 = np.matrix([[1, 1], [-1, -1]])
# b1 = np.matrix([[-0.5, 1.5]])
#
# r1 = c1*w0 + b1
# r2 = c2*w0 + b1
# r3 = c3*w0 + b1
# r4 = c4*w0 + b1
#
# print(r1)
# print(r2)
# print(r3)
# print(r4)
#
# w1 = np.matrix([[-1, 0], [-1, 0]])
# b2 = np.matrix([[1.5, 0]])
#
# x = np.matrix([[1, 0]])
# y = np.matrix([[1]])
# #
# def back_prop(train_set):
#     count = 0
#     epoch = 0
#     layers = 2
#     while count < 10:
#         w0 = np.random.rand(2, 2)
#         b1 = np.random.rand(1, 2)
#         w1 = np.random.rand(2, 2)
#         b2 = np.random.rand(1, 2)
#         while epoch < 100:
#             for x, y in train_set:
#                 a0 = x
#                 dot1 = a0*w0 + b1
#                 a1 = A(dot1)
#                 dot2 = a1*w1 + b2


def check_xor(train_set):
    for x, y in train_set:
        dot1 = a0 * w0 + b1
        a1 = A(dot1)

        dot2 = a1 * w1 + b2
        a2 = A(dot2)






a0 = x

dot1 = a0*w0 + b1
a1 = A(dot1)
# print(a1)

dot2 = a1*w1 + b2
a2 = A(dot2)
# print(a2)

print(.5*(np.linalg.norm(y-a2))**2)

lamb = 0.1

err2 = np.multiply(dA(dot2), (y-a2))
err1 = np.multiply(dA(dot1), err2*np.transpose(w1))

b1 = b1 + lamb*err1*1
w0 = w0 + lamb*np.transpose(a0)*err1

b2 = b2 + lamb*err2*1
w1 = w1 + lamb*np.transpose(a1)*err2

a0 = x

dot1 = a0*w0 + b1
a1 = A(dot1)
# print(a1)

dot2 = a1*w1 + b2
a2 = A(dot2)
# print(a2)

print(.5*(np.linalg.norm(y-a2))**2)


