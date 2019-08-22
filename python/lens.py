#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018
OBSERVACIONES: 12/02 ESTE PROGRAMA ENGLOBA A "Point.py"
@author: arioboo
"""
#------------------------MODULOS-------------------------------
import numpy as np

#----------MODULOS_ANADIDOS_MIOS------------
from sys_params import *
#------------------------FUNCTION_DEFS------------------------------------------------------
def Point(x1,x2,x1l,x2l,ml): # 'P'
    x1ml=(x1-x1l) # Distance along x axis of ray to lens position
    x2ml=(x2-x2l) # Distance along y axis of ray to lens position
	
    d=x1ml*x1ml+x2ml*x2ml+1.0e-12 #Distance between ray and lens squared # Add a tiny number to avoid division by zero
	
    y1=x1-ml*(x1-x1l)/d # Lens equation for x coordinate
    y2=x2-ml*(x2-x2l)/d # Lens equation for y coordinate
    return (y1,y2)
def TwoPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,ml1,ml2): #'2P'
    x1ml1=(x1-x1l1) ; x2ml1=(x2-x2l1)
    x1ml2=(x1-x1l2) ; x2ml2=(x2-x2l2)
    	
    d1=x1ml1*x1ml1+x2ml1*x2ml1+1.0e-12 # Add a tiny number to avoid division by zero
    d2=x1ml2*x1ml2+x2ml2*x2ml2+1.0e-12
    	
    y1=x1-ml1*(x1-x1l1)/d1-ml2*(x1-x1l2)/d2 # Lens equation for x coordinate
    y2=x2-ml1*(x2-x2l1)/d1-ml2*(x2-x2l2)/d2
    return (y1,y2)
def Binary(x1,x2,x1l1,x2l1,x1l2,x2l2,e1,e2): #'BIN'

    x1ml1=(x1-x1l1) ; x2ml1=(x2-x2l1)
    x1ml2=(x1-x1l2) ; x2ml2=(x2-x2l2)
    	
    d1=x1ml1*x1ml1+x2ml1*x2ml1+1.0e-12 # Add a tiny number to avoid division by zero
    d2=x1ml2*x1ml2+x2ml2*x2ml2+1.0e-12
    	
    y1=x1-e1*(x1-x1l1)/d1-e2*(x1-x1l2)/d2 # Lens equation for x coordinate
    y2=x2-e1*(x2-x2l1)/d1-e2*(x2-x2l2)/d2
    return (y1,y2)

def ChangRefsdal(x1,x2,x1l,x2l,ml,k,g): #'CR' o lente cuadrupolar (quadrupolar lens), lente puntual en un campo grav. externo.
	x1ml=(x1-x1l)  ; x2ml=(x2-x2l)
	d=x1ml*x1ml+x2ml*x2ml+1.0e-12 # Add a tiny number to avoid division by zero
	y1=x1*(1.0-k-g)-ml*(x1-x1l)/d  # Lens equation for x coordinate
	y2=x2*(1.0-k+g)-ml*(x2-x2l)/d
	return (y1,y2)

def SIS(x1,x2, x1l,x2l,ml): #'SIS'
    x1ml=(x1-x1l) ; x2ml=(x2-x2l)
    	
    d=np.sqrt(x1ml*x1ml+x2ml*x2ml+1.0e-12) # 13/02 Esta distancia no es al cuadrado! Add a tiny number to avoid division by zero
    	
    y1=x1-ml*(x1-x1l)/d # Lens equation for x coordinate
    y2=x2-ml*(x2-x2l)/d 
    return (y1,y2)

#--------------LENTES_AÑADIDAS_POR_MI--------------------------------#
def SIS_dist(x1,x2,x1l,x2l,ml,k,g):# 'SIS+g' , 'dist' es de 'distorsión (gamma)'
    x1ml=(x1-x1l) ; x2ml=(x2-x2l)
    
    d=np.sqrt(x1ml*x1ml+x2ml*x2ml+1.0e-12) # 13/02 Esta distancia no es al cuadrado! Add a tiny number to avoid division by zero    
    
    y1=x1*(1.0-g-k)-ml*(x1-x1l)/d # Lens equation for x coordinate
    y2=x2*(1.0+g-k)-ml*(x2-x2l)/d     
    return (y1,y2)

def SIS_dist_2P(x1,x2,x1l1,x2l1,x1l2,x2l2,ml1,ml2,k,g): #'SIS+g_2p' , 'dist' es de 'distorsión (gamma)', no de distribucción
    x1ml1=(x1-x1l1) ; x2ml1=(x2-x2l1)
    x1ml2=(x1-x1l2) ; x2ml2=(x2-x2l2)
    
    d1=np.sqrt(x1ml1*x1ml1+x2ml1*x2ml1+1.0e-12) # 13/02 Esta distancia no es al cuadrado! Add a tiny number to avoid division by zero
    d2=np.sqrt(x1ml2*x1ml2+x2ml2*x2ml2+1.0e-12)
    
    m=ml1+ml2
    
    y1=x1*(1.0-k-g)-ml1/m*(x1-x1l1)/d1-ml2/m*(x1-x1l2)/d2 # Lens equation for x coordinate
    y2=x2*(1.0-k+g)-ml1/m*(x2-x2l1)/d1-ml2/m*(x2-x2l2)/d2 
    return (y1,y2)
    
def ThreePoints(x1,x2,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,ml1,ml2,ml3): #'3P'
    x1ml1=(x1-x1l1)
    x2ml1=(x2-x2l1)
    x1ml2=(x1-x1l2)
    x2ml2=(x2-x2l2)
    x1ml3=(x1-x1l3)
    x2ml3=(x2-x2l3)
    d1=x1ml1*x1ml1+x2ml1*x2ml1+1.0e-12 # Add a tiny number to avoid division by zero
    d2=x1ml2*x1ml2+x2ml2*x2ml2+1.0e-12
    d3=x1ml3*x1ml3+x2ml3*x2ml3+1.0e-12
    
    y1=x1-ml1*(x1-x1l1)/d1-ml2*(x1-x1l2)/d2+ml3*(x1-x1l3)/d3 # Lens equation for x coordinate
    y2=x2-ml1*(x2-x2l1)/d1-ml2*(x2-x2l2)/d2+ml3*(x2-x2l3)/d3
    return (y1,y2)

def FourPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4,ml1,ml2,ml3,ml4): #'4P'
    x1ml1=(x1-x1l1)
    x2ml1=(x2-x2l1)
    x1ml2=(x1-x1l2)
    x2ml2=(x2-x2l2)
    x1ml3=(x1-x1l3)
    x2ml3=(x2-x2l3)
    x1ml4=(x1-x1l4)
    x2ml4=(x2-x2l4)
    d1=x1ml1*x1ml1+x2ml1*x2ml1+1.0e-12 # Add a tiny number to avoid division by zero
    d2=x1ml2*x1ml2+x2ml2*x2ml2+1.0e-12
    d3=x1ml3*x1ml3+x2ml3*x2ml3+1.0e-12
    d4=x1ml4*x1ml4+x2ml4*x2ml4+1.0e-12
    
    y1=x1-ml1*(x1-x1l1)/d1-ml2*(x1-x1l2)/d2+ml3*(x1-x1l3)/d3+ml4*(x1-x1l4)/d4 # Lens equation for x coordinate
    y2=x2-ml1*(x2-x2l1)/d1-ml2*(x2-x2l2)/d2+ml3*(x2-x2l3)/d3+ml4*(x2-x2l4)/d4 
    return (y1,y2)
#And so on...

'''
#-----------------------------------NOTES-------------------------------------
12/02 Programa operativo en Python 2.x

13/02 Se añade "LENTES_AÑADIDAS_POR_MI", hay que calcular el caso de 3 o más lentes , lo cual se hace trivialmente extendiendo el caso:
    Se define x1mln, x2mln. Se define dn=x1mln**2+x2mln**2+1.0e-12 . Se añade a y1 ,y2 el término mln*(x1-x1ln)/dn

    Se han añadido las lentes "ThreePoints"('3P'), "FourPoints"('4P'),SIS_dist('SIS_dist'),SIS_dist_2P ('SIS_dist_2p')
    El procedimiento para crear lentes es bastante similar.

#---------------------------------------------------------------------------
'''
