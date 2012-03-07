#!/usr/bin/env python

import roslib; roslib.load_manifest('rosclient')
import rospy

import socket
import sys
import time

# std_msgs
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32

def callback(data):
	#rospy.loginfo("server_spammer: %s",data.data)
	#if sendflag is set, send the data
	sendflag = 1
	sendData("hi", sendflag)
	recvData()
# ##################################################
#
# If a new XYZ is published, this callback will happen and send the pose to the server
#
def setXYZ(data):
	#subscribe to XYZ
	#convert XYZ double array to string
	
	tempStr = ''
	
	#Convert the double array of XYZ in to a string (to .3 decimal places)
	for i in range(len(data.data)):
		if(i < 1):
			tempStr = tempStr + "%.3f" % data.data[i]
		else:
			tempStr = tempStr + ",%.3f" % data.data[i]
	
	tempStr = "setXYZ#" + tempStr + "#0\n"

	print tempStr
	
	#send string with setXYZ to server.
	sock.send(tempStr)
	time.sleep(0.2)
	#Clear string
	tempStr = ''
# ##################################################
#
# If a new rotation matrix is published, this callback will send the data to the server
#	
def setROT(data):
	#subscribe to ROT
	tempStr = data.data
		
	tempStr1 = ''
	tempStr2 = ''
	tempStr3 = ''
	
	
	#convert rotation array to 3 strings, maybe a little LOL?
	
	for i in range(len(data.data)):
	
		if(i < 1):
			tempStr1 = tempStr1 + "%.2f" % data.data[i]
		elif(i < 4):
			tempStr1 = tempStr1 + ",%.2f" % data.data[i]
		elif(i == 4):
			tempStr2 = tempStr2 + "%.2f" % data.data[i]
		elif(i < 8):
			tempStr2 = tempStr2 + ",%.2f" % data.data[i]
		elif(i == 8):
			tempStr3 = tempStr3 + "%.2f" % data.data[i]
		elif(i < 14):
			tempStr3 = tempStr3 + ",%.2f" % data.data[i]
	
	tempStr1 = "setROT1#" + tempStr1 + "#0\n"	
	print tempStr1
	tempStr2 = "setROT2#" + tempStr2 + "#0\n"
	print tempStr2
	tempStr3 = "setROT3#" + tempStr3 + "#0\n"
	print tempStr3
	
	#send each string of ROT to server:
	sock.send(tempStr1)
	time.sleep(0.2)
	sock.send(tempStr2)
	time.sleep(0.2)
	sock.send(tempStr3)
	time.sleep(0.2)
	#Clear strings
	tempStr = ''
	tempStr1 = ''
	tempStr2 = ''
	tempStr3 = ''
# ##################################################
#
# If armMoveFlag is set, a move command will be sent to the server.
#
def moveArm(data):
	#subscribe to armMoveFlag, if 1 send the move command:
	if(data.data == 1):
		sock.send("MoveJ_fc#0\n")
		time.sleep(0.2)
		#publish armMoveFlag to 0 (to say it's moved.)
		
	print "MoveJ_fc#0\n"
	
def pubCurrentPose(currentX, currentY, currentZ):

	print "Publishing Position"
	pubX = rospy.Publisher('currentX', Float32)
	pubY = rospy.Publisher('currentY', Float32)
	pubZ = rospy.Publisher('currentZ', Float32)

	while not rospy.is_shutdown():
	
		info = "Current XYZ: " + str(round(currentX,4)) + ", " + str(round(currentY,4)) + ", " + str(round(currentZ,4))
		
		rospy.loginfo(info)
		
		pubX.publish(Float32(currentX))
		pubY.publish(Float32(currentY))
		pubZ.publish(Float32(currentZ))
		
		rospy.sleep(1.0)

def listener():
	
	rospy.init_node('listener', anonymous=True)
	
	#check subscriptions
	rospy.Subscriber("server_spammer", String, callback)
	rospy.Subscriber("armXYZArr", 	Float32MultiArray, setXYZ)
	rospy.Subscriber("armRotArr",	Float32MultiArray, setROT)
	rospy.Subscriber("armMoveFlag", Int32, moveArm)
	
	#

	#check for data
	sock.send("CRobT_fc#0\n")
	time.sleep(0.2)
	recvData()

	rospy.spin()


# ##################################################
#
# Send a data packet
#
def sendData(sendPacket, sendflag):

	if sendflag == 1:
		sock.send(sendPacket)
		time.sleep(0.2)
		print "\tSent: ", sendPacket
		sendflag = 0
	
# ##################################################
#
# Get a data packet and check what it is..
#
def recvData():

	print "Checking rcvdata"
	received = sock.recv(1024)
	
	
	#Check what command was returned:
	temp = received.split('#')
	#If it begins with an ACK, print it and recheck the socket:
	if temp[0] == "ACK:":
		print "\tRecieved: " + received
		#print "Recheck"
		received = sock.recv(1024)
		#Check what command was returned:
		temp = received.split('#')
		
	#Check how the received string starts and publish acordingly	
	if temp[0] == "CurrentXYZ":
		print "Publishing " + temp[0]
		pose = temp[1].split(',')
		pubCurrentPose(float(pose[0]), float(pose[1]), float(pose[2]))
	elif temp[0] == "CurrentMotor":
		#publish them
		print "Publishing " + temp[0]
	elif temp[0] == "CurrentJoints":
		#publish them
		print "Publishing " + temp[0]
	else:
		print received
			

if __name__ == '__main__':

# Set up sockets
	print "starting socket"
	HOST, PORT = "164.11.73.252", 1025
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
	

