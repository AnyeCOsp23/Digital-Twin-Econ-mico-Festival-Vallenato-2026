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
import pandas as pd
from data.datos_festival import DATOS, ANIOS, NODOS


def calcular_estadisticas_nodo(nodo, anio):
    """
    Calcula estadísticas descriptivas para un nodo y año específico.
    
    Según la rúbrica del proyecto:
    - Media: Ingreso promedio por visitante (ingresos / visitantes)
    - Mediana: Para identificar sesgos por consumos de alto valor (VIP)
      → Se calcula sobre los valores de consumo/gasto del nodo
    - Moda: Departamento de procedencia predominante de los turistas
    - Desviación Estándar: Como medida de volatilidad y riesgo del empleo
      → Se calcula sobre los empleos temporales de todos los años del nodo
    
    Parámetros:
    -----------
    nodo : str - Nombre del nodo económico
    anio : int - Año de análisis (2021-2026)
    
    Retorna:
    --------
    dict con todas las estadísticas calculadas
    """
    datos = DATOS[nodo][anio]
    
    # ---- CÁLCULOS SEGÚN RÚBRICA ----
    
    # 1. MEDIA: Ingreso promedio por visitante
    #    Fórmula: Media = Ingresos totales (en COP) / Visitantes
    #    ingresos_millones está en millones de COP, se convierte a COP
    ingresos_cop = datos["ingresos_millones"] * 1_000_000  # Convertir a COP
    visitantes = datos["visitantes"]
    media_ingreso_por_visitante = ingresos_cop / visitantes if visitantes > 0 else 0
    
    # 2. MEDIANA: Para identificar sesgos por consumos de alto valor (VIP)
    #    Se calcula sobre los valores de consumo/gasto asociados al nodo:
    #    gasto_promedio, precio_hospedaje, actividad_comercial, impacto_transporte
    #    (todos representan niveles de consumo/gasto por persona o sector)
    valores_consumo = [
        datos["gasto_promedio"],             # Gasto promedio por visitante
        datos["precio_hospedaje_promedio"],   # Precio hospedaje por noche
        datos["actividad_comercial_millones"] * 1_000_000 / visitantes if visitantes > 0 else 0,  # Act. comercial per cápita
        datos["impacto_transporte_millones"] * 1_000_000 / visitantes if visitantes > 0 else 0,   # Transporte per cápita
    ]
    arr_consumo = np.array(valores_consumo, dtype=float)
    mediana_consumo = np.median(arr_consumo)
    
    # 3. MODA: Departamento de procedencia predominante de turistas
    moda_procedencia = datos["procedencia_moda"]
    
    # 4. DESVIACIÓN ESTÁNDAR: Volatilidad y riesgo del empleo generado
    #    Se calcula sobre los empleos temporales de TODOS los años del nodo
    #    Fórmula: σ = √[Σ(xᵢ - x̄)² / (n-1)]  (muestral, ddof=1)
    empleos_todos_anios = [DATOS[nodo][a]["empleos_temporales"] for a in ANIOS]
    arr_empleos = np.array(empleos_todos_anios, dtype=float)
    desviacion_std_empleos = np.std(arr_empleos, ddof=1)
    media_empleos = np.mean(arr_empleos)
    varianza_empleos = np.var(arr_empleos, ddof=1)
    rango_empleos = np.max(arr_empleos) - np.min(arr_empleos)
    
    # CV del empleo: mide el riesgo relativo
    cv_empleos = (desviacion_std_empleos / media_empleos) * 100 if media_empleos != 0 else 0
    
    return {
        "nodo": nodo,
        "anio": anio,
        "media": round(media_ingreso_por_visitante, 2),
        "mediana": round(mediana_consumo, 2),
        "moda_procedencia": moda_procedencia,
        "desviacion_std": round(desviacion_std_empleos, 2),
        "varianza": round(varianza_empleos, 2),
        "rango": round(rango_empleos, 2),
        "coeficiente_variacion": round(cv_empleos, 2),
        "media_empleos": round(media_empleos, 2),
        "empleos_serie": empleos_todos_anios,
        "empleos_actual": datos["empleos_temporales"],
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
                "Media (Ingreso/Visitante COP)": est["media"],
                "Mediana (Sesgo VIP COP)": est["mediana"],
                "Desv. Std (σ Empleo)": est["desviacion_std"],
                "CV Empleo (%)": est["coeficiente_variacion"],
                "Moda (Procedencia)": est["moda_procedencia"],
                "Fuente": est["fuente"]
            })
    
    return pd.DataFrame(filas)


def imprimir_estadisticas(nodo, anio):
    """Imprime las estadísticas descriptivas de forma legible (según rúbrica)."""
    est = calcular_estadisticas_nodo(nodo, anio)
    print(f"\n{'='*70}")
    print(f"  ESTADÍSTICA DESCRIPTIVA: {nodo} - {anio}")
    print(f"{'='*70}")
    print(f"  Media (ingreso/visitante): ${est['media']:>12,.0f} COP")
    print(f"  Mediana (sesgo VIP):       ${est['mediana']:>12,.0f} COP")
    print(f"  Moda (procedencia):        {est['moda_procedencia']:>13s}")
    print(f"  Desv. Std (σ empleo):      {est['desviacion_std']:>13,.2f} empleos")
    print(f"  Varianza empleo:           {est['varianza']:>13,.2f}")
    print(f"  Rango empleo:              {est['rango']:>13,.0f}")
    print(f"  CV empleo (riesgo):        {est['coeficiente_variacion']:>13.2f}%")
    print(f"  Fuente: {est['fuente']}")
    print(f"{'='*70}")
    return est
