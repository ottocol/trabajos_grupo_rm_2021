#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import sys

#Uso de la acción move_base en ROS para moverse a un punto determinado
#En ROS una acción es como una petición de un "cliente" a un "servidor"
#En este caso este código es el cliente y el servidor es ROS
#(en concreto el nodo de ROS 'move_base')
class ClienteMoveBase:
    def __init__(self,robot):
        self.client =  actionlib.SimpleActionClient('robot'+str(robot)+'/move_base',MoveBaseAction)
        #esperamos hasta que el nodo 'move_base' esté activo`
        self.client.wait_for_server()

    def moveTo(self, x, y, qx, qy, qz,qw):
        #un MoveBaseGoal es un punto objetivo al que nos queremos mover
        goal = MoveBaseGoal()
        #sistema de referencia que estamos usando
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        #La orientación es un quaternion. Tenemos que fijar alguno de sus componentes
        goal.target_pose.pose.orientation.x = qx
        goal.target_pose.pose.orientation.y = qy
        goal.target_pose.pose.orientation.w = qz
        goal.target_pose.pose.orientation.w = qw

        #enviamos el goal
        self.client.send_goal(goal)
        #esperamos que el robot llegue al punto
        result = self.client.wait_for_result()
        if not result:
            rospy.logerr("No se ha podido ejecutar la acción!!")
        else:
            return self.client.get_result()

if __name__ == "__main__":
    rospy.init_node('movebase1')
    cliente1 = ClienteMoveBase(1)
    result=cliente1.moveTo(1,1,0,0,0.5,0.5)
    if (result):
        result2=cliente1.moveTo(1,2,0,0,0.5,0.5)
    else:
        print "Error, robot1 no puede llegar"
