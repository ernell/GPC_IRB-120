#!/usr/bin/env python

import roslib; roslib.load_manifest('rosclient')
import rospy

#This stuff isn't in rospy, it's from normal python, will this work?
import socket
import sys
import time

HOST, PORT = "localhost", 1025
data = " ".join(sys.argv[1:])

print "Hi"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server
sock.connect((HOST, PORT))

sock.send(data)

while True:

	#try:
	    # and send data
	
	    # Receive data from the server and shut down
	received = sock.recv(1024)
	#print "Iteration ", i, ":"
	print "\tSent: " , data
	print "\tRecieved: ", received
	
	if received == "closeClient ":
		print "hi"
		break		

#finally:
print "sleepytime"
time.sleep(1)
print "fin"
sock.send("closeSocket")
time.sleep(1)
sock.close()
