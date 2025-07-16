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

def guardar_perfiles(eq, profiles, RX, RZ, CIX, CIZ, CIX1, CIZ1, CIX2, CIZ2, CIX3, CIZ3, path_tablas, nombre1, P, I, R, Bt, F ):
    """Genera y guarda los parámetros del plasma en un archivo CSV."""
    
    perfil_data = [
        ["PERFIL DE ARRANQUE", "", ""],
        ["Corriente", I, "Amps"],
        ["Presión", P, "Pa"],
        ["Radio menor", R, "m"],
        ["Campo Toroidal", Bt, "T"],
        [r'Vacuum $F = RB_t$', F, ""],
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
    
    # Obtener datos (psi_n, q)
    psi_n, q = eq.q()
    
    """Genera y guarda la gráfica del factor de seguridad."""
    plt.figure('Safety Factor', figsize=(6, 5), dpi=120)
    plt.plot(psi_n,q)
    plt.title('Safety Factor')
    plt.xlabel(r"Normalised $\psi$")
    plt.ylabel("Safety factor")
    plt.grid()
    ruta_imagen = os.path.join(path_imagenes, f'q_{nombre}.png')
    plt.savefig(ruta_imagen)
    plt.close()

    df = pd.DataFrame({
        "psi_normalizado": psi_n,
        "q": q
    })
    ruta_csv = os.path.join(path_imagenes, f'q_{nombre}.csv')
    df.to_csv(ruta_csv, index=False)

    print(f"✅ Imagen guardada en: {ruta_imagen}")
    print(f"✅ CSV guardado en: {ruta_csv}")

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
            plt.xlabel("Tiempo")
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

#%% 
#Mapas de calor
def graficar_mapa_presion(eq, pres, path_imagenes, nombre="presion"):
    """Genera y guarda un mapa 2D de la presión del plasma."""
    R2D = eq.R
    Z2D = eq.Z

    plt.figure(figsize=(6, 5), dpi=120)
    cp = plt.contourf(R2D, Z2D, pres, levels=100, cmap="inferno")
    plt.colorbar(cp, label='Presión [Pa]')
    plt.contour(R2D, Z2D, eq.psi(), levels=[eq.psi_bndry], colors='cyan', linewidths=1.5, linestyles='--', label='Separatriz')
    plt.title("Mapa de Presión del Plasma")
    plt.xlabel("R [m]")
    plt.ylabel("Z [m]")
    plt.grid(True)
    plt.axis("equal")
    
    plt.savefig(os.path.join(path_imagenes, f"mapa_presion_{nombre}.png"))
    plt.close()
#%%
def graficar_mapa_corriente(eq, jtor, path_imagenes, nombre="corriente"):
    """Genera y guarda un mapa 2D de la densidad de corriente toroidal."""
    R2D = eq.R
    Z2D = eq.Z

    plt.figure(figsize=(6, 5), dpi=120)
    cp = plt.contourf(R2D, Z2D, jtor, levels=100, cmap="viridis")
    plt.colorbar(cp, label='Densidad de Corriente $J_\\phi$ [A/m²]')
    plt.contour(R2D, Z2D, eq.psi(), levels=[eq.psi_bndry], colors='white', linewidths=1.5, linestyles='--')
    plt.title("Mapa de Densidad de Corriente Toroidal")
    plt.xlabel("R [m]")
    plt.ylabel("Z [m]")
    plt.grid(True)
    plt.axis("equal")
    plt.savefig(os.path.join(path_imagenes, f"mapa_corriente_{nombre}.png"))
    plt.close()

