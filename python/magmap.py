#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#-----------------------MODULOS--------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from math import pi
import time
#---------MODULOS_AÑADIDOS_MIOS--------------------------
from sys_params import *
from function_params import *
import aux
import lens as l
#---------------------COMIENZO_PROGRAMA--------------------------------------
plt.ion()
plt.close()  
print('#--------COMIENZO_DEL_PROGRAMA_MAGMAP.PY-----------#')
#-------------------PARAMETROS-------------------------------------------
ny=401                       #####IIIIII!!###### (RESOLUCION,S/R, no tocar) # ny=401 (DEFAULT)


#MATRIZ IMAGEN
b=np.zeros((ny,ny))
#---
raypix=15. # This is the number of rays per pixel in absence of lensing.     #####IIIII!!#### (S/R , tocar)    # raypix=15 
sqrpix=np.sqrt(raypix) # Rays per pixel square root (rays/pix in one dir)
sqrinpix=np.sqrt(1./raypix)
#---
scale_xy=2                    ####IIII!!### (CONSISTENCIA, tocar)  --->#xl=2.*yl (DEFAULT)
yl=2.              ;  ys=2.*yl/(ny-1) # Pixel size on source plane  #NO SE TOCA
xl= scale_xy * yl # Size of the shooting region at the image plane                   
xs=ys/sqrpix # Side of the square area transported back by a ray.         


nx=np.round(2*xl/xs)+1# Number of rays on a column/row at the image plane    #I! (se modifica con raypix) 
yr=np.arange(0,nx) # This is an array with pixels on y direction
y,x=np.mgrid[0.0:1.0,0:nx] # Grid with pixel coordinates for a row at the image

perc0=5. # Percentage step for printing progress
perc=5. # Initial value for perc

startt = time.clock()
print('\nProcedemos al cálculo del bucle:\n')
for i in yr: # Loop over rows or rays
    if ((i*100/nx)>=perc): # Check if we have already completed perc.
        perc=perc+perc0 # Increase perc.
        print(round(i*100/nx),"%") # Print progress
            
    x1=-xl+y*xs # Convert pixels to coordinates in the image plane
    x2=-xl+x*xs
    
    #--------------------LENTES-----------------------------------------    
    if respuesta=='P':
        ml=1  #Masa de la lente
        xd=0; yd=0; #COORDENADAS (X,Y) LENTE
        
        y1,y2=l.Point(x1,x2,xd,yd,ml)   #12/02 LENTE PUNTUAL :::DEFAULT: USO FUNCION l.Point (LENTE PUNTUAL)
    #+-+-+-+-+-+-+--+-+-DOS LENTES PUNTUALES+-+-+-+-+-+-+-+-+-+-+-+-
    elif respuesta=='2P':
        ml1=.5;ml2=2.5;  #Masas de las lentes 1 y 2
        x1l1=-.75;x2l1=0; #COORDENADAS (X,Y) LENTE 1
        x1l2=0.75;x2l2=0.; #COORDENADAS (X,Y) LENTE 2
    
        y1,y2=l.TwoPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,ml1,ml2) 
    #+-+-+-+-+-+-+--+-+-+-+-BINARIAS+-+-+-+-+-+-+-+-+-+-+-+-
    elif respuesta=='BIN':
        # necesita: alpha , nu  ->> definidos en function_params.py
        e1    = (1.+1./nu)**(-1)  ;    e2=1-e1; # Razones de masa nu=Mi/M   #e1 [0,1]
        #Y para que coincida con el centroide:
        x1l1=-e2*alpha ; x2l1=0.;  #COORDENADAS (X,Y) LENTE 1
        x1l2= e1*alpha ; x2l2=0.; #COORDENADAS (X,Y) LENTE 2
    
        y1,y2=l.TwoPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,e1,e2)  #BINARIAS
    #+-+-+-+-+-+-+-+-+-+ CHANG-REFSDAL -+-+-+-+-+-+-+--+-+-+--++-+-+-+-
    elif respuesta=='CR':
        k=0  ;g=0.2    # Parámetros de Chang-Refsdal kappa= convergence (CONVERGENCIA), gamma = shear (DISTORSIÓN)
        # Lente puntual pert. cuad ---> k=0. (no convergence) ; g=0.1-0.7 (shear)
        ml=1         #Masa de la lente
        x1l=-1;x2l=x1l #COORDENADAS (X,Y) LENTE
        
        
        y1,y2=l.ChangRefsdal(x1,x2,x1l,x2l,ml,k,g) #CHANG_REFSDAL
    #+-+-+-+-+-+-+-+-+-+-SIS(SINGULAR ISOTHERMAL SPHERE)+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    elif respuesta=='SIS':
        ml=1;#
        x1l=0.4; x2l=0;  #COORDENADAS (X,Y) LENTE
    
        y1,y2=l.SIS(x1,x2,x1l,x2l,ml) #SIS 12/02
    #+-+-+-+-+-+-+-+-+-+-+-+SIS+GAMMA(SINGULAR ISOTHERMAL SPHERE + DISTORSION)-+---+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
    elif respuesta=='SIS+g':
        k=0; g=.3;     # kappa= convergence (CONVERGENCIA), gamma = shear (DISTORSIÓN)
        ml=1  # Masas de la lente
        x1l=0; x2l=0 #COORDENADAS (X,Y) LENTE
    
        y1,y2=l.SIS_dist(x1,x2,x1l,x2l,ml,k,g) # 15/02
    #--------------------------OTRAS!!!LENTES!!!(OPCIONALES)-----------------------------------------------------
    elif respuesta=='SIS+g_2p':
        k=0.0;g=0.0;
        ml1=1.;ml2=3.
        x1l1=0.5; x2l1=0.6
        x1l2=0.1;x2l2=0.1
        
        y1,y2=l.SIS_dist_2P(x1,x2,x1l1,x2l1,x1l2,x2l2,ml1,ml2,k,g) #15/02
        
    elif respuesta=='3P':
        ml1=2. ;ml2=1.; ml3=0.5 #Masa de las lentes
        x1l1=0.; x2l1=0.; #COORDENADAS (X,Y) LENTES
        x1l2=0.;x2l2=1.;
        x1l3=0.;x2l3=1.5;
        
        
        y1,y2=l.ThreePoints(x1,x2,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,ml1,ml2,ml3)   #15/02    
    elif respuesta=='4P':
        ml1=2.;ml2=1.;ml3=0.5 ;ml4=0.1 #MASA DE LAS LENTES
        x1l1=0.; x2l1=0.; #COORDENADAS (X,Y) LENTES
        x1l2=0.; x2l2=1.0;
        x1l3=1.0;x2l3=0.0;
        x1l4=1.0;x2l4=1.0;
        
        y1,y2=l.FourPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4,ml1,ml2,ml3,ml4) #15/02
    elif respuesta=='no':
        continue
    else:
        if j1==1 and j2==1: #12/02 ARTIMAÑA PARA QUE SOLO PRINTEE UNA VEZ EL MENSAJE
            print('No he entendido la respuesta, procedo a SIN LENTES\n\n\n\n\n\n\n\n')
            
    #------------------------------COORDENADAS A PIXELES-------------------------------------------
    i1=(y1+yl)/ys            # Convert coords to pixels at the source plane
    i2=(y2+yl)/ys    
    i1=np.array(np.round(i1),dtype=int)         #13/02 Redefinimos las coordenadas en pixeles como enteros # 12/02 ESTO EN PYTHON 2.x SIGUEN SIENDO REALES (i1=np.round(i1))-> ESTA MAL
    i2=np.array(np.round(i2),dtype=int)
    
    ind=(i1>=0) & (i1<ny) & (i2>=0) & (i2<ny) #13/02 MASCARA Indices of rays falling into our source plane
    i1n=i1[ind] # Coordinates of pixels hitting our source plane
    i2n=i2[ind]
    
    for i in range(np.size(i1n)): # Loop over hits "on target" #13/02 Originalmente era xrange , pero puse range
        b[i2n[i],i1n[i]]+=1 # Increase magnification at those pixels
    y=y+1.0 # Increase the y coordinate of the pixel/rays 13/02 IMPORTANTE!
    
#----------------------NORMALIZACION-------------------------------------
b=b/raypix # Normalize magnification with N_r
#PRINT
print("(100.0 '%') COMPLETE\n")
time_comp = round(time.clock()-startt,3)
print("Exec. time = ",time_comp, ' seconds\n') # Print execution time

print('Magnificacion media=%f5\n'%np.mean(b)) # Print mean magnification


#SOME STATISTICS:
print('max(b)         = %.2f'%b.max())
print('min(b)         = %.2f'%b.min())
print('mean(b)        = %.2f'%b.mean())
print('standard_dev(b)= %.2f'%b.std())


#CONSEJO
print('\nComo consejo, aumentar la consistencia y la señal/ruido, con mapas de baja resolución:\n\n\
      consistencia = xl    = %.2f pix\n\
      S/R          = nx/xl = %.2f \n\
      resolución   = ny/yl = %.2f \n\
      tiempo_computación   = %.2f s\n\
      '%(xl,nx/xl,ny/yl,time_comp))

print('\n#------------FIN_DEL_PROGRAMA_MAGMAP.PY---------------#')

#--------------------OPTIONAL_STRING---------------------------------------
opt_str=''
def optional_string(respuesta):
    global seq     # hacemos global 'seq' para verlo despues    
    if   respuesta == 'P'       : seq=[str(round(s,1)) for s in (ml,xd,yd)]                      ; opt_str='(ml,xd,yd)_('+','.join(seq)+')'
    elif respuesta == '2P'      : seq=[str(round(s,1)) for s in (ml1,ml2,x1l1,x2l1,x1l2,x2l2)]     ; opt_str='(ml1,ml2,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == 'BIN'     : seq=[str(round(s,1)) for s in (e1,e2,x1l1,x2l1,x1l2,x2l2)]                    ; opt_str='(e1,e2,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'     
    elif respuesta == 'CR'      : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS'     : seq=[str(round(s,1)) for s in (ml,x1l,x2l)]                      ; opt_str='(ml,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g'   : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                  ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g_2p': seq=[str(round(s,1)) for s in (ml1,ml2,g,k,x1l1,x2l1,x1l2,x2l2)]      ; opt_str='(ml1,ml2,g,k,,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == '3P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)]   ; opt_str='(ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)_('+','.join(seq)+')'
    elif respuesta == '4P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)] ; opt_str='(ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)_('+','.join(seq)+')'
    else                        : print('No he entendido la respuesta, procedo a SIN LENTES\n\n\n\n\n\n\n\n')
    
    return opt_str       
      
      
      
#--------------------PLOTS---------------------------------------------------
cmap_choose='gnuplot2'
if if_im_plot:
    fig1=plt.figure(1) ; plt.clf();
    ax1=fig1.gca()
    ax1.set_title('IMAGEN(x)(Magnification map)')
    #PLOT1
    rule_normal=None  # Para cambiar descomentando la línea siguiente:
    rule_normal= Normalize(vmin=0,vmax=10,clip=True)  #clip=True. # Creo una normalizacion para el imshow:
    implot=ax1.imshow(b,extent=(-xl,xl,-xl,xl),norm=rule_normal,cmap=cmap_choose) # 13/02 DEFAULT vmin=0, vmax=15     
    fig1.colorbar(implot)


if if_save_plot:
    aux.guardar(magmaps_dir,'magmap_'+respuesta,optional_string(respuesta)) #opt_str=''


#-----------------------------CURVE--------------
#CREAR CELDAS ES UTIL, CON CTRL+ENTER puedes ejecutar parte del código donde tengas el cursor (celda seleccionada)
#%%
def curve(u0,theta,comps=ny):   # ny bajo para probar
    global y1_or,y2_or
    y1_or,y2_or= ( 0 - u0*np.sin(theta), 0 + u0*np.cos(theta) )    #BIEN                  
    #global func,func_inv
    func     = lambda var     : np.tan(theta)*( var - y1_or) + y2_or    # y(x)
    func_inv = lambda var_inv : (var_inv-y2_or)/np.tan(theta) + y1_or   # x(y)       
    #global y1_muestra,y2_muestra
    y1_muestra=np.linspace(-xl,xl,comps)   # Creamos muestras iniciales para ver donde cruzan nuestras curvas
    y2_muestra= func(y1_muestra)
    
    Ptop_y2_curve=y2_muestra[-1] ; Pbot_y2_curve=y2_muestra[0]  # Inicializamos valores
    
    if  Ptop_y2_curve > xl:     #PLANO SUPERIOR
        Ptop_y2_curve = xl             ; Ptop_y1_curve= func_inv(Ptop_y2_curve)  
    elif Ptop_y2_curve < -xl:  #PLANO INFERIOR  
        Ptop_y2_curve = -xl            ; Ptop_y1_curve= func_inv(Ptop_y2_curve)          
    else:                        #PLANO DERECHO 
        Ptop_y1_curve = xl             ; Ptop_y2_curve = func(Ptop_y1_curve)  
      
    if Pbot_y2_curve > xl:      #PLANO SUPERIOR
        Pbot_y2_curve = xl            ; Pbot_y1_curve= func_inv(Pbot_y2_curve)        
    elif  Pbot_y2_curve < - xl: #PLANO INFERIOR
        Pbot_y2_curve = -xl            ; Pbot_y1_curve= func_inv(Pbot_y2_curve)
    else:                        #PLANO IZQUIERDO
        Pbot_y1_curve = -xl            ; Pbot_y2_curve = func(Pbot_y1_curve)     

    y1_curve=np.linspace(Pbot_y1_curve,Ptop_y1_curve,comps) # Redefino para hacer el buen intervalo:
    y2_curve = func(y1_curve)
    
    Pbot_y2_curve=func(Pbot_y1_curve) ; Ptop_y2_curve=func(Ptop_y1_curve)
    
    print('Pbot_y1_curve= %.2f ; Ptop_y1_curve= %.2f'%(Pbot_y1_curve,Ptop_y1_curve))
    print('Pbot_y2_curve= %.2f ; Ptop_y2_curve= %.2f'%(Pbot_y2_curve,Ptop_y2_curve))
    
    fig1=plt.figure(1);# no a plt.clf(), queremos que salga con todo # clean the active figure
    ax2 = fig1.add_subplot(111)
    ax2.set_title('IMAGEN(x)(1D cut from magn. map)') ;plt.xlabel('X');plt.ylabel('Y')
    ax2.plot(y1_or   ,y2_or   ,'ro',markersize=2)  ### III!!
    ax2.plot(y1_curve,y2_curve,'g-',linewidth=0.6) 
    img_axe_plus = 0.           # DEFAULT=0. # Ver graficamente si la linea se pasa de la caja
    #ax2.axis([-xl-img_axe_plus,xl+img_axe_plus,-xl-img_axe_plus,xl+img_axe_plus])
    if task_microl_nature or task_binarias:
        ax2.plot(scale_xy*x1l1,scale_xy*x2l1,'wx',label='Masa 1');
        ax2.plot(scale_xy*x1l2,scale_xy*x2l2,'gx',label='Masa 2')
        ax2.legend(loc=0)
    if if_save_lightcurve:
        fig1.savefig(lightcurves_dir+'current_1Dcut'+image_extension)
        fig1.savefig(lightcurves_dir+'1Dcut_'+respuesta+optional_string(respuesta)+image_extension)
                
         
    return y1_curve,y2_curve   #i1_curve,i2_curve

#y1_curve,y2_curve=curve(0,0)

#%%
#SOME OPTIONS-------------------------------------:
#from matplotlib.colors import LogNorm
#norm=LogNorm()
#bbox_inches='tight'

#LIGHT_CURVES
def light_curve(u0,theta): 
    print('\n-------START LIGHT-CURVES_1D------------\n')
    global y1_curve,y2_curve
    y1_curve,y2_curve= curve(u0,theta_mod(theta))
    global i1_curve,i2_curve
    i1_curve = (y1_curve/scale_xy + yl)/ys ; i1_curve=np.array(np.round(i1_curve),dtype=int) # Convert coords to pixels at the source plane
    i2_curve = (y2_curve/scale_xy + yl)/ys ; i2_curve=np.array(np.round(i2_curve),dtype=int)
    #II! Necesario y1_curve/scale_xy dado que y1_curve en realidad está calculado en el plano imagen
    
    fig2=plt.figure(2); plt.clf(); #plt.figure(numero) activa la figura "número" o la crea si no existe
    ax3=fig2.gca()#ax2=fig2.add_subplot(111)
    ax3.grid()
    ax3.set_title('Light-Curve (1D cut from magn. map) (lente %s)'%respuesta)
    ax3.set_xlabel('Time(x_bins)'); # se puede traducir a tiempo a través del timescale de la lente
    ax3.set_ylabel('Magnification') # sin unidades
    #curve_ind =round(len(b)/2.)
    cadena_label='1Dcut: u0=%.1f ; theta= %.1f'%(u0,theta)
    ax3.plot(b[i2_curve,i1_curve],label=cadena_label,marker='o',markersize=.3) # primero va el eje vertical, luego el horizontal  !!!III!
    ax3.legend(loc='upper left')
    #markersize=1, r*'

    if if_save_1Dcut:
        fig2.savefig(lightcurves_dir+'current_lc'+image_extension)  
        fig2.savefig(lightcurves_dir+'lc_'+respuesta+optional_string(respuesta)+image_extension)   
       
    print('\n-------END LIGHT-CURVES_1D------------\n')
    return
''' DEFINIDO EN function_params.py
u0        = 0
theta_mod = lambda theta : theta % (2*pi) ; 
theta     = 0*pi/4 # theta (-pi/2,pi/2)  # theta(-1.5708,+1.5708)
'''
if task_lightcurve :
    light_curve(u0,theta_mod(theta)) # call the function
    
# se puede hacer:
# o cambiar este último rango para ver las cosas mejor (centro=200)    
    
#plt.plot(b[200,0:400])  # corte VERTICAL
#plt.imshow(b[180:220,0:400]) # eje VERTICAL
    
#plt.plot(b[0:400,200])  # corte HORIZONTAL
#plt.imshow(b[0:400,180:220])  # eje HORIZONTAL  
    
# SE COMPRUEBA QUE ESTA BIEN  # primero va el eje vertical, luego el horizontal en imshow !!!III!  
#%%

'''
#--------------------------NOTES---------------------------------------------
12/02 Tenemos que corregir i1, i2 para que sean listas de enteros y no reales, se puede hacer con numpy.ndarray(i1,dtype='int') por ejemplo.

13/02 El programa está operativo en python 2.x

13/02 El programa está operativo en python 3.x

13/02 Añadidas las funcionesde lens.py para las lentes como if dentro de los bucles for, elegir cada caso variando la variable 'respuesta' tal como se muestra.

25/08 Basta mejora. Terminado.
#----------------------------------------------------------------------------
'''
