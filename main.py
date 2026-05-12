# -*- coding: utf-8 -*-
"""
============================================================================
    DIGITAL TWIN ECONOMICO - FESTIVAL DE LA LEYENDA VALLENATA 2026
    59a Edicion | Valledupar, Cesar, Colombia
============================================================================

    Autores:    [Nombres del grupo]
    Materia:    Modelos y Simulacion
    Semestre:   6to Semestre - Ingenieria de Sistemas
    Fecha:      Mayo 2026

    Descripcion:
    Aplicacion de simulacion dinamica que analiza el impacto economico
    regional del Festival Vallenato 2026 mediante georreferenciacion,
    estadistica descriptiva/inferencial y modelado de distribucion normal.

    Fuentes de datos:
    - Camara de Comercio de Valledupar (ccvalledupar.org.co)
    - SITUR Cesar
    - DANE (dane.gov.co)
    - El Pilon, Semana, Pulzo, La Republica
============================================================================
"""

import matplotlib
matplotlib.use('Agg')  # Backend no interactivo: guarda sin abrir ventanas

import sys
import os
import io
import warnings
warnings.filterwarnings('ignore')

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos del proyecto
from data.datos_festival import (
    DATOS, DATOS_AGREGADOS, NODOS_COORDENADAS,
    ANIOS, NODOS, DIST_NORMAL_PARAMS
)
from estadistica.descriptiva import (
    calcular_estadisticas_nodo, calcular_estadisticas_serie_temporal,
    generar_tabla_resumen, imprimir_estadisticas
)
from estadistica.inferencial import (
    calcular_probabilidad_superar_meta, imprimir_analisis_normal
)
from estadistica.airbnb_vs_hotel import (
    analizar_airbnb_vs_hotel, imprimir_analisis as imprimir_airbnb
)
from visualizaciones.campana_gauss import graficar_campana_gauss
from visualizaciones.graficos import generar_todas_visualizaciones
from visualizaciones.mapa_interactivo import generar_mapa_interactivo


# Directorio de salida para gráficos y mapas
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def banner():
    """Muestra el banner del proyecto."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   🎵  DIGITAL TWIN ECONÓMICO                                        ║
║       FESTIVAL DE LA LEYENDA VALLENATA 2026                          ║
║       59ª Edición – Valledupar, Cesar                                ║
║                                                                      ║
║   📊  Modelos y Simulación – 6° Semestre                            ║
║   🏫  Ingeniería de Sistemas                                        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def resumen_ejecutivo():
    """Genera e imprime el resumen ejecutivo del proyecto."""
    print("\n" + "="*70)
    print("  1. RESUMEN EJECUTIVO")
    print("="*70)
    
    total_2026 = DATOS_AGREGADOS[2026]
    print(f"""
  El presente estudio analiza el impacto económico de la 59ª edición
  del Festival de la Leyenda Vallenata (2026) en Valledupar, Cesar.

  Resultados principales del Festival 2026:
  ─────────────────────────────────────────
  • Visitantes totales:      {total_2026['visitantes_total']:>10,} personas
  • Impacto económico:       ${total_2026['impacto_total_millones']:>10,} millones COP
  • Ocupación hotelera:      {total_2026['ocupacion_hotelera_prom']:>10}% (pico 98%)
  • Empleos generados:       {total_2026['empleos_total']:>10,} puestos
  • Vehículos ingresados:    {total_2026['vehiculos']:>10,} (+37.7% vs 2025)

  Fuente: Cámara de Comercio de Valledupar para el Valle del Río Cesar
  """)


def seccion_estadistica_descriptiva():
    """Ejecuta y muestra la sección de estadística descriptiva."""
    print("\n" + "="*70)
    print("  3. ESTADÍSTICA DESCRIPTIVA POR NODO Y AÑO")
    print("="*70)
    
    # Mostrar estadísticas para cada nodo en 2026
    for nodo in NODOS:
        imprimir_estadisticas(nodo, 2026)
    
    # Análisis de series temporales
    print("\n" + "-"*70)
    print("  ANÁLISIS DE SERIES TEMPORALES (Ingresos 2021-2026)")
    print("-"*70)
    for nodo in NODOS:
        st = calcular_estadisticas_serie_temporal(nodo, "ingresos_millones")
        print(f"\n  {nodo}:")
        print(f"    Valores: {st['valores']}")
        print(f"    Media: ${st['media']:,.2f}M | Mediana: ${st['mediana']:,.2f}M")
        print(f"    Desv. Std: ${st['desviacion_std']:,.2f}M | CV: {st['cv']:.2f}%")
        print(f"    Crecimiento anual promedio: {st['tasa_crecimiento_anual']:.2f}%")
    
    # Generar tabla resumen
    print("\n  Generando tabla resumen consolidada...")
    df = generar_tabla_resumen()
    csv_path = os.path.join(OUTPUT_DIR, "tabla_resumen_estadisticas.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"  ✓ Tabla resumen guardada: {csv_path}")


def seccion_distribucion_normal():
    """Ejecuta y muestra la sección de distribución normal."""
    print("\n" + "="*70)
    print("  4. ANÁLISIS DE DISTRIBUCIÓN NORMAL (CAMPANA DE GAUSS)")
    print("="*70)
    
    resultado = imprimir_analisis_normal()
    
    # Graficar la campana
    print("\n  Generando gráfica de la Campana de Gauss...")
    graficar_campana_gauss(guardar=True, output_dir=OUTPUT_DIR)


def seccion_airbnb():
    """Ejecuta y muestra la sección Airbnb vs Hotelería."""
    print("\n" + "="*70)
    print("  5. ANÁLISIS AIRBNB VS HOTELERÍA (PUNTO EXTRA)")
    print("="*70)
    
    imprimir_airbnb()


def seccion_mapa():
    """Genera el mapa interactivo."""
    print("\n" + "="*70)
    print("  6. MAPA INTERACTIVO DE VALLEDUPAR")
    print("="*70)
    
    generar_mapa_interactivo(output_dir=OUTPUT_DIR)


def seccion_visualizaciones():
    """Genera todas las visualizaciones."""
    generar_todas_visualizaciones(output_dir=OUTPUT_DIR)


def conclusiones():
    """Genera las conclusiones del proyecto."""
    resultado_normal = calcular_probabilidad_superar_meta()
    resultado_airbnb = analizar_airbnb_vs_hotel()
    
    print(f"\n{'='*70}")
    print("  7. CONCLUSIONES")
    print(f"{'='*70}")
    print(f"""
  CONCLUSIONES TÉCNICAS, ECONÓMICAS Y ESTADÍSTICAS
  ─────────────────────────────────────────────────

  1. CRECIMIENTO SOSTENIDO: El Festival Vallenato ha mostrado un
     crecimiento continuo desde la reactivación post-pandemia (2022),
     pasando de ~$120,000M a ~$230,000M en impacto económico total,
     lo que representa un crecimiento del 91.7% en 4 años.

  2. DISTRIBUCIÓN NORMAL: La probabilidad de que el Parque de la
     Leyenda supere la meta de $10,000M fue de {resultado_normal['prob_superar_porcentaje']:.2f}%
     (Z={resultado_normal['z_score']:.2f}). Esto indica que la meta fue
     ambiciosa pero estadísticamente improbable sin medidas
     extraordinarias de captación de ingresos.

  3. VOLATILIDAD EN HOSPEDAJE: El sector {resultado_airbnb['sector_mas_volatil']}
     presentó mayor volatilidad (CV={resultado_airbnb['estadisticas']['airbnb']['cv_porcentaje']:.2f}%
     Airbnb vs {resultado_airbnb['estadisticas']['hotel']['cv_porcentaje']:.2f}% Hotel),
     evidenciando especulación de precios en temporada alta.

  4. NODO DOMINANTE: El Parque de la Leyenda es el nodo con mayor
     generación de ingresos ($9,800M en 2026), seguido por la
     Feria Ganadera ($7,500M), lo que refleja la importancia del
     sector de espectáculos y el agropecuario.

  5. RECUPERACIÓN POST-PANDEMIA: El Festival demostró resiliencia
     económica, recuperando los niveles de visitantes pre-pandemia
     en 2023 (~210,000) y superándolos en 2024 (~227,727).

  6. IMPACTO SOCIAL: Se generaron más de 2,630 empleos temporales
     en 2026, beneficiando principalmente a los sectores de
     gastronomía, logística, hotelería y transporte.

  7. TURISMO INTERNACIONAL: La proporción de turistas internacionales
     creció al 10% en 2026, con visitantes de México, Chile,
     Ecuador, República Dominicana, EE.UU. y España.
  """)


def main():
    """Función principal que ejecuta todo el proyecto."""
    banner()
    
    print("  Iniciando Digital Twin Económico...")
    print(f"  Directorio de salida: {OUTPUT_DIR}\n")
    
    # Crear directorio de salida
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Resumen ejecutivo
    resumen_ejecutivo()
    
    # 2. Estadística descriptiva
    seccion_estadistica_descriptiva()
    
    # 3. Distribución normal
    seccion_distribucion_normal()
    
    # 4. Airbnb vs Hotelería
    seccion_airbnb()
    
    # 5. Mapa interactivo
    seccion_mapa()
    
    # 6. Visualizaciones
    seccion_visualizaciones()
    
    # 7. Conclusiones
    conclusiones()
    
    print(f"\n{'='*70}")
    print("  ✅ PROYECTO COMPLETADO EXITOSAMENTE")
    print(f"{'='*70}")
    print(f"\n  Archivos generados en: {OUTPUT_DIR}/")
    print("  • mapa_interactivo_valledupar.html")
    print("  • campana_gauss_parque_leyenda_2026.png")
    print("  • serie_tiempo_ingresos.png")
    print("  • serie_tiempo_visitantes.png")
    print("  • histograma_ingresos_2026.png")
    print("  • boxplot_ingresos.png")
    print("  • barras_airbnb_vs_hotel.png")
    print("  • ⭐ PUNTO_EXTRA_airbnb_vs_hotel_dashboard.png")
    print("  • ocupacion_hotelera.png")
    print("  • tabla_resumen_estadisticas.csv")
    print()


if __name__ == "__main__":
    main()
