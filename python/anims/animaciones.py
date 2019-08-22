import numpy as np 
import matplotlib.pyplot as plt
import os,time
import glob
import subprocess

# NO CORRER ESTE FICHERO. SIRVE DE GUÍA.

path=os.getcwd()
os.chdir(path)
list_images=os.listdir(path)

respon='hst_08591'


lista_respon = [img for img in glob.glob(os.path.join(respon+'*.png'))]
lista_respon=sorted(lista_respon)
#-----BIEN,pasos seguros

lista_respon[:5]=lista_respon[:5][::-1]  # 5 se ve a ojo, puede ser otro numero. Se recomienda trasteo manual por consola

      
lista_respon_abs = [img for img in glob.glob(os.path.join(path+'/'+respon+'*.png'))] 
lista_respon_abs=sorted(lista_respon_abs)

#os.system('convert -loop 0 %s ./SIS_hor.gif' %' '.join(lista_respon_abs)) # uses sh

os.system('convert -delay 30 -loop 0 %s ./hdf_fits_SIS_hor.gif ' %('"'+'" "'.join(lista_respon)+'"')) # mas general, prepara los archivos según el idioma de 'bash'


# ./P_vert.gif
# ./hdf_image_SIS_hor.gif
# ./hdf_fits_SIS_hor.gif
# ./CR_vert.gif
# ./SIS_hor.gif
# ./SIS+g_hor.gif
