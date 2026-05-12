# -*- coding: utf-8 -*-
"""
============================================================================
ESTADÍSTICA DESCRIPTIVA - DIGITAL TWIN FESTIVAL VALLENATO 2026
============================================================================
Calcula: Media, Mediana, Moda, Desviación Estándar, Varianza, Rango, CV
Para cada nodo y año del Festival.
============================================================================
"""

import numpy as np
from scipy import stats as sp_stats
import pandas as pd
from data.datos_festival import DATOS, ANIOS, NODOS


def calcular_estadisticas_nodo(nodo, anio):
    """
    Calcula estadísticas descriptivas para un nodo y año específico.
    
    Parámetros:
    -----------
    nodo : str - Nombre del nodo económico
    anio : int - Año de análisis (2021-2026)
    
    Retorna:
    --------
    dict con todas las estadísticas calculadas
    """
    datos = DATOS[nodo][anio]
    
    # Variables numéricas para análisis
    valores_numericos = [
        datos["visitantes"],
        datos["ingresos_millones"],
        datos["gasto_promedio"],
        datos["ocupacion_hotelera"],
        datos["empleos_temporales"],
        datos["precio_hospedaje_promedio"],
        datos["actividad_comercial_millones"],
        datos["impacto_transporte_millones"]
    ]
    
    arr = np.array(valores_numericos, dtype=float)
    
    # ---- CÁLCULOS DE ESTADÍSTICA DESCRIPTIVA ----
    
    # 1. Media aritmética
    media = np.mean(arr)
    
    # 2. Mediana
    mediana = np.median(arr)
    
    # 3. Moda (procedencia predominante)
    moda_procedencia = datos["procedencia_moda"]
    # Moda numérica (si aplica)
    moda_result = sp_stats.mode(arr, keepdims=True)
    moda_numerica = moda_result.mode[0] if len(moda_result.mode) > 0 else media
    
    # 4. Desviación estándar
    desviacion_std = np.std(arr, ddof=1)  # ddof=1 para muestra
    
    # 5. Varianza
    varianza = np.var(arr, ddof=1)
    
    # 6. Rango
    rango = np.max(arr) - np.min(arr)
    
    # 7. Coeficiente de variación (CV)
    cv = (desviacion_std / media) * 100 if media != 0 else 0
    
    return {
        "nodo": nodo,
        "anio": anio,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "moda_procedencia": moda_procedencia,
        "moda_numerica": round(moda_numerica, 2),
        "desviacion_std": round(desviacion_std, 2),
        "varianza": round(varianza, 2),
        "rango": round(rango, 2),
        "coeficiente_variacion": round(cv, 2),
        "datos_originales": datos,
        "fuente": datos["fuente"]
    }


def calcular_estadisticas_serie_temporal(nodo, variable="ingresos_millones"):
    """
    Calcula estadísticas para la serie temporal de una variable en un nodo.
    
    Parámetros:
    -----------
    nodo : str - Nombre del nodo
    variable : str - Variable a analizar
    
    Retorna:
    --------
    dict con estadísticas de la serie temporal
    """
    valores = [DATOS[nodo][anio][variable] for anio in ANIOS]
    arr = np.array(valores, dtype=float)
    
    media = np.mean(arr)
    mediana = np.median(arr)
    desviacion = np.std(arr, ddof=1)
    varianza = np.var(arr, ddof=1)
    rango = np.max(arr) - np.min(arr)
    cv = (desviacion / media) * 100 if media != 0 else 0
    
    # Tasa de crecimiento promedio anual
    if valores[0] > 0:
        tasa_crecimiento = ((valores[-1] / valores[0]) ** (1 / (len(valores) - 1)) - 1) * 100
    else:
        tasa_crecimiento = 0
    
    return {
        "nodo": nodo,
        "variable": variable,
        "valores": valores,
        "anios": ANIOS,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "desviacion_std": round(desviacion, 2),
        "varianza": round(varianza, 2),
        "rango": round(rango, 2),
        "cv": round(cv, 2),
        "tasa_crecimiento_anual": round(tasa_crecimiento, 2),
        "minimo": round(np.min(arr), 2),
        "maximo": round(np.max(arr), 2)
    }


def generar_tabla_resumen():
    """
    Genera una tabla resumen con estadísticas para todos los nodos y años.
    
    Retorna:
    --------
    pd.DataFrame con la tabla resumen completa
    """
    filas = []
    for nodo in NODOS:
        for anio in ANIOS:
            est = calcular_estadisticas_nodo(nodo, anio)
            d = DATOS[nodo][anio]
            filas.append({
                "Nodo": nodo,
                "Año": anio,
                "Visitantes": d["visitantes"],
                "Ingresos (M COP)": d["ingresos_millones"],
                "Gasto Promedio (COP)": d["gasto_promedio"],
                "Ocupación Hotelera (%)": d["ocupacion_hotelera"],
                "Empleos Temporales": d["empleos_temporales"],
                "Precio Hospedaje (COP)": d["precio_hospedaje_promedio"],
                "Media": est["media"],
                "Mediana": est["mediana"],
                "Desv. Estándar": est["desviacion_std"],
                "CV (%)": est["coeficiente_variacion"],
                "Procedencia Moda": est["moda_procedencia"],
                "Fuente": est["fuente"]
            })
    
    return pd.DataFrame(filas)


def imprimir_estadisticas(nodo, anio):
    """Imprime las estadísticas descriptivas de forma legible."""
    est = calcular_estadisticas_nodo(nodo, anio)
    print(f"\n{'='*70}")
    print(f"  ESTADÍSTICA DESCRIPTIVA: {nodo} - {anio}")
    print(f"{'='*70}")
    print(f"  Media:                    {est['media']:>15,.2f}")
    print(f"  Mediana:                  {est['mediana']:>15,.2f}")
    print(f"  Moda (procedencia):       {est['moda_procedencia']:>15s}")
    print(f"  Desviación Estándar:      {est['desviacion_std']:>15,.2f}")
    print(f"  Varianza:                 {est['varianza']:>15,.2f}")
    print(f"  Rango:                    {est['rango']:>15,.2f}")
    print(f"  Coef. de Variación (%):   {est['coeficiente_variacion']:>15.2f}%")
    print(f"  Fuente: {est['fuente']}")
    print(f"{'='*70}")
    return est
