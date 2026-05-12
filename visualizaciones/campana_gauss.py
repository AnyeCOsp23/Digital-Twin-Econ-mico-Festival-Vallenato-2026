# -*- coding: utf-8 -*-
"""
============================================================================
CAMPANA DE GAUSS - DISTRIBUCIÓN NORMAL
============================================================================
Genera la curva de distribución normal con área sombreada para
P(X > 10,000) del nodo Parque de la Leyenda en 2026.
============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from data.datos_festival import DIST_NORMAL_PARAMS
import os


def graficar_campana_gauss(guardar=True, output_dir="output"):
    """
    Genera la gráfica de la Campana de Gauss con área sombreada.
    
    Parámetros:
    -----------
    guardar : bool - Si True, guarda la imagen en output_dir
    output_dir : str - Directorio de salida
    """
    media = DIST_NORMAL_PARAMS["media"]
    sigma = DIST_NORMAL_PARAMS["desviacion"]
    meta = DIST_NORMAL_PARAMS["meta"]
    
    # Calcular Z-score y probabilidad
    z_score = (meta - media) / sigma
    prob_superar = 1 - stats.norm.cdf(z_score)
    
    # Crear rango de valores para la curva
    x = np.linspace(media - 4*sigma, media + 4*sigma, 1000)
    y = stats.norm.pdf(x, media, sigma)
    
    # Configurar la figura
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#0a0a1a')
    ax.set_facecolor('#0a0a1a')
    
    # Dibujar la curva principal
    ax.plot(x, y, color='#00d4ff', linewidth=2.5, label='Distribución Normal')
    
    # Sombrear área bajo la curva (total)
    ax.fill_between(x, y, alpha=0.15, color='#00d4ff')
    
    # Sombrear área de éxito P(X > meta)
    x_exito = np.linspace(meta, media + 4*sigma, 300)
    y_exito = stats.norm.pdf(x_exito, media, sigma)
    ax.fill_between(x_exito, y_exito, alpha=0.6, color='#ff4444',
                    label=f'P(X > ${meta:,}M) = {prob_superar*100:.2f}%')
    
    # Sombrear área complementaria
    x_comp = np.linspace(media - 4*sigma, meta, 300)
    y_comp = stats.norm.pdf(x_comp, media, sigma)
    ax.fill_between(x_comp, y_comp, alpha=0.25, color='#00ff88',
                    label=f'P(X ≤ ${meta:,}M) = {(1-prob_superar)*100:.2f}%')
    
    # Línea de la media
    ax.axvline(x=media, color='#ffcc00', linestyle='--', linewidth=2,
               label=f'μ = ${media:,}M')
    
    # Línea de la meta
    ax.axvline(x=meta, color='#ff4444', linestyle='-', linewidth=2.5,
               label=f'Meta = ${meta:,}M')
    
    # Anotaciones
    ax.annotate(f'μ = ${media:,}M\n(Media histórica)',
                xy=(media, stats.norm.pdf(media, media, sigma)),
                xytext=(media - 1200, stats.norm.pdf(media, media, sigma) * 0.7),
                arrowprops=dict(arrowstyle='->', color='#ffcc00', lw=1.5),
                fontsize=11, color='#ffcc00', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor='#ffcc00'))
    
    ax.annotate(f'Meta = ${meta:,}M\nZ = {z_score:.2f}',
                xy=(meta, stats.norm.pdf(meta, media, sigma)),
                xytext=(meta + 300, stats.norm.pdf(meta, media, sigma) * 1.8),
                arrowprops=dict(arrowstyle='->', color='#ff4444', lw=1.5),
                fontsize=11, color='#ff4444', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor='#ff4444'))
    
    # Texto con resultado
    resultado_text = (
        f"Z-score = ({meta:,} - {media:,}) / {sigma} = {z_score:.2f}\n"
        f"P(X > ${meta:,}M) = {prob_superar*100:.2f}%\n"
        f"Interpretación: La probabilidad de superar\n"
        f"la meta es estadísticamente baja."
    )
    ax.text(0.02, 0.95, resultado_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', color='white',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                     edgecolor='#00d4ff', alpha=0.9))
    
    # Marcas de desviación estándar
    for i in range(-3, 4):
        val = media + i * sigma
        if media - 4*sigma < val < media + 4*sigma:
            ax.axvline(x=val, color='gray', linestyle=':', linewidth=0.5, alpha=0.4)
            label_text = f'{i}σ' if i != 0 else 'μ'
            ax.text(val, -0.00002, label_text, ha='center', fontsize=8,
                   color='gray', alpha=0.7)
    
    # Configurar ejes
    ax.set_xlabel('Ingresos (Millones COP)', fontsize=13, color='white', labelpad=10)
    ax.set_ylabel('Densidad de Probabilidad', fontsize=13, color='white', labelpad=10)
    ax.set_title(
        'Distribución Normal – Parque de la Leyenda Vallenata 2026\n'
        'Probabilidad de Superar la Meta de Ingresos',
        fontsize=16, color='white', fontweight='bold', pad=20
    )
    
    ax.legend(loc='upper right', fontsize=10, facecolor='#1a1a2e',
              edgecolor='#333', labelcolor='white', framealpha=0.9)
    ax.tick_params(colors='white', labelsize=10)
    ax.spines['bottom'].set_color('#333')
    ax.spines['left'].set_color('#333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.1, color='white')
    
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "campana_gauss_parque_leyenda_2026.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print(f"  ✓ Campana de Gauss guardada: {filepath}")
    
    plt.close(fig)
    return fig
