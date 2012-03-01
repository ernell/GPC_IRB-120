#!/usr/bin/env python

import roslib; roslib.load_manifest('rosclient')
import rospy

import socket
import sys
import time

# subscribe
from std_msgs.msg import String
def callback(data):
	#rospy.loginfo("server_spammer: %s",data.data)
	#if sendflag is set, send the data
	sendflag = 1
	sendData("hi", sendflag)
	recvData()

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("server_spammer", String, callback)
	rospy.spin()


# ##################################################
#
# Send a data packet
#
def sendData(sendPacket, sendflag):

	if sendflag == 1:
		sock.send(sendPacket)
		print "\tSent: ", sendPacket
		sendflag = 0
	
# ##################################################
#
# Get a data packet
#
def recvData():

	received = sock.recv(1024)
	print "\tRecieved: ", received

if __name__ == '__main__':

# Set up sockets
	print "starting socket"
	HOST, PORT = "localhost", 1025
	#data = ",".join(sys.argv[1:])
	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect to server
	sock.connect((HOST, PORT))

# will end up in the callback loop, so stuff happens there
	listener()

#Close down (ctrl+c should do this!)
	print "Shutting Down.."
	time.sleep(1)
	sock.send("closeSocket")
	time.sleep(1)
	sock.close()

