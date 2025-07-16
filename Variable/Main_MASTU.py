# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 18:54:40 2025

@author: LENOVO
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


# Save and change the name of the enviroment 

######################################### 
# Create the machine, which specifies coil locations 
# and equilibrium, specifying the domain to solve over 
tokamak = freegs.machine.MASTU() 
eq = freegs.Equilibrium(tokamak=tokamak,
                            Rmin=0.1, Rmax=2.3,    # Radial domain
                            Zmin=-2.5, Zmax=2.5,   # Height range
                            nx=129, ny=129,          # Number of grid points
                            boundary=freegs.boundary.freeBoundaryHagenow)  # Boundary condition

#########################################
# Plasma profiles
##########
# Plasma profiles 
P = float(os.environ.get("PRESIÓN_P", 1.5e5)) 
#I = 0.9e6 
R = 0.9
# P = 1.5e6 #
beta = 0.33 # poloidal #0.03 datos mostrados al Dr.
# I = -1533632 
# Límite 2.0 MA 
#I = 700000 #0.7e6 
I = float(os.environ.get("INTENSIDAD_I", 0.9e6))  # Ahora `I` se toma de `variacion de arranque...`
Bt = float(os.environ.get("CAMPO_BT", 0.85))  #Ahora Bt es dinámico
an = int(os.environ.get("PARAM_AN", 1))  # Ahora an es dinámico
am = int(os.environ.get("PARAM_AM", 2))  # Ahora am es dinámico
F = R*Bt # uviera

profiles = freegs.jtor.ConstrainPaxisIp(eq,
                                            P, # Plasma pressure on axis [Pascals]
                                            I, # Plasma current [Amps]
                                            F,
                                            am,
                                            an
                                            )  # Vacuum f=R*Bt
########################################

######################################## '''
# Create the folders with the enviroment name 
N = "Triang_Pos_1_Low_Pressure" 
# N = "Snowflake_1_1" 

nombre = "MASTU_"+N+".png" 
nombre1 = "MASTU_"+N+".csv" 
nombre2 = "MASTU_"+N 

'''
path_tablas = './Tablas_'+nombre2 
if not os.path.exists(path_tablas): 
    os.mkdir(path_tablas) 
    
path_imagenes = './Imagenes_'+nombre2 
if not os.path.exists(path_imagenes): 
    os.mkdir(path_imagenes)
'''

    

    # Plasma Contrains

RX = 0.62
RZ = 1.02
xpoints = [(RX, -RZ),   # (R,Z) locations of X-points
               (RX, RZ)]


CIX = 1.25; CIZ = 0.0
CIX1 = 0.83; CIZ1 = 0.84
CIX2 = 1.11; CIZ2 = 0.5
CIX3 = RX ; CIZ3 = 0.0 
#'''

#isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX,-CIZ), (RX,RZ,CIX,CIZ)]
#isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX,CIZ), (CIX1,CIZ1,CIX,CIZ)]
isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]
#isoflux = [(RX,RZ, CIX3,CIZ3),(CIX3, CIZ3, RX,-RZ) ,(RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]


constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux)
constrain(eq)

#%matplotlib qt
#%matplotlib inline
freegs.solve(eq,          # The equilibrium to adjust
                 profiles,    # The toroidal current profile function
                 constrain,
                 show=True) 

# Guardar perfiles del plasma en CSV
guardar_perfiles(eq, profiles, RX, RZ, CIX, CIZ, CIX1, CIZ1, CIX2, CIZ2, CIX3, CIZ3, path_tablas, nombre1, P, I, R, Bt, F)

# Obtener datos físicos del plasma
jtor, pres, Ax = calcular_densidad_corriente(eq, profiles)
#Coils Current for MASTU only

# assign data
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
 
# create header
headC = ['Coil','Current','MA']

# display table
#print(tabulate(Coils_Current,headers=headC,tablefmt="grid"))
Coil = pd.DataFrame(Coils_Current)
Coil.to_csv(path_tablas+'/Coil_Currents_'+nombre1, index=False)

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