#include <stdio.h>
#include <stdlib.h>
#include "ros/ros.h"
#include "std_msgs/Int32.h"
#include "commands.hpp"

//Defs
#define 	TIPTHRESH 	100
//Globals
int tipval = 0;
//Function Declerations
void tipCallback(const std_msgs::Int32::ConstPtr& tip);
//Functions
int main(int argc, char **argv)
{

	ros::init(argc, argv, "arraySubscriber");

	ros::NodeHandle n;	
	//Subscriptions
	ros::Subscriber sub1 = n.subscribe("tactipReading", 100, tipCallback);
	//Publishing 
	ros::Publisher pubXYZ = n.advertise<std_msgs::Float32MultiArray>("armXYZArr", 100);
	ros::Publisher pubROT = n.advertise<std_msgs::Float32MultiArray>("armRotArr", 100);
	ros::Publisher pubMOV = n.advertise<std_msgs::Int32>("armMoveFlag", 100);
	
	ros::Rate loop_rate(1);

	//Send Start XZY, ROT etc:
	double X = 313.20, Y = 472.74, Z = 286.61;
	setArmXYZ(pubXYZ, 	X, Y, Z);
	setArmROT(pubROT,	0.0, 0.0, 0.0, 0.0,
				0.0, 0.0, 0.0, 0.0,
				0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
	sendArmMove(pubMOV);

	while(ros::ok())
	{
		ros::spinOnce();
		loop_rate.sleep();
		if(tipval > TIPTHRESH)
		{
			printf("Tactip hit (%d)\n",tipval);
			//sendArmStop();
		}
		else
		{
			printf("%d\n", tipval);
			Z = Z - 0.1;
			setArmXYZ(pubXYZ, X, Y, Z);
			sendArmMove(pubMOV);
		}
	}
	return 0;
}

void tipCallback(const std_msgs::Int32::ConstPtr& tip)
{
	// print all the remaining numbers

	tipval = tip->data;

	//return i;
	return;
}