###########################################################################################
# Name: 
# Date: 
# Description: 
###########################################################################################
from tkinter import *

#the defalut size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600
###########################################################################################
#Player class that tracks inventory and status effects
class Player():
    #Construtor
    def __init__(self):
        self.setStatus("Normal")
        self.inventory = []
        
    #Changes player status to input value
    def setStatus(self, status):
        self.status = status
        
    #Adds or removes item to inventory
    def changeInventory(self,object,add):
        if add is True:
            self.inventory.append(object)
        elif add is False and object in self.inventory:
            self.inventory.remove(object) 

#Game lass inherits from the Frame class of Tkinter
class Game(Frame):
    #Constructor
	def __init__(self, parent):
        #Call the constructor of Frame
		Frame.__init__(self, parent)
  		#intialize player
		self.player = Player()
        
    #creates rooms
	def createRooms(self):
		#r1 through r4 are the 4 rooms of the mansion
		#currentRoom is the room the player is currently in
		#which can be r1-4

		#create the rooms and assign images
		self.r1 = Room("Room 1", "room1.gif")
		self.r2 = Room("Room 2", "room2.gif")
		self.r3 = Room("Room 3", "room3.gif")
		self.r4 = Room("Room 4", "room4.gif")

		# add exits to room 1
		self.r1.addExit("east", self.r2)	# -> to the east of room 1 is room 2
		self.r1.addExit("south", self.r3)
		# add grabbables to room 1
		self.r1.addGrabbable("key")
		# add items to room 1
		self.r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
		self.r1.addItem("table", "It is made of oak.  A golden key rests on it.")

		# add exits to room 2
		self.r2.addExit("west", self.r1)
		self.r2.addExit("south", self.r4)
		#add grabbables to room 2
		self.r2.addGrabbable("stein")
		# add items to room 2
		self.r2.addItem("rug", "It is nice and Indian.  It also needs to be vacuumed.")
		self.r2.addItem("fireplace", "It is full of ashes. With an ornate German stein resting on the mantle")

		# add exits to room 3
		self.r3.addExit("north", self.r1)
		self.r3.addExit("east", self.r4)
		# add grabbables to room 3
		self.r3.addGrabbable("book")
		# add items to room 3
		self.r3.addItem("bookshelves", "They are empty.  Go figure.")
		self.r3.addItem("statue", "There is nothing special about it.")
		self.r3.addItem("desk", "The statue is resting on it.  So is a book.")

		# add exits to room 4
		self.r4.addExit("north", self.r2)
		self.r4.addExit("west", self.r3)
		self.r4.addExit("south", None)	# DEATH!
		# add grabbables to room 4
		self.r4.addGrabbable("6-pack")
		# add items to room 4
		self.r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig.  A 6-pack is resting beside it.")
  


		# set room 1 as the current room at the beginning of the game
		Game.currentRoom = self.r1

  
	#Sets up the GUI
	def setupGUI(self):
		self.pack(fill=BOTH, expand=1)
		Game.player_input = Entry(self, bg='white')
		Game.player_input.bind("<Return>", self.process)
		Game.player_input.bind("<Left>")
		Game.player_input.pack(side=BOTTOM, fill=X)
		Game.player_input.focus()

		#setup image on the left
		img = None
		Game.image = Label(self,width = WIDTH//2, image = img)
		Game.image.image = img
		Game.image.pack(side=LEFT, fill=Y)
		Game.image.pack_propagate(False)

		#setup label on the right
		text_frame = Frame(self, width=WIDTH/2)
		Game.text = Text(text_frame, bg = "lightgrey", state=DISABLED)
		Game.text.pack(fill=Y, expand=1)
		text_frame.pack(side=RIGHT, fill=Y)
		Game.image.pack_propagate(False)
	
 	#sets the current room image
	def setRoomImage(self):
		if Game.currentRoom is None:
			#if room is none, player has died
			Game.img = PhotoImage(file="skull.gif")
		else:
			#otherwise grab image from current room
			Game.img = PhotoImage(file=Game.currentRoom.image)

		#display the image
		Game.image.config(image=Game.img)
		Game.image.image = Game.img
  
	def setStatus(self, status):
		#enable text widget, clear it, set it and disable it
		Game.text.config(state=NORMAL)
		Game.text.delete("1.0", END)
		if Game.currentRoom is None:
			Game.text.insert(END, "You are Dead. The only thing you can do now is quit.\n")
		else:
			Game.text.insert(END, str(Game.currentRoom) + "\nYou are carrying: " + str(self.player.inventory) + "\n\n" + status)
		Game.text.config(state=DISABLED)
			
	
	#play the game
	def play(self):
    	#add rooms to the game
		self.createRooms()
		#configure GUI
		self.setupGUI()
		#set the current room
		self.setRoomImage()
		#set the current status
		self.setStatus("")
		
	
	#process the players input
	def process(self, event):
		#Grab player input from bottom widget
		action = Game.player_input.get()
		#set the user's input to lowercase for processing
		action = action.lower()
		
		#set a default response
		response = "I don't understand. Try verb noun. Valid verbs are: go, look and take"

		if (action in ["quit", "bye", "close", "exit", "au revoir"]):
			exit(0)
		if Game.currentRoom is None:
			Game.player_input.delete(0,END)
			return
		# split the user input into words (words are separated by
		# spaces) and store the words in a list
		words = action.split()
  
		if len(words) == 2:
			verb = words[0]
			noun = words[1]
		if verb == "go":
			response = "Invalid Exit"

			if noun in Game.currentRoom.exits:
				Game.currentRoom = Game.currentRoom.exits[noun]
				response = "Room Changed"
		
		elif verb == "look":
			response = "I don't see that item"

			if noun in Game.currentRoom.items:
				response = Game.currentRoom.items[noun]

		elif verb == "take":
			response = "I don't see that item"

			for grabbable in Game.currentRoom.grabbables:
				if noun == grabbable:
					self.player.changeInventory(grabbable, True)
					Game.currentRoom.delGrabbable(grabbable)
					response = f"{grabbable} grabbed"
					break
 
		elif verb == "use":
			response = "I cant do that"
			if self.currentRoom is self.r4 and "stein" in self.player.inventory:
				self.player.changeInventory("stein", False)
				self.player.changeInventory("filled_stein", True)
				response = "You filled the stein with the mystery brew"
			
			elif "filled_stein" in self.player.inventory and self.currentRoom is not self.r4:
				self.player.changeInventory("filled_stein", False)
				self.player.changeInventory("stein", True)
				self.currentRoom.addItem("key_hole", "It is small and glowing. You peer inside but cant see to the other side")
				response = "You down the mystery brew in the stein. It tastes like mushrooms. Across the room you see a shining key hole in the wall that certianly not there before"
			
			elif "key_hole" in self.currentRoom.items and "key" in self.player.inventory:
				self.player.changeInventory("key", False)
				exit = Room("Exit", "win.gif")
				self.currentRoom.addExit("down", exit)
				response = "A trapdoor with a ladder decending into an escape tunnel, Your escape."
					
		self.setStatus(response)
		self.setRoomImage()
		Game.player_input.delete(0, END)
  
# the blueprint for a room
class Room:
	# the constructor
	def __init__(self, name, image):
		# rooms have a name, exits (e.g., south), exit locations (e.g., to the south is room n),
		# and an image
		# items (e.g., table), item descriptions (for each item), and grabbables (things that can
		# be taken into inventory)
		self.name = name
		self.exits = {}
		self.items = {}
		self.grabbables = []
		self.image = image

    # getters and setters for the instance variables
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def image(self):
		return self._image

	@image.setter
	def image(self, value):
		self._image = value
 
	@property
	def exits(self):
		return self._exits

	@exits.setter
	def exits(self, value):
		self._exits = value

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, value):
		self._items = value

	@property
	def grabbables(self):
		return self._grabbables

	@grabbables.setter
	def grabbables(self, value):
		self._grabbables = value

	# adds an exit to the room
	# the exit is a string (e.g., north)
	# the room is an instance of a room
	def addExit(self, exit, room):
		# append the exit and room to the appropriate lists
		self._exits[exit] = room


	# adds an item to the room
	# the item is a string (e.g., table)
	# the desc is a string that describes the item (e.g., it is made of wood)
	def addItem(self, item, desc):
		# append the item and description to the appropriate lists
		self._items[item] = desc

	# adds a grabbable item to the room
	# the item is a string (e.g., key)
	def addGrabbable(self, item):
		# append the item to the list
		self._grabbables.append(item)

	# removes a grabbable item from the room
	# the item is a string (e.g., key)
	def delGrabbable(self, item):
		# remove the item from the list
		self._grabbables.remove(item)

	# returns a string description of the room
	def __str__(self):
		# first, the room name
		s = "You are in {}.\n".format(self.name)

		# next, the items in the room
		s += "You see: "
		for item in self.items.keys():
			s += item + " "
		s += "\n"

		# next, the exits from the room
		s += "Exits: "
		for exit in self.exits.keys():
			s += exit + " "

		return s

###########################################################################################
def death():
	print(" " * 17 + "u" * 7)
	print(" " * 13 + "u" * 2 + "$" * 11 + "u" * 2)
	print(" " * 10 + "u" * 2 + "$" * 17 + "u" * 2)
	print(" " * 9 + "u" + "$" * 21 + "u")
	print(" " * 8 + "u" + "$" * 23 + "u")
	print(" " * 7 + "u" + "$" * 25 + "u")
	print(" " * 7 + "u" + "$" * 25 + "u")
	print(" " * 7 + "u" + "$" * 6 + "\"" + " " * 3 + "\"" + "$" * 3 + "\"" + " " * 3 + "\"" + "$" * 6 + "u")
	print(" " * 7 + "\"" + "$" * 4 + "\"" + " " * 6 + "u$u" + " " * 7 + "$" * 4 + "\"")
	print(" " * 8 + "$" * 3 + "u" + " " * 7 + "u$u" + " " * 7 + "u" + "$" * 3)
	print(" " * 8 + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3)
	print(" " * 9 + "\"" + "$" * 4 + "u" * 2 + "$" * 3 + " " * 3 + "$" * 3 + "u" * 2 + "$" * 4 + "\"")
	print(" " * 10 + "\"" + "$" * 7 + "\"" + " " * 3 + "\"" + "$" * 7 + "\"")
	print(" " * 12 + "u" + "$" * 7 + "u" + "$" * 7 + "u")
	print(" " * 13 + "u$\"$\"$\"$\"$\"$\"$u")
	print(" " * 2 + "u" * 3 + " " * 8 + "$" * 2 + "u$ $ $ $ $u" + "$" * 2 + " " * 7 + "u" * 3)
	print(" u" + "$" * 4 + " " * 8 + "$" * 5 + "u$u$u" + "$" * 3 + " " * 7 + "u" + "$" * 4)
	print(" " * 2 + "$" * 5 + "u" * 2 + " " * 6 + "\"" + "$" * 9 + "\"" + " " * 5 + "u" * 2 + "$" * 6)
	print("u" + "$" * 11 + "u" * 2 + " " * 4 + "\"" * 5 + " " * 4 + "u" * 4 + "$" * 10)
	print("$" * 4 + "\"" * 3 + "$" * 10 + "u" * 3 + " " * 3 + "u" * 2 + "$" * 9 + "\"" * 3 + "$" * 3 + "\"")
	print(" " + "\"" * 3 + " " * 6 + "\"" * 2 + "$" * 11 + "u" * 2 + " " + "\"" * 2 + "$" + "\"" * 3)
	print(" " * 11 + "u" * 4 + " \"\"" + "$" * 10 + "u" * 3)
	print(" " * 2 + "u" + "$" * 3 + "u" * 3 + "$" * 9 + "u" * 2 + " \"\"" + "$" * 11 + "u" * 3 + "$" * 3)
	print(" " * 2 + "$" * 10 + "\"" * 4 + " " * 11 + "\"\"" + "$" * 11 + "\"")
	print(" " * 3 + "\"" + "$" * 5 + "\"" + " " * 22 + "\"\"" + "$" * 4 + "\"\"")
	print(" " * 5 + "$" * 3 + "\"" + " " * 25 + "$" * 4 + "\"")

###########################################################################################
# START THE GAME!!!

#create window
window = Tk()
window.title("Room Adventure")

#Create GUI as a Tkinter canvas inside the window
g = Game(window)
g.play()

#wait for window to close
window.mainloop()