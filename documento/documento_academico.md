# DIGITAL TWIN ECONÓMICO – FESTIVAL DE LA LEYENDA VALLENATA 2026

## 59ª Edición | Valledupar, Cesar, Colombia

**Materia:** Modelos y Simulación – 6° Semestre  
**Programa:** Ingeniería de Sistemas  
**Fecha:** Mayo 2026

---

## 1. RESUMEN EJECUTIVO

El presente estudio analiza el impacto económico de la 59ª edición del Festival de la Leyenda Vallenata (2026) en Valledupar, Cesar, mediante un modelo de simulación dinámica denominado **Digital Twin Económico**. La investigación integra georreferenciación, bases de datos reales y estadística descriptiva e inferencial para evaluar el comportamiento económico de cinco nodos críticos de la ciudad durante el festival.

Los resultados principales del Festival 2026 indican:
- **222,000+ visitantes** llegaron a Valledupar
- **$230,000 millones COP** en impacto económico total
- **87% de ocupación hotelera** promedio (pico de 98%)
- **2,630+ empleos temporales** generados
- **35,475 vehículos** ingresados (+37.7% respecto a 2025)

El análisis de distribución normal reveló que la probabilidad de que el Parque de la Leyenda superara su meta de ingresos de $10,000 millones fue del **5.48% (Z = 1.60)**, indicando una meta estadísticamente ambiciosa.

En el análisis comparativo de hospedaje, **Airbnb presentó mayor volatilidad** (CV = 51.89%) frente a la hotelería tradicional (CV = 39.06%), evidenciando especulación de precios en temporada alta.

---

## 2. INTRODUCCIÓN

El Festival de la Leyenda Vallenata, declarado Patrimonio Cultural Inmaterial de la Humanidad por la UNESCO en 2015, constituye el evento cultural y económico más importante del departamento del Cesar y uno de los más relevantes de Colombia. Celebrado anualmente en Valledupar, este festival no solo preserva las tradiciones musicales del vallenato, sino que actúa como un poderoso motor de desarrollo económico regional.

La 59ª edición, celebrada hasta el 3 de mayo de 2026, presentó cifras récord según el balance oficial de la Cámara de Comercio de Valledupar, con una dinamización económica superior a los $230,000 millones de pesos (Cámara de Comercio de Valledupar, 2026).

El concepto de **Gemelo Digital (Digital Twin)** aplicado al análisis económico permite crear una réplica virtual del sistema económico del festival, integrando datos históricos reales, modelos estadísticos y visualizaciones georreferenciadas que facilitan la toma de decisiones en tiempo real.

Este proyecto desarrolla una herramienta de simulación que:
1. Visualiza un mapa interactivo de Valledupar con los 5 nodos de mayor flujo económico
2. Permite navegación cronológica por los últimos 6 años (2021-2026)
3. Calcula automáticamente estadísticas descriptivas e inferenciales
4. Proyecta la distribución normal para evaluar metas de ingresos
5. Compara la volatilidad de precios entre Airbnb y hotelería tradicional

---

## 3. MARCO TEÓRICO

### 3.1 Gemelo Digital (Digital Twin)

Un **Gemelo Digital** es una representación virtual de un sistema físico, proceso o servicio que permite simular su comportamiento en tiempo real mediante la integración de datos provenientes de sensores, modelos matemáticos y algoritmos de análisis (Grieves & Vickers, 2017). En el contexto económico, un Digital Twin permite modelar flujos de ingresos, patrones de consumo y dinámicas de mercado de un ecosistema económico como el Festival Vallenato.

Los componentes fundamentales de un gemelo digital son:
- **Espacio físico**: Los cinco nodos económicos de Valledupar
- **Espacio virtual**: El modelo computacional con datos históricos
- **Conexión de datos**: Las fuentes oficiales (SITUR, DANE, CC Valledupar)
- **Motor de simulación**: Los algoritmos estadísticos y de visualización

### 3.2 Modelado y Simulación Estocástica

La **simulación estocástica** se refiere al uso de modelos matemáticos que incorporan variables aleatorias para representar la incertidumbre inherente a los sistemas reales (Law, 2015). A diferencia de los modelos determinísticos, los modelos estocásticos reconocen que variables como el número de visitantes, los ingresos y la ocupación hotelera tienen un componente de variabilidad que debe ser modelado probabilísticamente.

En este proyecto, la estocasticidad se manifiesta en:
- La **distribución normal** aplicada a los ingresos del Parque de la Leyenda
- La **varianza** en los precios de hospedaje (Airbnb vs Hotel)
- La **volatilidad** medida a través del coeficiente de variación

### 3.3 Estadística Descriptiva

La **estadística descriptiva** comprende técnicas para resumir, organizar y presentar datos de manera informativa (Wackerly et al., 2014). Las medidas utilizadas en este proyecto son:

| Medida | Fórmula | Interpretación |
|--------|---------|----------------|
| **Media** (x̄) | x̄ = Σxᵢ / n | Promedio aritmético de los valores |
| **Mediana** (Me) | Valor central ordenado | Robusta ante valores atípicos (VIP) |
| **Moda** (Mo) | Valor más frecuente | Procedencia predominante de turistas |
| **Desviación Estándar** (σ) | √[Σ(xᵢ - x̄)² / (n-1)] | Dispersión respecto a la media |
| **Varianza** (σ²) | Σ(xᵢ - x̄)² / (n-1) | Dispersión cuadrática |
| **Rango** (R) | max(x) - min(x) | Amplitud total de los datos |
| **Coeficiente de Variación** (CV) | (σ / x̄) × 100% | Dispersión relativa (comparabilidad) |

### 3.4 Estadística Inferencial

La **estadística inferencial** permite realizar generalizaciones sobre una población a partir de una muestra, utilizando pruebas de hipótesis, intervalos de confianza y modelos probabilísticos (Montgomery & Runger, 2018).

En este proyecto, la inferencia se aplica mediante:
- **Prueba Z**: Para evaluar si los ingresos observados difieren significativamente de la meta establecida
- **Modelo de distribución normal**: Para proyectar probabilidades de alcanzar metas económicas

### 3.5 Tendencia Central y Dispersión

Las **medidas de tendencia central** (media, mediana, moda) identifican el valor representativo de un conjunto de datos. Las **medidas de dispersión** (desviación estándar, varianza, rango, CV) cuantifican la variabilidad de los datos respecto a su centro.

En el contexto del Festival Vallenato:
- La **media** de ingresos permite estimar el rendimiento económico esperado
- La **mediana** identifica sesgos causados por consumos de alto valor (VIP)
- La **moda** de procedencia revela el departamento dominante de origen turístico
- La **desviación estándar** mide la volatilidad y riesgo del empleo generado

### 3.6 Distribución Normal (Campana de Gauss)

La **distribución normal** o Gaussiana es una distribución de probabilidad continua simétrica respecto a su media, definida por dos parámetros: la media (μ) y la desviación estándar (σ). Su función de densidad de probabilidad es:

f(x) = (1 / σ√2π) × e^[-(x-μ)²/(2σ²)]

Propiedades fundamentales:
- ~68.27% de los datos caen dentro de ±1σ de la media
- ~95.45% caen dentro de ±2σ
- ~99.73% caen dentro de ±3σ

El **Z-score** estandariza un valor: Z = (X - μ) / σ

### 3.7 Sistemas GIS (Geographic Information Systems)

Los **Sistemas de Información Geográfica** integran datos espaciales con atributos temáticos para análisis georreferenciado (Longley et al., 2015). En este proyecto, se utiliza la librería **Folium** (basada en Leaflet.js) para generar mapas interactivos que vinculan las coordenadas geográficas de los nodos económicos con sus datos estadísticos.

### 3.8 ETL (Extract, Transform, Load)

El proceso **ETL** comprende tres fases (Kimball & Caserta, 2004):
1. **Extracción**: Obtención de datos de fuentes heterogéneas (SITUR, DANE, CC Valledupar, medios)
2. **Transformación**: Limpieza, normalización y cálculo de métricas derivadas
3. **Carga**: Almacenamiento estructurado en el modelo de datos Python

En este proyecto, el ETL se implementa en el módulo `data/datos_festival.py`, donde los datos extraídos de fuentes oficiales son transformados en estructuras de datos Python (diccionarios) y cargados en el sistema de simulación.

---

## 4. METODOLOGÍA

### 4.1 Diseño de la investigación
Estudio descriptivo-analítico con enfoque cuantitativo, utilizando datos secundarios de fuentes oficiales para el período 2021-2026.

### 4.2 Fuentes de datos
| Fuente | Tipo de dato | URL |
|--------|-------------|-----|
| Cámara de Comercio de Valledupar | Balances económicos del festival | ccvalledupar.org.co |
| SITUR Cesar | Estadísticas turísticas | situr.gov.co |
| DANE | Indicadores laborales y económicos | dane.gov.co |
| El Pilón | Reportajes económicos | elpilon.com.co |
| Semana | Cobertura nacional del festival | semana.com |
| Pulzo | Cifras de impacto 2026 | pulzo.com |
| La República | Análisis económico | larepublica.co |
| Alcaldía de Valledupar | Datos oficiales del municipio | valledupar-cesar.gov.co |

### 4.3 Herramientas tecnológicas
- **Python 3.11**: Lenguaje de programación principal
- **NumPy / SciPy**: Cálculos estadísticos
- **Matplotlib**: Visualizaciones estáticas
- **Folium**: Mapas interactivos georreferenciados
- **Pandas**: Manipulación y análisis de datos

### 4.4 Nodos económicos analizados
1. **Parque de la Leyenda Consuelo Araujonoguera** (10.4969°N, 73.2646°W) – Eventos masivos y boletería
2. **Plaza Alfonso López** (10.4776°N, 73.2445°W) – Centro histórico y turismo cultural
3. **Balneario Hurtado / Río Guatapurí** (10.5011°N, 73.2705°W) – Economía popular e informalidad
4. **Desfile de Piloneras / Carrera 9** (10.4796°N, 73.2492°W) – Flujo logístico y servicios
5. **Feria Ganadera** (10.4637°N, 73.2462°W) – Impacto comercial y agropecuario

---

## 5. RECOLECCIÓN DE DATOS

### 5.1 Datos del Festival por año (agregados ciudad)

| Año | Visitantes | Impacto Total (M COP) | Ocupación Hotelera | Empleos | Vehículos | Fuente |
|-----|-----------|----------------------|-------------------|---------|-----------|--------|
| 2021 | 45,000 | $35,000 | 35% | 490 | 8,000 | Estimación – Formato híbrido COVID-19 |
| 2022 | 137,672 | $120,000 | 65% | 1,300 | 45,000 | CC Valledupar / Semanario La Calle |
| 2023 | 210,000 | $180,000 | 79% | 1,860 | 90,954 | CC Valledupar – Expofestival |
| 2024 | 227,727 | $210,000 | 79% | 1,551 | 110,000 | CC Valledupar / Semana |
| 2025 | 200,000+ | $200,000 | 88-93% | 1,800 | 25,751 | CC Valledupar / RTA Noticias |
| 2026 | 222,000+ | $230,000 | 87% (pico 98%) | 2,630 | 35,475 | CC Valledupar / Pulzo / La República |

**Nota sobre 2021:** El Festival fue realizado en formato híbrido/virtual debido a las restricciones por COVID-19, lo que explica las cifras significativamente menores.

**Nota sobre 2022:** Fue la primera edición con retorno a la presencialidad masiva, marcando el inicio de la recuperación económica post-pandemia (Semanario La Calle, 2022).

### 5.2 Datos sectoriales 2026 (verificados)

Según el balance oficial de la Cámara de Comercio de Valledupar (2026):

| Sector | Ingresos (M COP) | Crecimiento vs 2025 |
|--------|------------------|-------------------|
| Espectáculos / Boletería | $23,000+ | — |
| Gastronomía | $13,000+ | +30% |
| Hotelería | $7,000+ | — |
| Economía popular (Plaza Alfonso López) | $3,100 | — |

**Procedencia de turistas 2026:** 69% nacional, 20.5% Cesar, 10% internacional (México, Chile, Ecuador, República Dominicana, EE.UU., España).

---

## 6. TABLAS CONSOLIDADAS

Las tablas consolidadas con datos detallados por nodo y año se encuentran en el archivo generado `output/tabla_resumen_estadisticas.csv`.

---

## 7. CÁLCULOS ESTADÍSTICOS

### 7.1 Ejemplo: Parque de la Leyenda – 2026

**Datos del nodo:**
- Visitantes: 95,000
- Ingresos: $9,800M COP
- Gasto promedio: $260,000 COP
- Ocupación hotelera: 87%
- Empleos temporales: 810
- Precio hospedaje: $400,000 COP
- Actividad comercial: $5,200M COP
- Impacto transporte: $1,500M COP

**Cálculos paso a paso:**

Las estadísticas se calculan sobre el vector de 8 variables numéricas del nodo.

**Fuente:** Cámara de Comercio de Valledupar – Balance 59° Festival (2026); Pulzo; Alcaldía de Valledupar.

---

## 8. DISTRIBUCIÓN NORMAL

### 8.1 Problema planteado

Si el ingreso meta para el nodo **Parque de la Leyenda** en 2026 era de **$10,000 millones COP**, y el modelo histórico arroja:
- **Media (μ) = $8,800 millones COP**
- **Desviación estándar (σ) = $750 millones COP**

### 8.2 Cálculo del Z-score

**Paso 1:** Calcular Z = (X - μ) / σ

Z = (10,000 - 8,800) / 750 = 1,200 / 750 = **1.60**

### 8.3 Cálculo de P(X > 10,000)

**Paso 2:** Consultar la tabla de distribución normal estándar

P(X > 10,000) = P(Z > 1.60) = 1 - Φ(1.60)

Φ(1.60) = 0.9452 (tabla normal)

P(X > 10,000) = 1 - 0.9452 = **0.0548 = 5.48%**

### 8.4 Interpretación económica

La probabilidad de superar la meta de $10,000 millones es del **5.48%**, lo cual es **poco probable pero no imposible**. Un Z-score de 1.60 indica que la meta está 1.60 desviaciones estándar por encima del rendimiento histórico promedio. Para alcanzar esta cifra se necesitarían condiciones excepcionales como:
- Mayor afluencia de turistas internacionales
- Programación de conciertos con artistas de alto perfil comercial
- Estrategias agresivas de captación de ingresos por boletería

---

## 9. ANÁLISIS AIRBNB VS HOTELERÍA

### 9.1 Evolución de medianas de precio (COP/noche)

| Año | Airbnb (Mediana) | Hotel (Mediana) | Rango Airbnb | Rango Hotel |
|-----|-----------------|----------------|-------------|------------|
| 2021 | $90,000 | $130,000 | $150,000 | $170,000 |
| 2022 | $150,000 | $200,000 | $370,000 | $280,000 |
| 2023 | $220,000 | $250,000 | $700,000 | $350,000 |
| 2024 | $300,000 | $300,000 | $1,080,000 | $420,000 |
| 2025 | $380,000 | $380,000 | $1,650,000 | $480,000 |
| 2026 | $450,000 | $420,000 | $2,320,000 | $550,000 |

### 9.2 Resumen estadístico

| Métrica | Airbnb | Hotel |
|---------|--------|-------|
| Media | $265,000 | $280,000 |
| Mediana Global | $260,000 | $275,000 |
| Desviación Estándar | $137,514 | $109,362 |
| **CV (%)** | **51.89%** | **39.06%** |

### 9.3 Conclusiones del análisis

- **Sector con mayor volatilidad:** Airbnb (CV = 51.89%)
- **Diferencia de volatilidad:** 12.83 puntos porcentuales
- **En 2026:** El rango de precios Airbnb ($2,320,000) fue **4.2 veces mayor** que el de hotelería ($550,000)
- **Interpretación:** Los precios en plataformas de economía colaborativa son más susceptibles a la especulación durante eventos de alta demanda como el Festival Vallenato

Fuentes: RCN Noticias, RTA Noticias, CC Valledupar.

---

## 10. VISUALIZACIONES

El sistema genera las siguientes visualizaciones (almacenadas en `output/`):

1. **Serie de tiempo de ingresos** (`serie_tiempo_ingresos.png`) – Evolución de ingresos por nodo 2021-2026
2. **Serie de tiempo de visitantes** (`serie_tiempo_visitantes.png`) – Evolución de visitantes por nodo
3. **Histograma de ingresos 2026** (`histograma_ingresos_2026.png`) – Comparación de ingresos por nodo
4. **Boxplot de ingresos** (`boxplot_ingresos.png`) – Distribución de ingresos por nodo
5. **Barras Airbnb vs Hotel** (`barras_airbnb_vs_hotel.png`) – Comparación de medianas de precios
6. **Ocupación hotelera** (`ocupacion_hotelera.png`) – Evolución de la ocupación 2021-2026
7. **Campana de Gauss** (`campana_gauss_parque_leyenda_2026.png`) – Distribución normal con área sombreada
8. **Mapa interactivo** (`mapa_interactivo_valledupar.html`) – Mapa georreferenciado de los 5 nodos

---

## 11. CÓDIGO PYTHON

El código fuente completo se encuentra organizado en la siguiente estructura:

```
Festival Vallenato/
├── main.py                         # Aplicación principal
├── requirements.txt                # Dependencias
├── data/
│   ├── __init__.py
│   └── datos_festival.py           # Datos consolidados (270 datos)
├── estadistica/
│   ├── __init__.py
│   ├── descriptiva.py              # Media, mediana, moda, σ, CV
│   ├── inferencial.py              # Z-score, distribución normal
│   └── airbnb_vs_hotel.py          # Análisis comparativo
├── visualizaciones/
│   ├── __init__.py
│   ├── graficos.py                 # Series, histogramas, boxplots
│   ├── campana_gauss.py            # Curva normal sombreada
│   └── mapa_interactivo.py         # Mapa Folium con popups
└── output/                         # Archivos generados
```

**Para ejecutar:**
```bash
pip install -r requirements.txt
python main.py
```

---

## 12. CONCLUSIONES

1. **Crecimiento sostenido:** El Festival Vallenato ha mostrado un crecimiento continuo desde la reactivación post-pandemia (2022), pasando de ~$120,000M a ~$230,000M en impacto económico total, lo que representa un crecimiento del 91.7% en 4 años.

2. **Distribución normal:** La probabilidad de que el Parque de la Leyenda supere la meta de $10,000M fue de 5.48% (Z=1.60). Esto indica que la meta fue ambiciosa pero estadísticamente improbable sin medidas extraordinarias.

3. **Volatilidad en hospedaje:** El sector Airbnb presentó mayor volatilidad (CV=51.89%) frente a la hotelería tradicional (CV=39.06%), evidenciando especulación de precios en temporada alta.

4. **Nodo dominante:** El Parque de la Leyenda es el nodo con mayor generación de ingresos ($9,800M en 2026), seguido por la Feria Ganadera ($7,500M).

5. **Recuperación post-pandemia:** El Festival demostró resiliencia económica, recuperando los niveles pre-pandemia en 2023 (~210,000 visitantes) y superándolos en 2024 (~227,727).

6. **Impacto social:** Se generaron más de 2,630 empleos temporales en 2026, beneficiando a gastronomía, logística, hotelería y transporte.

7. **Turismo internacional:** La proporción de turistas internacionales creció al 10% en 2026 (México, Chile, Ecuador, R. Dominicana, EE.UU., España).

---

## 13. REFERENCIAS (APA 7)

Cámara de Comercio de Valledupar para el Valle del Río Cesar. (2022). *Balance comercial y turístico – 55° Festival de la Leyenda Vallenata*. https://ccvalledupar.org.co

Cámara de Comercio de Valledupar para el Valle del Río Cesar. (2023). *Balance comercial y turístico – 56° Festival de la Leyenda Vallenata*. https://ccvalledupar.org.co

Cámara de Comercio de Valledupar para el Valle del Río Cesar. (2024). *Balance comercial y turístico – 57° Festival de la Leyenda Vallenata*. https://ccvalledupar.org.co

Cámara de Comercio de Valledupar para el Valle del Río Cesar. (2025). *Balance comercial y turístico – 58° Festival de la Leyenda Vallenata y ExpoFestival 2025*. https://ccvalledupar.org.co

Cámara de Comercio de Valledupar para el Valle del Río Cesar. (2026). *Balance comercial y turístico – 59° Festival de la Leyenda Vallenata*. https://ccvalledupar.org.co

Departamento Administrativo Nacional de Estadística (DANE). (2026). *Gran Encuesta Integrada de Hogares (GEIH) – Mercado laboral*. https://www.dane.gov.co

El Pilón. (2026). *Impacto económico del 59° Festival Vallenato en Valledupar*. https://elpilon.com.co

Grieves, M. & Vickers, J. (2017). Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems. En F.-J. Kahlen, S. Flumerfelt & A. Alves (Eds.), *Transdisciplinary perspectives on complex systems* (pp. 85-113). Springer.

Kimball, R. & Caserta, J. (2004). *The Data Warehouse ETL Toolkit: Practical Techniques for Extracting, Cleaning, Conforming, and Delivering Data*. Wiley.

La República. (2026). *Festival Vallenato 2026 registró más de 222,000 visitantes*. https://www.larepublica.co

Law, A. M. (2015). *Simulation Modeling and Analysis* (5th ed.). McGraw-Hill.

Longley, P. A., Goodchild, M. F., Maguire, D. J. & Rhind, D. W. (2015). *Geographic Information Systems and Science* (4th ed.). Wiley.

Montgomery, D. C. & Runger, G. C. (2018). *Applied Statistics and Probability for Engineers* (7th ed.). Wiley.

Pulzo. (2026). *Festival Vallenato 2026 dinamizó más de $230,000 millones*. https://www.pulzo.com

Semana. (2024). *Festival de la Leyenda Vallenata 2024: cifras de visitantes e impacto económico*. https://www.semana.com

Semanario La Calle. (2022). *Balance del 55° Festival de la Leyenda Vallenata*. https://www.semanariolacalle.com

Wackerly, D. D., Mendenhall III, W. & Scheaffer, R. L. (2014). *Mathematical Statistics with Applications* (7th ed.). Cengage Learning.

Alcaldía de Valledupar. (2026). *Balance del 59° Festival de la Leyenda Vallenata*. https://valledupar-cesar.gov.co
