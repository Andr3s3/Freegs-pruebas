# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
import freegs 
from tabulate import tabulate 
import os 


# Obtener la carpeta de resultados desde `rango_I.py`
path_resultados = os.environ.get("RESULTADOS_PATH", "./Resultados_Completos/Default")
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)  # Asegurar que la carpeta existe

# Usar `path_resultados` en lugar de rutas fijas
path_tablas = path_resultados  
path_imagenes = path_resultados  


######################################### 
# Create the machine, which specifies coil locations 
# and equilibrium, specifying the domain to solve over 
tokamak = freegs.machine.DIIID() 
eq = freegs.Equilibrium(tokamak=tokamak, 
                        Rmin=0.1, Rmax=3.0, # Radial domain 
                        Zmin=-1.8, Zmax=1.8, # Height range 
                        nx=129, ny=129, # Number of grid points b
                        boundary=freegs.boundary.freeBoundaryHagenow) # Boundary condition 

######################################### 
# Plasma profiles 
# P = 1e6 
# I = 1e6 
# F = 2.0 
R = 2 
# P = 1.5e6 #
beta = 0.3 # kPa 
# I = -1533632 
# Límite 2.0 MA 
#I = 700000 #0.7e6 
I = float(os.environ.get("INTENSIDAD_I", 660000.0))  # Ahora `I` se toma de `variacion de arranque...`
Bt = float(os.environ.get("CAMPO_BT", 0.4))  #Ahora Bt es dinámico
#Bt = 0.4 # Límite 2.2 T 
an = int(os.environ.get("PARAM_AN", 2))  # Ahora an es dinámico
#an = 2
am = int(os.environ.get("PARAM_AM", 2))  # Ahora am es dinámico
#am = 2
F = R*Bt 
profiles = freegs.jtor.ConstrainBetapIp(eq, 
                                        beta, # Plasma pressure on axis [Pascals] 
                                        I, # Plasma current [Amps] 
                                        F, 
                                        am, 
                                        an
                                        ) # Vacuum f=R*Bt 

######################################## '''
# Create the folders with the enviroment name 
N = "Triang_Pos_1_Low_Pressure" 
# N = "Snowflake_1_1" 

nombre = "DIIID_"+N+".png" 
nombre1 = "DIIID_"+N+".csv" 
nombre2 = "DIIID_"+N 

'''
path_tablas = './Tablas_'+nombre2 
if not os.path.exists(path_tablas): 
    os.mkdir(path_tablas) 
    
path_imagenes = './Imagenes_'+nombre2 
if not os.path.exists(path_imagenes): 
    os.mkdir(path_imagenes) # Enviar un mensaje a Copilot 
'''

    
######################################## 
# Plasma Contrains 
RX = 1.30 
RZ = 1.0 
xpoints = [(RX, -RZ), # (R,Z) locations of X-points 
           (RX, RZ)] 
CIX = 2.00 
CIZ = 0.0 
CIX1 = 1.76 
CIZ1 = 0.66 
CIX2 = 1.91 
CIZ2 = 0.376 
CIX3 = RX 
CIZ3 = 0.0 

# isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX,-CIZ), (RX,RZ,CIX,CIZ)]
isoflux = [(RX, -RZ, RX, RZ), (RX, -RZ, CIX1, -CIZ1), (RX, RZ, CIX1,
                                                       CIZ1), (CIX1, -CIZ1, CIX, CIZ), (CIX1, CIZ1, CIX, CIZ)]
# isoflux = [(RX,-RZ, RX,RZ), (RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]
# isoflux = [(RX,RZ, CIX3,CIZ3),(CIX3, CIZ3, RX,-RZ) ,(RX,-RZ,CIX1,-CIZ1), (RX,RZ,CIX1,CIZ1), (CIX1,-CIZ1,CIX2,-CIZ2), (CIX1,CIZ1,CIX2,CIZ2), (CIX2,CIZ2,CIX,CIZ), (CIX2,-CIZ2,CIX,CIZ)]

constrain = freegs.control.constrain(xpoints=xpoints, isoflux=isoflux) 
constrain(eq) 

# %matplotlib qt 
# %matplotlib inline 
freegs.solve(eq, # The equilibrium to adjust 
             profiles, # The toroidal current profile function 
             constrain, 
             show=True) 
######################################## 

# Save and change the name of the enviroment 

Profile = [ 
    ["PERFIL DE ARRANQUE", '', ''], 
    #["Presión", P, 'Pa'], 
    ["Corriente", I, 'Amps'], 
    ["Radio Mayor", R, 'm'], 
    ["Campo Toroidal", Bt, 'T'], 
    [r'Vacuum $F = RB_t$', F, ''], 
    ['FORMA DEL PLASMA', '', ''], 
    ["Poloidal Beta", (eq.poloidalBeta()), ''], 
    ["Toroidal Beta", (eq.toroidalBeta()), ''], 
    ["Total Beta", (eq.totalBeta()), ''], 
    ["Normalized Beta", (eq.betaN()), ''], 
    ["Elongation", (eq.elongation()), ''], 
    ["Triangularity", (eq.triangularity()), ''], 
    ["Intersect Walls", (eq.intersectsWall()), ''], 
    ["Plasma Aspect Ratio", (eq.aspectRatio()), ''], 
    ["Inverse Plasma Aspect Ratio", (eq.inverseAspectRatio()), ''], 
    ["Minour Radius", (eq.minorRadius()), 'm'], 
    ["Plasma Volume", (eq.plasmaVolume()), 'm^2'], 
    ['', '', ''], 
    ['PARÁMETROS DEL PLASMA', '', ''], 
    ["Plasma Current", (eq.plasmaCurrent()), 'Amps'], 
    ["Plasma Pressure on Axis", (eq.pressure(0.0)), 'Pascals'], 
    ["Plasma Average Pressure", (eq.pressure_ave()), 'Pascals'], 
    ["Plasma Thermal Energy", (eq.w_th()), 'Joules'], 
    ["am", (am)],
    ["an", (an)],
    ["L", (profiles.L)],
    ["Beta0", (profiles.Beta0)],
    ['', '', ''], 
    ["Geometric Axis", [eq.geometricAxis()], '(R,Z)'], 
    ["Magnetic Axis", eq.magneticAxis(), '(R,Z,psi)'], 
    ["Separatrix Boundary (Z=0.0)", (eq.innerOuterSeparatrix()), '(R,Z)'], 
    ["Shafranov Shift", [(eq.shafranovShift())], '(R,Z)'], 
    ['', '', ''], 
    ['FORMA DEL PLASMA', '', ''], 
    ["(RX,RZ)", RX, RZ], 
    ["(CIX,CIZ)", CIX, CIZ], 
    ["(CIX1,CIZ1)", CIX1, CIZ1], 
    ["(CIX2,CIZ2)", CIX2, CIZ2], 
    ["(CIX3,CIZ3)", CIX3, CIZ3], 
    ['', '', ''] 
           
]
 
# create header 
headp = ['Perfil', '', ''] 

# display tablep 

# print(tabulate(Profile,headers=headp,tablefmt="grid")) 
Prof = pd.DataFrame(Profile) 
Prof.to_csv(path_tablas+'/Perfil_'+nombre1, index=False) 

######################################################## 
# Toroidal Current And Pressure 
jtor = profiles.Jtor(eq.R, eq.Z, eq.psi(), eq.psi_bndry) 
pres = profiles.pressure(eq.psiN()) 

Pressx = [] 
Pressy = [] 

# for psi in np.linspace(0.01,0.95,40): 
# Pressx.append([psi]); Pressy.append(eq.pressure(psi)) 
Ax = eq.magneticAxis()[0] # Posición en R del eje magnético 

''' 
plt.figure('Current Density',figsize=(6, 5), dpi=120) 
plt.plot(eq.R,jtor) 
plt.axvline(Ax,linestyle=':') 
plt.title(r'Current Density'); plt.xlabel(r'$R$') 
plt.ylabel(r'$J$'); plt.grid(); plt.legend() 
plt 
'''
#Safety Factor 
print("\nSafety factor:\n\tpsi \t q") 
for psi in [0.01, 0.5, 0.9, 0.95]: 
    print("\t{:.2f}\t{:.2f}".format(psi, eq.q(psi))) 

# Safety factor 
plt.figure('Safety Factor',figsize=(6, 5), dpi=120) 
plt.plot(*eq.q()) 
plt.title('Safety Factor') 
plt.xlabel(r"Normalised $\psi$") 
plt.ylabel("Safety factor") 
plt.grid() 
plt.savefig(path_imagenes+'/Ch6_q_'+nombre) 
plt.show() 




# %% ##################################################### 
# Final plot of equilibrium 
axis = eq.plot(show=False) 
eq.tokamak.plot(axis=axis, show=False) 
constrain.plot(axis=axis, show=True) 
plt.savefig(path_imagenes+'/Ch6_eq_'+nombre) 

# %% 
# Coils Current for MASTU only 

# assign data 
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

# create header 
headC = ['Coil', 'Current', 'MA'] 

# display table 
# print(tabulate(Coils_Current,headers=headC,tablefmt="grid")) 
Coil = pd.DataFrame(Coils_Current) 
Coil.to_csv(path_tablas+'/Coil_Currents_'+nombre1, index=False) 


# %% 
print('[L, Beta0] = ',profiles.L,',', profiles.Beta0) 
print('[am, an] = ',profiles.alpha_m,',', profiles.alpha_n) 
# Obtención de la energía térmica del plasma 
try: 
    print("Ejecutando eq.w_th()...") 
    W = eq.w_th() # Obtener el valor numérico de la energía térmica 
    print(f"Energía térmica devuelta por eq.w_th(): {W}") 
    
# Verificar que W sea un número válido antes de graficar 
    if isinstance(W, (int, float)): 
        import matplotlib.pyplot as plt 
        plt.figure(figsize=(6, 5), dpi=120) 
        plt.plot([0, 1], [0, W], label=f"Energía Térmica: {W:.2f} J") # Crear un gráfico básico 
        plt.title("Energía Térmica del Plasma") 
        plt.xlabel("vs algo a escoger, ej presión") 
        plt.ylabel("Energía Térmica (Joules)") 
        plt.grid() 
        plt.legend() 
        plt.savefig(path_imagenes + '/Ch6_Thermal_Energy_' + nombre) # Guardar el gráfico 
        plt.show() 
    else: 
        print("eq.w_th() no devolvió un número válido para graficar.") 
except Exception as e: 
    print(f"Error al ejecutar eq.w_th(): {e}") 
        
# print((eq.w_th())).savefig(path_imagenes+'/Ch6_J'+nombre) 
# ''' 
# %% 
plt.figure('Pressure and Current Density', figsize=(13, 6), dpi=120) 
plt.subplot(1, 2, 1) 
plt.plot(eq.R, pres[:, 64]) 
plt.axvline(Ax, linestyle=':') 
plt.title(r'Pressure') 
plt.xlabel(r'$R$')
plt.ylabel(r'$P$ [Pa]') 
plt.grid() 
plt.legend() 
plt.subplot(1, 2, 2)
plt.plot(eq.R, jtor[:, 64]) 
plt.axvline(Ax, linestyle=':') 
plt.title(r'Current Density') 
plt.xlabel(r'$R$') 
plt.ylabel(r'$J$ [A]') 
plt.grid() 
plt.legend() 
plt.savefig(path_imagenes+'/Ch6_P_J_'+nombre) 

# %% 
####################################################### 
# Tokamak Magnetic Field, Toroidal and Poloidal Magnetic Field 


S1 = eq.innerOuterSeparatrix()[0] 
S2 = eq.innerOuterSeparatrix()[1] 

Tokamak = eq.getMachine() 
plt.figure('B_Tokamak_Plasma', figsize=(12, 8), dpi=120) 
plt.subplot(2, 2, 1) 
plt.plot(eq.R, Tokamak.Br(eq.R, 0)) 
plt.axvline(Ax, ls=':') 
plt.axvline(S1, ls='-.', c='red') 
plt.axvline(S2, ls='-.', c='red') 
plt.title(r'Campo Magnetico $B_r$ Tokamak') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{r} [Teslas]$') 
plt.grid() 
plt.subplot(2, 2, 3) 
plt.plot(eq.R, Tokamak.Bz(eq.R, 0)) 
plt.axvline(Ax, ls=':') 
plt.axvline(S1, ls='-.', c='red') 
plt.axvline(S2, ls='-.', c='red') 
plt.title(r'Campo Magnetico $B_z$ Tokamak') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{z} [Teslas]$')
plt.grid() 
# plt.figure('B_plasma',figsize=(6,10), dpi=120); 
plt.subplot(2, 2, 2) 
plt.plot(eq.R, eq.Btot(eq.R, 0)) 
plt.axvline(Ax, linestyle=':') 
plt.title('Campo Magnetico Total') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{T} [Teslas]$') 
plt.grid() 
plt.tight_layout() 
plt.savefig(path_imagenes+'/Ch6_B2_'+nombre)

# %% 
###################################################### 
# Tokamak Magnetic Field and Total Magnetic Field 
plt.figure('B_p, B_t y B_T', figsize=(12, 8), dpi=120) 
plt.subplot(2, 2, 2) 
plt.plot(eq.R, eq.Bpol(eq.R, 0)) 
plt.axvline(Ax, linestyle=':') 
plt.title('Campo Magnetico Poloidal') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{\theta} [Teslas]$') 
plt.grid() 
plt.subplot(2, 2, 4) 
plt.plot(eq.R, eq.Btor(eq.R, 0)) 
plt.axvline(Ax, linestyle=':') 
plt.title('Campo Magnetico Toroidal') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{\phi} [Teslas]$') 
plt.grid() 
plt.subplot(2, 2, 1) 
plt.plot(eq.R, eq.plasmaBr(eq.R, 0)) 
plt.axvline(Ax, linestyle=':') 
plt.title(r'Campo Magnetico $B_r$ Plasma') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{r} [Teslas]$') 
plt.grid() 
plt.subplot(2, 2, 3) 
plt.plot(eq.R, eq.plasmaBz(eq.R, 0)) 
plt.axvline(Ax, linestyle=':') 
plt.title(r'Campo Magnetico $B_z$ Plasma') 
plt.xlabel('Radio Menor (R)') 
plt.ylabel(r'$B_{z} [Teslas]$') 
plt.grid() 
plt.tight_layout() 
plt.savefig(path_imagenes+'/Ch6_B1_'+nombre) 
# %% 
# ''' 
###################################################### 

'''
# Safety Factor 
print("\nSafety factor:\n\tpsi \t q") 
for psi in [0.01, 0.5, 0.9, 0.95]: 
    print("\t{:.2f}\t{:.2f}".format(psi, eq.q(psi))) 
  

# Safety factor plt.figure('Safety Factor', figsize=(6, 5), dpi=120) 
plt.plot(*eq.q()) 
plt.title('Safety Factor') 
plt.xlabel(r"Normalised $\psi$") 
plt.ylabel("Safety factor") 
plt.grid() 
plt.savefig(path_imagenes+'/Ch6_q_'+nombre) 
plt.show() 
'''

# %% 
##################################################### 
# Final plot of equilibrium 
axis = eq.plot(show=False) 
eq.tokamak.plot(axis=axis, show=False) 
constrain.plot(axis=axis, show=True) 
plt.savefig(path_imagenes+'/Ch6_eq_'+nombre) 

# %% 
##################################################### 
# Separatrix 

RZ = eq.separatrix() 

R = RZ[:, 0] 
Z = RZ[:, 1] 


Rmin = 0.1 
Rmax = 3.0 

plt.figure('Separatrix', figsize=(6, 5), dpi=120) 
plt.title('Plasma Separatrix') 
plt.plot(R, Z, label='Triangularidad: %.3f' % eq.triangularity()) 
plt.xlim(Rmin, Rmax) 
plt.legend(loc="upper right") 
plt.grid() 
plt.savefig(path_imagenes+'/Ch6_Separatrix_'+nombre) 
plt.show() 


# %%
# Coils Current for MASTU only

# assign data
Current = [ 
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

# create header 
headC = ['Coil', 'Current', 'MA'] 

# display table 
# print(tabulate(Coils_Current,headers=headC,tablefmt="grid"))
Coil = pd.DataFrame(Coils_Current) 
Coil.to_csv(path_tablas+'/Coil_Currents_'+nombre1, index=False)