# -*- coding: utf-8 -*-
"""
============================================================================
ESTADÍSTICA INFERENCIAL - DISTRIBUCIÓN NORMAL (Campana de Gauss)
============================================================================
Análisis del Parque de la Leyenda 2026:
  Media (μ) = 8,800 millones COP
  Desviación Estándar (σ) = 750 millones COP
  Meta = 10,000 millones COP

Problema: Calcular P(X > 10,000) y graficar la campana de Gauss.
============================================================================
"""

import numpy as np
from scipy import stats
from data.datos_festival import DIST_NORMAL_PARAMS


def calcular_zscore(valor, media, desviacion):
    """
    Calcula el Z-score (puntuación estándar).
    
    Fórmula: Z = (X - μ) / σ
    
    Parámetros:
    -----------
    valor : float - Valor a evaluar (X)
    media : float - Media de la distribución (μ)
    desviacion : float - Desviación estándar (σ)
    
    Retorna:
    --------
    float - Z-score
    """
    z = (valor - media) / desviacion
    return z


def calcular_probabilidad_superar_meta():
    """
    Calcula la probabilidad de que el ingreso supere la meta.
    
    Problema planteado:
    - Media (μ) = 8,800 millones COP
    - Desviación Estándar (σ) = 750 millones COP
    - Meta (X) = 10,000 millones COP
    
    Paso 1: Calcular Z = (X - μ) / σ = (10,000 - 8,800) / 750 = 1.60
    Paso 2: P(X > 10,000) = P(Z > 1.60) = 1 - Φ(1.60)
    Paso 3: Usando tabla normal estándar: Φ(1.60) ≈ 0.9452
    Paso 4: P(X > 10,000) = 1 - 0.9452 = 0.0548 ≈ 5.48%
    
    Retorna:
    --------
    dict con Z-score, probabilidad e interpretación
    """
    media = DIST_NORMAL_PARAMS["media"]
    sigma = DIST_NORMAL_PARAMS["desviacion"]
    meta = DIST_NORMAL_PARAMS["meta"]
    
    # Paso 1: Calcular Z-score
    z_score = calcular_zscore(meta, media, sigma)
    
    # Paso 2: Calcular P(X > meta) = 1 - Φ(Z)
    prob_acumulada = stats.norm.cdf(z_score)  # Φ(Z)
    prob_superar = 1 - prob_acumulada          # P(X > meta)
    
    # Paso 3: Interpretación económica
    if prob_superar < 0.05:
        interpretacion = (
            f"La probabilidad de superar la meta de ${meta:,} millones es de "
            f"{prob_superar*100:.2f}%, lo cual es ESTADÍSTICAMENTE IMPROBABLE. "
            f"El nodo tendría que generar ingresos {z_score:.2f} desviaciones "
            f"estándar por encima de su promedio histórico. Se recomienda "
            f"ajustar la meta a un valor más realista o implementar estrategias "
            f"agresivas de captación de ingresos."
        )
    elif prob_superar < 0.10:
        interpretacion = (
            f"La probabilidad de superar la meta de ${meta:,} millones es de "
            f"{prob_superar*100:.2f}%, lo cual es POCO PROBABLE pero no "
            f"imposible. Un Z-score de {z_score:.2f} indica que la meta está "
            f"significativamente por encima del rendimiento histórico promedio. "
            f"Se necesitarían condiciones excepcionales (mayor afluencia, "
            f"eventos especiales) para alcanzar esta cifra."
        )
    else:
        interpretacion = (
            f"La probabilidad de superar la meta de ${meta:,} millones es de "
            f"{prob_superar*100:.2f}%, lo cual es razonablemente ALCANZABLE. "
            f"El Z-score de {z_score:.2f} sugiere que la meta está dentro de "
            f"un rango estadísticamente factible."
        )
    
    return {
        "media": media,
        "desviacion": sigma,
        "meta": meta,
        "z_score": round(z_score, 4),
        "prob_acumulada": round(prob_acumulada, 6),
        "prob_superar_meta": round(prob_superar, 6),
        "prob_superar_porcentaje": round(prob_superar * 100, 2),
        "interpretacion": interpretacion
    }


def imprimir_analisis_normal():
    """Imprime el análisis completo de distribución normal."""
    resultado = calcular_probabilidad_superar_meta()
    
    print(f"\n{'='*70}")
    print("  ANÁLISIS DE DISTRIBUCIÓN NORMAL - PARQUE DE LA LEYENDA 2026")
    print(f"{'='*70}")
    print(f"\n  Parámetros del modelo:")
    print(f"  • Media (μ):              ${resultado['media']:,} millones COP")
    print(f"  • Desv. Estándar (σ):     ${resultado['desviacion']:,} millones COP")
    print(f"  • Meta (X):               ${resultado['meta']:,} millones COP")
    print(f"\n  Cálculos paso a paso:")
    print(f"  ─────────────────────────────────────────────────────────")
    print(f"  Paso 1: Z = (X - μ) / σ")
    print(f"          Z = ({resultado['meta']:,} - {resultado['media']:,}) / {resultado['desviacion']:,}")
    print(f"          Z = {resultado['meta'] - resultado['media']:,} / {resultado['desviacion']:,}")
    print(f"          Z = {resultado['z_score']:.4f}")
    print(f"\n  Paso 2: P(X > {resultado['meta']:,}) = P(Z > {resultado['z_score']:.2f})")
    print(f"          = 1 - Φ({resultado['z_score']:.2f})")
    print(f"          = 1 - {resultado['prob_acumulada']:.6f}")
    print(f"          = {resultado['prob_superar_meta']:.6f}")
    print(f"\n  Resultado:")
    print(f"  ─────────────────────────────────────────────────────────")
    print(f"  P(X > ${resultado['meta']:,}M) = {resultado['prob_superar_porcentaje']:.2f}%")
    print(f"\n  Interpretación económica:")
    print(f"  {resultado['interpretacion']}")
    print(f"{'='*70}")
    
    return resultado
