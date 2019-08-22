#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#--------------------MODULOS------------------------------------------------
import numpy as np
import scipy.ndimage
from math import sqrt
import matplotlib.pylab as plt
#---------MODULOS_ANADIDOS_MIOS--------------------------
from sys_params import *
#-----------------------FUNCIONES--------------------------------------------------
#08/02 Include funcion: profile


### PROGRAM_FUNCTIONS
def profile(c,x0,y0,x1,y1,method='nn'): # Coords are in pixels
	num=int(round(sqrt((x1-x0)**2.+(y1-y0)**2.))) # Length of track in pixels
	xp, yp = np.linspace(xpp0, xpp1, num), np.linspace(ypp0, ypp1, num) # x and y coordinates of track
	zp =c[yp.astype(np.int), xp.astype(np.int)]
	return zp

#-------------------------------------------------------------------------------
#11/02 Include funcion : gassconv

def gaussconv(a,size): #a is the input map and size the sigma of the gaussian
	b=a*0.0  #Create the output array. Same size as input array
	scipy.ndimage.gaussian_filter(a,[size,size],output=b)
	return b

#------------------------------------------------------------------------------





### FUNCTIONALITY_FUNCTIONS:
    
        
def guardar(directory,response,opt_str):   
    plt.savefig(directory+response+opt_str+image_extension)
    print('Imagen guardada: %s'%directory+response+opt_str+image_extension)
    return  
'''
#-----------------------------------NOTES-------------------------------------
08/02 Programa operativo en Python 3.x

12/02 Programa operativo en Python 2.x
'''
