from Vehicle import *

c1 = Car("Brendan", "Toyota", "Forerunner")
c2 = Car("Ian", "Hyundai", "Veloster")
c3 = Car("Alex", "Jeep", "Cherokee")

c1.setIssue("head gasket blown")
c2.setIssue("funny sound")
c3.setIssue("oil change")

print(c1)
print(c2)
print(c3)

m1 = Motorcycle("Jacob","Harley", "a big one")
m1.setIssue("too big")

print(m1)

b1 = Bicycle("Sacha","Bromption", "A Line")
print(b1)