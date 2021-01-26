#!/usr/bin/env python2.7
# coding: utf-8

import rospy
from sensor_msgs.msg import Image
import numpy as np
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
from pyzbar.pyzbar import decode
from std_msgs.msg import String

bridge = CvBridge() # Funcion que convierte de topic tipo imagen a imagen con opencv

# Funcion callback
def callback(msg):

    try:
        # Convierte la imagen de la camara del dron a una imagen que se puede procesar en opencv
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

    except CvBridgeError, e:
        # EN caso de que falle, salta un error
        rospy.logerr("CvBridge Error: {0}".format(e))


    data = decode(cv_image) # Se decodifica el QR

    # Si la decodificacion tiene una longitud >0 es que se ha leido el QR
    if len(data)>0:
        qr_encontrado=data[0][0] #Se guarda el dato del qr que contiene

    else:
        qr_encontrado="0" #Si no se ha detectado qr se guarda un 0 
    
    print qr_encontrado #imprime el valor del codigo qr detectado, en caso de no detectar qr vale 0
    pub.publish(String(qr_encontrado)) # Se publica la informacion en el topic
    

# Inicializacion del nodo
rospy.init_node('read_camera')

sub = rospy.Subscriber('/front_cam/camera/image', Image, callback) #Se subscribe a la camara del dron 

pub = rospy.Publisher('/qrscan', String, queue_size=10) #Se publica la informacion detectada del qr en el topic /qrscan

rospy.spin() # El codigo se mantiene en espera
