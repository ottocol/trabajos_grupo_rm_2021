#!/usr/bin/env python
# coding: utf-8
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
import rospy
import actionlib
from std_msgs.msg import String
import time 
import sys
#Variables globales empleadas para la cuenta de cajas
pub =0
conPoseCajas =0
rangoX = False
rangoY = False
rangoZ = False
rangoTheta = False
countBoxes =0
fin = True

#Clase para introducir las posiciones a las que tiene que ir el dron 
class Pose:
    def __init__(self, x, y, z, theta, w,giro):
        self.x = x
        self.y = y
        self.z = z
        self.theta = theta
        self.w = w
        self.giro = giro
    def __str__(self):
        return "(%f,%f,%f,%f,%f)" % (self.x,self.y,self.z,self.theta, self.w,self.giro) 	


# Lista de posiciones establecidas
dronePositions=[]
#Columna 1 estanteria 1
dronePositions.append(Pose(1.19,0.7,1.78,0.7,0.7,False))
dronePositions.append(Pose(1.23,0.7,3.42,0.7,0.7,False))
dronePositions.append(Pose(1.23,0.7,5.03,0.7,0.7,False))
dronePositions.append(Pose(1.23,0.7,5.03,0.0,1.0,True))
#Columna 2 estanteria 1
dronePositions.append(Pose(3.8,0.7,5.03,0.7,0.7,False))
dronePositions.append(Pose(3.8,0.7,3.4,0.7,0.7,False)) 
dronePositions.append(Pose(3.8,0.7,1.78,0.7,0.7,False))
dronePositions.append(Pose(3.8,0.7,1.78,0.0,1.0,True))

#Columna 1 estanteria 2
dronePositions.append(Pose(6.35,0.7,1.78,0.7,0.7,False)) 
dronePositions.append(Pose(6.35,0.7,3.4,0.7,0.7,False)) 
dronePositions.append(Pose(6.35,0.7,5.2,0.7,0.7,False)) 
dronePositions.append(Pose(6.35,0.7,5.2,0.0,1.0,True)) 
#Columna 2 estanteria 2
dronePositions.append(Pose(8.85,0.7,5.0,0.7,0.7,False))
dronePositions.append(Pose(8.85,0.7,3.5,0.7,0.7,False))
dronePositions.append(Pose(8.85,0.7,1.78,0.7,0.7,False))

dronePositions.append(Pose(8.85,0.7,0.0,0.7,0.7,True))  

# Funcion callback
def callback(msg):
    #Variables globales empleadas
    global pub
    global conPoseCajas
    global rangoX 
    global rangoY 
    global rangoZ 
    global rangoTheta
    global countBoxes
    global fin
    cmd = Twist()

    #Control de la velocidad en el eje X para llegar a la posicion deseada
    if msg.pose.position.x >=(dronePositions[conPoseCajas].x-0.1) and msg.pose.position.x <=(dronePositions[conPoseCajas].x):
        rangoX = True
        cmd.linear.x = 0.01
    elif msg.pose.position.x < dronePositions[conPoseCajas].x-0.1:
        cmd.linear.x = 0.2
    elif msg.pose.position.x > dronePositions[conPoseCajas].x + 0.1:
        cmd.linear.x = -0.15

    elif msg.pose.position.x > dronePositions[conPoseCajas].x and  msg.pose.position.x <= dronePositions[conPoseCajas].x + 0.1:
        cmd.linear.x = -0.01
        rangoX = True


    #Control de la velocidad en el eje Y para llegar a la posicion deseada
    if msg.pose.position.y >=(dronePositions[conPoseCajas].y-0.1) and msg.pose.position.y <=(dronePositions[conPoseCajas].y):
        cmd.linear.y = 0.01
        rangoY = True
    elif msg.pose.position.y < dronePositions[conPoseCajas].y-0.1:
        cmd.linear.y = 0.2
    elif msg.pose.position.y > dronePositions[conPoseCajas].y + 0.1:
        cmd.linear.y = -0.15
    elif msg.pose.position.y > dronePositions[conPoseCajas].y and  msg.pose.position.y <= dronePositions[conPoseCajas].y + 0.1:
        cmd.linear.y = -0.01
        rangoY = True

    #Control de la velocidad en el eje z para llegar a la posicion deseada
    if msg.pose.position.z >=(dronePositions[conPoseCajas].z-0.1) and msg.pose.position.z <=(dronePositions[conPoseCajas].z):
        cmd.linear.z = 0.01
        rangoZ =True
    elif msg.pose.position.z < dronePositions[conPoseCajas].z-0.1:
        cmd.linear.z = 0.2
    elif msg.pose.position.z > dronePositions[conPoseCajas].z + 0.1:
        cmd.linear.z = -0.15
    elif msg.pose.position.z > dronePositions[conPoseCajas].z and  msg.pose.position.z <= dronePositions[conPoseCajas].z + 0.1:
        cmd.linear.z = -0.01
        rangoZ =True

    #Control de la velocidad angular de z en funcion del angulo Theta para llegar a la posicion deseada

    if rangoZ and rangoX and rangoY: #El drone empieza a girar cuando llega a la posicion
        if  dronePositions[conPoseCajas].theta == 0.7:
            if (msg.pose.orientation.z >= dronePositions[conPoseCajas].theta-0.05) and msg.pose.orientation.z <= dronePositions[conPoseCajas].theta: 
                rangoTheta = True
                cmd.angular.z = 0.001
            elif msg.pose.orientation.z > dronePositions[conPoseCajas].theta:
                cmd.angular.z = -0.001
                rangoTheta = True
            else:
                cmd.angular.z = 0.2

        elif dronePositions[conPoseCajas].theta == -0.7: 

            if (msg.pose.orientation.z <= dronePositions[conPoseCajas].theta-0.05) and msg.pose.orientation.z >= dronePositions[conPoseCajas].theta: 
                rangoTheta = True
                cmd.angular.z = -0.001
            elif msg.pose.orientation.z < dronePositions[conPoseCajas].theta:
                cmd.angular.z = 0.001
                rangoTheta = True
            else:
                cmd.angular.z = -0.2
        else:
            if (msg.pose.orientation.z >= dronePositions[conPoseCajas].theta-0.05) and msg.pose.orientation.z <= dronePositions[conPoseCajas].theta:
                rangoTheta = True
                cmd.angular.z = -0.001
            elif msg.pose.orientation.z < dronePositions[conPoseCajas].theta:
                cmd.angular.z = 0.001
                rangoTheta = True
            else:
                cmd.angular.z = -0.2



    if rangoTheta and rangoZ and rangoX and rangoY: #En el caso de que se ha establecido en la posicion objetivo
        rangoTheta = False
        rangoZ = False
        rangoX = False
        rangoY = False
        detectQR = rospy.wait_for_message('/qrscan', String) #Lectura del topic qrscan para identificar si hay qr o no
        detectQR.data=int(detectQR.data)
        if not dronePositions[conPoseCajas].giro:
            if detectQR.data != 0: #Si se ha detectado caja
                countBoxes+=1
                conPoseCajas +=1
                print 'Caja detectada, total de cajas: ', countBoxes
            else: #En el caso de que no se ha detectado caja
                conPoseCajas +=1
                print 'Caja no detectada, total de cajas: ',countBoxes
        else:
            conPoseCajas +=1
    
    if conPoseCajas==15 and fin: #Si se ha llegado a la ultima posicion aterrizar el dron
        fin = False
        print 'Aterrizando '
        print 'Total de cajas detectadas: ',countBoxes

    pub.publish(cmd)

def main():
    global pub
    rospy.init_node('contar_cajas') #Inicio del nodo
    sub = rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, callback) #Subscribirse a este topic para obtener la odometria del dron
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #Publicar la velocidad
    rospy.spin()


if __name__ == "__main__":
    main()
