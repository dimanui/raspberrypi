"""
An example application using pimoteutils
To run: python app.py 0.0.0.0 8080

Needs porting into python3 for use with PiFace

"""

import sys
# Import PhoneServer and Phone classes from pimoteutils.
# Button only imported so we can access the variables
from phoneutils import *


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Override Phone so you can control what you do with the messages
#   "id" - the ID of the button that has been pressed
#   "message" - the message sent by the phone. If no message it will be ""
class MyPhone(Phone):
	#Override
	num = 0
	def buttonPressed(self, id, message):
		print("Message")
		#########----------------------------------------------###########
		# Your code will go here! Check for the ID of the button pressed #
		# and handle that button press as you wish.                      #
		#########----------------------------------------------###########
		if id == b1.getId():
			o1.setText("Button pressed")
		elif id == b2.getId():
			o1.setText("Toggle switched to " + message)
		elif id == b3.getId():
			o1.setText(message)
		elif id == vi.getId():
			o1.setText(message)
		elif id == r.getId():
			o2.setText(str(self.num))
			self.num+=1

# Create the phone object
thisphone = MyPhone()

b1 = Button("Hello") #Regular button
b2 = ToggleButton("This is a toggle button", True) #Toggle
b3 = InputText("Input text here") #Text Input
o1 = OutputText("Hello") #Output field
v = VideoFeed(320, 240) #Live video feed
vi = VoiceInput() #Voice input
r = RecurringInfo(500)
o2 = OutputText("Hello") #Output field

#Add the buttons to the phone
thisphone.addButton(b1)
thisphone.addButton(b2)
thisphone.addButton(b3)
thisphone.addOutput(o1)
thisphone.addButton(r)
thisphone.addOutput(o2)

thisphone.addButton(vi)
#Create the server
myserver = PhoneServer()
myserver.setPassword("helloworld")
#Add the phone
myserver.addPhone(thisphone)
# Start server
myserver.start(ip, port)
