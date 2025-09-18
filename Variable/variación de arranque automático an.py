#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 07:32:45 2025

@author: andr3s
"""
import subprocess
import os

an_values = range(1, 11, 1)  # an desde 1 hasta 10 en pasos de 1

path_resultados = "./Resultados_an"
if not os.path.exists(path_resultados):
    os.makedirs(path_resultados)

for an in an_values:
    carpeta_resultados = f"{path_resultados}/an_{an}"  

    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    print(f"🚀 Ejecutando simulación para an = {an}...")

    os.environ["RESULTADOS_PATH"] = carpeta_resultados
    os.environ["PARAM_AN"] = str(an)

    resultado = subprocess.run(["python", "/home/andr3s/Documentos/SS/DIIID 2.py"], capture_output=True, text=True)
    print(resultado.stdout)

print("Simulación completada para variaciones de an.")
