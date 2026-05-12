# -*- coding: utf-8 -*-
"""
============================================================================
ANÁLISIS AIRBNB VS HOTELERÍA - FESTIVAL VALLENATO 2021-2026
============================================================================
Compara medianas de precios, desviación estándar y volatilidad entre
plataformas de economía colaborativa (Airbnb) y hotelería tradicional.
Fuentes: RCN Noticias, RTA Noticias, CC Valledupar
============================================================================
"""

import numpy as np
from data.datos_festival import AIRBNB_VS_HOTEL, ANIOS


def analizar_airbnb_vs_hotel():
    """
    Realiza el análisis comparativo completo entre Airbnb y hotelería.
    
    Calcula para cada sector (2021-2026):
    - Mediana de precios por año
    - Desviación estándar de las medianas
    - Coeficiente de variación (volatilidad)
    - Rango de precios
    
    Retorna:
    --------
    dict con análisis completo y conclusiones
    """
    medianas_airbnb = []
    medianas_hotel = []
    rangos_airbnb = []
    rangos_hotel = []
    
    for anio in ANIOS:
        d = AIRBNB_VS_HOTEL[anio]
        medianas_airbnb.append(d["airbnb_mediana"])
        medianas_hotel.append(d["hotel_mediana"])
        rangos_airbnb.append(d["airbnb_max"] - d["airbnb_min"])
        rangos_hotel.append(d["hotel_max"] - d["hotel_min"])
    
    arr_airbnb = np.array(medianas_airbnb, dtype=float)
    arr_hotel = np.array(medianas_hotel, dtype=float)
    
    # Estadísticas Airbnb
    media_airbnb = np.mean(arr_airbnb)
    mediana_global_airbnb = np.median(arr_airbnb)
    std_airbnb = np.std(arr_airbnb, ddof=1)
    cv_airbnb = (std_airbnb / media_airbnb) * 100
    
    # Estadísticas Hotel
    media_hotel = np.mean(arr_hotel)
    mediana_global_hotel = np.median(arr_hotel)
    std_hotel = np.std(arr_hotel, ddof=1)
    cv_hotel = (std_hotel / media_hotel) * 100
    
    # Determinar mayor volatilidad
    if cv_airbnb > cv_hotel:
        sector_volatil = "Airbnb"
        conclusion_volatilidad = (
            f"El sector Airbnb presenta un coeficiente de variación de "
            f"{cv_airbnb:.2f}% frente al {cv_hotel:.2f}% de la hotelería "
            f"tradicional. Esto indica que Airbnb ha mostrado MAYOR "
            f"VOLATILIDAD (especulación de precios) durante los festivales "
            f"2021-2026. La diferencia de {cv_airbnb - cv_hotel:.2f} puntos "
            f"porcentuales sugiere que los precios en plataformas de economía "
            f"colaborativa son más susceptibles a la especulación durante "
            f"eventos de alta demanda como el Festival Vallenato."
        )
    else:
        sector_volatil = "Hotelería"
        conclusion_volatilidad = (
            f"La hotelería tradicional presenta un coeficiente de variación de "
            f"{cv_hotel:.2f}% frente al {cv_airbnb:.2f}% de Airbnb, mostrando "
            f"MAYOR VOLATILIDAD en el período analizado."
        )
    
    # Análisis 2026 específico
    datos_2026 = AIRBNB_VS_HOTEL[2026]
    rango_airbnb_2026 = datos_2026["airbnb_max"] - datos_2026["airbnb_min"]
    rango_hotel_2026 = datos_2026["hotel_max"] - datos_2026["hotel_min"]
    
    conclusion_2026 = (
        f"En el Festival 2026, el rango de precios de Airbnb fue de "
        f"${rango_airbnb_2026:,} COP (${datos_2026['airbnb_min']:,} a "
        f"${datos_2026['airbnb_max']:,}), mientras que en hotelería fue de "
        f"${rango_hotel_2026:,} COP (${datos_2026['hotel_min']:,} a "
        f"${datos_2026['hotel_max']:,}). "
        f"La brecha de precios en Airbnb es {rango_airbnb_2026/rango_hotel_2026:.1f}x "
        f"mayor que en hotelería, evidenciando especulación en temporada alta."
    )
    
    return {
        "anios": ANIOS,
        "medianas_airbnb": medianas_airbnb,
        "medianas_hotel": medianas_hotel,
        "rangos_airbnb": rangos_airbnb,
        "rangos_hotel": rangos_hotel,
        "estadisticas": {
            "airbnb": {
                "media": round(media_airbnb, 2),
                "mediana_global": round(mediana_global_airbnb, 2),
                "desviacion_std": round(std_airbnb, 2),
                "cv_porcentaje": round(cv_airbnb, 2)
            },
            "hotel": {
                "media": round(media_hotel, 2),
                "mediana_global": round(mediana_global_hotel, 2),
                "desviacion_std": round(std_hotel, 2),
                "cv_porcentaje": round(cv_hotel, 2)
            }
        },
        "sector_mas_volatil": sector_volatil,
        "conclusion_volatilidad": conclusion_volatilidad,
        "conclusion_2026": conclusion_2026,
        "datos_2026": datos_2026
    }


def imprimir_analisis():
    """Imprime el análisis comparativo."""
    r = analizar_airbnb_vs_hotel()
    
    print(f"\n{'='*70}")
    print("  ANÁLISIS COMPARATIVO: AIRBNB VS HOTELERÍA (2021-2026)")
    print(f"{'='*70}")
    
    print(f"\n  {'Año':<8} {'Airbnb Med.':<15} {'Hotel Med.':<15} {'Rango Airbnb':<15} {'Rango Hotel':<15}")
    print(f"  {'─'*68}")
    for i, anio in enumerate(ANIOS):
        print(f"  {anio:<8} ${r['medianas_airbnb'][i]:>11,} ${r['medianas_hotel'][i]:>11,} "
              f"${r['rangos_airbnb'][i]:>11,} ${r['rangos_hotel'][i]:>11,}")
    
    print(f"\n  Resumen Estadístico:")
    print(f"  {'─'*50}")
    print(f"  {'Métrica':<25} {'Airbnb':>12} {'Hotel':>12}")
    print(f"  {'─'*50}")
    for k, label in [("media", "Media"), ("mediana_global", "Mediana Global"),
                     ("desviacion_std", "Desv. Estándar"), ("cv_porcentaje", "CV (%)")]:
        va = r["estadisticas"]["airbnb"][k]
        vh = r["estadisticas"]["hotel"][k]
        if k == "cv_porcentaje":
            print(f"  {label:<25} {va:>11.2f}% {vh:>11.2f}%")
        else:
            print(f"  {label:<25} ${va:>10,.0f} ${vh:>10,.0f}")
    
    print(f"\n  Sector con mayor volatilidad: {r['sector_mas_volatil']}")
    print(f"\n  Conclusión:")
    print(f"  {r['conclusion_volatilidad']}")
    print(f"\n  Análisis 2026:")
    print(f"  {r['conclusion_2026']}")
    print(f"{'='*70}")
    
    return r
