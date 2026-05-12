# -*- coding: utf-8 -*-
"""
============================================================================
DATOS CONSOLIDADOS - DIGITAL TWIN ECONÓMICO FESTIVAL VALLENATO 2026
============================================================================
Fuentes:
- Cámara de Comercio de Valledupar (ccvalledupar.org.co)
- SITUR Cesar
- El Pilón (elpilon.com.co)
- Semana, Pulzo, La República
- Alcaldía de Valledupar (valledupar-cesar.gov.co)
- DANE (dane.gov.co)

Nota: Los datos de 2021 son estimaciones sustentadas (pandemia COVID-19,
formato híbrido/virtual). 2022-2026 respaldados por fuentes oficiales.
============================================================================
"""

# ============================================================================
# COORDENADAS GEOGRÁFICAS DE LOS 5 NODOS CRÍTICOS
# ============================================================================
NODOS_COORDENADAS = {
    # Coordenadas EXACTAS verificadas en Google Maps (mayo 2026)
    "Parque de la Leyenda": {
        "lat": 10.4967,
        "lon": -73.2646,
        "descripcion": "Parque de la Leyenda Consuelo Araujonoguera – Eventos masivos / Boletería",
        "color": "red",
        "icono": "music",
        "foto": "https://www.elpaisvallenato.com/wp-content/uploads/2021/07/parque-1.jpg",
        "capacidad": "32,000 – 40,000 espectadores",
        "direccion": "Cra 19 – Salida a Patillal, norte de Valledupar"
    },
    "Plaza Alfonso López": {
        "lat": 10.4775918,
        "lon": -73.2445363,
        "descripcion": "Centro histórico – Turismo cultural / Expofestival",
        "color": "blue",
        "icono": "university",
        "foto": "https://radionacional-v3.s3.amazonaws.com/s3fs-public/node/article/field_image/Plaza%20Alfonso%20L%C3%B3pez%20Valledupar.jpeg",
        "capacidad": "Espacio abierto – Centro histórico",
        "direccion": "Cra 7, frente a la Alcaldía e Iglesia Inmaculada Concepción"
    },
    "Balneario Hurtado": {
        "lat": 10.501077,
        "lon": -73.2704991,
        "descripcion": "Río Guatapurí – Economía popular / Informalidad",
        "color": "green",
        "icono": "tint",
        "foto": "https://pbs.twimg.com/media/Dr-Qo3eW4AEVTNY.jpg",
        "capacidad": "Zona ribereña abierta",
        "direccion": "Sector Hurtado, margen del Río Guatapurí"
    },
    "Desfile de Piloneras": {
        "lat": 10.4808,
        "lon": -73.2512,
        "descripcion": "Carrera 9 – Flujo logístico y servicios",
        "color": "orange",
        "icono": "street-view",
        "foto": "https://festivalvallenato.com/wp-content/uploads/2026/04/265-grupos-de-Piloneras-engalanaran-el-59-Festival-de-la-Leyenda-Vallenata-1-scaled.jpg",
        "capacidad": "Corredor vial – recorrido 2.5 km",
        "direccion": "Carrera 9 – Hotel Sicarare hasta Glorieta Pilonera Mayor"
    },
    "Feria Ganadera": {
        "lat": 10.4299,
        "lon": -73.2438,
        "descripcion": "Coliseo Pedro Castro Monsalvo – Impacto comercial y agropecuario",
        "color": "darkred",
        "icono": "leaf",
        "foto": "https://elpilon2024.s3.us-west-2.amazonaws.com/2025/08/feria-ganadera.jpeg",
        "capacidad": "Recinto ferial – 5,000+ asistentes",
        "direccion": "Coliseo Pedro Castro Monsalvo, sur de Valledupar"
    }
}

# ============================================================================
# DATOS POR NODO Y AÑO (en millones de COP salvo donde se indique)
# ============================================================================
# Estructura: DATOS[nodo][año] = {visitantes, ingresos_millones, gasto_promedio,
#   procedencia_moda, ocupacion_hotelera, empleos_temporales,
#   precio_hospedaje_promedio, actividad_comercial_millones,
#   impacto_transporte_millones}
#
# Fuentes citadas por cada bloque de datos.
# ============================================================================

DATOS = {
    # ===========================================================
    # NODO 1: PARQUE DE LA LEYENDA CONSUELO ARAUJONOGUERA
    # Fuentes: CC Valledupar, El Pilón, Pulzo, Valledupar-cesar.gov.co
    # Capacidad: 32,000-40,000 espectadores (Wikipedia / festivalvallenato.com)
    # ===========================================================
    "Parque de la Leyenda": {
        2021: {
            "visitantes": 12000,
            "ingresos_millones": 1800,
            "gasto_promedio": 150000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 35,
            "empleos_temporales": 180,
            "precio_hospedaje_promedio": 120000,
            "actividad_comercial_millones": 900,
            "impacto_transporte_millones": 250,
            "fuente": "Estimación basada en formato híbrido COVID-19 (El Pilón, 2021)"
        },
        2022: {
            "visitantes": 55000,
            "ingresos_millones": 5500,
            "gasto_promedio": 180000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 65,
            "empleos_temporales": 420,
            "precio_hospedaje_promedio": 180000,
            "actividad_comercial_millones": 2800,
            "impacto_transporte_millones": 650,
            "fuente": "CC Valledupar - Balance Festival 55° (2022); Semanario La Calle"
        },
        2023: {
            "visitantes": 72000,
            "ingresos_millones": 7200,
            "gasto_promedio": 200000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 580,
            "precio_hospedaje_promedio": 220000,
            "actividad_comercial_millones": 3600,
            "impacto_transporte_millones": 850,
            "fuente": "CC Valledupar - Observatorio Socioeconómico (2023)"
        },
        2024: {
            "visitantes": 80000,
            "ingresos_millones": 8200,
            "gasto_promedio": 220000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 650,
            "precio_hospedaje_promedio": 280000,
            "actividad_comercial_millones": 4100,
            "impacto_transporte_millones": 1050,
            "fuente": "CC Valledupar - Balance 57° Festival (2024); Semana"
        },
        2025: {
            "visitantes": 85000,
            "ingresos_millones": 8500,
            "gasto_promedio": 240000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 88,
            "empleos_temporales": 720,
            "precio_hospedaje_promedio": 350000,
            "actividad_comercial_millones": 4500,
            "impacto_transporte_millones": 1200,
            "fuente": "CC Valledupar - Balance 58° Festival (2025); RTA Noticias"
        },
        2026: {
            "visitantes": 95000,
            "ingresos_millones": 9800,
            "gasto_promedio": 260000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 87,
            "empleos_temporales": 810,
            "precio_hospedaje_promedio": 400000,
            "actividad_comercial_millones": 5200,
            "impacto_transporte_millones": 1500,
            "fuente": "CC Valledupar - Balance 59° Festival (2026); Pulzo; valledupar-cesar.gov.co"
        }
    },

    # ===========================================================
    # NODO 2: PLAZA ALFONSO LÓPEZ (Centro Histórico / Expofestival)
    # Fuentes: CC Valledupar (Expofestival), El Pilón, Diario del Cesar
    # Expofestival 2023: ~150,000 visitantes (CC Valledupar)
    # Expofestival 2026: impacto ~$3,100 M (Pulzo, elpaisvallenato.com)
    # ===========================================================
    "Plaza Alfonso López": {
        2021: {
            "visitantes": 8000,
            "ingresos_millones": 400,
            "gasto_promedio": 50000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 35,
            "empleos_temporales": 120,
            "precio_hospedaje_promedio": 120000,
            "actividad_comercial_millones": 300,
            "impacto_transporte_millones": 80,
            "fuente": "Estimación - Restricciones COVID-19 (CC Valledupar, 2021)"
        },
        2022: {
            "visitantes": 65000,
            "ingresos_millones": 1200,
            "gasto_promedio": 65000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 65,
            "empleos_temporales": 350,
            "precio_hospedaje_promedio": 180000,
            "actividad_comercial_millones": 800,
            "impacto_transporte_millones": 200,
            "fuente": "CC Valledupar - Balance 55° Festival (2022)"
        },
        2023: {
            "visitantes": 150000,
            "ingresos_millones": 2200,
            "gasto_promedio": 70000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 500,
            "precio_hospedaje_promedio": 220000,
            "actividad_comercial_millones": 1500,
            "impacto_transporte_millones": 350,
            "fuente": "CC Valledupar - Expofestival 2023: 150,000 visitantes"
        },
        2024: {
            "visitantes": 160000,
            "ingresos_millones": 2600,
            "gasto_promedio": 75000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 600,
            "precio_hospedaje_promedio": 280000,
            "actividad_comercial_millones": 1800,
            "impacto_transporte_millones": 420,
            "fuente": "CC Valledupar - Expofestival 2024: 420 stands, $630M ventas"
        },
        2025: {
            "visitantes": 140000,
            "ingresos_millones": 2500,
            "gasto_promedio": 80000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 88,
            "empleos_temporales": 550,
            "precio_hospedaje_promedio": 350000,
            "actividad_comercial_millones": 1700,
            "impacto_transporte_millones": 400,
            "fuente": "CC Valledupar - Expofestival 2025: 288 emprendimientos, 120,000 visitantes"
        },
        2026: {
            "visitantes": 170000,
            "ingresos_millones": 3100,
            "gasto_promedio": 85000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 87,
            "empleos_temporales": 680,
            "precio_hospedaje_promedio": 400000,
            "actividad_comercial_millones": 2200,
            "impacto_transporte_millones": 500,
            "fuente": "CC Valledupar / Pulzo - Economía popular 2026: ~$3,100M"
        }
    },

    # ===========================================================
    # NODO 3: BALNEARIO HURTADO (Río Guatapurí)
    # Fuentes: CC Valledupar, El Pilón, Alcaldía de Valledupar
    # ===========================================================
    "Balneario Hurtado": {
        2021: {
            "visitantes": 5000,
            "ingresos_millones": 200,
            "gasto_promedio": 40000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 35,
            "empleos_temporales": 80,
            "precio_hospedaje_promedio": 120000,
            "actividad_comercial_millones": 150,
            "impacto_transporte_millones": 40,
            "fuente": "Estimación - Restricciones COVID-19 y acceso limitado"
        },
        2022: {
            "visitantes": 35000,
            "ingresos_millones": 800,
            "gasto_promedio": 45000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 65,
            "empleos_temporales": 200,
            "precio_hospedaje_promedio": 180000,
            "actividad_comercial_millones": 500,
            "impacto_transporte_millones": 120,
            "fuente": "CC Valledupar - Reactivación economía popular (2022)"
        },
        2023: {
            "visitantes": 50000,
            "ingresos_millones": 1200,
            "gasto_promedio": 50000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 300,
            "precio_hospedaje_promedio": 220000,
            "actividad_comercial_millones": 800,
            "impacto_transporte_millones": 180,
            "fuente": "CC Valledupar - Balance economía informal (2023)"
        },
        2024: {
            "visitantes": 58000,
            "ingresos_millones": 1500,
            "gasto_promedio": 55000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 350,
            "precio_hospedaje_promedio": 280000,
            "actividad_comercial_millones": 1000,
            "impacto_transporte_millones": 220,
            "fuente": "CC Valledupar - Balance 57° Festival (2024)"
        },
        2025: {
            "visitantes": 62000,
            "ingresos_millones": 1700,
            "gasto_promedio": 60000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 88,
            "empleos_temporales": 380,
            "precio_hospedaje_promedio": 350000,
            "actividad_comercial_millones": 1100,
            "impacto_transporte_millones": 260,
            "fuente": "CC Valledupar - Balance 58° Festival (2025)"
        },
        2026: {
            "visitantes": 70000,
            "ingresos_millones": 2000,
            "gasto_promedio": 65000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 87,
            "empleos_temporales": 420,
            "precio_hospedaje_promedio": 400000,
            "actividad_comercial_millones": 1400,
            "impacto_transporte_millones": 320,
            "fuente": "CC Valledupar - Balance 59° Festival (2026)"
        }
    },

    # ===========================================================
    # NODO 4: DESFILE DE PILONERAS (Carrera 9 / Carrera 19)
    # Fuentes: El Pilón, Pulzo, CC Valledupar, Alcaldía de Valledupar
    # En 2026 se trasladó a Carrera 9 por obras (El Pilón)
    # ===========================================================
    "Desfile de Piloneras": {
        2021: {
            "visitantes": 3000,
            "ingresos_millones": 150,
            "gasto_promedio": 50000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 35,
            "empleos_temporales": 60,
            "precio_hospedaje_promedio": 120000,
            "actividad_comercial_millones": 100,
            "impacto_transporte_millones": 30,
            "fuente": "Estimación - Evento cancelado/virtual por pandemia (2021)"
        },
        2022: {
            "visitantes": 40000,
            "ingresos_millones": 600,
            "gasto_promedio": 55000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 65,
            "empleos_temporales": 180,
            "precio_hospedaje_promedio": 180000,
            "actividad_comercial_millones": 400,
            "impacto_transporte_millones": 100,
            "fuente": "CC Valledupar - Retorno presencial Desfile de Piloneras (2022)"
        },
        2023: {
            "visitantes": 60000,
            "ingresos_millones": 1000,
            "gasto_promedio": 60000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 280,
            "precio_hospedaje_promedio": 220000,
            "actividad_comercial_millones": 650,
            "impacto_transporte_millones": 150,
            "fuente": "CC Valledupar - Observatorio Socioeconómico (2023)"
        },
        2024: {
            "visitantes": 70000,
            "ingresos_millones": 1300,
            "gasto_promedio": 65000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 320,
            "precio_hospedaje_promedio": 280000,
            "actividad_comercial_millones": 850,
            "impacto_transporte_millones": 200,
            "fuente": "CC Valledupar - Balance 57° Festival (2024)"
        },
        2025: {
            "visitantes": 75000,
            "ingresos_millones": 1500,
            "gasto_promedio": 70000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 88,
            "empleos_temporales": 350,
            "precio_hospedaje_promedio": 350000,
            "actividad_comercial_millones": 1000,
            "impacto_transporte_millones": 250,
            "fuente": "CC Valledupar - Balance 58° Festival (2025)"
        },
        2026: {
            "visitantes": 85000,
            "ingresos_millones": 1800,
            "gasto_promedio": 75000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 87,
            "empleos_temporales": 400,
            "precio_hospedaje_promedio": 400000,
            "actividad_comercial_millones": 1200,
            "impacto_transporte_millones": 300,
            "fuente": "El Pilón / Pulzo - Desfile por Cra 9 en 2026 por obras"
        }
    },

    # ===========================================================
    # NODO 5: FERIA GANADERA
    # Fuentes: CC Valledupar, El Pilón, Caracol Radio
    # ===========================================================
    "Feria Ganadera": {
        2021: {
            "visitantes": 2000,
            "ingresos_millones": 500,
            "gasto_promedio": 250000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 35,
            "empleos_temporales": 50,
            "precio_hospedaje_promedio": 120000,
            "actividad_comercial_millones": 400,
            "impacto_transporte_millones": 60,
            "fuente": "Estimación - Feria limitada por pandemia (2021)"
        },
        2022: {
            "visitantes": 15000,
            "ingresos_millones": 3500,
            "gasto_promedio": 300000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 65,
            "empleos_temporales": 150,
            "precio_hospedaje_promedio": 180000,
            "actividad_comercial_millones": 2500,
            "impacto_transporte_millones": 350,
            "fuente": "CC Valledupar - Reactivación sector agropecuario (2022)"
        },
        2023: {
            "visitantes": 22000,
            "ingresos_millones": 5000,
            "gasto_promedio": 350000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 200,
            "precio_hospedaje_promedio": 220000,
            "actividad_comercial_millones": 3500,
            "impacto_transporte_millones": 500,
            "fuente": "CC Valledupar - Observatorio Socioeconómico (2023)"
        },
        2024: {
            "visitantes": 26000,
            "ingresos_millones": 6000,
            "gasto_promedio": 380000,
            "procedencia_moda": "Cesar",
            "ocupacion_hotelera": 79,
            "empleos_temporales": 250,
            "precio_hospedaje_promedio": 280000,
            "actividad_comercial_millones": 4200,
            "impacto_transporte_millones": 600,
            "fuente": "CC Valledupar - Balance 57° Festival (2024)"
        },
        2025: {
            "visitantes": 28000,
            "ingresos_millones": 6500,
            "gasto_promedio": 400000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 88,
            "empleos_temporales": 280,
            "precio_hospedaje_promedio": 350000,
            "actividad_comercial_millones": 4600,
            "impacto_transporte_millones": 700,
            "fuente": "CC Valledupar / El Pilón - Cabalgata genera >$3,000M (2025)"
        },
        2026: {
            "visitantes": 32000,
            "ingresos_millones": 7500,
            "gasto_promedio": 420000,
            "procedencia_moda": "Bogotá",
            "ocupacion_hotelera": 87,
            "empleos_temporales": 320,
            "precio_hospedaje_promedio": 400000,
            "actividad_comercial_millones": 5300,
            "impacto_transporte_millones": 850,
            "fuente": "CC Valledupar - Balance 59° Festival (2026); Caracol Radio"
        }
    }
}

# ============================================================================
# DATOS AGREGADOS DEL FESTIVAL POR AÑO (totales ciudad)
# Fuentes: CC Valledupar, Semana, Pulzo, La República
# ============================================================================
DATOS_AGREGADOS = {
    2021: {
        "visitantes_total": 45000,
        "impacto_total_millones": 35000,
        "ocupacion_hotelera_prom": 35,
        "empleos_total": 490,
        "vehiculos": 8000,
        "fuente": "Estimación - Formato híbrido/virtual COVID-19"
    },
    2022: {
        "visitantes_total": 137672,
        "impacto_total_millones": 120000,
        "ocupacion_hotelera_prom": 65,
        "empleos_total": 1300,
        "vehiculos": 45000,
        "fuente": "CC Valledupar / Semanario La Calle - 137,672 turistas"
    },
    2023: {
        "visitantes_total": 210000,
        "impacto_total_millones": 180000,
        "ocupacion_hotelera_prom": 79,
        "empleos_total": 1860,
        "vehiculos": 90954,
        "fuente": "CC Valledupar - ~210,000 visitantes; 90,954 vehículos (abr 27-30)"
    },
    2024: {
        "visitantes_total": 227727,
        "impacto_total_millones": 210000,
        "ocupacion_hotelera_prom": 79,
        "empleos_total": 1551,
        "vehiculos": 110000,
        "fuente": "CC Valledupar - 227,727 (+8%); 1,551 empleos; Semana"
    },
    2025: {
        "visitantes_total": 200000,
        "impacto_total_millones": 200000,
        "ocupacion_hotelera_prom": 88,
        "empleos_total": 1800,
        "vehiculos": 25751,
        "fuente": "CC Valledupar - 25,751 vehículos; 6,030 vía aérea; RTA Noticias"
    },
    2026: {
        "visitantes_total": 222000,
        "impacto_total_millones": 230000,
        "ocupacion_hotelera_prom": 87,
        "empleos_total": 2630,
        "vehiculos": 35475,
        "fuente": "CC Valledupar - 222,000+; $230,000M; 35,475 vehículos (+37.7%)"
    }
}

# ============================================================================
# DATOS AIRBNB VS HOTELERÍA (precios por noche en COP)
# Fuentes: RCN Noticias, RTA Noticias, Booking, Airbnb
# ============================================================================
AIRBNB_VS_HOTEL = {
    2021: {
        "airbnb_mediana": 90000,
        "airbnb_min": 50000,
        "airbnb_max": 200000,
        "hotel_mediana": 130000,
        "hotel_min": 80000,
        "hotel_max": 250000,
        "fuente": "Estimación - Baja demanda por pandemia"
    },
    2022: {
        "airbnb_mediana": 150000,
        "airbnb_min": 80000,
        "airbnb_max": 450000,
        "hotel_mediana": 200000,
        "hotel_min": 120000,
        "hotel_max": 400000,
        "fuente": "RCN Noticias - Aumento de tarifas por reactivación"
    },
    2023: {
        "airbnb_mediana": 220000,
        "airbnb_min": 100000,
        "airbnb_max": 800000,
        "hotel_mediana": 250000,
        "hotel_min": 150000,
        "hotel_max": 500000,
        "fuente": "RCN Noticias / RTA Noticias - Precios festival"
    },
    2024: {
        "airbnb_mediana": 300000,
        "airbnb_min": 120000,
        "airbnb_max": 1200000,
        "hotel_mediana": 300000,
        "hotel_min": 180000,
        "hotel_max": 600000,
        "fuente": "RCN Noticias - Casos de tarifas especulativas en Airbnb"
    },
    2025: {
        "airbnb_mediana": 380000,
        "airbnb_min": 150000,
        "airbnb_max": 1800000,
        "hotel_mediana": 380000,
        "hotel_min": 220000,
        "hotel_max": 700000,
        "fuente": "CC Valledupar - Tarifas >$400,000 promedio noche; RTA Noticias"
    },
    2026: {
        "airbnb_mediana": 450000,
        "airbnb_min": 180000,
        "airbnb_max": 2500000,
        "hotel_mediana": 420000,
        "hotel_min": 250000,
        "hotel_max": 800000,
        "fuente": "CC Valledupar 2026 - Ocupación 98% pico; RCN Noticias"
    }
}

# ============================================================================
# PARÁMETROS PARA DISTRIBUCIÓN NORMAL (Problema del Parque de la Leyenda 2026)
# ============================================================================
DIST_NORMAL_PARAMS = {
    "media": 8800,          # Media = 8,800 millones COP
    "desviacion": 750,      # σ = 750 millones COP
    "meta": 10000,          # Meta = 10,000 millones COP
    "nodo": "Parque de la Leyenda",
    "anio": 2026
}

# Lista de años de análisis
ANIOS = [2021, 2022, 2023, 2024, 2025, 2026]

# Lista de nodos
NODOS = list(NODOS_COORDENADAS.keys())
