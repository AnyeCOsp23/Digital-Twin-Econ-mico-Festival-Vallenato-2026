# -*- coding: utf-8 -*-
"""
============================================================================
VISUALIZACIONES - Series de Tiempo, Histogramas, Boxplots, Barras
============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from data.datos_festival import DATOS, DATOS_AGREGADOS, AIRBNB_VS_HOTEL, ANIOS, NODOS

# Estilo global oscuro
plt.rcParams.update({
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor': '#0a0a1a',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': '#333',
    'grid.color': '#222',
    'grid.alpha': 0.3,
    'font.family': 'sans-serif'
})

COLORES_NODOS = {
    "Parque de la Leyenda": "#ff4444",
    "Plaza Alfonso López": "#4488ff",
    "Balneario Hurtado": "#00cc66",
    "Desfile de Piloneras": "#ff8800",
    "Feria Ganadera": "#cc44ff"
}


def serie_tiempo_ingresos(guardar=True, output_dir="output"):
    """Series de tiempo de ingresos por nodo (2021-2026)."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for nodo in NODOS:
        ingresos = [DATOS[nodo][a]["ingresos_millones"] for a in ANIOS]
        ax.plot(ANIOS, ingresos, marker='o', linewidth=2.5, markersize=8,
                color=COLORES_NODOS[nodo], label=nodo)
        # Anotar último valor
        ax.annotate(f'${ingresos[-1]:,}M', xy=(ANIOS[-1], ingresos[-1]),
                   xytext=(10, 5), textcoords='offset points',
                   fontsize=9, color=COLORES_NODOS[nodo], fontweight='bold')
    
    ax.set_xlabel('Año', fontsize=13, labelpad=10)
    ax.set_ylabel('Ingresos (Millones COP)', fontsize=13, labelpad=10)
    ax.set_title('Serie de Tiempo – Ingresos por Nodo Económico\nFestival Vallenato 2021-2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=9, facecolor='#1a1a2e', edgecolor='#333',
              labelcolor='white', framealpha=0.9)
    ax.set_xticks(ANIOS)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True)
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "serie_tiempo_ingresos.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Serie de tiempo de ingresos guardada")
    plt.close(fig)
    return fig


def serie_tiempo_visitantes(guardar=True, output_dir="output"):
    """Series de tiempo de visitantes por nodo (2021-2026)."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for nodo in NODOS:
        visitantes = [DATOS[nodo][a]["visitantes"] for a in ANIOS]
        ax.plot(ANIOS, visitantes, marker='s', linewidth=2.5, markersize=8,
                color=COLORES_NODOS[nodo], label=nodo)
    
    ax.set_xlabel('Año', fontsize=13, labelpad=10)
    ax.set_ylabel('Número de Visitantes', fontsize=13, labelpad=10)
    ax.set_title('Serie de Tiempo – Visitantes por Nodo Económico\nFestival Vallenato 2021-2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=9, facecolor='#1a1a2e', edgecolor='#333',
              labelcolor='white', framealpha=0.9)
    ax.set_xticks(ANIOS)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.grid(True)
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "serie_tiempo_visitantes.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Serie de tiempo de visitantes guardada")
    plt.close(fig)
    return fig


def histograma_ingresos_2026(guardar=True, output_dir="output"):
    """Histograma de ingresos por nodo para 2026."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    nodos_labels = [n.replace(" ", "\n") for n in NODOS]
    ingresos = [DATOS[n][2026]["ingresos_millones"] for n in NODOS]
    colores = [COLORES_NODOS[n] for n in NODOS]
    
    bars = ax.bar(nodos_labels, ingresos, color=colores, edgecolor='white',
                  linewidth=0.5, width=0.6, alpha=0.85)
    
    for bar, val in zip(bars, ingresos):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
               f'${val:,}M', ha='center', va='bottom', fontsize=11,
               fontweight='bold', color='white')
    
    ax.set_xlabel('Nodo Económico', fontsize=13, labelpad=10)
    ax.set_ylabel('Ingresos (Millones COP)', fontsize=13, labelpad=10)
    ax.set_title('Histograma – Ingresos por Nodo Económico\n59° Festival Vallenato 2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "histograma_ingresos_2026.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Histograma de ingresos 2026 guardado")
    plt.close(fig)
    return fig


def boxplot_ingresos(guardar=True, output_dir="output"):
    """Boxplot de ingresos por nodo (distribución 2021-2026)."""
    fig, ax = plt.subplots(figsize=(13, 7))
    
    data = []
    labels = []
    for nodo in NODOS:
        ingresos = [DATOS[nodo][a]["ingresos_millones"] for a in ANIOS]
        data.append(ingresos)
        labels.append(nodo.replace(" ", "\n"))
    
    bp = ax.boxplot(data, patch_artist=True, labels=labels,
                    boxprops=dict(linewidth=1.5),
                    whiskerprops=dict(color='white', linewidth=1.5),
                    capprops=dict(color='white', linewidth=1.5),
                    medianprops=dict(color='#ffcc00', linewidth=2.5),
                    flierprops=dict(markerfacecolor='#ff4444', markersize=8))
    
    colores = [COLORES_NODOS[n] for n in NODOS]
    for patch, color in zip(bp['boxes'], colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax.set_xlabel('Nodo Económico', fontsize=13, labelpad=10)
    ax.set_ylabel('Ingresos (Millones COP)', fontsize=13, labelpad=10)
    ax.set_title('Boxplot – Distribución de Ingresos por Nodo\nFestival Vallenato 2021-2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "boxplot_ingresos.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Boxplot de ingresos guardado")
    plt.close(fig)
    return fig


def barras_comparativas_airbnb_hotel(guardar=True, output_dir="output"):
    """Barras comparativas Airbnb vs Hotelería (medianas de precio)."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(ANIOS))
    width = 0.35
    
    medianas_airbnb = [AIRBNB_VS_HOTEL[a]["airbnb_mediana"] for a in ANIOS]
    medianas_hotel = [AIRBNB_VS_HOTEL[a]["hotel_mediana"] for a in ANIOS]
    
    bars1 = ax.bar(x - width/2, medianas_airbnb, width, label='Airbnb',
                   color='#ff6b35', edgecolor='white', linewidth=0.5, alpha=0.85)
    bars2 = ax.bar(x + width/2, medianas_hotel, width, label='Hotel',
                   color='#4ecdc4', edgecolor='white', linewidth=0.5, alpha=0.85)
    
    for bar, val in zip(bars1, medianas_airbnb):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
               f'${val:,}', ha='center', va='bottom', fontsize=8,
               fontweight='bold', color='#ff6b35', rotation=45)
    for bar, val in zip(bars2, medianas_hotel):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
               f'${val:,}', ha='center', va='bottom', fontsize=8,
               fontweight='bold', color='#4ecdc4', rotation=45)
    
    ax.set_xlabel('Año', fontsize=13, labelpad=10)
    ax.set_ylabel('Mediana de Precio por Noche (COP)', fontsize=13, labelpad=10)
    ax.set_title('Comparación Airbnb vs Hotelería\nMediana de Precios por Noche – Festival Vallenato 2021-2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(ANIOS)
    ax.legend(fontsize=11, facecolor='#1a1a2e', edgecolor='#333',
              labelcolor='white', framealpha=0.9)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, axis='y')
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "barras_airbnb_vs_hotel.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Barras comparativas Airbnb vs Hotel guardadas")
    plt.close(fig)
    return fig


def dashboard_airbnb_vs_hotel(guardar=True, output_dir="output"):
    """
    PUNTO EXTRA (+0.5): Dashboard completo de Airbnb vs Hotelería.
    
    Panel de 4 gráficas que muestra claramente:
    1. Crecimiento de Mediana de Precios (2021-2026)
    2. Desviación Estándar comparativa (cuál sector tiene más ruido)
    3. Rango de precios Min-Max por año (volatilidad visual)
    4. Conclusión visual: CV% y veredicto final
    """
    from estadistica.airbnb_vs_hotel import analizar_airbnb_vs_hotel
    resultado = analizar_airbnb_vs_hotel()
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle(
        '⭐ PUNTO EXTRA: ANÁLISIS AIRBNB vs HOTELERÍA – FESTIVAL VALLENATO 2021-2026\n'
        'Mediana de Precios · Desviación Estándar · Volatilidad · Conclusión',
        fontsize=17, fontweight='bold', color='#00d4ff', y=0.98
    )
    fig.patch.set_facecolor('#0a0a1a')
    
    COLOR_AIRBNB = '#ff6b35'
    COLOR_HOTEL = '#4ecdc4'
    
    medianas_airbnb = resultado['medianas_airbnb']
    medianas_hotel = resultado['medianas_hotel']
    rangos_airbnb = resultado['rangos_airbnb']
    rangos_hotel = resultado['rangos_hotel']
    stats_airbnb = resultado['estadisticas']['airbnb']
    stats_hotel = resultado['estadisticas']['hotel']
    
    # ─── PANEL 1: Crecimiento de Mediana de Precios ───
    ax1 = axes[0, 0]
    ax1.set_facecolor('#0a0a1a')
    x = np.arange(len(ANIOS))
    width = 0.35
    
    b1 = ax1.bar(x - width/2, medianas_airbnb, width, label='Airbnb (Mediana)',
                 color=COLOR_AIRBNB, edgecolor='white', linewidth=0.5, alpha=0.9)
    b2 = ax1.bar(x + width/2, medianas_hotel, width, label='Hotel (Mediana)',
                 color=COLOR_HOTEL, edgecolor='white', linewidth=0.5, alpha=0.9)
    
    for bar, val in zip(b1, medianas_airbnb):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8000,
                f'${val:,}', ha='center', va='bottom', fontsize=8,
                fontweight='bold', color=COLOR_AIRBNB)
    for bar, val in zip(b2, medianas_hotel):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8000,
                f'${val:,}', ha='center', va='bottom', fontsize=8,
                fontweight='bold', color=COLOR_HOTEL)
    
    ax1.set_title('📊 1. Crecimiento de Mediana de Precios\n(Precio por noche en COP)',
                  fontsize=12, fontweight='bold', color='white', pad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(ANIOS)
    ax1.set_ylabel('Mediana Precio/Noche (COP)', fontsize=10)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax1.legend(fontsize=9, facecolor='#1a1a2e', edgecolor='#333', labelcolor='white')
    ax1.grid(True, axis='y', alpha=0.2)
    
    # ─── PANEL 2: Desviación Estándar (el "ruido") ───
    ax2 = axes[0, 1]
    ax2.set_facecolor('#0a0a1a')
    
    sectores = ['Airbnb\n(Economía Colaborativa)', 'Hotelería\n(Tradicional)']
    std_vals = [stats_airbnb['desviacion_std'], stats_hotel['desviacion_std']]
    colores_bar = [COLOR_AIRBNB, COLOR_HOTEL]
    
    bars_std = ax2.bar(sectores, std_vals, color=colores_bar, edgecolor='white',
                       linewidth=1.5, width=0.5, alpha=0.9)
    
    # Valor sobre cada barra
    for bar, val in zip(bars_std, std_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'σ = ${val:,.0f}', ha='center', va='bottom', fontsize=14,
                fontweight='bold', color='#ffcc00')
    
    # Flecha señalando al mayor
    max_idx = 0 if std_vals[0] > std_vals[1] else 1
    ax2.annotate('⚠️ MAYOR\nRUIDO', xy=(max_idx, std_vals[max_idx]),
                xytext=(max_idx, std_vals[max_idx] + 25000),
                ha='center', fontsize=11, fontweight='bold', color='#ff4444',
                arrowprops=dict(arrowstyle='->', color='#ff4444', lw=2.5))
    
    ax2.set_title('📈 2. Desviación Estándar (σ)\n¿Cuál sector tiene más "ruido" en precios?',
                  fontsize=12, fontweight='bold', color='white', pad=10)
    ax2.set_ylabel('Desviación Estándar (COP)', fontsize=10)
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax2.grid(True, axis='y', alpha=0.2)
    
    # ─── PANEL 3: Rango de Precios (Min-Max) con fill_between ───
    ax3 = axes[1, 0]
    ax3.set_facecolor('#0a0a1a')
    
    mins_airbnb = [AIRBNB_VS_HOTEL[a]["airbnb_min"] for a in ANIOS]
    maxs_airbnb = [AIRBNB_VS_HOTEL[a]["airbnb_max"] for a in ANIOS]
    mins_hotel = [AIRBNB_VS_HOTEL[a]["hotel_min"] for a in ANIOS]
    maxs_hotel = [AIRBNB_VS_HOTEL[a]["hotel_max"] for a in ANIOS]
    
    # Fill between min-max para cada sector
    ax3.fill_between(ANIOS, mins_airbnb, maxs_airbnb, alpha=0.25, color=COLOR_AIRBNB,
                     label='Rango Airbnb (Min-Max)')
    ax3.plot(ANIOS, medianas_airbnb, color=COLOR_AIRBNB, marker='o', linewidth=2.5,
             markersize=8, label='Mediana Airbnb', zorder=5)
    
    ax3.fill_between(ANIOS, mins_hotel, maxs_hotel, alpha=0.25, color=COLOR_HOTEL,
                     label='Rango Hotel (Min-Max)')
    ax3.plot(ANIOS, medianas_hotel, color=COLOR_HOTEL, marker='s', linewidth=2.5,
             markersize=8, label='Mediana Hotel', zorder=5)
    
    # Anotar rangos 2026
    rango_a26 = maxs_airbnb[-1] - mins_airbnb[-1]
    rango_h26 = maxs_hotel[-1] - mins_hotel[-1]
    ax3.annotate(f'Rango 2026:\n${rango_a26:,}',
                xy=(2026, maxs_airbnb[-1]), xytext=(2024.5, maxs_airbnb[-1] + 100000),
                fontsize=9, fontweight='bold', color=COLOR_AIRBNB,
                arrowprops=dict(arrowstyle='->', color=COLOR_AIRBNB, lw=1.5))
    ax3.annotate(f'Rango 2026:\n${rango_h26:,}',
                xy=(2026, maxs_hotel[-1]), xytext=(2023.8, maxs_hotel[-1] + 200000),
                fontsize=9, fontweight='bold', color=COLOR_HOTEL,
                arrowprops=dict(arrowstyle='->', color=COLOR_HOTEL, lw=1.5))
    
    ax3.set_title('💰 3. Rango de Precios (Min – Max por Año)\nLa amplitud = especulación',
                  fontsize=12, fontweight='bold', color='white', pad=10)
    ax3.set_xlabel('Año', fontsize=10)
    ax3.set_ylabel('Precio por Noche (COP)', fontsize=10)
    ax3.set_xticks(ANIOS)
    ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax3.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='#333', labelcolor='white',
               loc='upper left')
    ax3.grid(True, alpha=0.2)
    
    # ─── PANEL 4: Conclusión Visual – CV% y veredicto ───
    ax4 = axes[1, 1]
    ax4.set_facecolor('#0a0a1a')
    ax4.axis('off')
    
    cv_airbnb = stats_airbnb['cv_porcentaje']
    cv_hotel = stats_hotel['cv_porcentaje']
    sector_volatil = resultado['sector_mas_volatil']
    diferencia_cv = abs(cv_airbnb - cv_hotel)
    
    # Título del panel
    ax4.text(0.5, 0.95, '🏆 4. CONCLUSIÓN: ¿CUÁL SECTOR ES MÁS VOLÁTIL?',
             transform=ax4.transAxes, fontsize=14, fontweight='bold',
             color='#ffcc00', ha='center', va='top')
    
    # Cajas de CV
    # Airbnb
    rect_a = plt.Rectangle((0.05, 0.55), 0.42, 0.3, transform=ax4.transAxes,
                            facecolor=f'{COLOR_AIRBNB}22', edgecolor=COLOR_AIRBNB,
                            linewidth=2, clip_on=False)
    ax4.add_patch(rect_a)
    ax4.text(0.26, 0.82, '🏠 AIRBNB', transform=ax4.transAxes, fontsize=12,
             fontweight='bold', color=COLOR_AIRBNB, ha='center', va='center')
    ax4.text(0.26, 0.72, f'CV = {cv_airbnb:.2f}%', transform=ax4.transAxes,
             fontsize=18, fontweight='bold', color=COLOR_AIRBNB, ha='center', va='center')
    ax4.text(0.26, 0.62, f'σ = ${stats_airbnb["desviacion_std"]:,.0f}',
             transform=ax4.transAxes, fontsize=11, color='#aaa', ha='center', va='center')
    
    # Hotel
    rect_h = plt.Rectangle((0.53, 0.55), 0.42, 0.3, transform=ax4.transAxes,
                            facecolor=f'{COLOR_HOTEL}22', edgecolor=COLOR_HOTEL,
                            linewidth=2, clip_on=False)
    ax4.add_patch(rect_h)
    ax4.text(0.74, 0.82, '🏨 HOTELERÍA', transform=ax4.transAxes, fontsize=12,
             fontweight='bold', color=COLOR_HOTEL, ha='center', va='center')
    ax4.text(0.74, 0.72, f'CV = {cv_hotel:.2f}%', transform=ax4.transAxes,
             fontsize=18, fontweight='bold', color=COLOR_HOTEL, ha='center', va='center')
    ax4.text(0.74, 0.62, f'σ = ${stats_hotel["desviacion_std"]:,.0f}',
             transform=ax4.transAxes, fontsize=11, color='#aaa', ha='center', va='center')
    
    # Veredicto
    rect_v = plt.Rectangle((0.08, 0.08), 0.84, 0.38, transform=ax4.transAxes,
                            facecolor='#ff444422', edgecolor='#ff4444',
                            linewidth=3, linestyle='--', clip_on=False)
    ax4.add_patch(rect_v)
    
    ax4.text(0.5, 0.40, f'⚠️ SECTOR CON MAYOR ESPECULACIÓN:',
             transform=ax4.transAxes, fontsize=12, fontweight='bold',
             color='#ff4444', ha='center', va='center')
    ax4.text(0.5, 0.30, f'▶ {sector_volatil.upper()} ◀',
             transform=ax4.transAxes, fontsize=22, fontweight='bold',
             color='#ffcc00', ha='center', va='center')
    ax4.text(0.5, 0.20, f'Diferencia de volatilidad: {diferencia_cv:.2f} puntos porcentuales',
             transform=ax4.transAxes, fontsize=11, color='#aaa', ha='center', va='center')
    ax4.text(0.5, 0.12, f'Los precios de {sector_volatil} presentan MAYOR "RUIDO"',
             transform=ax4.transAxes, fontsize=11, fontweight='bold',
             color='#ff8800', ha='center', va='center')
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "PUNTO_EXTRA_airbnb_vs_hotel_dashboard.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print(f"  ✓ ⭐ PUNTO EXTRA: Dashboard Airbnb vs Hotel guardado")
    plt.close(fig)
    return fig


def serie_ocupacion_hotelera(guardar=True, output_dir="output"):
    """Serie de tiempo de ocupación hotelera agregada."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ocupaciones = [DATOS_AGREGADOS[a]["ocupacion_hotelera_prom"] for a in ANIOS]
    
    ax.plot(ANIOS, ocupaciones, marker='D', linewidth=3, markersize=10,
            color='#00d4ff', markerfacecolor='#ffcc00', markeredgecolor='white',
            markeredgewidth=2)
    ax.fill_between(ANIOS, ocupaciones, alpha=0.15, color='#00d4ff')
    
    for a, o in zip(ANIOS, ocupaciones):
        ax.annotate(f'{o}%', xy=(a, o), xytext=(0, 12),
                   textcoords='offset points', ha='center',
                   fontsize=12, fontweight='bold', color='#ffcc00')
    
    ax.set_xlabel('Año', fontsize=13, labelpad=10)
    ax.set_ylabel('Ocupación Hotelera (%)', fontsize=13, labelpad=10)
    ax.set_title('Evolución de la Ocupación Hotelera\nFestival Vallenato 2021-2026',
                fontsize=15, fontweight='bold', pad=15)
    ax.set_xticks(ANIOS)
    ax.set_ylim(0, 105)
    ax.axhline(y=80, color='#ff4444', linestyle='--', alpha=0.5, label='Umbral 80%')
    ax.legend(fontsize=10, facecolor='#1a1a2e', edgecolor='#333',
              labelcolor='white', framealpha=0.9)
    ax.grid(True)
    plt.tight_layout()
    
    if guardar:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, "ocupacion_hotelera.png"),
                   dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
        print("  ✓ Serie de ocupación hotelera guardada")
    plt.close(fig)
    return fig


def generar_todas_visualizaciones(output_dir="output"):
    """Genera todas las visualizaciones del proyecto."""
    print("\n" + "="*70)
    print("  GENERANDO VISUALIZACIONES")
    print("="*70 + "\n")
    
    serie_tiempo_ingresos(guardar=True, output_dir=output_dir)
    serie_tiempo_visitantes(guardar=True, output_dir=output_dir)
    histograma_ingresos_2026(guardar=True, output_dir=output_dir)
    boxplot_ingresos(guardar=True, output_dir=output_dir)
    barras_comparativas_airbnb_hotel(guardar=True, output_dir=output_dir)
    dashboard_airbnb_vs_hotel(guardar=True, output_dir=output_dir)
    serie_ocupacion_hotelera(guardar=True, output_dir=output_dir)
    
    print(f"\n  ✓ Todas las visualizaciones generadas en '{output_dir}/'")
