import random
import sys

for i in range(5):
    print('hello ')


i = 0
while i < 5:
    print('number: ' + str(i))
    i = i + 1

for i in range(0, 10, 3):
    print(i)

print('')

for i in range(5):
    print(random.randint(1, 10))