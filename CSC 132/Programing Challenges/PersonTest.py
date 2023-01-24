#####################################################################
# description:  A class to test out the Person class designed in
# CSC/CYEN 132 programming assignment #1
####################################################################

# import everything from the Person file
from Item import *

# Create some people
p1 = Person()
p2 = Person("John Doe")
p3 = Person("Jane Doe", 3)
p4 = Person("James Doe", 4, 67)
p3.size = 5
p4.size = 15

print(p1)
print(p2)
print(p3)
print(p4)

# Creating some people with wrong input values
p5 = Person("a")
p6 = Person("b", 1000, -600)
p7 = Person("c", -12, 1000)
p7.size = -10

print(p5)
print(p6)
print(p7)

# Testing some of the other functions
for i in range(10):
    p1.goLeft()
    p2.goRight()
    p3.goUp()
    p4.goDown()

print(p1)
print(p2)
print(p3)
print(p4)
print("-" * 60)
print(f"The distance between p1 and p2 is {p1.getDistance(p2)}")
print(f"The distance between p1 and p3 is {p1.getDistance(p3)}")
print(f"The distance between p1 and p4 is {p1.getDistance(p4)}")
print("-" * 60)

for i in [12, 34, 89, -56, 3]:
    p1.goRight(i)
    p2.goLeft(i)
    p3.goDown(i)
    p4.goUp(i)

print(p1)
print(p2)
print(p3)
print(p4)
print("-" * 60)
print(f"The distance between p1 and p2 is {p1.getDistance(p2)}")
print(f"The distance between p1 and p3 is {p1.getDistance(p3)}")
print(f"The distance between p1 and p4 is {p1.getDistance(p4)}")
print("-" * 60)
