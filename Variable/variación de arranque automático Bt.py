#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 07:32:05 2025

@author: andr3s
"""
import subprocess
import os
import numpy as np

# Bt desde 0.1 T hasta 2.0 T con pasos de 0.1 T
Bt_values = np.arange(0.1, 2.1, 0.1)  

path_resultados = "./Resultados_Bt"
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)

for Bt in Bt_values:
    carpeta_resultados = f"{path_resultados}/Bt_{Bt:.1f}"  

    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    print(f"Ejecutando simulación para Bt = {Bt:.1f} T...")

    os.environ["RESULTADOS_PATH"] = carpeta_resultados
    os.environ["CAMPO_BT"] = str(Bt)

#Escribir el path donde se encuentra el main correspondiente
    resultado = subprocess.run(["python", "ESCRIBIR DIRECTORIO/Main DIIID.py"], capture_output=True, text=True)
    print(resultado.stdout)

print("Simulación completada para variaciones de Bt.")
