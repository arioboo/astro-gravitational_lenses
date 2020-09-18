#------------------------------------------------------------------------------------------------
#-- Seguimiento de la práctica de la asignatura Astrofísica Computacional por días de trabajo  --
#------------------------------------------------------------------------------------------------
PROGRAMAS ADAPTADOS DE PYTHON 2.x a PYTHON 3.x
Año 2018

05/02	Creación carpeta_japon , practica (WORKDIR:/media/MEGA_PEN/entregables/2Sem/ascomp/practica/)
Comienzo en la carpeta $WORKDIR$/FORTRAN con algunos archivos para compilar, inmediatamente el proyecto fracasa porque FORTRAN es complicado y es difícil plotear.
Solucion: Paso a Python

08/02:	Creación de la carpeta Python (WORKDIR:/media/MEGA_PEN/entregables/2Sem/ascomp/practica/)
Comienzo en la carpeta $WORKDIR$/Python 
Creación de fuentes extensas cuadrada, circular , y anular. Ploteo con imshow

11/02: Creación de la carpeta python_wsbook_programs (WORKDIR2:/media/MEGA_PEN/entregables/2Sem/ascomp/carpeta_japon/)
Comienzo en la carpeta $WORKDIR2$/python_wsbook_programs. Hago una recopilación de todos los programas escritos en el archivo y artículo wsbook.pdf del profesor(Evencio Mediavilla)
Compilo los programas (source.py..irs0.py)  y hago pequeñas modificaciones ornamentales (print y espaciados entre otros). El output de las imagenes y fuentes se muestra sin problema.
Modulos añadidos: ( source.py ..irs0.py)
	- source.py as s
	- lens.py as l
Modificaciones lens.py:
	- Añado (ademas de lente puntual): Binarias, Chang-Refsdal, SIS (singular isothermal sphere)
Compilado ers1.py, modificaciones:
	- Ornamentales (print,#s)
	- Compatibilidad (python 2.x > 3.x)
Añadidas los diversos tipos de lentes a ers1.py

12/02: Hecha una gran mejora de los archivos. Añadidas notas y comentarios a la mayoría de ellos. El código de "irs0.py" ya dispone de las lentes para ser usadas en la computación, se puede usar
cualquier lente de las disponibles con cualquier parámetro disponible. 

Quedan hacer las imagenes con ésto y el vídeo (que no sé de qué trata realmente).

El siguiente paso son los mapas de magnificación.




15/02: Hechos los mapas de magnificación.

El siguiente paso es hacer cortes en los mapas de magnificación.





02/08: Añadida la funcionalidad para descargar imágenes del DST , HLA, MAST.

Cargarlas con "source.py" , la rutina fitsims() a partir del archivo fits que queremos cargar.

04/08: Importado a "sys_params.py" la posibilidad de verificar si el sistema es Linux o no . (La estructura de directorios, comandos, y opciones de guardado 
y zipeado varían enormemente). Si es Windows no deja ejecutar el programa (a propósito)

Implementado "from sys_params import *" en todos los ".py" necesarios.

20/08: Implementado function_params.py , sirve para controlar los procesos de todos los ficheros ".py". Muchas funcionalidades introducidas por medio de variables, if_variables , y for_variables.

21/08: Basta mejora a "sources.py". El tiempo de computación para las lentes cuadrada y gcirc es bastante corto, en cambio, para las lentes circular y de anillos concéntricos el tiempo se dispara a ~10s . De todas maneras, no es muy problemático.

4 LENTES: gcirc, cuadrada, circular,anillos.
Usar cada una como fuente, variando  " b = s.<lente>(<params>) , en el lugar de los programas donde proceda.

22/08: Resta calcular todos los casos de las lentes que se piden usando "irs0.py". Creación de "python_210818.tar" con los códigos correctos hasta las lentes, pero sin las imágenes adecuadas, creación posterior.

23/08 : Calculados todos los casos de lentes "irs0.py". Basta mejora (final) a "irs0.py", que incluye ahora fuentes '.fits' y '.jpg' del directorio "HubbleDeepField/". Se elige por prompt lo que se desea y se guarda la imagen resultante como '.jpg' distintivo del caso elegido.

Animaciones creadas en la carpeta "/anims" siguiendo "animaciones.py". Fáciles de realizar con un poco de artesanía pythoniana. También hay animaciones en "/CASTLES" . Acabado todo lo referente a las "lentes". 



                                                                                             
                                                                                             
                                                                                             
                                                                                             
