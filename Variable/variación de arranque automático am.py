#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 07:32:44 2025

@author: andr3s
"""
import subprocess
import os

am_values = range(1, 11, 1)  # am desde 1 hasta 10 en pasos de 1

path_resultados = "./Resultados_am"
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)

for am in am_values:
    carpeta_resultados = f"{path_resultados}/am_{am}"  

    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    print(f"Ejecutando simulación para am = {am}...")

    os.environ["RESULTADOS_PATH"] = carpeta_resultados
    os.environ["PARAM_AM"] = str(am)

    resultado = subprocess.run(["python", "/home/andr3s/Documentos/SS/main.py"], capture_output=True, text=True)
    print(resultado.stdout)

print("Simulación completada para variaciones de am.")
