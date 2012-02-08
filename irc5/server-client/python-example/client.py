#!/usr/bin/python

import socket
import sys
import time

HOST, PORT = "192.168.125.1", 1025
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server
sock.connect((HOST, PORT))

# Split up the string in to 3 bits of 70

#print len(data)
count = 0;
string1 = string2 = string3 = ''

for i in data:
	
	if count <= 70: 
		string1 = string1 + i
	elif count <= 140:
		string2 = string2 + i
	else:
		string3 = string3 + i
	count = count + 1

print "String 1: " + string1
print "String 2: " + string2
print "String 3: " + string3

sock.send(string1)
received = sock.recv(1024)
#print "Iteration ", i, ":"
print "\tSent: " , data
print "\tRecieved: ", received	

if string2 == '':
	string2 = '#0'

sock.send(string2)
received = sock.recv(1024)
#print "Iteration ", i, ":"
print "\tSent: " , data
print "\tRecieved: ", received	

if string3 == '':
	string3 = '#0'

sock.send(string3)
received = sock.recv(1024)
#print "Iteration ", i, ":"
print "\tSent: " , data
print "\tRecieved: ", received	


while True:

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


