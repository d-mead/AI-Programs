list = ["cat", "dog", "fish", "cow"]
print(list[1])
print(list[-1])
print(list[1:3])
print(len(list))
del list[1]
print(list)
print("cat" in list)

# characteristics = ["fat", "grumpy", "old"]
# weight, mood, age = characterisitcs         --> alowed! (must be exactly the same number

list.append("moose")
list.insert(1, "chicken")
print(list)
list.remove("cow")
print(list)
list.append('ants')
list.sort()
print(list)
list.sort(reverse=True)
print(list)
