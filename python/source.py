#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#---------------------------------MODULOS--------------------------------------
import numpy as np
import matplotlib.pylab as plt
import time
#---------MODULOS_AÑADIDOS_MIOS--------------------------
from sys_params import *
from function_params import *

import lens as l
import aux

#-------------------------BEGIN_OF_PROGRAM--------------------------------
#---------FUNCIONES----------
# FUNCTION: GCIRC------------- FUENTE CIRCULAR GAUSSIANA DE SIGMA: "rad"   # PREFERIDA: DEFAULT
def gcirc(ny=1000,rad=100,x1=0.0,y1=0.0): # DEFAULT: (0,0) 
    
    x,y=np.mgrid[0:ny,0:ny]  #CREA UN GRID DE NY x NY
    r=(x-x1-ny/2.)**2.+(y-y1-ny/2.)**2.     #CALCULA EL RADIO CENTRAL
    #-----------------------------------------
    start_time=time.clock()
    
    a=np.exp(-r*0.5/rad**2.) #CORE
      
    print("--- %.3s seconds ---  fuente circular exponencial decreciente (DEFAULT)" % (time.clock() - start_time) )
    #~0.0s
    #-----------------------------------------
    if if_save_sources:
        plt.close()
        plt.imshow(a,extent=(0,ny,0,ny),cmap='afmhot');plt.title('FUENTE/OBJETO(y)') #cmap='amhot','gnuplot','gnuplot2'
        plt.colorbar()
        plt.savefig(initialsources_dir+'gcirc'+initial_sources_extension)
        
    return a/a.sum() # 12/02 RETORNA MATRIZ NORMALIZADA, NO HACE FALTA INTRODUCIR NORMALIZACION EN a

#FUNCTION: CUADRADA -----------FUENTE CUADRADA DE LADO: "lado"
def cuadrada(ny=1000,lado=100,x1=0.0,y1=0.0):
    
    #Inicializamos la matriz a cero
    a=np.zeros((ny,ny))#Definimos la matriz de ceros     
    center=[np.round(np.shape(a)[0]/2.),np.round(np.shape(a)[1]/2.)] # COORDS CENTRO
    
    esquina_inf = lambda indice : int(round(center[indice]-lado/2.))
    esquina_sup = lambda indice : int(round(center[indice]+lado/2.))
    
    #-------------------------------------
    start_time=time.clock()
    
    for i in range(esquina_inf(0),esquina_sup(0)):
        for j in range(esquina_inf(1),esquina_sup(1)):
            a[i,j]=np.exp(-(i*j)**(0.5)/lado**2.)
                
    print("--- %.3s seconds ---  fuente cuadrada" % (time.clock() - start_time) ) 
    #~0.1s
    #-----------------------------------------
    if if_save_sources:
        plt.close()       
        plt.imshow(a,extent=(0,ny,0,ny),cmap='gnuplot');plt.title('FUENTE/OBJETO(y)')
        plt.colorbar()
        plt.savefig(initialsources_dir+'cuadrada'+initial_sources_extension)
        
    return a/a.sum() #15/02 retorna matriz a

#FUNCTION: CUADRADA -----------FUENTE CIRCULAR DE RADIO: "rad" Y GROSOR "grosor"
def circular(ny=1000,rad=100):
    grosor=0.01*ny # GROSOR del anillo (not implemented)
    #Inicializamos la matriz a cero
    a=np.zeros((ny,ny))#Definimos la matriz de ceros     
    center=[np.round(np.shape(a)[0]/2.),np.round(np.shape(a)[1]/2.)] # COORDS CENTRO
    #-----------------------------------------
    start_time=time.clock()
    
    
    for i in np.arange(len(a[:,0])): #CORE
        for j in np.arange(len(a[0,:])):
            if rad >= np.sqrt((i-center[0])**2.+(j-center[1])**2.) :
                a[i,j]=1.
  
    print("--- %.3s seconds ---  fuente circular" % (time.clock() - start_time) )  
    #~9.2s
    #-----------------------------------------
    if if_save_sources:
        plt.close()
        plt.imshow(a,extent=(0,ny,0,ny),cmap='gnuplot');plt.title('FUENTE/OBJETO(y)')
        plt.colorbar()
        plt.savefig(initialsources_dir+'circular'+initial_sources_extension)

    return a/a.sum()



#FUNCTION: ANILLOS -----------FUENTE DE ANILLOS HASTA RADIO: "rad" (9 anillos)
def anillos(ny=1000,rad=100):
    #Inicializamos la matriz a cero
    a=np.zeros((ny,ny))#Definimos la matriz de ceros     
    center=[np.round(np.shape(a)[0]/2.),np.round(np.shape(a)[1]/2.)] # COORDS CENTRO

    #NUMERO DE ANILLOS
    r1=0.17*rad
    r2=0.28*rad
    r3=0.52*rad
    r4=0.60*rad
    r5=0.67*rad
    r6=0.74*rad
    r7=0.83*rad
    r8=0.9*rad
    r9=rad
    
    #---------------------------------------------------------
    start_time = time.clock() #VER TIEMPO DE ESTE PROCESO
    
    for i in np.arange(len(a[0,:])):#CORE
      for j in np.arange(len(a[:,0])):
          r=np.sqrt((i-center[0])**2.+(j-center[1])**2.)
          if   r<=r1: a[i,j]=7.   ; continue # No importan los valores que le demos porque luego se va a normalizar.
          elif r<=r2: a[i,j]=6.   ; continue
          elif r<=r3: a[i,j]=5.   ; continue
          elif r<=r4: a[i,j]=4.   ; continue
          elif r<=r5: a[i,j]=3.   ; continue
          elif r<=r6: a[i,j]=2.   ; continue
          elif r<=r7: a[i,j]=1.   ; continue
          elif r<=r8: a[i,j]=0.5  ; continue
          elif r<=r9: a[i,j]=0.25 ; continue
      
    print("--- %.3s seconds ---  fuente de anillos conćentricos" % (time.clock() - start_time) )  
    # ~ 9.9 secs (mucho)
    #----------------------------------------------------
    
    if if_save_sources:
        plt.close()
        plt.imshow(a,extent=(0,ny,0,ny),cmap='afmhot');plt.title('FUENTE/OBJETO(y)')
        plt.colorbar()
        plt.savefig(initialsources_dir+'anillos'+initial_sources_extension)
        
    return a/a.sum()
 
    

#----------------END_OF_PROGRAM----------------------------


#---TESTS---

if if_test_sources:
    print("---------source.py OUTPUT:--------")
    gcirc(1000,100)
    cuadrada(1000,100)
    circular(1000,50)
    anillos(1000,100)
    print("---------source.py END:-----------")    



#---OTHERS---
    
#Can include the function to source.py module to read a fits image as source:
import astropy.io.fits as io   #12/02 pyfits deprecated en python>3.0 ,USAR astropy.io.fits en su lugar
def fitsim(filename):
	a=io.getdata(filename)		# 13/02 LEE EL FICHERO
	if (len(a.shape)>2): a=a[0]	# 13/02 CABECERA PRIMERA DONDE SE ALOJAN LOS DATOS DE FLUJO
	return (1.0*a)/a.sum()		#13/02 RETORNA IMAGEN NORMALIZADA


#To implement this : 
    
# a=s.fitsim('Edgeons2.fit')	#Read file 'Edgeons2.fits'
# When calling, i.e. :
# plt.imshow(a)   ; it's not enough to see galaxies due to low brightness
# we can do some operations like:
# rule_normal=matplotlib.colors.Normalize(vmin=0,vmax=0.4, clip=True)  .# instance for the next command:
# plt.imshow(a,cmap='gray',norm=rule_normal,interpolation='bilinear')    



'''
#-----------------------------------NOTES-------------------------------------
08/12 Programa operativo en Python 3.x
12/02 Programa operativo en Python 2.x



'''
