#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:16:10 2018
This file is on purpose of defining some parameters that could be useful in order to 
mantain and develop the archive tree and system of photos, reports, etc.
@author: arioboo
"""
#----------------MODULOS-----------------------------------
import numpy as np
import matplotlib.pyplot as plt
import os, sys
#---------MODULOS_ANADIDOS_MIOS--------------------------
# (no necesitamos importar modulos)
# poner :
#from sys_params import *  #( charge this module)
#--------------------------------------------------------

#os.name  es 'posix' para Linux y 'nt' para Windows
#os.getcwd() nos da el current working directory
#sys.platform nos dice la plataforma
print("-------- sys_params.py OUTPUT:----------\n")
if os.name == 'posix' : #VERIFICAMOS SI EL SISTEMA ES LINUX
    cwd   =   os.getcwd()+'/'  #workdir 	=  '/home/arl94/PENDRIVE/entregables/2Sem/ascomp/carpeta_japon/python_wsbook_programs/'
    opsystem  =   sys.platform
    
    print("workdir='%s'"%cwd)
    print("operative_system='%s'"%opsystem)
    
   #DIRECTORIES---
    initialsources_dir = cwd + 'initial_sources/'
    images_dir         = cwd + 'images/'
    anims_dir          = cwd + 'anims/'     
    CASTLES_dir        = cwd + 'CASTLES/'
    HDF_dir            = cwd + 'HubbleDeepField/'
    magmaps_dir        = cwd + 'magmaps/'
    lightcurves_dir    = magmaps_dir + 'light_curves/'
    microls_dir        = cwd + 'microls/'
    #pdfs_dir   =  cwd + '/pdfs/'
    #latex_dir =  cwd + '/latex/'
    #zips_dir   =  cwd + '/zips/' 
    
    
    #EXTENSIONS---
    initial_sources_extension = '.jpeg' 
    image_extension   = '.png'  #'.png' (# '.png','.jpeg','.jpg','.pdf' 
    anims_extension   = '.gif'
    
    latex_extension	 = '.tex'  #'.tex' (# '. '
    tar_extension 	 = '.tar'  #'.zip' (#'.tar','.gz','.bz','.bz2'...
    fits_extension    = '.fits' #'. '   (#'.
    pdf_extension	     = '.pdf'  #'.pdf' (# '. '
    
elif os.name == 'nt': 
    print('\nERROR:\nEl sistema operativo no es Linux, no se recomienda hacer operaciones con scripts')
     
    ''' 
    cwd  =   os.getcwd()  
    opsystem  =   sys.platform
    
    print("workdir='%s'"%workdir)
    print("operative_system=%s"%opsystem)
    '''
    
    
print("-------- sys_params.py END:-------------\n")  


