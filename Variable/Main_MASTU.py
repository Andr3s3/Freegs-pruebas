# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 18:54:40 2025

@author: Uriel, Andr3s, Luis
"""
import matplotlib
matplotlib.use("Agg")
import freegs
import os
import pandas as pd
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
path_resultados = os.environ.get("RESULTADOS_PATH", "./Resultados_MASTU/Default")
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)  # Asegurar que la carpeta existe

# Usar `path_resultados` en lugar de rutas fijas
path_tablas = path_resultados  
path_imagenes = path_resultados  

######################################### 
# Crea una máquina específica (MAST-U)
# Define el dominio para solucionar el equilibrio 
tokamak = freegs.machine.MASTU() 
eq = freegs.Equilibrium(tokamak=tokamak,
                            Rmin=0.1, Rmax=2.3,    # Dominio radial
                            Zmin=-2.5, Zmax=2.5,   # Altura
                            nx=129, ny=129,        # Número de puntos en la malla
                            boundary=freegs.boundary.freeBoundaryHagenow)  # Condiciones de frontera libre

#########################################

# Perfil de arranque 
P = float(os.environ.get("PRESIÓN_P", 1.5e5))  
R = 0.9
beta = float(os.environ.get("PARAM_BETA",0.33))  # beta poloidal
I = float(os.environ.get("INTENSIDAD_I", 0.9e6)) #`I` puede variar desde `variacion de arranque...`
Bt = float(os.environ.get("CAMPO_BT", 0.85))     #Bt puede ser usado de forma dinámica
an = int(os.environ.get("PARAM_AN", 1))          #an es dinámico, modifica el perfil de densidad de corriente
am = int(os.environ.get("PARAM_AM", 2))          #am es dinámico, modifica el perfil de densidad de corriente
F = R*Bt # uviera

profiles = freegs.jtor.ConstrainPaxisIp(eq,
                                            P, # Presión del plasma en el eje magnético [Pascals]
                                            I, # Corriente del plasma [Amps]
                                            F, # Vacio f=R*Bt
                                            am,
                                            an
                                            )  
########################################

######################################## '''
# Crea carpetas con el nombre del entorno
# Modificar N, permite tener orden y control sobre los datos obtenidos
N = "Triang_Pos_1_Low_Pressure"  

nombre = "MASTU_"+N+".png" 
nombre1 = "MASTU_"+N+".csv" 
nombre2 = "MASTU_"+N 

# Constricciones del plasma

RX = 0.62
RZ = 1.02
xpoints = [(RX, -RZ),   # (R,Z) Ubicación de los puntos x, donde el campo magnético total es cero
               (RX, RZ)]


CIX = 1.25; CIZ = 0.0
CIX1 = 0.83; CIZ1 = 0.84
CIX2 = 1.11; CIZ2 = 0.5
CIX3 = RX ; CIZ3 = 0.0 

#Condiciones de isoflujo que definen la separatríz
#isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX,-CIZ), (RX,RZ,CIX,CIZ)]
#isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX,CIZ), (CIX1,CIZ1,CIX,CIZ)]
isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]
#se pueden escoger los puntos dependiendo de la forma y triangularidad que se desee en la separatriz

constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux)
constrain(eq)


freegs.solve(eq,              #Solucionador de equilibrio
                 profiles,    #Función que genera los perfiles
                 constrain,
                 show=True) 

#Corrientes en las bobinas específicamente de MAST-U
Coils_Current = [
    ["Solenoid", eq.tokamak["Solenoid"].current/1e+6,''],
    ["Pc", eq.tokamak["Pc"].current/1e+6,'MA'],
    ["Px", eq.tokamak["Px"].current/1e+6,'MA'],
    ["D1", eq.tokamak["D1"].current/1e+6,'MA'],
    ["D2", eq.tokamak["D2"].current/1e+6,'MA'],
    ["D3", eq.tokamak["D3"].current/1e+6,'MA'],
    ["Dp", eq.tokamak["Dp"].current/1e+6,'MA'],
    ["D5", eq.tokamak["D5"].current/1e+6,'MA'],
    ["D6", eq.tokamak["D6"].current/1e+6,'MA'],
    ["D7", eq.tokamak["D7"].current/1e+6,'MA'],
    ["P4", eq.tokamak["P4"].current/1e+6,'MA'],
    ["P5", eq.tokamak["P5"].current/1e+6,'MA'],
    ["P6", eq.tokamak["P6"].current/1e+6,'MA']
]
 
headC = ['Coil','Current','MA']

#Tabulador de corrientes
Coil = pd.DataFrame(Coils_Current)
Coil.to_csv(path_tablas+'/Coil_Currents_'+nombre1, index=False)

#Perfiles del plasma en CSV
guardar_perfiles(eq, profiles, RX, RZ, CIX, CIZ, CIX1, CIZ1, CIX2, CIZ2, CIX3, CIZ3, path_tablas, nombre1, P, I, R, Bt, F)

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
