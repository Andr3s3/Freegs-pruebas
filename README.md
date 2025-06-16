# Freegs-pruebas

#### En este documento se comparten los scripts creados para ejecutar el código [FreeGS](https://github.com/freegs-plasma/freegs). Se recomienda visitar el enlace pues se detalla la operación del código y las consideraciones tomadas. El código presente se encuentra escrito en python y se tiene 


#### Existen tres configuraciones de parámetros iniciales sobre el eje magnético del plasma en FreeGS:
+ Presión $P$, Corriente del Plasma $I_{p}$, Campo Magnético Toroidal $B_{t}$.
+ Beta Poloidal $\beta_{p}$, Corriente del Plasma $I_{p}$, Campo Magnético Toroidal $B_{t}$.
+ Expresiones polinomiales para P y F. (no considerada en este trabajo).

#### Se ha modificado el código de tal manera que sea posible realizar múltiples iteraciones sobre una lista de valores para algún parámetro de inicio dada una forma del plasma. Esto se muestra en la carpeta ```Variable```.

#### Para simulaciones individuales se ha dividido el script en 2 partes ```main.py``` y ```graph.py```, dónde el primero es el archivo de control y el segundo contiene las rutinas de graficación.
