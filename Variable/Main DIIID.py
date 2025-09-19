#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:36:21 2025

@author: Uriel, Andr3s, Luis
"""
import matplotlib
matplotlib.use("Agg")  
import pandas as pd
import freegs 
import os 
from graf import (
    guardar_perfiles, 
    calcular_densidad_corriente, 
    graficar_densidad_corriente, 
    graficar_factor_seguridad, 
    graficar_equilibrio_final, 
    graficar_energia_termica, 
    graficar_presion_corriente, 
    graficar_campo_magnetico, 
    graficar_campo_magnetico_total, 
    graficar_separatrix,
    graficar_mapa_corriente,
    graficar_mapa_presion
)

# Obtener la carpeta de resultados desde `rango_I.py`
path_resultados = os.environ.get("RESULTADOS_PATH", "./Resultados_DIIID/Default")
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)  # Asegurar que la carpeta existe

# Usar `path_resultados` en lugar de rutas fijas
path_tablas = path_resultados  
path_imagenes = path_resultados  


######################################### 
# Crea una máquina específica (DIII-D)
# Define el dominio para solucionar el equilibrio 
tokamak = freegs.machine.DIIID() 
eq = freegs.Equilibrium(tokamak=tokamak, 
                        Rmin=0.1, Rmax=3.0,  # Dominio radial 
                        Zmin=-1.8, Zmax=1.8, # Altura 
                        nx=129, ny=129,      # Número de puntos en la malla
                        boundary=freegs.boundary.freeBoundaryHagenow) # Condiciones de frontera 

######################################### 
# Perfil de arranque  
P = float(os.environ.get("PRESIÓN_P",1e6)) 
R = 0.9
beta = float(os.environ.get("PARAM_BETA",0.33))     #Beta poloidal 
I = float(os.environ.get("INTENSIDAD_I", 1533632))  # `I` puede variar desde `variacion de arranque...`
Bt = float(os.environ.get("CAMPO_BT", 1.93))        #Bt puede ser usado de forma dinámica
an = int(os.environ.get("PARAM_AN", 1))   # an es dinámico, modifica el perfil de densidad de corriente
am = int(os.environ.get("PARAM_AM", 2))   # am es dinámico, modifica el perfil de densidad de corriente
F = R*Bt 
profiles = freegs.jtor.ConstrainBetapIp(eq, 
                                        beta, # Presión del plasma en el eje magnético [Pascals] 
                                        I,    # Corriente del plasma [Amps] 
                                        F,    # Vacio f=R*Bt
                                        am, 
                                        an
                                        ) 

######################################## 
# Crea carpetas con el nombre del entorno
# Modificar N, permite tener orden y control sobre los datos obtenidos
N = "Triang_Pos_1_Low_Pressure" 
# N = "Snowflake_1_1" 

nombre = "DIIID_"+N+".png" 
nombre1 = "DIIID_"+N+".csv" 
nombre2 = "DIIID_"+N 

# Constricciones del plasma 
RX = 1.30 
RZ = 1.0 
xpoints = [(RX, -RZ), # Ubicación de los puntos x, donde el campo magnético total es cero
           (RX, RZ)] 
CIX = 2.00 
CIZ = 0.0 
CIX1 = 1.76 
CIZ1 = 0.66 
CIX2 = 1.91 
CIZ2 = 0.376 
CIX3 = RX 
CIZ3 = 0.0 

#Condiciones de isoflujo que definen la separatríz
# isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX,-CIZ), (RX,RZ,CIX,CIZ)]
isoflux = [(RX, -RZ, RX, RZ), (RX, -RZ, CIX1, -CIZ1), (RX, RZ, CIX1,
                                                       CIZ1), (CIX1, -CIZ1, CIX, CIZ), (CIX1, CIZ1, CIX, CIZ)]
# isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]
# isoflux = [(RX,RZ, CIX3,CIZ3),(CIX3, CIZ3, RX,-RZ) ,(RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]
#se pueden escoger los puntos dependiendo de la forma y triangularidad que se desee en la separatriz
constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux) 
constrain(eq) 
 
freegs.solve(eq,         #Solucionador de equilibrio 
             profiles,   #Función que genera los perfiles 
             constrain, 
             show=True) 

#Corrientes en las bobinas específicamente de DIII-D
Coils_Current = [ 
    ["FC1", eq.tokamak["FC1"].current/1e+6, 'MA'], 
    ["FC2", eq.tokamak["FC2"].current/1e+6, 'MA'], 
    ["FC3", eq.tokamak["FC3"].current/1e+6, 'MA'], 
    ["FC4", eq.tokamak["FC4"].current/1e+6, 'MA'], 
    ["FC5", eq.tokamak["FC5"].current/1e+6, 'MA'], 
    ["FC6", eq.tokamak["FC6"].current/1e+6, 'MA'], 
    ["FC7", eq.tokamak["FC7"].current/1e+6, 'MA'], 
    ["FC8", eq.tokamak["FC8"].current/1e+6, 'MA'], 
    ["FC9", eq.tokamak["FC9"].current/1e+6, 'MA'], 
    ["FC10", eq.tokamak["FC10"].current/1e+6, 'MA'], 
    ["FC11", eq.tokamak["FC11"].current/1e+6, 'MA'], 
    ["FC12", eq.tokamak["FC12"].current/1e+6, 'MA'], 
    ["FC13", eq.tokamak["FC13"].current/1e+6, 'MA'], 
    ["FC14", eq.tokamak["FC14"].current/1e+6, 'MA'], 
    ["FC15", eq.tokamak["FC15"].current/1e+6, 'MA'], 
    ["FC16", eq.tokamak["FC16"].current/1e+6, 'MA'], 
    ["FC17", eq.tokamak["FC17"].current/1e+6, 'MA'], 
    ["FC18", eq.tokamak["FC18"].current/1e+6, 'MA'] 

] 
headC = ['Coil', 'Current', 'MA'] 

#Tabulador de corrientes 
Coil = pd.DataFrame(Coils_Current) 
Coil.to_csv(path_tablas+'/Coil_Currents_'+nombre1, index=False) 

#Perfiles del plasma en CSV
guardar_perfiles(eq, profiles, RX, RZ, CIX, CIZ, CIX1, CIZ1, CIX2, CIZ2, CIX3, CIZ3, path_tablas, nombre1, P,  I, R, Bt, F)

#Datos físicos del plasma con rutinas de graf.py
jtor, pres, Ax = calcular_densidad_corriente(eq, profiles)

graficar_densidad_corriente(eq, jtor, Ax, path_imagenes, nombre)
graficar_factor_seguridad(eq, path_imagenes, nombre)
graficar_equilibrio_final(eq, constrain, path_imagenes, nombre)
graficar_energia_termica(eq, path_imagenes, nombre)
graficar_presion_corriente(eq, pres, jtor, Ax, path_imagenes, nombre)
graficar_campo_magnetico(eq, Ax, path_imagenes, nombre)
graficar_campo_magnetico_total(eq, Ax, path_imagenes, nombre)
graficar_separatrix(eq, path_imagenes, nombre)
graficar_mapa_corriente(eq, jtor, path_imagenes)
graficar_mapa_presion(eq, pres, path_imagenes)
