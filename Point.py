#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#--------------------------MODULOS-------------------------------------------
import numpy as np
#----------MODULOS_ANADIDOS_MIOS------------
from sys_params import *
#----------------FUNCION_PUNTO----------------------------------------------

def Point(x1,x2,x1l,x2l,ml): # Point lens of mass ml at x1l,x2l
	x1ml=(x1-x1l)
	# Distance along x axis of ray to lens position
	x2ml=(x2-x2l)
	# Distance along y axis of ray to lens position
	d=x1ml*x1ml+x2ml*x2ml+1.0e-12 # Distance between ray and lens squared
	y1=x1-ml*(x1-x1l)/d
	# Lens equation for x coordinate
	y2=x2-ml*(x2-x2l)/d
	# Lens equation for y coordinate
	return (y1,y2)


'''
#-----------------------------------NOTES-------------------------------------
08/02 Programa operativo en Python 3.x

12/02 Programa operativo en Python 2.x


#------------------------------------------------------------------------------
'''