#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018

@author: arioboo
"""
#---------------------------------MODULOS--------------------------------------
import numpy as np
import matplotlib.pylab as pl

#---------MODULOS_AÑADIDOS_MIOS--------------------------
from sys_params import *

# ------------------GENERAL:---------------------------------
respuesta='BIN' #12/02 NECESITO UN DESCRIMINADOR PARA EL TIPO DE LENTE ('P','2P','BIN','CR','SIS')#15/02 TAMBIÉN ('SIS+g','SIS+g_2p','3P','4P')
#source.py
if_save_sources       =             1              # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
if_test_sources       =             0              # 0 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
  
#------------TASKS----------------------------
# DEJAR TODOS LOS VALORES SIGUIENTES A CERO SALVO LA TAREA REQUERIDA
task_sources    =   0    #0 

task_irs0       =   1    #0  

task_magmap     =   0    #0 

#--
if task_magmap:  
    task_lightcurve  =  1 # 1  # NO MODIFICAR  
           
    task_binarias      =  0 # 0  
    task_microl_nature =  0  #0
    if task_binarias: respuesta='BIN'       # 'BIN' (por si acaso nos despistamos)
    elif task_microl_nature: respuesta='BIN'

               



    
#___________________irs0.py___________________________   
if task_irs0:
    #TIPO DE FUENTE (definidas por usuario , o a través de imágnes '.fits' o '.jpeg')
    if_source_defined  =                0                   # 0 .!!!I!! ELEGIR LA FUENTE EN IRS0.py
    if_source_fits     =             not if_source_defined  # Elegir una u otra
    #PLOTTING
    if if_source_defined:
        #PLOTTTING (imagen ,ó imagen y objeto)
        if_im_plot            =             0                   # 0 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
        if_im_o_plot          =             not if_im_plot      # not if_im_plot (para que no solape con el otro plot) . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
        #SAVE_PLOT
        if_save_plot          =             1                   # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
    #--------------
    if if_source_fits:    
        #PLOTTING (imagen ,ó imagen y objeto)
        if_HDF_im_plot        =             0
        if_HDF_im_o_plot      =             not if_HDF_im_plot
        #SAVE_PLOT
        if_HDF_save_plot      =             1                     # 1 (para que no solape con el otro plot) . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO 
    #ACLARACIONES
    if_aclaraciones    =                0               # 0.  MODIFICAR PARA CORRECTO FUNCIONAMIENTO.

#______________________magmap.py__________________________

if task_magmap:
    #PLOTTING (imagen , imagen y objeto)
    if_im_plot            =             1                   # 0. NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO 
    #SAVE
    if_save_plot          =             1                   # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO    
    #PARAMS------------------
    u0        = 0               # (1)u0= -0.054       (2)u0=0.106     (3)u0=0.234
    theta_mod = lambda theta : theta % (2*np.pi) ; 
    theta     = 1*np.pi/2       # (1)theta=0.086 (2)theta=-0.664 (3)theta=2.583
    # en caso de Binarias (sin task 'binarias'):
    nu= 0.418 ;alpha= 0.931;
        
    #TASK_LIGHTCURVE:    
    if task_lightcurve:

        if_save_lightcurve   =             1                   # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO 
        if_save_1Dcut        =             if_save_lightcurve  # MISMO QUE EL ANTERIOR
    #TASK_BINARIAS
    if task_binarias:
        print('Eventos binarios de microlensing:')
        # 1 y los demás 0
        binaria_1=1   #LMC-9     u0 =-0.054 ;theta= 0.086 ;alpha = 1.657 ;nu = 1.627 #BIEN
        binaria_2=0   #95-BLG-12 u0 = 0.106 ;theta=-0.664 ;alpha = 0.421 ;nu = 2.148 #BIEN
        binaria_3=0   #97-BLG-1  u0 = 0.234 ;theta= 2.583 ;alpha = 0.931 ;nu = 0.418 #BIEN
        if   binaria_1: u0 =-0.054 ;theta= 0.056 ;alpha = 1.657;nu = 1.627 #BIEN
        elif binaria_2: u0 = 0.207 ;theta= -0.67 ;alpha = 0.46 ;nu = 2.148 #BIEN
        elif binaria_3: u0 = 0.234 ;theta= 2.900 ;alpha = 1.01 ;nu = 0.598 #BIEN
 
    #TASK_MICROL
    if task_microl_nature:
        print('Evento de microlensing_NATURE:')
        alpha = 1.610  # 1.610+-0.008   (d)   (-)
        nu    = 7.6e-5 # (7.6+-0.7)e-5  (q)   (+)
        u0    = 0.359  # 0.359+-0.005   (closest approach) (+) 
        theta = 2.756  # 2.756+-0.003  (theta)  (+)  
    #ACLARACIONES
    if_aclaraciones       =             0         # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO

    
'''    
#_____________________qmic.py__________________________

if task_qmic:
    #PLOTS (imagen , imagen y objeto)
    if_im_plot            =             0                   # 0. NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO 
    if_im_o_plot          =             not if_im_plot      # not if_im_plot (para que no solape con el otro plot) . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO   
    #SAVE
    if_save_plot          =             1                   # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
    if_save_fits          =             not if_save_plot    # 1 . NO MODIFICAR PARA UN CORRECTO FUNCIONAMIENTO
#--------------
'''