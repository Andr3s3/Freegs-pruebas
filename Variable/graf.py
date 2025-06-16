#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:40:21 2025

@author: andr3s
"""
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt 
import pandas as pd 
import os
######################################## 

# Save and change the name of the enviroment 

def guardar_perfiles(eq, profiles, RX, RZ, CIX, CIZ, CIX1, CIZ1, CIX2, CIZ2, CIX3, CIZ3, path_tablas, nombre1):
    """Genera y guarda los parámetros del plasma en un archivo CSV."""
    
    perfil_data = [
        ["PERFIL DE ARRANQUE", "", ""],
        ["Corriente", eq.plasmaCurrent(), "Amps"],
        ["Radio Mayor", eq.geometricAxis()[0], "m"],
        ["Campo Toroidal", eq.magneticAxis()[1], "T"],
        [r'Vacuum $F = RB_t$', eq.geometricAxis()[0] * eq.magneticAxis()[1], ""],
        ["FORMA DEL PLASMA", "", ""],
        ["Poloidal Beta", eq.poloidalBeta(), ""],
        ["Toroidal Beta", eq.toroidalBeta(), ""],
        ["Total Beta", eq.totalBeta(), ""],
        ["Normalized Beta", eq.betaN(), ""],
        ["Elongation", eq.elongation(), ""],
        ["Triangularity", eq.triangularity(), ""],
        ["Intersect Walls", eq.intersectsWall(), ""],
        ["Plasma Aspect Ratio", eq.aspectRatio(), ""],
        ["Inverse Plasma Aspect Ratio", eq.inverseAspectRatio(), ""],
        ["Minor Radius", eq.minorRadius(), "m"],
        ["Plasma Volume", eq.plasmaVolume(), "m^2"],
        ["PARÁMETROS DEL PLASMA", "", ""],
        ["Plasma Current", eq.plasmaCurrent(), "Amps"],
        ["Plasma Pressure on Axis", eq.pressure(0.0), "Pascals"],
        ["Plasma Average Pressure", eq.pressure_ave(), "Pascals"],
        ["Plasma Thermal Energy", eq.w_th(), "Joules"],
        ["am", profiles.alpha_m, ""],
        ["an", profiles.alpha_n, ""],
        ["L", profiles.L, ""],
        ["Beta0", profiles.Beta0, ""],
        ["Geometric Axis", eq.geometricAxis(), "(R, Z)"],
        ["Magnetic Axis", eq.magneticAxis(), "(R, Z, psi)"],
        ["Separatrix Boundary (Z=0.0)", eq.innerOuterSeparatrix(), "(R, Z)"],
        ["Shafranov Shift", eq.shafranovShift(), "(R, Z)"],
        ["FORMA DEL PLASMA", "", ""],
        ["(RX,RZ)", RX, RZ],
        ["(CIX,CIZ)", CIX, CIZ],
        ["(CIX1,CIZ1)", CIX1, CIZ1],
        ["(CIX2,CIZ2)", CIX2, CIZ2],
        ["(CIX3,CIZ3)", CIX3, CIZ3]
    ]

    # Asegurar que la carpeta de tablas existe
    os.makedirs(path_tablas, exist_ok=True)

    # Guardar el perfil en CSV
    df = pd.DataFrame(perfil_data, columns=["Descripción", "Valor", "Unidad"])
    df.to_csv(os.path.join(path_tablas, f"Perfil_{nombre1}.csv"), index=False)
    
    print(f"Perfil guardado en {path_tablas}/Perfil_{nombre1}.csv")

######################################################## 
# Toroidal Current And Pressure 
def calcular_densidad_corriente(eq, profiles):
    """Calcula la densidad de corriente y presión del plasma."""
    jtor = profiles.Jtor(eq.R, eq.Z, eq.psi(), eq.psi_bndry)
    pres = profiles.pressure(eq.psiN())
    Ax = eq.magneticAxis()[0]  # Posición en R del eje magnético
    return jtor, pres, Ax

def graficar_densidad_corriente(eq, jtor, Ax, path_imagenes, nombre):
    """Genera y guarda la gráfica de la densidad de corriente."""
    plt.figure('Current Density', figsize=(6, 5), dpi=120)
    plt.plot(eq.R, jtor)
    plt.axvline(Ax, linestyle=':')
    plt.title(r'Current Density')
    plt.xlabel(r'$R$')
    plt.ylabel(r'$J$')
    plt.grid()
    plt.savefig(os.path.join(path_imagenes, f'Ch6_J_{nombre}.png'))
    plt.close()

def graficar_factor_seguridad(eq, path_imagenes, nombre):
    """Genera y guarda la gráfica del factor de seguridad."""
    plt.figure('Safety Factor', figsize=(6, 5), dpi=120)
    plt.plot(*eq.q())
    plt.title('Safety Factor')
    plt.xlabel(r"Normalised $\psi$")
    plt.ylabel("Safety factor")
    plt.grid()
    plt.savefig(os.path.join(path_imagenes, f'Ch6_q_{nombre}.png'))
    plt.close()



# %% 
##################################################### 
# Final plot of equilibrium 

def graficar_equilibrio(eq, constrain, path_imagenes, nombre):
    """Genera y guarda la gráfica del equilibrio del plasma."""
    axis = eq.plot(show=False)
    eq.tokamak.plot(axis=axis, show=False)
    constrain.plot(axis=axis, show=True)
    plt.savefig(os.path.join(path_imagenes, f'Ch6_eq_{nombre}.png'))
    plt.close()

def guardar_corriente_bobinas(eq, path_tablas, nombre1):
    """Guarda la corriente de las bobinas en un CSV."""
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
    #Coils_Current = [[f"FC{i+1}", eq.tokamak[f"FC{i+1}"].current / 1e+6, 'MA'] for i in range(18)]
    
    df = pd.DataFrame(Coils_Current, columns=["Coil", "Current", "MA"])
    os.makedirs(path_tablas, exist_ok=True)
    df.to_csv(os.path.join(path_tablas, f'Coil_Currents_{nombre1}.csv'), index=False)
    print(f"Corrientes guardadas en {path_tablas}/Coil_Currents_{nombre1}.csv")

def graficar_energia_termica(eq, path_imagenes, nombre):
    """Genera la gráfica de la energía térmica del plasma si el valor es válido."""
    try:
        print("Ejecutando eq.w_th()...")
        W = eq.w_th()
        print(f"Energía térmica devuelta por eq.w_th(): {W}")

        if isinstance(W, (int, float)):
            plt.figure(figsize=(6, 5), dpi=120)
            plt.plot([0, 1], [0, W], label=f"Energía Térmica: {W:.2f} J")
            plt.title("Energía Térmica del Plasma")
            plt.xlabel("vs algo a escoger, ej presión")
            plt.ylabel("Energía Térmica (Joules)")
            plt.grid()
            plt.legend()
            plt.savefig(os.path.join(path_imagenes, f'Ch6_Thermal_Energy_{nombre}.png'))
            plt.close()
        else:
            print("eq.w_th() no devolvió un número válido para graficar.")
    except Exception as e:
        print(f"Error al ejecutar eq.w_th(): {e}")

def graficar_presion_corriente(eq, pres, jtor, Ax, path_imagenes, nombre):
    """Genera y guarda la gráfica de presión y densidad de corriente."""
    plt.figure('Pressure and Current Density', figsize=(13, 6), dpi=120)
    
    plt.subplot(1, 2, 1)
    plt.plot(eq.R, pres[:, 64])
    plt.axvline(Ax, linestyle=':')
    plt.title('Pressure')
    plt.xlabel(r'$R$')
    plt.ylabel(r'$P$ [Pa]')
    plt.grid()
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(eq.R, jtor[:, 64])
    plt.axvline(Ax, linestyle=':')
    plt.title('Current Density')
    plt.xlabel(r'$R$')
    plt.ylabel(r'$J$ [A]')
    plt.grid()
    plt.legend()
    
    plt.savefig(os.path.join(path_imagenes, f'Ch6_P_J_{nombre}.png'))
    plt.close()


# %% 
####################################################### 
# Tokamak Magnetic Field, Toroidal and Poloidal Magnetic Field 
def graficar_campo_magnetico(eq, Ax, path_imagenes, nombre):
    """Genera y guarda las gráficas del campo magnético del tokamak."""
    
    S1 = eq.innerOuterSeparatrix()[0]
    S2 = eq.innerOuterSeparatrix()[1]
    Tokamak = eq.getMachine()
    
    plt.figure('B_Tokamak_Plasma', figsize=(12, 8), dpi=120)
    
    # Campo magnético radial (B_r)
    plt.subplot(2, 2, 1)
    plt.plot(eq.R, Tokamak.Br(eq.R, 0))
    plt.axvline(Ax, ls=':')
    plt.axvline(S1, ls='-.', c='red')
    plt.axvline(S2, ls='-.', c='red')
    plt.title(r'Campo Magnético $B_r$ Tokamak')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{r} [Teslas]$')
    plt.grid()

    # Campo magnético axial (B_z)
    plt.subplot(2, 2, 3)
    plt.plot(eq.R, Tokamak.Bz(eq.R, 0))
    plt.axvline(Ax, ls=':')
    plt.axvline(S1, ls='-.', c='red')
    plt.axvline(S2, ls='-.', c='red')
    plt.title(r'Campo Magnético $B_z$ Tokamak')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{z} [Teslas]$')
    plt.grid()

    # Campo magnético total (B_T)
    plt.subplot(2, 2, 2)
    plt.plot(eq.R, eq.Btot(eq.R, 0))
    plt.axvline(Ax, linestyle=':')
    plt.title('Campo Magnético Total')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{T} [Teslas]$')
    plt.grid()

    plt.tight_layout()
    plt.savefig(os.path.join(path_imagenes, f'Ch6_B2_{nombre}.png'))
    plt.close()
    
    print(f"Gráficas del campo magnético guardadas en {path_imagenes}")
# %% 
###################################################### 
# Tokamak Magnetic Field and Total Magnetic Field 
def graficar_campo_magnetico_total(eq, Ax, path_imagenes, nombre):
    """Genera y guarda las gráficas de los campos magnéticos poloidal, toroidal y del plasma."""
    
    plt.figure('B_p, B_t y B_T', figsize=(12, 8), dpi=120)

    # Campo magnético poloidal
    plt.subplot(2, 2, 2)
    plt.plot(eq.R, eq.Bpol(eq.R, 0))
    plt.axvline(Ax, linestyle=':')
    plt.title('Campo Magnético Poloidal')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{\theta} [Teslas]$')
    plt.grid()

    # Campo magnético toroidal
    plt.subplot(2, 2, 4)
    plt.plot(eq.R, eq.Btor(eq.R, 0))
    plt.axvline(Ax, linestyle=':')
    plt.title('Campo Magnético Toroidal')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{\phi} [Teslas]$')
    plt.grid()

    # Campo magnético radial del plasma
    plt.subplot(2, 2, 1)
    plt.plot(eq.R, eq.plasmaBr(eq.R, 0))
    plt.axvline(Ax, linestyle=':')
    plt.title(r'Campo Magnético $B_r$ Plasma')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{r} [Teslas]$')
    plt.grid()

    # Campo magnético axial del plasma
    plt.subplot(2, 2, 3)
    plt.plot(eq.R, eq.plasmaBz(eq.R, 0))
    plt.axvline(Ax, linestyle=':')
    plt.title(r'Campo Magnético $B_z$ Plasma')
    plt.xlabel('Radio Menor (R)')
    plt.ylabel(r'$B_{z} [Teslas]$')
    plt.grid()

    plt.tight_layout()
    plt.savefig(os.path.join(path_imagenes, f'Ch6_B1_{nombre}.png'))
    plt.close()

    print(f"Gráficas del campo magnético total guardadas en {path_imagenes}")

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
def graficar_equilibrio_final(eq, constrain, path_imagenes, nombre):
    """Genera y guarda la gráfica final del equilibrio del plasma."""
    
    fig, axis = plt.subplots()
    axis = eq.plot(axis=axis, show=False)
    eq.tokamak.plot(axis=axis, show=False)
    constrain.plot(axis=axis, show=True)

    # Posiciona la leyenda fuera de los ejes para mejor visualización
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0.)

    plt.draw()
    plt.pause(0.1)  # Breve pausa para asegurar el renderizado
    
    # Guardar la imagen con ajuste de los bordes
    plt.savefig(os.path.join(path_imagenes, f'Ch6_eq_{nombre}.png'), bbox_inches='tight')
    plt.close()

    print(f"Gráfica final de equilibrio guardada en {path_imagenes}")

# %% 
##################################################### 
# Separatrix 

def graficar_separatrix(eq, path_imagenes, nombre):
    """Genera y guarda la gráfica de la separatrix del plasma."""
    
    RZ = eq.separatrix()
    R, Z = RZ[:, 0], RZ[:, 1]

    Rmin = 0.1
    Rmax = 3.0

    plt.figure('Separatrix', figsize=(6, 5), dpi=120)
    plt.title('Plasma Separatrix')
    plt.plot(R, Z, label='Triangularidad: %.3f' % eq.triangularity())
    plt.xlim(Rmin, Rmax)
    plt.legend(loc="upper right")
    plt.grid()
    plt.savefig(os.path.join(path_imagenes, f'Ch6_Separatrix_{nombre}.png'))
    plt.close()

    print(f"Gráfica de la separatrix guardada en {path_imagenes}")



# %%
# Coils Current for MASTU only

# assign data
def guardar_corriente_bobinas2(eq, path_tablas, nombre1):
    """Genera y guarda un CSV con la corriente de las bobinas del tokamak."""
    
    # Crear la lista de datos de las bobinas
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

    #Coils_Current = [[f"FC{i+1}", eq.tokamak[f"FC{i+1}"].current / 1e+6, 'MA'] for i in range(18)]
    
    # Convertir a DataFrame
    df = pd.DataFrame(Current, columns=["Coil", "Current", "MA"])
    
    # Asegurar que la carpeta de tablas existe
    os.makedirs(path_tablas, exist_ok=True)
    
    # Guardar el archivo CSV
    df.to_csv(os.path.join(path_tablas, f'Coil_Currents_{nombre1}.csv'), index=False)
    
    print(f"Corrientes de bobinas guardadas en {path_tablas}/Coil_Currents_{nombre1}.csv")
