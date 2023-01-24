#####################################################################
# author: Alex Hebert
# date: 14 December 2022
# description: Person Class that exists on a coordinate plane
#####################################################################
import math

# global Constants to restrict the maximum x and y values that a person object
# can have.
MAX_X = 1000
MAX_Y = 800

# A class representing a person. A person can be initialized with a
# name, as well as x and y coordinates. However, there are default
# values for all those (i.e. player 1, 0 and 0 respectively). A person
# also has a size which is set to 1 by default. A person can go left, 
# go right, go up and go down. A person also has a string function 
# that prints out their name location, and size. A person also has a 
# function that calculates the euclidean distance from another person 
# object.
class Item:
    def __init__(self, name = "player 1", x = 0, y = 0, size = 1.0):
        self.name = name
        self.x = x
        self.y = y
        self.size = size

    #Accessors and Mutators for instance variables
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if len(value) > 1:
            self._name = value
        else:
            self._name = "player 1"
            
    @property
    def x(self):
        return self._x 
    
    @x.setter
    def x(self, value):
        if value >= 0 and value <= MAX_X:
            self._x = value
        else:
            self._x = 0
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        if value >= 0 and value <= MAX_Y:
            self._y = value
        else:
            self._y = 0
            
    @property
    def size(self):
        return self._size 
    
    @size.setter
    def size(self, value):
        if value >= 1.0:
            self._size = value    

    #Move along the negative x axis
    def goLeft(self, distance = 1):
        self.x -= distance
    
    #Move along the positve x axis
    def goRight(self, distance = 1):
        self.x += distance
        
    #Move along the negative y axis
    def goUp(self, distance = 1):
        self.y -= distance
    
    #Move along the positive y axis
    def goDown(self, distance = 1):
        self.y += distance
    
    #use euclidian distance formula to find distance between two persons
    def getDistance(self, other):
        return math.sqrt(math.pow(other.x - self.x,2) + math.pow(other.y - self.y,2))
    
    #Overloaded string function
    def __str__(self):
        return f"Person ({self.name}):\tsize = {self.size},\tx = {self.x},\ty = {self.y}"