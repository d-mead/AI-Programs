# David Mead April 1st, 2019
from itertools import product
import time
import math
import matplotlib.pyplot as plt
import random
import numpy as np
from numpy import array
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

x_vals = []
y_vals = []
z_vals = []


def main():
    bits = 2
    num = 4
    print(bits, num)
    pretty_print_tt(truth_table(bits, num))
    # inputs = format_inputs()
    # # my_w = [0.3460277080149674, 0.9997888285131714, 1.0005258903466563, -1.9989396917190063, -1.0005259606396537, 1.0003389382002976, -2.0003296718447157, 1.000646057344232, -1.0001337215377093, -2.0005333190191514, -0.9994063343391223, -1.0004777223891832, -1.9996298209562562, -1.9999131963913226, -2.0002401945753445, -2.000127788318436, -2.000832275569176, 0.49965774720918443, -1.2004849448493655]
    # my_w = [.33, 1, 1, -2, -1, 1, -2, 1, -1, -2, -1, -1, -2, -2, -2, -2, -2, .5, -1.2]
    # #[0.3460277080149674, 1, 1, -2, -1, 1, -2, 1, -1, -2, -1, -1, -2, -2, -2, -2, -2, .5, -1.2004849448493655]
    # network = 0
    # print(error(network, inputs, my_w))
    # three_chart(network, inputs, 5, my_w)
    # print(hill_climb(network, inputs, 10, my_w))
    # print(minimize(1, 1))
    # print(one_d_minimize(f_s, -1, 0, 10**-8))
    # start = time.perf_counter()
    # print(grad_desc_w_line_search(f_1, grad_f_1, (0, 0), 10 ** -8))
    # print(time.perf_counter()-start)
    # start = time.perf_counter()
    # print(grad_desc_w_line_search(f_2, grad_f_2, (0, 0), 10**-8))
    # print(time.perf_counter()-start)
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # # ax = fig.add_subplot(111, projection='3d')
    #
    # # x_vals, y_vals = np.meshgrid(x_vals, y_vals)
    #
    # zs = array(z_vals)
    #
    # ax.plot_trisurf(x_vals, y_vals, z_vals)
    #
    # print(x_vals)
    # print(y_vals)
    # print(z_vals)
    #
    # plt.show()

    # start = time.perf_counter()
    # draw_plot_unit_circle()
    # print("run time:\t\t", time.perf_counter()-start)


def grad_desc_w_line_search(f, grad_f, start, tol):
    location = start
    lmda = 0
    while mag(grad_f(location)) > tol:
        direction = grad_f(location)
        closed_f = make_f_c(f, location, direction)
        if lmda != 0:
            left = lmda/2
            right = lmda*2
        else:
            left = 0
            right = 1

        lmda = one_d_minimize_s(closed_f, left, right, 10**-8, 10, -1)
        # print(location, lmda)
        location = tuple([l-lmda*d for l, d in zip(location, direction)])
    return location


def one_d_minimize(f, left, right, tol):
    if right-left < tol:
        return (left+right)/2
    one = left + (1/3)*(right-left)
    two = left + (2/3)*(right-left)
    if f(one) > f(two):
        return one_d_minimize(f, one, right, tol)
    else:
        return one_d_minimize(f, left, two, tol)


def one_d_minimize_s(f, left, right, tol, sim, fs):
    if right-left < tol:
        return (left+right)/2
    if sim > right:
        one = left + (1 / 3) * (right - left)
        two = left + (2 / 3) * (right - left)
        fo = f(one)
        ft = f(two)
    elif sim > (left+right)/2:
        one = left + (1 / 3) * (right - left)
        two = sim
        fo = f(one)
        ft = fs
    else:
        one = sim
        two = left + (2 / 3) * (right - left)
        fo = fs
        ft = f(two)

    if fo > ft:
        return one_d_minimize_s(f, one, right, tol, two, ft)
    else:
        return one_d_minimize_s(f, left, two, tol, one, fo)


def grad_f_1(loc):
    x = loc[0]
    y = loc[1]
    return dx_1(x, y), dy_1(x, y)


def grad_f_2(loc):
    x = loc[0]
    y = loc[1]
    return dx_2(x, y), dy_2(x, y)


def make_f_c(f, location, direction):
    def funct(x):
        return f(tuple([l-x*d for l, d in zip(location, direction)]))
    return funct


def make_f(a, b):
    def funct(x):
        return a*x + b
    return funct


def mag(w2):
    return (w2[0] ** 2 + w2[1] ** 2) ** .5


def f_2(loc):
    x = loc[0]
    y = loc[1]
    return (1-y)**2 + 100*((x-y**2)**2)


def dx_2(x, y):
    return 200*(x-y**2)


def dy_2(x, y):
    return 2*(-200*x*y + 200*(y**3) + y - 1)


def f_1(loc):
    x = loc[0]
    y = loc[1]
    return 4*(x**2) - 3*x*y + 2*(y**2) + 24*x - 20*y


def dx_1(x, y):
    return 8 * x - 3 * y + 24


def dy_1(x, y):
    return 4 * (y - 5) - 3 * x


def f_s(x):
    return math.sin(x) + math.sin(3*x) + math.sin(4*x)


def minimize(x, y):
    lamb = .00001
    grad = (dx(x, y), dy(x, y))
    w2 = (lamb * grad[0], lamb * grad[1])
    x += w2[0]
    y += w2[1]
    print(mag(w2))
    while True:#mag(w2) > 1.001:
        print(x ,y, mag(w2))
        grad = (dx(x, y), dy(x, y))
        w2 = (lamb * grad[0], lamb * grad[1])
        x += w2[0]
        y += w2[1]
        # print(x, y, mag(w2))
    return x, y





# 10 [0.3460372843455998, 1.000349541235336, 1.0001277862421012, -1.999084791035572, -1.000391565282702, 1.0008452695906376, -1.999908918210447, 1.0009670215287199, -1.000032307245475, -2.000638942263174, -0.9993181858304734, -0.9999927065351633, -2.0000361669305953, -2.0000202279205554, -2.0008583715003927, -1.9997871258770146, -2.001205400374133, 0.49962789100852056, -1.2006107079954722]
# 9 [0.3460277080149674, 0.9997888285131714, 1.0005258903466563, -1.9989396917190063, -1.0005259606396537, 1.0003389382002976, -2.0003296718447157, 1.000646057344232, -1.0001337215377093, -2.0005333190191514, -0.9994063343391223, -1.0004777223891832, -1.9996298209562562, -1.9999131963913226, -2.0002401945753445, -2.000127788318436, -2.000832275569176, 0.49965774720918443, -1.2004849448493655]
# plots the linear separation of a binary perceptron
# returns nothing, shows a color coded plot
def draw_plot(bits, num):
    plt.axis([-2, 2, -2, 2])
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.gca().set_aspect('equal', adjustable='box')

    w, b = training_return_result(bits, num)

    color = {1: 'green', 0: 'red'}

    reds_x = []
    reds_y = []
    greens_x = []
    greens_y = []

    for x in range(-20, 21):
        for y in range(-20, 21):
            if (x / 10, y / 10) in {(1, 1), (1, 0), (0, 1), (0, 0)}:
                plt.plot(x / 10, y / 10, 'ro', color=color.get(perceptron(the_func, w, b, (x / 10, y / 10))))
            elif color.get(perceptron(the_func, w, b, (x / 10, y / 10))) == 'red':
                reds_x.append(x / 10)
                reds_y.append(y / 10)
            else:
                greens_x.append(x / 10)
                greens_y.append(y / 10)

    pretty_print_tt(truth_table(bits, num))

    plt.plot(reds_x, reds_y, '.', color='red')
    plt.plot(greens_x, greens_y, '.', color='green')

    plt.show()


def format_inputs():
    xs = []
    ys = []
    f = open("ten_thou.txt", "r")
    fl = f.readlines()
    for line in fl:
        x = float(line[0:line.index(' ')])
        y = float(line[line.index(' ') + 1:len(line)])
        xs.append(x)
        ys.append(y)

    return list(zip(xs, ys))

# 6108 [0.49121190531917547, -0.8167678153106261, 0.4358652355608621, 0.3032921817233445, -0.3072201306144964, 0.3916372246547526, -0.04940550028042234, -0.22866661168664604, -0.27165486194111876, -0.22090692541499446, -0.8519557044539452, -0.2957014253879009, 0.4608800742218795, -0.6478964565802927, 0.7007024643387032, -0.8364934824516979, -0.04653535747778381, -0.2980101751853339, 0.7182878116990132]
# 4747 good [0.04478149739951087, 0.8482291105590045, -0.19310319407068421, 0.14293343258820745, -0.3433142427697775, -0.6180685350282626, 0.14128351844515197, -0.15432890311304348, -0.03120853754884867, 0.06554264923365483, -0.3837239369953209, -0.5243249378214565, 0.6026106217042795, 0.43956280425068806, -0.8481420142343901, -0.2939219201011747, 0.08717812049419127, 0.6208754242489121, 0.8846093393262684]
# 162 [0.5557913264563648, 0.4860984200214829, 0.659168904938611, 0.7959517556295718, -0.7025398173898303, -0.20525496954470313, 0.6848034298131613, -0.41549201424134113, -0.6341625952341636, 0.3506951263732535, 0.3698144907892851, -1.0156796341154788, 0.9269212379035904, 0.4063572806274616, 0.7834393955961328, -0.40340517047360264, 0.5277066474477738, -0.45458689999660606, 0.2006755943973839]

def hill_climb(network, inputs, epsilon, start_w):
    count = 0

    while count < 100:
        print("COUNT", count)
        # w = [-0.4631476066828972, 0.8894448189093602, -0.05582210439635926, 0.4263360900558171, 0.227224233730719, 0.018002880599842883, 0.8080867106736382, 0.43099360503532425, 0.07922437437304997, 0.0950904121672474, -0.6360945790105424, -0.4235137250438644, 0.5713538993984757, -0.1467844322077114, -0.09281234942405195, 1.1817572245338555, 0.858216498821759, -0.5520127378744439, 0.6160810052236956]
        # w = [0.5557913264563648, 0.4860984200214829, 0.659168904938611, 0.7959517556295718, -0.7025398173898303, -0.20525496954470313, 0.6848034298131613, -0.41549201424134113, -0.6341625952341636, 0.3506951263732535, 0.3698144907892851, -1.0156796341154788, 0.9269212379035904, 0.4063572806274616, 0.7834393955961328, -0.40340517047360264, 0.5277066474477738, -0.45458689999660606, 0.2006755943973839]
        w = random_vector(19)
        er = error_o(network, inputs, w)
        while er == 3504 or er == 6496:# or er > 4000:
            w = random_vector(19)
            er = error_o(network, inputs, w)
            print("error:", er)
        # w = start_w#[s + .1*a for s, a in zip(start_w, random_vector(19))]#random_vector(19)#
        still_progress = True
        count_fails = 0
        old_error = er#ror_o(network, inputs, w)
        # print(old_error, w)
        print("O", 'error', 'lamb', 'fails', 'sec/fail', 'weights vector', sep='\t')
        while still_progress:
            start = time.perf_counter()
            if old_error > 3000:
                lamb = .1
            elif old_error > 1000:
                lamb = .1
            elif old_error > 200:
                lamb = .005
            elif old_error > 30:
                lamb = .0025
            else:
                lamb = .00025
            rand = random_vector(19)
            delta_w = [lamb * r for r in rand]
            w2 = [a+d for a, d in zip(w, delta_w)]
            new_error = error_o(network, inputs, w2)
            old_error = error_o(network, inputs, w)

            # x_vals.append(w[0])
            # y_vals.append(w[18])
            # z_vals.append(new_error)
            # print(new_error, w)

            if new_error <= old_error:
                w = w2
                print("O", new_error, str(lamb)+' ', str(count_fails)+'   ', round((time.perf_counter()-start)/(count_fails+1), 7), w2, sep='\t')
                # count_fails = 0
                # count_fails += 1
                if new_error == 3504:
                    break
                if new_error <= epsilon:
                    return w2

            if old_error <= new_error:
                # print("X", new_error, lamb, count_fails, w2)
                if count_fails > 1000:
                    still_progress = False
                count_fails += 1
            else:
                count_fails = 0
            # print(count_fails)
        count += 1
    return False


def three_chart(network, inputs, epsilon, start_w):
    count = 0
    # while count < 100:
    #     print("COUNT", count)
    # w = start_w
    # still_progress = True
    # count_fails = 0
    # old_error = error_o(network, inputs, w)
    a = 20
    div = 10
    for xx in range(-a, a):
        for yy in range(-a, a):
            x = .3 + (xx/100)#.346 + (xx/10000)
            y = -.5 + (yy/100)#-1.20 + (yy/1000)
            w = [x] + [1, 1, -2, -1, 1, -2, 1, -1, -2, -1, -1, -2, -2, -2, -2, -2, .5] + [y]
            err = error_o(network, inputs, w)

            x_vals.append(x)
            y_vals.append(y)

            # if err > 1000:
            #     err = 1000
            z_vals.append(-err)

            print((xx+a)*2*a + (yy+a))
            # print(x, y, err)
    return False

e_dict = {}
def error(network, inputs, weights):
    if tuple(weights) in e_dict.keys():
        return e_dict[tuple(weights)]
    thresh = weights[0]#.346325

    error = 0

    for x, y in inputs:
        result = asses_inputs_weights(x, y, weights)
        error += wrong(x, y, result, thresh)

    e_dict[tuple(weights)] = error
    return error


def error_o(network, inputs, weights):
    if tuple(weights) in e_dict.keys():
        return e_dict[tuple(weights)]
    thresh = 1/(1+math.e**(-1*weights[0]))  # .346325

    error = 0

    for x, y in inputs:
        result = asses_inputs_weights(x, y, weights)
        error += wrong_o(x, y, result, thresh)

    e_dict[tuple(weights)] = error
    return error


def wrong(x, y, result, thresh):
    if in_unit_circle(x, y):
        return 1/((result-thresh))**2
        # if result > thresh:
        #     return 0
        # else:
        #     return 1
    else:
        return 1/((result - thresh)) ** 2
        # if result > thresh:
        #     return 1
        # else:
        #     return 0


def wrong_o(x, y, result, thresh):
    if in_unit_circle(x, y):
        # return (1-(result-thresh))**2
        if result > thresh:
            return 0
        else:
            return 1
    else:
        # return (0 - (result - thresh)) ** 2
        if result > thresh:
            return 1
        else:
            return 0


def random_vector(size):
    # return [(random.random()-.5)*2] + [0]*17 +[(random.random()-.5)*2, (random.random()-.5)*2]
    return [(random.random() - .5) * 2 for x in range(0, size)]

# def random_vector(size):
#     # return [random.randint(-2, 2) for x in range(0, size)]
#     return [(random.random()-.5)*2]
#     return [(random.random() - .5) * 2 for x in range(0, size)]


my_w = [.346325, 1, 1, -2, -1, 1, -2, 1, -1, -2, -1, -1, -2, -2, -2, -2, -2, .5, -1.2]


def asses_inputs_weights(x, y, w):
    w13 = w[1]
    w23 = w[2]
    b3 =  w[3]

    w14 = w[4]
    w24 = w[5]
    b4 = w[6]

    w15 = w[7]
    w25 = w[8]
    b5 = w[9]

    w16 = w[10]
    w26 = w[11]
    b6 = w[12]

    w37 = w[13]
    w47 = w[14]
    w57 = w[15]
    w67 = w[16]
    b7 = w[17]
    k = (w[18]+1)*2

    r3 = perceptron_k(sigmoid_func_k, (w13, w23), b3, (x, y), k)
    r4 = perceptron_k(sigmoid_func_k, (w14, w24), b4, (x, y), k)
    r5 = perceptron_k(sigmoid_func_k, (w15, w25), b5, (x, y), k)
    r6 = perceptron_k(sigmoid_func_k, (w16, w26), b6, (x, y), k)

    r7 = perceptron_k(sigmoid_func_k, (w37, w47, w57, w67), b7, (r3, r4, r5, r6), k)

    return r7


percep_dict = {}

def perceptron_k(A, w, b, x, k):
    # if (w, b, x, k) in percep_dict.keys():
    #     return percep_dict[(w, b, x, k)]
    vector_prod = sum([x[0]*x[1] for x in zip(w, x)]) + b
    result = A(vector_prod, k)
    # percep_dict[(w, b, x, k)] = result
    return result


def sigmoid_func_k(num, k):
    return 1/(1 + math.e**(k * num))


# constructs a plot, tests unit circle points on the net
# returns nothing, shows a matplotlib plot of the color coded results
def draw_plot_unit_circle():
    plt.axis([-2, 2, -2, 2])
    # plt.plot(1, 1, '.', color='blue', )
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.gca().set_aspect('equal', adjustable='box')

    colors_dict = {'darkblue': ([], []), 'darkgreen': ([], []), 'lightgreen': ([], []), 'lightblue': ([], [])}

    thresh = .346325

    # # use this to to all points from -2 to 2 at 1/mult invervals
    # mult = 50
    # for x in range(-2*mult, 2*mult+1):
    #     for y in range(-2*mult, 2*mult+1):
    #         result = asses_inputs(x/mult, y/mult)#perceptron(the_func, w, b, (x / 10, y / 10))
    #         the_color = assign_color(x/mult, y/mult, result, thresh) # .361825)
    #         colors_dict.get(the_color)[0].append(x / mult)
    #         colors_dict.get(the_color)[1].append(y / mult)

    # use this chunk instead if you want to test on 1000 random points
    xs, ys = random_1000()
    for x, y in zip(xs, ys):
        result = asses_inputs(x, y)
        the_color = assign_color(x, y, result, thresh)
        colors_dict.get(the_color)[0].append(x)
        colors_dict.get(the_color)[1].append(y)

    total = 0
    good = 0
    for color, xy in colors_dict.items():
        plt.plot(xy[0], xy[1], '.', color=color)
        total += len(xy[0])
        if 'dark' in color:
            good += len(xy[0])
        print(color, "\t\t", len(xy[0]))

    print("% correct:\t\t", 100-(((total-good)/total)*100))
    print("% error:\t\t", (((total-good)/total)*100))

    plt.show()


# generates 1000 random coordinates
# returns a list of x values and y values
def random_1000():
    xs = []
    ys = []
    f = open("ten_thou.txt", "r")
    fl = f.readlines()
    for line in fl:
        x = float(line[0:line.index(' ')])
        y = float(line[line.index(' ')+1:len(line)])
        xs.append(x)
        ys.append(y)

    # xs = [random.random() * 4 - 2 for i in range(0, 1000)]
    # ys = [random.random() * 4 - 2 for i in range(0, 1000)]
    return xs, ys


# takes the input coordinates and runs them through the 2 layer net
# retuns a decimal value from 0 to 1
def asses_inputs(x, y):
    w13 = 1
    w23 = 1
    b3 = -2

    w14 = -1
    w24 = 1
    b4 = -2

    w15 = 1
    w25 = -1
    b5 = -2

    w16 = -1
    w26 = -1
    b6 = -2

    w = -2
    w37 = w
    w47 = w
    w57 = w
    w67 = w
    b7 = .5

    r3 = perceptron(sigmoid_func, (w13, w23), b3, (x, y))
    r4 = perceptron(sigmoid_func, (w14, w24), b4, (x, y))
    r5 = perceptron(sigmoid_func, (w15, w25), b5, (x, y))
    r6 = perceptron(sigmoid_func, (w16, w26), b6, (x, y))

    r7 = perceptron(sigmoid_func, (w37, w47, w57, w67), b7, (r3, r4, r5, r6))

    return r7


# tried to make the 2 perceptron 'clever' net
# returns the final result (1 or 0)
def asses_inputs_2(x, y):
    wx1 = 1
    wy1 = 0
    b1 = 0

    wx2 = 0
    wy2 = 1
    b2 = 0

    w13 = 1
    w23 = 1
    b3 = -1

    r1 = perceptron(square, (wx1, wy1), b1, (x, y))
    r2 = perceptron(square, (wx2, wy2), b2, (x, y))

    r3 = perceptron(the_func_i, (w13, w23), b3, (r1, r2))

    return r3


# the activiation function for the 'clever' net
def square(num):
    return num**2


# asses function from when I tried to train the last perceptron
def asses_inputs_3(x, y, w7x, b7):
    w13 = 1
    w23 = 1
    b3 = -2

    w14 = -1
    w24 = 1
    b4 = -2

    w15 = 1
    w25 = -1
    b5 = -2

    w16 = -1
    w26 = -1
    b6 = -2

    w37, w47, w57, w67 = w7x

    r3 = perceptron(sigmoid_func, (w13, w23), b3, (x, y))
    r4 = perceptron(sigmoid_func, (w14, w24), b4, (x, y))
    r5 = perceptron(sigmoid_func, (w15, w25), b5, (x, y))
    r6 = perceptron(sigmoid_func, (w16, w26), b6, (x, y))

    r7 = perceptron(sigmoid_func, (w37, w47, w57, w67), b7, (r3, r4, r5, r6))

    return r7


# takes an x and y position as well as a result (from the perceptron) and determines the color
# returns the color name as a string
def assign_color(x, y, result, base):
    if in_unit_circle(x, y):
        if result > base:
            return 'darkgreen'
        else:
            return 'lightgreen'
    else:
        if result > base:
            return 'lightblue'
        else:
            return 'darkblue'


# determines if a number is within the unit circle
# returns True or False
def in_unit_circle(x, y):
    return (x**2 + y**2)**.5 <= 1


# applies the sigmoid function to the input number
# returns a decimal 0 to 1
def sigmoid_func(num):
    return 1/(1 + math.e**(-1.2 * num))


# trains a perceptron to match the input integer representation for the input bits
# returns the accuracy of the final perceptron from 0 to 1 (decimal)
def training(bits, n):
    table = truth_table(bits, n)
    w = tuple([0]*bits)
    b = 0
    w_prev, b_prev = w, b
    for epoch in range(0, 100):
        for x, y in table:
            y_star = perceptron(the_func, w, b, x)
            err = y-y_star
            w = tuple((w + err*x) for (w, x) in zip(w, x))
            b += err
        if w == w_prev and b == b_prev:
            break
        w_prev, b_prev = w, b

    return check(n, w, b)


# function to train the last perceptron to the unit circle
# returns the weights vector and scalar
def train_circle():
    w = tuple([-2]*4)
    b = .5
    w_prev, b_prev = w, b
    mult = 20
    for epoch in range(0, 100):
        for x in range(-2 * mult, 2 * mult + 1):
            for y in range(-2 * mult, 2 * mult + 1):
                ins = get_four_outs(x, y)
                y_star = perceptron(sigmoid_func, w, b, ins)
                err = in_unit_circle(x, y)-(y_star-.5)
                w = tuple((w + err * ins) for (w, ins) in zip(w, ins))
                b += err
            if w == w_prev and b == b_prev:
                break
            w_prev, b_prev = w, b

    return w, b


# returns the results from the first 4 perceptrons to later train the last one
def get_four_outs(x, y):
    w13 = 1
    w23 = 1
    b3 = -2

    w14 = -1
    w24 = 1
    b4 = -2

    w15 = 1
    w25 = -1
    b5 = -2

    w16 = -1
    w26 = -1
    b6 = -2

    w = -1.85
    w37 = w
    w47 = w
    w57 = w
    w67 = w
    b7 = .5

    r3 = perceptron(sigmoid_func, (w13, w23), b3, (x, y))
    r4 = perceptron(sigmoid_func, (w14, w24), b4, (x, y))
    r5 = perceptron(sigmoid_func, (w15, w25), b5, (x, y))
    r6 = perceptron(sigmoid_func, (w16, w26), b6, (x, y))

    return r3, r4, r5, r6


# trains a perceptron to match the input integer representation for the input bits
# returns the weight vector and scalar for the best found perceptron
def training_return_result(bits, n):
    table = truth_table(bits, n)
    w = tuple([0] * bits)#(-.5, 2)#
    b = 0
    w_prev, b_prev = w, b
    for epoch in range(0, 100):
        for x, y in table:
            y_star = perceptron(the_func, w, b, x)
            err = y - y_star
            w = tuple((w + err * x) for (w, x) in zip(w, x))
            b += err
        if w == w_prev and b == b_prev:
            break
        w_prev, b_prev = w, b

    return w, b


# find the number of linearly separable conical integer representations for the given number of bits
# returns the number
def find_correct_for_bit(bits):
    num_possible = 2**2**bits
    count = 0
    for n in range(0, num_possible):
        if training(bits, n) == 1:
            count += 1
    return count


# takes an activation function, weight vector, scalar, and input vector and does a perceptron
# returns either 1 or 0, according to the perceptron operation
def perceptron(A, w, b, x):
    vector_prod = sum([x[0]*x[1] for x in zip(w, x)]) + b
    return A(vector_prod)


# the activation function for the perceptron
# returns 1 or 0
def the_func(num):
    if num > 0:
        return 1
    return 0


# the activation function for the perceptron
# returns 1 or 0
def the_func_i(num):
    if num > 0:
        return 0
    return 1


# returns a truth table for a given number of bits and conical integer representation
# retuns a tuple of tuples and ints ie. (((1, 1), 1), ((1, 0), 0), ...)
def truth_table(bits, n):
    combos = list(product((1, 0), repeat=bits))
    base_rep = numberToBase(n, 2)
    for add in range(0, len(combos)-len(base_rep)):
        base_rep.insert(0, 0)
    # base_rep = list(add_to_base_rep + base_rep)
    return tuple(zip(combos, base_rep))


# counts the number of conditions derived from the conical integer representation 
# the input weight vector and scaler are good for
# returns a decimal from 1 to 0
def check(n, w, b):
    table = truth_table(len(w), n)
    count = 0
    for conds, result in table:
        if perceptron(the_func, w, b, conds) == result:
            count += 1
    return count/len(table)


# displays a neat readable table from the input table
# returns nothing
def pretty_print_tt(table):
    for conds, result in table:
        to_print = "\t"
        for cond in conds:
            to_print += str(cond) + '\t'
        to_print += '|\t'
        to_print += str(result)
        print(to_print)


# converts the number n to its number in base b
# returns a string ie. "10011101"
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


if __name__ == "__main__":
    main()