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

# w0 = np.matrix([[-1, -.5],
#                [1, .5]])
# b1 = np.matrix([[1, -1]])
#
# w1 = np.matrix([[1, 2],
#                [-1, -2]])
# b2 = np.matrix([[-.5, .5]])
#
# x = np.matrix([[2, 3]])
# y = np.matrix([[.8, 1]])

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


# x = np.matrix([[1, 0]])
# y = np.matrix([[1]])

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


train_set = [(np.matrix([0.0, 0.0]), np.matrix([0.0, 0.0])),
             (np.matrix([1.0, 0.0]), np.matrix([1.0, 0.0])),
             (np.matrix([0.0, 1.0]), np.matrix([0.0, 1.0])),
             (np.matrix([1.0, 1.0]), np.matrix([1.0, 1.0]))]

def back_prop(train_set):
    count = 0
    epoch = 0
    lamb = .05
    while count < 1:
        w0 = np.random.rand(2, 2)
        b1 = np.random.rand(1, 2)
        w1 = np.random.rand(2, 2)
        b2 = np.random.rand(1, 2)
        while epoch < 2500:
            print()
            for x, y in train_set:
                a0 = x
                dot1 = a0*w0 + b1
                a1 = A(dot1)
                dot2 = a1*w1 + b2
                a2 = A(dot2)

                delt2 = np.multiply(dA(dot2), (y-a2))
                delt1 = np.multiply(dA(dot1), delt2*np.transpose(w1))

                b1 = b1 + lamb * delt1*1
                w0 = w0 + lamb * np.transpose(a0)*delt1

                b2 = b2 + lamb * delt2 * 1
                w1 = w1 + lamb * np.transpose(a1) * delt2

                err = .5*(np.linalg.norm(y-a2))**2
                print(err)

            epoch += 1
        count += 1
    return w0, b1, w1, b2


def test_sum(w0, b1, w1, b2, train_set):
    for x, y in train_set:
        a0 = x
        dot1 = a0 * w0 + b1
        a1 = A(dot1)
        dot2 = a1 * w1 + b2
        a2 = A(dot2)

        print()
        print(a2)
        print(y)



w0, b1, w1, b2 = back_prop(train_set)

print()

test_sum(w0, b1, w1, b2, train_set)







# a0 = x
#
# dot1 = a0*w0 + b1
# a1 = A(dot1)
# # print(a1)
#
# dot2 = a1*w1 + b2
# a2 = A(dot2)
# # print(a2)
#
# # print(.5*(np.linalg.norm(y-a2))**2)
#
# lamb = 0.1
#
# err2 = np.multiply(dA(dot2), (y-a2))
# err1 = np.multiply(dA(dot1), err2*np.transpose(w1))
#
# b1 = b1 + lamb*err1*1
# w0 = w0 + lamb*np.transpose(a0)*err1
#
# b2 = b2 + lamb*err2*1
# w1 = w1 + lamb*np.transpose(a1)*err2
#
# a0 = x
#
# dot1 = a0*w0 + b1
# a1 = A(dot1)
# # print(a1)
#
# dot2 = a1*w1 + b2
# a2 = A(dot2)
# # print(a2)

# print(.5*(np.linalg.norm(y-a2))**2)





#  NUMBER 2
# w0 = np.matrix([[1, -1], [1, -1]])
# b1 = np.matrix([[-0.5, 1.5]])
#
# w1 = np.matrix([[1], [1]])
# b2 = np.matrix([[-1.5]])
#
# train_list = [(np.matrix([1, 1]), np.matrix([[0]])),
#               (np.matrix([1, 0]), np.matrix([[1]])),
#               (np.matrix([0, 1]), np.matrix([[1]])),
#               (np.matrix([0, 0]), np.matrix([[0]]))]
#
# for x, y in train_list:
#     a0 = x
#     dot1 = a0 * w0 + b1
#     a1 = A(dot1)
#
#     dot2 = a1 * w1 + b2
#     a2 = A(dot2)
#
#     if a2 == y:
#         print(x, ": ", a2, ": Passed")


