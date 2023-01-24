class Vehicle:
    def __init__(self, owner = "", make = "", model = ""):
        self.owner = owner
        self.make = make
        self.model = model
        self.issue = "None"
        self.tires = 4
        
    def setIssue(self, string):
        self.issue = string
        
    def __str__(self):
        return f"{self.owner}\t{self.make},{self.model},{self.tires}:\t{self.issue}"
    
class Cycle(Vehicle):
    def __init__(self, owner, make, model):
        super().__init__(owner, make, model)
        self.tires = 2
        
class Car(Vehicle):
    def __init__(self, owner, make, model):
        Vehicle.__init__(self,owner, make, model)
        
class Motorcycle(Cycle):
    def __init__(self, owner, make, model):
        super().__init__(owner, make, model)
        
class Bicycle(Cycle):
    def __init__(self, owner, make, model):
        super().__init__(owner, make, model)   
        
    def __str__(self):
        return super().__str__() + "this is just a bike"
    
############################################################################