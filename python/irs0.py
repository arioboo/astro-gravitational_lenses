#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018
@author: arioboo
"""
#----------------MODULOS-----------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os , time
from scipy import ndimage
#---------MODULOS_AÑADIDOS_MIOS--------------------------
from sys_params import *
from function_params import *

import source as s
import lens as l
import aux
#from Point import *  #Esto ya está incluido en lens
#------------------------COMIENZO_PROGRAMA--------------------------------
plt.ion()
plt.close()  
print('#--------------COMIENZO_PROGRAMA----------------------#')
#--------------------PIXEL_MAP-------------------------------------------------
nx=401 #Number of pixels in image plane   DEFAULT=401
ny=2*nx #Number of pixels in source plane   DEFAULT=401

xl=2. #Half size of image plane covered (in "Einstein radii")
yl=2. #Half size of source plane covered (in "Einstein radii")#------------------FINAL_PROGRAMA------------------------------------------------

xs=2.*xl/(nx-1) # pixel size on the image map
ys=2.*yl/(ny-1) # pixel size on the source map
#---------------------Source parameters---------------------------------------
xpos=0.0 # Source position. X coordinate  DEFAULT=0.0
ypos=0.0 # Source position. Y coordinate  DEFAULT=0.0

rad=0.2 # Radius of source  DEFAULT=0.1
ipos=int(round(xpos/ys))
#---------------------------Convert source parameters to pixels-------------------------
jpos=int(round(-ypos/ys))
rpix=int(round(rad/ys))


#--SOURCE_PLANE---
if if_source_defined:
    a=s.gcirc(ny,rpix,jpos,ipos) # This is a circular gaussian source (FUENTE DE ANILLOS!)
    #a=s.cuadrada(ny,rpix,jpos,ipos)
    #a=s.circular(ny,rpix)
    #a=s.anillos(ny,rpix)
elif if_source_fits:

    print('Puedes escoger entre las siguientes imágenes ".fits" ó ".jpg" :\n')
    lista_images=[]  ; iterator=0

    for name in os.listdir(HDF_dir):  
        if name.endswith('.fits') or name.endswith('.jpg'):
            lista_images.append(name);            print('[%i] %s'%(iterator,name))
            iterator+=1        
    
    print ('\nElige un número entero entero desde %i hasta %i:'%(0,len(lista_images)-1)) ;
    eleccion=int(input())        
    
    if lista_images[eleccion].endswith('.fits'): 
        imgname= lista_images[eleccion][0:-len('.fits')]
        a=s.fitsim(HDF_dir+imgname+'.fits') # This is a real galaxy source of a .fits archive 
        # NO HAY QUE REDEFINIR INDICES!    # ny ~ 2024 , nx ~3/2 ny , inaceptable, alto tiempo computacion, para eso se queda con los que tiene
        #ny=a.shape[0]       ; ys=2*yl/(ny-1)     
        #nx=2*ny             ; xs=2*xl/(nx-1)
    elif lista_images[eleccion].endswith('.jpg'):
        imgname= lista_images[eleccion][0:-len('.jpg')]
        a=ndimage.imread(HDF_dir+imgname+'.jpg')
        # Es una matrix (m x n x l) --> (m x n) , l es 3, no se porque sale asi
        a=a[:,:,0]         #a=a[:,:,1]          #a=a[:,:,2]
        # HAY QUE REDEFINIR INDICES!
        ny=a.shape[0]       ; ys=2*yl/(ny-1)   # ny ~ 500 , aceptable , para que cumpla condiciones del bucle
        nx=2*ny             ; xs=2*xl/(nx-1)   
        
        
        
#--IMAGE_PLANE----
b=np.zeros((nx,nx)) # This is the image plane. We define a nule matrix to be filled up

start_time=time.clock() ; print('---start_time = 0.00 seg ')
#--------------------BUCLE_PRINCIPAL----------------------------------------------------
#This is the main loop over pixels at the image plane
for j1 in range(nx):
    	for j2 in range(nx):
        #-------------CONVERSION DE PIXELES A COORDENADAS EN LA IMAGEN------------
            x1=-xl+j2*xs # Convert pix to coords on image.
            x2=-xl+j1*xs
        #12/02-----------AQUÍ ES DONDE TENEMOS QUE DEFINIR LAS COORDENADAS DE
        #LA FUENTE O IMAGEN, COMO DEFAULT SE TOMA EL ANGULO DE DEFLEXION = 0, USAMOS
        #LENS.PY , CUALQUIER FUNCION DEFINIDA DENTRO DE ESE FICHERO--------------
        #12/02 ECUACION DE LAS LENTES (IRS, INVERSE RAY SHOOTING) (SIN LENTES)
            #------------------FINAL_PROGRAMA------------------------------------------------

            y1=x1-0.0 # Deflect X coordinate     DEFAULT=0.0
            y2=x2-0.0 # Deflect Y coordinate     DEFAULT=0.0
        		
         #-----------------------------FUNCION_DE_LENS+PARAMETROS-----------------
            # DEFINIDO EN function_params.py
            #respuesta='SIS+g' #12/02 NECESITO UN DESCRIMINADOR PARA EL TIPO DE LENTE ('P','2P','CR','SIS')
                              #15/02 TAMBIÉN ('SIS+g','SIS+g_2p','3P','4P')
            #+-+-+-+-+-+-+-+-+-+- LENTE PUNTUAL +-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-++
            if respuesta=='P':
                ml=1  #Masa de la lente
                xd=0; yd=0; #COORDENADAS (X,Y) LENTE
                
                y1,y2=l.Point(x1,x2,xd,yd,ml)   #12/02 LENTE PUNTUAL :::DEFAULT: USO FUNCION l.Point (LENTE PUNTUAL)
            #+-+-+-+-+-+-+--+-+-DOS LENTES PUNTUALES+-+-+-+-+-+-+-+-+-+-+-+-
            elif respuesta=='2P':
                ml1=1.;ml2=.1;  #Masas de las lentes 1 y 2
                x1l1=0.75;x2l1=0.; #COORDENADAS (X,Y) LENTE 1
                x1l2=0.75;x2l2=0.; #COORDENADAS (X,Y) LENTE 2
            
                y1,y2=l.TwoPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,ml1,ml2)                  
            #+-+-+-+-+-+-+--+-+-+-+-BINARIAS+-+-+-+-+-+-+-+-+-+-+-+-
            elif respuesta=='BIN':
                alpha = 1         #separaciones 'a'
                e1    = 1  ;    e2=1-e1;  # Razones de masa Mi/M  #e1 [0,1]
                #Y para que coincida con el centroide:
                x1l1=-e2*alpha ; x2l1=0;  #COORDENADAS (X,Y) LENTE 1
                x1l2= e1*alpha ; x2l2=0.; #COORDENADAS (X,Y) LENTE 2
            
                y1,y2=l.TwoPoints(x1,x2,x1l1,x2l1,x1l2,x2l2,e1,e2)  #BINARIAS                
            #+-+-+-+-+-+-+-+-+-+ CHANG-REFSDAL -+-+-+-+-+-+-+--+-+-+--++-+-+-+-
            elif respuesta=='CR':
                k=0  ;g=0.2    # Parámetros de Chang-Refsdal: kappa= convergence (CONVERGENCIA), gamma = shear (DISTORSIÓN)
                # Lente puntual pert. cuad ---> k=0. (no convergence) ; g=0.1-0.7 (shear)
                ml=1         #Masa de la lente
                x1l=1;x2l=x1l #COORDENADAS (X,Y) LENTE
                
                y1,y2=l.ChangRefsdal(x1,x2,x1l,x2l,ml,k,g) #CHANG_REFSDAL
            #+-+-+-+-+-+-+-+-+-+-SIS(SINGULAR ISOTHERMAL SPHERE)+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
            elif respuesta=='SIS':
                ml=1;#
                x1l=0.4; x2l=0;  #COORDENADAS (X,Y) LENTE
            
                y1,y2=l.SIS(x1,x2,x1l,x2l,ml) #SIS 12/02
            #+-+-+-+-+-+-+-+-+-+-+-+SIS+GAMMA(SINGULAR ISOTHERMAL SPHERE + DISTORSION)-+---+-+-+-+--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
            elif respuesta=='SIS+g':
                k=0; g=.3;     # kappa= convergence (CONVERGENCIA), gamma = shear (DISTORSIÓN)
                ml=1            # Masa de la lente
                x1l=0; x2l=0  #COORDENADAS (X,Y) LENTE
            
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
                
                
            
        #-------------------------PARTE_FINAL-----------------------------------------------
            i2=int(round((y1+yl)/ys)) # Convert coordinates to pixels
            i1=int(round((y2+yl)/ys))
            	    # If deflected ray hits a pixel within source then set image
            	    # to brightness on that pixel
            if ((i1 >= 0) and (i1 < ny) and (i2 >= 0) and (i2 < ny)):
                b[j1,j2]=a[i1,i2]
            
print('---final_time = %.4s seg' %(time.clock()-start_time))
 

#------------------------------------------------------------------------------
opt_str='' # INICIALIZAMOS LA VARIABLE opt_str  ( no pone nada más si no ponemos algo nosotros en la funcion)

def optional_string(respuesta):
    global seq     # hacemos global 'seq' para verlo despues    
    if   respuesta == 'P'       : seq=[str(round(s,1)) for s in (ml,xd,yd)]                      ; opt_str='(ml,xd,yd)_('+','.join(seq)+')'
    elif respuesta == '2P'      : seq=[str(round(s,1)) for s in (ml1,ml2,x1l1,x2l1,x1l2,x2l2)]   ; opt_str='(ml1,ml2,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == 'BIN'     : seq=[str(round(s,1)) for s in (e1,e2,x1l1,x2l1,x1l2,x2l2)]                    ; opt_str='(e1,e2,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')' 
    elif respuesta == 'CR'      : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS'     : seq=[str(round(s,1)) for s in (ml,x1l,x2l)]                    ; opt_str='(ml,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g'   : seq=[str(round(s,1)) for s in (ml,g,k,x1l,x2l)]                ; opt_str='(ml,g,k,x1l,x2l)_('+','.join(seq)+')'
    elif respuesta == 'SIS+g_2p': seq=[str(round(s,1)) for s in (ml1,ml2,g,k,x1l1,x2l1,x1l2,x2l2)]   ; opt_str='(ml1,ml2,g,k,,x1l1,x2l1,x1l2,x2l2)_('+','.join(seq)+')'
    elif respuesta == '3P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)]  ; opt_str='(ml1,ml2,ml3,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3)_('+','.join(seq)+')'
    elif respuesta == '4P'      : seq=[str(round(s,1)) for s in (ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)] ; opt_str='(ml1,ml2,ml3,ml4,x1l1,x2l1,x1l2,x2l2,x1l3,x2l3,x1l4,x2l4)_('+','.join(seq)+')'
    else                        : print('No he entendido la respuesta, procedo a SIN LENTES\n\n\n\n\n\n\n\n')
    
    return opt_str 

# ----------------------PLOTTING--------------------------------------------

if if_source_defined:
    cmap_choose='afmhot'
    if if_im_plot:
                           #limpia figura si hay existente
        fig=plt.figure(1);plt.clf()                #genera marco de la figura si no existe y queda activa para los comandos plt.         
        #PLOT_IMAGEN  
        ax=fig.gca()                                                #llama a todo ese marco    
        ax.imshow(b,extent=(-xl,xl,-xl,xl),cmap=cmap_choose);ax.set_title('IMAGEN(x)'); # genera el gráfico        
    if if_im_o_plot:
  
        fig=plt.figure(1) ; plt.clf()
                 
        #SUBPLOT1_FUENTE
        ax1=fig.add_subplot(121)
        ax1.imshow(a,extent=(-yl,yl,-yl,yl),cmap=cmap_choose);ax1.set_title('FUENTE/OBJETO(y)');
        #SUBPLOT2_IMAGEN
        ax2=fig.add_subplot(122)
        ax2.imshow(b,extent=(-xl,xl,-xl,xl),cmap=cmap_choose);ax2.set_title('IMAGEN(x)');
    #GUARDA EL PLOT    
    if if_save_plot : 
        plt.figure(1)
        aux.guardar(images_dir,respuesta,opt_str=optional_string(respuesta)) 
        
        











if if_source_fits:
    cmap_choose='afmhot'
    if if_HDF_im_plot:
        plt.close()                     #limpia figura si hay existente
        fig=plt.figure()                #genera marco de la figura  
        
        rule_norm=Normalize(vmin=0,vmax=1e-6,clip=True)
        #PLOT_IMAGEN  
        ax=fig.gca()                                                #llama a todo ese marco    
        ax.imshow(b/b.sum(),extent=(-xl,xl,-xl,xl),cmap=cmap_choose,norm=rule_norm);ax.set_title('IMAGEN(x)'); # genera el gráfico
        #plt.show()
        
    if if_HDF_im_o_plot:
        plt.close()    
        fig=plt.figure()
        
        
        rule_normal_a=Normalize(vmin=0,vmax=10*np.mean(a))
        rule_normal_b=Normalize(vmin=0,vmax=10*np.mean(b))         
        #SUBPLOT1_FUENTE
        ax1=fig.add_subplot(121)
        ax1.imshow(a,extent=(-yl,yl,-yl,yl),cmap=cmap_choose,norm=rule_normal_a);ax1.set_title('FUENTE/OBJETO(y)');
        #SUBPLOT2_IMAGEN
        ax2=fig.add_subplot(122)
        ax2.imshow(b,extent=(-xl,xl,-xl,xl),cmap=cmap_choose,norm=rule_normal_b);ax2.set_title('IMAGEN(x)');
    if if_HDF_save_plot:
        plt.savefig(HDF_dir+imgname+'_'+respuesta+optional_string(respuesta)+image_extension)


#------------------FINAL_PROGRAMA------------------------------------------------
print('#----------------FINAL_PROGRAMA-----------------------#')



      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
if if_aclaraciones :               
    #-------------------EXPLICACIONES_MIAS-----------------------------------------
    print('\nACLARACIONES:\n\n\
    Hemos definido que tanto la fuente como el objeto tengan un grid de 2000x2000, pero nuestros objetos se hicieron con un grid de 1000x1000\n\
    Según tengo entendido:\na = fuente/objeto\nb = imagen\n(xpos,ypos) = Posición del objeto en el grid de 2000x2000 \n(xs,ys) = Tamaño del pixel en la imagen(xs) y en la fuente(ys)\n\
    (nx,ny) = Numero de pixeles en la imagen(nx) y en la fuente(ny)\n(xl,yl) = Tamaño medio del plano de la imagen(xl) y fuente(yl) en Radios de Einstein\n\n\
    Por lo general, tendremos 4 veces 1000x1000 que corresponde a 2000x2000, y esto es igual para la fuente y la imagen. Esto irá variando a lo largo de la práctica y según los parámetros que definamos.\n')
    
    
    
    """
    #------------------------------NOTES----------------------------------------
    08/02 Programa operativo para python 2.x
    
    11/02 Programa operativo para python 3.x
    
    12/02 Añadida compatibilidad con lentes y sus funciones . 'P','2P','CR,'SIS' o sin lente. Puede haber obviamente otros modelos de lentes no incluidos
    en el programa, pero se pueden añadir dento del for con un "if". Existe el modelo Non Singular Isothermal Sphere (NSIS) pero no lo contemplaremos aquí, 
    esto cambia el core de la lente para evitar la singularidad central. Se mencionan otros modelos posibles:
        - mayor que 2p lentes
        - NSIS (spheres or ellipsoids) with or without external shear
    
    Con los mapas de magnificación, seremos capaces de hacer el proceso contrario, es decir hallar los parámetros (como masa, convergencia, shear) y el tipo de lentes
    que estamos usando a partir de estos mapas.
    
    13/02 La distorsión es sólamente añadiendo un gamma~=0 , con lo que tendremos distorsión en la lente
    
    15/02 Añadidas las lentes SIS+g, SIS+g_2p, 3P,4P
    #---------------------------------------------------------------------------
    """