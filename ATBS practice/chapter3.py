import sys
def hello():
    print("howdy")
    print("how do you do")

hello()
hello()

def helloName(name):
    print(name + "hey")

helloName("jack")
helloName("david")

def increment(num):
    return num+5

print(increment(5))

print("hello", end='')
print(" world")

print('a', 'b', 'c')
print('a', 'b', 'c', sep='-')

eggs = "unmade"

def spam():
    global eggs
    eggs = "made"

print(eggs)
spam()
print(eggs)

def divide(num):
    try:
        return(10 / int(num))
    except ZeroDivisionError:
        print("can't divide by zero")

print(divide(input()))