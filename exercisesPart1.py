import sys
import math
#1
 # sum = int(sys.argv[1]) + int(sys.argv[2])
 # print(sum)

#2
# sum = 0
# for index in range(1, len(sys.argv)):
#     sum += int(sys.argv[index])
# print(sum)

#3
# for index in range(1, len(sys.argv)):
#     if int(sys.argv[index]) % 3 == 0:
#         print(sys.argv[index])

#4
# first = 1
# second = 1
# if int(sys.argv[1])>0:
#     print(first)
# if int(sys.argv[1])>1:
#     print(second)
# for i in range(2, int(sys.argv[1])):
#     print(first + second)
#     temp = first
#     first += second
#     second = temp

#5
# import math
# a = int(sys.argv[1])
# b = int(sys.argv[2])
# c = int(sys.argv[3])
# p = (a+b+c)/2
# sum = math.sqrt(p*(p-a)*(p-c)*(p-c))
# if(sum>0):
#     print(sum)
# else:
#     print("error: not a triangle")

#6
# tally = {'a':0, 'e':0, 'i':0, 'o':0, 'u':0}
# for letter in sys.argv[1]:
#     if(letter in "aeiou"):
#         tally[letter] = tally[letter] + 1
# print(tally)

#7
# namep = "N/A"
# name = "N/A"
# while not name == "quit":
#     namep = name
#     name = input("what is your name? ")
#     print("previous name: " + namep)

#8
# nameList = []
# name = "N/A"
# while not name == "quit":
#     nameList.append(name)
#     name = input("what is your name? ")
#     print("previous names: " + str(nameList))

#9
# for x in range(int(sys.argv[1]), int(sys.argv[2])+1):
#     print(str(int(math.pow(x,2)-3*x+2)))

#10
# prime = True
# for x in range(2, int(int(sys.argv[1])/2)+1):
#     if int(sys.argv[1]) % x is 0:
#         prime = False
#         print("not ", end="")
#         break
# print("prime")

#11
# for i in range(int(sys.argv[1]), int(sys.argv[2])):
#     prime = True
#     for x in range(2, int(i/2)+1):
#         if i % x is 0:
#             prime = False
#             break
#     if prime:
#         print(i)

#12
# if len(sys.argv)>2:
#     for i in range(int(sys.argv[1]), int(sys.argv[2])):
#         prime = True
#         for x in range(2, int(i / 2) + 1):
#             if i % x is 0:
#                 prime = False
#                 break
#         if prime:
#             print(i)
# else:
#     prime = True
#     for x in range(2, int(int(sys.argv[1])/2)+1):
#         if int(sys.argv[1]) % x is 0:
#             prime = False
#             print("not ", end="")
#             break
#     print("prime")

#13
import PIL
from PIL import Image
if sys.argv[1].lower().endswith(".jpg" or ".png" or ".jpeg"):
    im = Image.open(sys.argv[1])
    width, height = im.size
    print("width: " + str(width) + ", height: " + str(height))
else:
    print("not an image")

#14
# s = '"Don'"'"'t quote me," she said.'
# print(s)