#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 11:41:07 2025

@author: andr3s
"""

import subprocess
import os
import numpy as np  #  Importamos numpy para manejar floats

beta_values = np.arange(0.00, 0.35, 0.03)

# Carpeta base de resultados
path_resultados = "./Resultados_beta"
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)

for beta in beta_values:
    carpeta_resultados = f"{path_resultados}/beta_{beta}"  # Usamos formato `.1f` para nombres con decimales

 
    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    print(f"Ejecutando simulación para beta = {beta}...")

    os.environ["RESULTADOS_PATH"] = carpeta_resultados
    os.environ["PARAM_BETA"] = str(beta)  

    # Ejecutar `DIID.py` sin modificarlo
    resultado = subprocess.run(["python", "/home/andr3s/Documentos/SS/Códigos/DIIID 2.py"], capture_output=True, text=True)
    print(resultado.stdout)

print("Simulación completada para variaciones de beta.")
