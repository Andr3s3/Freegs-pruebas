#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 08:04:20 2025
 resultado = subprocess.run(["python", "/home/andr3s/Documentos/SS/DIIID 2.py"], capture_output=True, text=True)
@author: andr3s
"""
import subprocess
import os
import numpy as np  #  Importamos numpy para manejar floats

#  Definir el rango de valores de I con `numpy.arange()`
I_values = np.arange(100000, 1000001, 50000)  # Desde 10,000 hasta 1,000,000 con paso de 50,000

# Carpeta base de resultados
path_resultados = "./Resultados_Completos_variando I"
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)

# Iterar sobre los valores de I y crear las subcarpetas antes de llamar `DIID.py`
for I in I_values:
    carpeta_resultados = f"{path_resultados}/I_{I:.1f}"  # Usamos formato `.1f` para nombres con decimales

    # Crear la subcarpeta antes de ejecutar `DIID.py`
    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    print(f"Ejecutando simulación para I = {I:.1f} A...")

    # Asignar `RESULTADOS_PATH` para que `DIID.py` guarde en la carpeta correcta
    os.environ["RESULTADOS_PATH"] = carpeta_resultados
    os.environ["INTENSIDAD_I"] = str(I)  # 🔹 Pasar `I` para que `DIID.py` use el valor correcto

    # Imprimir la ruta para verificar antes de ejecutar `DIID.py`
    print(f"RUTA ASIGNADA A RESULTADOS_PATH: {os.environ['RESULTADOS_PATH']}")
    print(f"INTENSIDAD ASIGNADA A I: {os.environ['INTENSIDAD_I']}")

    # Ejecutar `DIID.py` sin modificarlo
    resultado = subprocess.run(["python", "/home/andr3s/Documentos/SS/DIIID 2.py"], capture_output=True, text=True)
    print(resultado.stdout)

print("Simulación completada. Todos los resultados han sido organizados correctamente.")





