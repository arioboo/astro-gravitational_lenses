#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#--------------MODULOS------------------------------------
import numpy as np # Import needed modules
from math import pi
import matplotlib.pyplot as plt
from random import seed, uniform # Random number stuff
#----------MODULOS_ANADIDOS_MIOS------------
import aux 
from sys_params import *
import lens as l
#--------------OTROS_MODULOS----------------------------------------
import time # Timing stuff   #time, clock, sleep
from pyfits import writeto # To be able to save output as fits

#----------------COMIENZO-----------------------------------------------

# ********** Model Parameters *************************
kappa=0.59 # Total Convergence                              DEFAULT=0.59
gamma=0.61 # Shear                                          DEFAULT=0.61
alpha=0.999 # Fraction of mass in form of microlenses       DEFAULT=0.999
raypix=15.0 # Rays per pixel in absence of lensing          DEFAULT=15.0
ny=1000 # Pixels in the magnification map                   DEFAULT=1000
yl=10 # Half size of magnification map in Einstein Radii    DEFAULT=10
eps=0.02 # Maximum fraction of flux lost                    DEFAULT=0.02
#------------------PRELIMINARY_CALCULATIONS------------------------------------
# **** Make some preliminary calculations **************
ks=kappa*alpha # Convergence in microlenses ###III (NEW!!!)
kc=kappa*(1.-alpha) # Convergence in smooth matter

ys=2.*yl/(ny-1) # Pix size in the image plane
ooys=1./ys # Inverse of pixel size on image plane
sqrpix=np.sqrt(raypix) # Rays per pixel in one dimension

f1=1./abs(1.-kappa-gamma) # Exp. factor on horizontal axis
f2=1./abs(1.-kappa+gamma) # Exp. factor on vertical axis
fmax=max(f1,f2) # Max Exp factor

xl1=1.5*yl*f1 ;      xl2= 1.5*yl*f2 # Half Size of shooting region in x and y  DEFAULT : xl1,xl2=1.5*yl*f1,1.5*yl*f2
xl=1.5*yl*fmax # Longest Half side of shooting region     DEFAULT=1.5*yl*fmax

nsmin=3*ks**2/eps/abs((1.-kappa)**2-gamma**2) # Min number of stars
xmin=np.sqrt(pi*nsmin/ks)/2 # Min half side of star region
xls=xl+xmin # Expand to account for shooting region

nx1=np.int16(np.round(1.5*ny*f1*sqrpix))# Rays in shoot. reg. along x axis
nx2=np.int16(np.round(1.5*ny*f2*sqrpix))# Rays in shoot. reg. along y axis

nx=max(nx1,nx2) # Number of rays along longest side
xs=2.*xl1/(nx1-1) # Pixel size on image plane
xnl=abs(ks*(2*xls)*(2*xls)/pi) # Number of microlenses
nl=int(xnl) # Number of microlenses (int)
thmag=1./(1-kappa-gamma)/(1-kappa+gamma) # Theoretical value of magnification

#---------------------------PRINT_PARÁMETROS-------------------------------------
print("********************************************************")
print("Half Size of map in Einstein radii=", yl) # Print some parameters
print("Number of pixels of magnification map =", ny)
print("Half size of shooting region=", xl)
print("Number of rays along the longest axis =", nx)
print("Half size of region with microlenses=", xls)
print("Total Convergence,k =", kappa)
print("Shear,gamma =", gamma)
print("Fraction of mass in microlenses, alpha =", alpha)
print("Convergence in form of microlenses, ks =", ks)
print("Number of microlenses=", nl)
print("Rays per unlensed pixel,raypix =", raypix)
print("Theoretical Mean Magnification,mu =", thmag)
print("********************************************************")

#-------------------------MATRIZ_OBJETO-------------------------------------
b=np.zeros((ny,ny)) # Initialize magnification map

#------------------DISTRIBUCION_UNIFORME_ESTRELLAS_REGION---------------------

# ***** Randomly distribute stars in region ******************
x1l=np.zeros(nl) # Initialize microlens positions to zero
x2l=np.zeros(nl)
seed(1.0) # Initialize random number generator          DEFAULT=1.0

for i in range(nl): # Generate positions of microlenses
	x1l[i]=uniform(-xls,xls)
	x2l[i]=uniform(-xls,xls)

#------------------------PRINT_PROGRESO---------------------------------------
# **************************************************************
perc0=5. # Percentage step to show progress             DEFAULT=5.
perc=5. # Initial Percentage                            DEFAULT=5.
yr=np.arange(0,nx2) # Array for looping over rows of rays
y,x=np.mgrid[0.0:1.0,0:nx1] # These are arrays with x and y coords of one row of rays in image plane
nlrange=np.arange(nl) # Array for looping over lenses

#----------------------BUCLE_PRINCIPAL-------------------------------------------------
# ********************* MAIN LOOP ******************************
startt=time.time() # Time at start of execution
for i in yr: # Main Loop (over rows of rays)
	if ((i*100/nx2)>=perc): # If perc is completed, then show progress
		perc=perc+perc0
		print(round(i*100/nx2),"%",round(time.time()-startt,3)," secs")
         #print('Completed fraction and elapsed execution time')
	x2=-xl2+y*xs # Convert pixels to coordinates in the image plane
	x1=-xl1+x*xs
	y2=x*0.0 # Initialize variables
	y1=x*0.0
    
for ii in nlrange: # Loop over microlenses
	x1ml=x1-x1l[ii]
	x2ml=x2-x2l[ii]
	d=x1ml**2+x2ml**2 # Distance to lens ii squared
	y1=y1+x1ml/d # Deflect x coordinate due to lens ii
	y2=y2+x2ml/d # Deflect y coordinate due to lens ii
	del x1ml,x2ml,d
	y2=x2-y2-(kc-gamma)*x2 # Calculate total y deflection
	y1=x1-y1-(kc+gamma)*x1 # Calculate total x deflection
	i1=(y1+yl)*ooys # Convert coordinates to pixels on source plane
	i2=(y2+yl)*ooys
	i1=np.round(i1) # Make indices integer
	i2=np.round(i2)
	ind=(i1>=0) & (i1<ny) & (i2>=0) & (i2<ny) # Select indices of rays falling onto our source plane
	i1n=i1[ind] # Array of x coordinates of rays within map
	i2n=i2[ind] # Array of y coordinates of rays within map

for ii in range(np.size(i1n)): # Loop over rays hitting the source plane
	b[i2n[ii],i1n[ii]]+=1 # Increase map in one unit if ray hit
	y=y+1.0 # Move on to next row of rays

print("(100.0 '%') COMPLETE\n")

print("Exec. time = ",round(time.clock()-startt,3), ' seconds\n') # Print execution time
#***************************************************************
b=b/raypix # Normalize by rays per unlensed pixel

#-----------------------PRINT_MAGNIFICACIÓN------------------------------------
print("********************************************************")
print("Measured mean magnification =",np.mean(b))
print("Theoretical magnification is =",thmag)
print("********************************************************")


if (thmag<0): # Vertical or horizontal flip in some cases
	if (gamma<0):
		b=np.flipud(b)
	else:
		b=np.fliplr(b)

#----------------------------------------------------------------------
opt_str=''
def optional_string(respuesta):
    global seq     # hacemos global 'seq' para verlo despues    
    if   respuesta == 'P'       : seq=[str(round(s,1)) for s in (ml,xd,yd)]                      ; opt_str='(ml,xd,yd)_('+','.join(seq)+')'
    elif respuesta == '2P'      : seq=[str(round(s,1)) for s in (ml1,ml2,x1l1,x2l1,x1l2,x2l2)]     ; opt_str='(ml1,ml2,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == 'CR'      : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS'     : seq=[str(round(s,1)) for s in (ml,x1l,x2l)]                      ; opt_str='(ml,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g'   : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                  ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g_2p': seq=[str(round(s,1)) for s in (ml1,ml2,g,k,x1l1,x2l1,x1l2,x2l2)]      ; opt_str='(ml1,ml2,g,k,,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == '3P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)]   ; opt_str='(ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)_('+','.join(seq)+')'
    elif respuesta == '4P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)] ; opt_str='(ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)_('+','.join(seq)+')'
    else                        : print('No he entendido la respuesta, procedo a SIN LENTES\n\n\n\n\n\n\n\n')
    
    return opt_str       
#--------------------PLOTS------------------------------
cmap_choose='afmhot'
if if_im_plot:
    plt.close();fig=plt.figure(1)  # Figure 1 #plt.rcParams #plt.clf() limpiaría el cuadro en vez de borrarlo
    #SUBPLOT1------------------------------------------
    ax=fig.add_subplot(121) # Left plot
    ax.set_title('Shooting region')
                #--PLOT1--
    ax.plot(x1l,x2l,'+') # Plot positions of stars
                #--PLOT2--
    rayboxx=[-xl1,-xl1,xl1,xl1,-xl1]
    rayboxy=[-xl2,xl2,xl2,-xl2,-xl2]
    ax.plot(rayboxx,rayboxy) # Show Shooting region
                #--PLOT3--
    mapboxx=np.array([-yl,-yl,yl,yl,-yl])
    mapboxy=np.array([-yl,yl,yl,-yl,-yl])
    ax.plot(mapboxx*f1,mapboxy*f2,'r') # Show region mapped onto map

    ax.set_xlim(-1.1*xls,1.1*xls)
    ax.set_ylim(-1.1*xls,1.1*xls)
    ax.set_aspect('equal') # Keep aspect ratio
    #----------------------------------------------------------------------
    plt.show() #muestra el plot

    
if if_im_o_plot:
    plt.close();fig=plt.figure(1)   # Figure 1
    #SUBPLOT1------------------------------------------
    ax1=fig.add_subplot(121) # Left plot
    ax1.set_title('Shooting region')
                #--PLOT1--
    ax1.plot(x1l,x2l,'+') # Plot positions of stars
                #--PLOT2--
    rayboxx=[-xl1,-xl1,xl1,xl1,-xl1]
    rayboxy=[-xl2,xl2,xl2,-xl2,-xl2]
    ax1.plot(rayboxx,rayboxy) # Show Shooting region
                #--PLOT3--
    mapboxx=np.array([-yl,-yl,yl,yl,-yl])
    mapboxy=np.array([-yl,yl,yl,-yl,-yl])
    ax1.plot(mapboxx*f1,mapboxy*f2,'r') # Show region mapped onto map

    ax1.set_xlim(-1.1*xls,1.1*xls)
    ax1.set_ylim(-1.1*xls,1.1*xls)
    ax1.set_aspect('equal') # Keep aspect ratio
    
    #SUBPLOT2----------------------------------------------
    ax2=fig.add_subplot(122) # Right plot
    ax2.set_title('Magnification map') 
            #--PLOT1--
    implot=ax2.imshow(b,origin='lower',cmap=cmap_choose) ; # Display magnification map

    
    #----------------------------------------------------------------------
    plt.show() #muestra el plot



#-------------------------GUARDAR_COMO_FITS------------------------------------
if if_save_plot:
    filename='mic_'+respuesta
    aux.guardar(microls_dir,filename,optional_string(respuesta))  #opt_str=''
elif if_save_fits:
    # no se puede usar "a.guardar()" por que es para imágenes '.png'
    filename='qmic_'+respuesta                                    # Without extension (.fits)		
    writeto(microls_dir+filename + fits_extension,b,clobber=True) # Write fits file # clobber=True sobreescribe.


'''
#--------------------------NOTES--------------------------------------------
12/02 Codigo operativo para python 2.x
Codigo de raw_input sabemos que en python 3.x difiere bastante, sólo es input. Por lo tanto hay que optar por uno de ellos (input para python 3.x)

13/02 Código operativo para python 3.x


24/08 Calling : 'fig', 'fig2'.. or whatever, shows them in the terminal
#----------------------------------------------------------------------------
'''




