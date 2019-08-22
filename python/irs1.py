#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#-------------MODULOS-------------------
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
#----------MODULOS_ANADIDOS_MIOS------------
from sys_params import *
from function_params import *

import source as s
import lens as l
#-----------------------------------

nx=801 # Number of pixels in image plane	#DEFAULT=801
ny=401 # Number of pixels in source plane  	 #DEFAULT=401

xl=2. # Size of image plane covered (in "Einstein" radii) DEFAULT=2.
yl=2. # Size of source plane covered (in Einstein radii)  DEFAULT=2.

#------------LENS_PARAMETERS-------------------------
xlens=0.0 	#DEFAULT=0.0
ylens=0.0 	#DEFAULT=0.0
mlens=1.0 	 #DEFAULT=1.0
#-----------------PIXEL_SIZE----------------------------------

xs=2.*xl/(nx-1) 	# pixel size on the image map
ys=2.*yl/(ny-1) 	# pixel size on the source map

#Source parameters
xpos=0.0  	#DEFAULT= 0.0
ypos=0.0  	#DEFAULT = 0.0
rad=0.10  	#DEFAULT = 0.10
ipos=int(round(xpos/ys))

# Convert source parameters to pixels
jpos=int(round(-ypos/ys))
rpix=int(round(rad/ys))
a=s.gcirc(ny,rpix,jpos,ipos) # This is the source plane
b=np.zeros((nx,nx)) # This is the image plane
#In this version, the main loop is implicit
#We use operations on numpy arrays instead which is faster.
j1,j2=np.mgrid[0:nx,0:nx]  # DEFINE INTEGERS PARA NUESTRA SUERTE 
x1=-xl+j2*xs # Pix to coord on image x
x2=-xl+j1*xs # Pix to coord on image y
y1,y2=l.SIS(x1,x2, xlens+0.1,ylens,1.2) # This line calculates the deflection

#---------------MODIFICACION-------------------------------
#PROGRAMA:
#i2=np.round((y1+yl)/ys)  # 12/02 ROUND DA ENTEROS, NP.ROUND DA FLOATS (LO QUE NO QUEREMOS)
#i1=np.round((y2+yl)/ys)

#12/02 YO:
i2=np.array(np.round((y1+yl)/ys),dtype=int)  # 12/02 ESTO DA PRECISAMENTE ENTEROS QUE ES LO QUE QUEREMOS
i1=np.array(np.round((y2+yl)/ys),dtype=int)

#----------continue----------------------------------------
# If deflected ray hits a pixel within source then set image to brightness on that pixel
ind= (i1 >= 0) & (i1 < ny) & (i2 >= 0) & (i2 < ny)  #12/02  ESTO ES LA LLAMADA MASCARA
#Now this is an array which is True if the ray hits the source plane.
i1n=i1[ind]  # 12/02 FLOATS (NO!)
i2n=i2[ind]  # 12/02 FLOATS (NO!)
j1in=j1[ind] # 12/02 INTEGERS (YES!)
j2in=j2[ind] # 12/02 INTEGERS(YES!)

for i in range(np.size(i1n)): # Loop over pixels that hit the source plane
	b[j1in[i],j2in[i]]=a[i1n[i],i2n[i]] # O se anade aqui int(i1n..)etc o se define mejor el 

#-------PLOTS(including Fluxes in both planes)---------------------
fig=plt.figure(1)
#SUBPLOT1
ax=plt.subplot(121)
ax.imshow(a,extent=(-yl,yl,-yl,yl))
fa=np.sum(a) #Flux on source plane
ax.set_title('Flux='+str(fa)) #Set title for subplot 1
#SUBPLOT2
ax=plt.subplot(122)
ax.imshow(b,extent=(-xl,xl,-xl,xl))
fb=np.sum(b)*(xs**2)/(ys**2) # Flux on image pl. (taking into acount pix size)
ax.set_title('Flux='+str(fb)) # Set title for subplot 2

plt.show()



'''
#-----------------------------------NOTES-------------------------------------
12/02 Deprecation of xrange in python 3.x , in 2.x still used. This program is changed accordingly to
be used in python 3.x

12/02 Failed in loop 'for'(L55) cause of non-defined integers inside.

12/02 Programa operativo en Python 2.x
#----------------------------------------------------------------------------
'''

#----------------------------PURPOSE---------------------------------------------

if if_aclaraciones :  
    print('\nACLARACIONES:\n\n\   12/02 Cito directamente de wsbook.pdf: \n\
          This python code is useful and may allow to get some insight into some lens systems, but we have to a ept that it is not very eficient.There are two nested loops (over rows and columns of the image plane) and, if there are many lenses,\n\
          there would still be a third one over lenses. Python is, in general, not very eficient in running loops, and consequently, nested loops are even worse. As the image plane becomes larger and/or we include more lenses, this code becomes very ineficient and, consequently, slow.Fortunately, improving its performance is both, easy and elegant, by using numpy arrays.\n\
          Instead of running over individual pixels, we an det the whole bunch of rays at on the by operating on an entire array of coordinates.\n\
          This way, the nested loop will be dealt with internally by numpy which is much more eficient (as numpy is already \n\
          compiled to machine code). And best news is that, as we were careful enough in writing our functions for the detection of the dierent lens systems to use numpy functions when neccessary, these functions, without any modification, are still as useful when called with full arrays of coordinates as they were with a single ray. \n\
          We then just need to make some manipulation to create an array with the column and row numbers of the pixels, and to remove the loop over pixels by operating on full numpy arrays. The code will now look something like this: \n\
          A magnification map is a map that shows the amount of the magnification produced by a certain lens system in a region of the source plane.  \n\
          If, as is usually the case, lens(es) and source move with respect to each other at a certain velocity, the source \n\
          suffers diferent magnifications at diferent times,which are observed as variations in the brightness of the source.\n\
          A curve of the brightness of a source versus time is called a light curve ,and contains plenty of information on the lens and/or source systems. Magnification maps \n\
          are therefore needed to be able to interpret this kind of observations and to compare them with dierent possible models. ')
    print("They allow to determine many properties of the lens system (mass, structure) and/or of the lens \n\
          (size, etc.) In order to calculate magnification maps, we will make use of the fact that gravitational lensing does not \n\
            change the surface brightness of the images, and therefore the magnification is just the ratio between the subtended solid angles of image(s) and source, \n\
            which is given by the inverse of the determinant of the A matrix(cf.Schneider, Ehlers & Falco, 1999,section 5.2)\n ")
#-------------------------------------------------------------------------------

