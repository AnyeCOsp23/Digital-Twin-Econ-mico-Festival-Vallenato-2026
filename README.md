# 🪗 Digital Twin Económico - Festival de la Leyenda Vallenata

Simulación computacional interactiva y análisis de datos (2021-2026) que proyecta el impacto económico del Festival Vallenato en Valledupar, utilizando Python, estadística inferencial y Folium para su visualización.

## 🚀 Cómo ejecutar el proyecto (Instrucciones para evaluar)

Existen dos formas de visualizar y evaluar este proyecto:

### Opción 1: Visualización Rápida (Recomendada)
Dado que los resultados ya han sido procesados y exportados, puede visualizar la simulación completa sin necesidad de instalar Python. 

1. Descargue y descomprima el proyecto (o acceda a la carpeta principal).
2. Navegue hacia la carpeta llamada `output/`.
3. Haga doble clic en el archivo `mapa_interactivo_valledupar.html`.
4. El mapa interactivo se abrirá en su navegador predeterminado (Chrome, Edge, Firefox, etc.) con todas las funcionalidades, animaciones y ventanas estadísticas activas.

---

### Opción 2: Ejecutar el Código Fuente (Simulación desde Cero)
Si desea evaluar la arquitectura del software, calcular nuevamente las proyecciones y ver cómo Python construye el mapa y las gráficas en tiempo real, siga estos pasos:

**1. Requisitos Previos:**
- Tener instalado **Python 3.8** o superior en su equipo.

**2. Instalación de Dependencias:**
Abra una terminal, consola de comandos (CMD) o PowerShell en la carpeta raíz del proyecto y ejecute:
```bash
pip install -r requirements.txt
```

**3. Ejecución del Modelo Matemático:**
Una vez instaladas las librerías necesarias (Folium, Numpy, Pandas, Matplotlib, Scipy, Plotly), ejecute el archivo principal:
```bash
python main.py
```

**4. Análisis de Resultados:**
- La consola le mostrará un reporte detallado con los resultados estadísticos (Probabilidades con la Campana de Gauss, Volatilidad de Airbnb vs Hoteles, etc.).
- Todos los gráficos estadísticos y el mapa interactivo se regenerarán y guardarán automáticamente en la carpeta `output/`.
- Al finalizar, abra el archivo `output/mapa_interactivo_valledupar.html` en su navegador para explorar la interfaz.

---

## 📂 Estructura del Proyecto

- `main.py`: Punto de entrada que orquesta el análisis estadístico y la generación de componentes visuales.
- `data/`: Diccionarios de datos geográficos, financieros y de visitantes.
- `estadistica/`: Módulos de procesamiento matemático (estadística descriptiva e inferencial).
- `visualizaciones/`: Motor de renderizado web utilizando Folium con inyección de CSS/JS moderno (Glassmorphism).
- `output/`: Directorio donde el programa exporta todos los resultados (`.html`, `.csv`, `.png`).
- `documento/`: Soporte textual del análisis académico y metodología.
