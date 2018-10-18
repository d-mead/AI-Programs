myCat = {'size': 'fat', 'color': 'gray', 'noise': 'loud'} # a dictionary
print(myCat['size'])
for x in myCat.values():
    print(x)
for x in myCat.keys():
    print(x)
print("FWFGDS")
for obj in myCat.items():
    print(obj)
for x in myCat.items():
    print(x)
if 'fat' in myCat.values():
    print('yes')
print("my cat's color is " + myCat.get('color'))
print("my cat's eye color is " + myCat.get("eyeColor", "problem"))

message = "I will uphold personal and academic integrity in the TJHSST Community"
count = {}
for character in message:
    count.setdefault(character, 0)
    count[character] = count[character]+1
print(count)

 