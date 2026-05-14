# -*- coding: utf-8 -*-
"""
============================================================================
MAPA INTERACTIVO ENRIQUECIDO - DIGITAL TWIN FESTIVAL VALLENATO 2026
============================================================================
Genera mapa de Valledupar con popups HTML enriquecidos que incluyen:
- Fotografía real del lugar (Wikimedia Commons)
- Estadísticas descriptivas calculadas
- Indicadores con iconos y colores
- Mini barras de progreso para métricas clave
- Datos reales con fuentes citadas
============================================================================
"""

import folium
from folium.plugins import MiniMap, Fullscreen, LocateControl, HeatMap
import os
from data.datos_festival import DATOS, NODOS_COORDENADAS, ANIOS, NODOS, DATOS_AGREGADOS
from estadistica.descriptiva import calcular_estadisticas_nodo, calcular_estadisticas_serie_temporal


COLORES_FOLIUM = {
    "Parque de la Leyenda": "red",
    "Plaza Alfonso López": "blue",
    "Balneario Hurtado": "green",
    "Desfile de Piloneras": "orange",
    "Feria Ganadera": "darkred"
}

ICONOS_FOLIUM = {
    "Parque de la Leyenda": "music",
    "Plaza Alfonso López": "university",
    "Balneario Hurtado": "tint",
    "Desfile de Piloneras": "street-view",
    "Feria Ganadera": "leaf"
}

# Emojis por nodo
EMOJIS = {
    "Parque de la Leyenda": "🎵",
    "Plaza Alfonso López": "🏛️",
    "Balneario Hurtado": "🌊",
    "Desfile de Piloneras": "💃",
    "Feria Ganadera": "🐄"
}

# Colores CSS por nodo — paleta suave y amigable
COLORES_CSS = {
    "Parque de la Leyenda": "#e07065",
    "Plaza Alfonso López": "#5b9bd5",
    "Balneario Hurtado": "#43b581",
    "Desfile de Piloneras": "#e8a838",
    "Feria Ganadera": "#9b7dc9"
}

# Fondos suaves por nodo
COLORES_BG = {
    "Parque de la Leyenda": "#fdf0ef",
    "Plaza Alfonso López": "#edf4fb",
    "Balneario Hurtado": "#edf8f3",
    "Desfile de Piloneras": "#fef6e8",
    "Feria Ganadera": "#f5f0fa"
}


def _barra_progreso(valor, maximo, color="#43b581", label=""):
    """Genera HTML de una mini barra de progreso — estilo limpio."""
    pct = min(100, (valor / maximo) * 100) if maximo > 0 else 0
    return f'''
    <div style="margin:4px 0;">
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#718096;">
            <span>{label}</span><span style="color:{color}; font-weight:600;">{valor:,.0f}</span>
        </div>
        <div style="background:#edf2f7; border-radius:6px; height:7px; overflow:hidden;">
            <div style="background:{color}; width:{pct:.1f}%;
                        height:100%; border-radius:6px; transition:width 0.5s;"></div>
        </div>
    </div>'''


def _calcular_crecimiento(nodo, anio, variable="ingresos_millones"):
    """Calcula el crecimiento porcentual respecto al año anterior."""
    anio_anterior = anio - 1
    if anio_anterior not in DATOS[nodo]:
        return None  # No hay año anterior para comparar
    v_ant = DATOS[nodo][anio_anterior][variable]
    v_act = DATOS[nodo][anio][variable]
    if v_ant > 0:
        return ((v_act - v_ant) / v_ant) * 100
    return 0


def _seccion_comparacion(nodo, anio, color):
    """
    Emite un div vacío con los datos del nodo en JSON.
    El JS del mapa escucha overlayadd/overlayremove del LayerControl
    y rellena este div solo cuando hay 2+ años activos.
    """
    import json as _json
    datos_nodo = {}
    for a in ANIOS:
        d = DATOS[nodo][a]
        datos_nodo[str(a)] = {
            "visitantes":                d["visitantes"],
            "ingresos_millones":         d["ingresos_millones"],
            "gasto_promedio":            d["gasto_promedio"],
            "procedencia_moda":          d["procedencia_moda"],
            "ocupacion_hotelera":        d["ocupacion_hotelera"],
            "empleos_temporales":        d["empleos_temporales"],
            "precio_hospedaje_promedio": d["precio_hospedaje_promedio"],
        }
    data_json = _json.dumps(datos_nodo, ensure_ascii=False).replace("'", "&#39;")
    return f"""<div class="comp-container"
         data-anio="{anio}"
         data-color="{color}"
         data-datos='{data_json}'
         style="margin-top:10px; margin-bottom:8px;"></div>"""


def crear_popup_html(nodo, anio):
    """Crea popup HTML enriquecido — diseño limpio, colores suaves y amigables."""
    datos = DATOS[nodo][anio]
    est = calcular_estadisticas_nodo(nodo, anio)
    info = NODOS_COORDENADAS[nodo]
    color = COLORES_CSS[nodo]
    color_bg = COLORES_BG[nodo]
    emoji = EMOJIS[nodo]

    # Foto del lugar
    foto_url = info.get("foto", "")
    foto_html = ""
    if foto_url:
        foto_html = f'''
        <div style="width:100%; height:140px; overflow:hidden; position:relative;">
            <img src="{foto_url}" alt="{nodo}" title="Clic para expandir"
                 style="width:100%; height:140px; object-fit:cover; cursor:pointer;"
                 onclick="window.parent.postMessage({{type: 'openLightbox', url: '{foto_url}'}}, '*'); window.openLightbox && window.openLightbox('{foto_url}')"
                 onerror="this.style.display='none'"/>
        </div>'''

    # Crecimiento (respecto al año anterior)
    crec_ingresos = _calcular_crecimiento(nodo, anio, "ingresos_millones")
    crec_visitantes = _calcular_crecimiento(nodo, anio, "visitantes")
    anio_anterior = anio - 1
    tiene_comparacion = crec_ingresos is not None
    crec_color_i = "#43b581" if (crec_ingresos or 0) >= 0 else "#e07065"
    crec_color_v = "#43b581" if (crec_visitantes or 0) >= 0 else "#e07065"
    crec_arrow_i = "▲" if (crec_ingresos or 0) >= 0 else "▼"
    crec_arrow_v = "▲" if (crec_visitantes or 0) >= 0 else "▼"

    # Serie temporal para mini sparkline
    ingresos_serie = [DATOS[nodo][a]["ingresos_millones"] for a in ANIOS]
    max_ingreso = max(ingresos_serie) if ingresos_serie else 1

    # Barras de serie temporal
    sparkline_html = '<div style="display:flex; align-items:flex-end; gap:3px; height:32px; margin:6px 0;">'
    for i, (a, v) in enumerate(zip(ANIOS, ingresos_serie)):
        h = max(3, (v / max_ingreso) * 28)
        bar_color = color if a == anio else f"{color}40"
        border = f"border:1px solid {color};" if a == anio else ""
        sparkline_html += f'<div title="{a}: ${v:,}M" style="flex:1; height:{h}px; background:{bar_color}; border-radius:3px; {border}"></div>'
    sparkline_html += '</div>'
    sparkline_html += '<div style="display:flex; justify-content:space-between; font-size:9px; color:#a0aec0;"><span>2021</span><span>2026</span></div>'

    # Estadísticas de serie temporal
    st = calcular_estadisticas_serie_temporal(nodo, "ingresos_millones")

    html = f"""
    <div style="width:460px; font-family:'Segoe UI',Arial,sans-serif;
                background:#ffffff; color:#2d3748; border-radius:16px; padding:0; overflow:hidden;
                box-shadow:0 4px 20px rgba(0,0,0,0.10); border:1px solid #e2e8f0;">

        <div style="background:{color}; padding:12px 16px; color:white;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:24px; filter:drop-shadow(0 1px 2px rgba(0,0,0,0.15));">{emoji}</span>
                <div>
                    <h3 style="margin:0; font-size:15px; font-weight:700; line-height:1.2; color:#fff;">
                        {nodo}
                    </h3>
                    <p style="margin:2px 0 0; font-size:10px; opacity:0.9;">
                        {info['descripcion']}
                    </p>
                </div>
            </div>
        </div>

        {foto_html}

        <div style="padding:14px 16px 16px;">

        <div style="display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap;">
            <span style="background:{color_bg}; color:{color}; padding:3px 10px;
                         border-radius:20px; font-size:10px; font-weight:600;
                         border:1px solid {color}33;">
                📅 {anio}
            </span>
            <span style="background:#edf8f3; color:#43b581; padding:3px 10px;
                         border-radius:20px; font-size:10px; font-weight:600;
                         border:1px solid #43b58133;">
                📍 {info.get('direccion', '')}
            </span>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">
            <div style="background:#f8fafb; padding:10px; border-radius:10px; text-align:center;
                        border:1px solid #e2e8f0;">
                <div style="font-size:10px; color:#a0aec0; font-weight:500;">👥 Visitantes</div>
                <div style="font-size:18px; font-weight:700; color:#43b581; margin:2px 0;">
                    {datos['visitantes']:,}
                </div>
                {'<div style="font-size:9px; color:' + crec_color_v + '; font-weight:600;">' + crec_arrow_v + ' ' + f'{abs(crec_visitantes):.1f}' + '% vs ' + str(anio_anterior) + '</div>' if tiene_comparacion else '<div style="font-size:9px; color:#a0aec0; font-weight:500;">— Año base</div>'}
            </div>
            <div style="background:#f8fafb; padding:10px; border-radius:10px; text-align:center;
                        border:1px solid #e2e8f0;">
                <div style="font-size:10px; color:#a0aec0; font-weight:500;">💰 Ingresos</div>
                <div style="font-size:18px; font-weight:700; color:{color}; margin:2px 0;">
                    ${datos['ingresos_millones']:,}M
                </div>
                {'<div style="font-size:9px; color:' + crec_color_i + '; font-weight:600;">' + crec_arrow_i + ' ' + f'{abs(crec_ingresos):.1f}' + '% vs ' + str(anio_anterior) + '</div>' if tiene_comparacion else '<div style="font-size:9px; color:#a0aec0; font-weight:500;">— Año base</div>'}
            </div>
        </div>

        <table style="width:100%; border-collapse:collapse; font-size:11px; margin-bottom:10px;">
            <tr style="background:#f8fafb;">
                <td style="padding:6px 10px; border-bottom:1px solid #edf2f7; color:#718096;">
                    🛒 Gasto Promedio</td>
                <td style="padding:6px 8px; border-bottom:1px solid #edf2f7;
                    text-align:right; font-weight:600; color:#e8a838;">
                    ${datos['gasto_promedio']:,}</td>
            </tr>
            <tr>
                <td style="padding:6px 10px; border-bottom:1px solid #edf2f7; color:#718096;">
                    🏨 Ocupación Hotelera</td>
                <td style="padding:6px 8px; border-bottom:1px solid #edf2f7;
                    text-align:right; font-weight:600; color:#2d3748;">
                    {datos['ocupacion_hotelera']}%</td>
            </tr>
            <tr style="background:#f8fafb;">
                <td style="padding:6px 10px; border-bottom:1px solid #edf2f7; color:#718096;">
                    👷 Empleos Temporales</td>
                <td style="padding:6px 8px; border-bottom:1px solid #edf2f7;
                    text-align:right; font-weight:600; color:#5b9bd5;">
                    {datos['empleos_temporales']}</td>
            </tr>
            <tr>
                <td style="padding:6px 10px; border-bottom:1px solid #edf2f7; color:#718096;">
                    🌎 Procedencia (Moda)</td>
                <td style="padding:6px 8px; border-bottom:1px solid #edf2f7;
                    text-align:right; font-weight:600; color:#2d3748;">{datos['procedencia_moda']}</td>
            </tr>
            <tr style="background:#f8fafb;">
                <td style="padding:6px 10px; border-bottom:1px solid #edf2f7; color:#718096;">
                    💵 Precio Hospedaje</td>
                <td style="padding:6px 8px; border-bottom:1px solid #edf2f7;
                    text-align:right; font-weight:600; color:#2d3748;">${datos['precio_hospedaje_promedio']:,}/noche</td>
            </tr>
        </table>

        <div style="background:#f8fafb; border-radius:10px; padding:10px; margin-bottom:10px;
                    border:1px solid #e2e8f0;">
            <div style="font-size:10px; color:{color}; font-weight:600; margin-bottom:4px;">
                📊 Evolución Ingresos 2021-2026
            </div>
            {sparkline_html}
        </div>

        <div style="background:#f8fafb; border-radius:10px; padding:10px; margin-bottom:8px;
                    border:1px solid #e2e8f0;">
            <div style="font-size:10px; color:#e07065; font-weight:600; margin-bottom:6px;">
                📈 Estadísticas Descriptivas (Rúbrica)
            </div>
            <div style="font-size:10px; color:#4a5568; line-height:1.8;">
                <div style="display:flex; justify-content:space-between; padding:2px 4px; background:#fef6e8; border-radius:4px; margin-bottom:2px;">
                    <span>📊 <b>Media</b> (ingreso/visitante):</span>
                    <b style="color:#e8a838;">${est['media']:,.0f} COP</b>
                </div>
                <div style="display:flex; justify-content:space-between; padding:2px 4px; background:#edf4fb; border-radius:4px; margin-bottom:2px;">
                    <span>📐 <b>Mediana</b> (sesgo VIP):</span>
                    <b style="color:#5b9bd5;">${est['mediana']:,.0f} COP</b>
                </div>
                <div style="display:flex; justify-content:space-between; padding:2px 4px; background:#edf8f3; border-radius:4px; margin-bottom:2px;">
                    <span>🌎 <b>Moda</b> (procedencia):</span>
                    <b style="color:#43b581;">{est['moda_procedencia']}</b>
                </div>
                <div style="display:flex; justify-content:space-between; padding:2px 4px; background:#fdf0ef; border-radius:4px; margin-bottom:2px;">
                    <span>📉 <b>Desv. Std</b> (σ empleo):</span>
                    <b style="color:#e07065;">{est['desviacion_std']:,.1f} empleos</b>
                </div>
                <div style="display:flex; justify-content:space-between; padding:2px 4px; background:#f5f0fa; border-radius:4px;">
                    <span>⚡ <b>CV empleo</b> (riesgo):</span>
                    <b style="color:#9b7dc9;">{est['coeficiente_variacion']:.1f}%</b>
                </div>
            </div>
            <div style="margin-top:6px; font-size:9px; color:#718096; line-height:1.4; border-top:1px solid #e2e8f0; padding-top:4px;">
                Media = Ingresos÷Visitantes · Mediana sobre gastos per cápita · σ sobre empleos 2021-2026
            </div>
            <div style="margin-top:4px; font-size:10px; color:#4a5568;">
                Crecimiento anual prom: <b style="color:#43b581;">{st['tasa_crecimiento_anual']:.1f}%</b>
            </div>
        </div>

        {_barra_progreso(datos['visitantes'], 170000, "#43b581", "Visitantes (vs Plaza máx)")}
        {_barra_progreso(datos['ingresos_millones'], 10000, "#e8a838", "Ingresos (vs $10,000M meta)")}
        {_barra_progreso(datos['ocupacion_hotelera'], 100, "#5b9bd5", "Ocupación hotelera (%)")}

        {_seccion_comparacion(nodo, anio, color)}

        <p style="margin:8px 0 0; font-size:8px; color:#a0aec0; font-style:italic; line-height:1.3;">
            📌 {datos['fuente']}<br>
            🗺️ Coords: {info['lat']:.6f}°N, {abs(info['lon']):.6f}°W
        </p>

        </div>
    </div>
    """
    return html


def generar_mapa_interactivo(output_dir="output"):
    """Genera mapa interactivo premium de Valledupar con los 5 nodos."""

    # Centro de Valledupar (ajustado para que todos los nodos se vean)
    centro_lat = 10.4830
    centro_lon = -73.2560

    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=14,
        tiles=None,
        control_scale=True
    )

    # Capas base
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; CartoDB',
        name='🌙 Mapa Oscuro',
        control=True
    ).add_to(mapa)

    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; OpenStreetMap',
        name='🗺️ Mapa Estándar',
        control=True
    ).add_to(mapa)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='&copy; Esri',
        name='🛰️ Satélite',
        control=True
    ).add_to(mapa)

    # Título
    titulo_html = """
    <div style="position:fixed; top:10px; left:50%; transform:translateX(-50%);
                z-index:9999; background:rgba(255,255,255,0.95);
                padding:14px 30px; border-radius:14px; border:1px solid #e2e8f0;
                box-shadow:0 4px 20px rgba(0,0,0,0.10); backdrop-filter:blur(8px);">
        <h3 style="margin:0; color:#2d3748; font-family:'Segoe UI',sans-serif;
                   font-size:17px; text-align:center; letter-spacing:0.3px;">
            🎵 Digital Twin Económico – Festival Vallenato 2026
        </h3>
        <p style="margin:4px 0 0; color:#718096; font-size:11px; text-align:center;">
            59ª Edición | Haga clic en cada nodo para ver datos reales |
            Seleccione el año en ➡️
        </p>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(titulo_html))

    # FeatureGroup por año
    for anio in ANIOS:
        grupo = folium.FeatureGroup(name=f"📅 Año {anio}", show=(anio == 2026))

        for nodo in NODOS:
            coord = NODOS_COORDENADAS[nodo]
            datos = DATOS[nodo][anio]

            radio = max(10, min(30, datos["ingresos_millones"] / 400))

            popup_html = crear_popup_html(nodo, anio)
            popup = folium.Popup(popup_html, max_width=480)

            tooltip = (f"{EMOJIS[nodo]} {nodo} ({anio})\n"
                       f"💰 ${datos['ingresos_millones']:,}M COP\n"
                       f"👥 {datos['visitantes']:,} visitantes")

            folium.Marker(
                location=[coord["lat"], coord["lon"]],
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(
                    color=COLORES_FOLIUM[nodo],
                    icon=ICONOS_FOLIUM[nodo],
                    prefix='fa'
                )
            ).add_to(grupo)

            folium.CircleMarker(
                location=[coord["lat"], coord["lon"]],
                radius=radio,
                color=COLORES_CSS[nodo],
                fill=True,
                fill_color=COLORES_CSS[nodo],
                fill_opacity=0.25,
                weight=2,
                opacity=0.6
            ).add_to(grupo)

        grupo.add_to(mapa)

    import random

    # Mapa de calor de visitantes (basado estrictamente en datos reales de visitantes)
    for anio in ANIOS:
        heat_data = []
        
        for n in NODOS:
            base_lat = NODOS_COORDENADAS[n]["lat"]
            base_lon = NODOS_COORDENADAS[n]["lon"]
            visitantes = DATOS[n][anio]["visitantes"]
            
            # Cada punto representa proporcionalmente una cantidad real de personas.
            # Disminuimos la escala a 100 para generar el doble de puntos y que se vea más tupido.
            escala = 100
            num_puntos = int(visitantes / escala)
            
            for i in range(num_puntos):
                # Mayor población concentrada en el núcleo directo para evitar dispersión en zonas no lógicas (como montañas o río)
                es_nucleo = (i < num_puntos * 0.85)
                # Reducimos drásticamente la desviación estándar para que no se alejen tanto
                std_dev = 0.0002 if es_nucleo else 0.0008
                
                dlat = random.gauss(0, std_dev)
                dlon = random.gauss(0, std_dev)
                
                # El peso es directamente proporcional a la escala para representar los visitantes exactos.
                heat_data.append([base_lat + dlat, base_lon + dlon, escala])
        
        HeatMap(
            heat_data,
            name=f"🔥 Mapa de Calor ({anio})",
            radius=15,
            blur=10,
            max_zoom=14,
            min_opacity=0.3,
            gradient={0.1: 'blue', 0.3: 'cyan', 0.5: 'lime', 0.7: 'yellow', 1.0: 'red'},
            show=False
        ).add_to(mapa)

    # Controles
    folium.LayerControl(collapsed=False).add_to(mapa)

    # Minimapa
    MiniMap(tile_layer=folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CartoDB'
    ), toggle_display=True, position='bottomright').add_to(mapa)

    # Pantalla completa
    Fullscreen(position='topright').add_to(mapa)

    # Leyenda + Navegador de nodos interactivo
    total_2026 = DATOS_AGREGADOS[2026]

    # Generar coordenadas JS para fly-to
    nodos_js_data = ""
    for nodo in NODOS:
        coord = NODOS_COORDENADAS[nodo]
        nodos_js_data += f'  "{nodo}": {{lat: {coord["lat"]}, lon: {coord["lon"]}}},\n'

    leyenda_html = f"""
    <div id="nodoNavigator" style="position:fixed; bottom:30px; left:10px; z-index:9999;
                background:rgba(255,255,255,0.95); backdrop-filter:blur(8px);
                padding:14px 16px; border-radius:14px; border:1px solid #e2e8f0;
                font-family:'Segoe UI',sans-serif; color:#2d3748; font-size:11px;
                box-shadow:0 4px 16px rgba(0,0,0,0.08); max-width:220px;">
        <div style="color:#43b581; font-weight:700; font-size:12px; margin-bottom:8px;
                    border-bottom:1px solid #e2e8f0; padding-bottom:6px;">
            📌 Ir a Nodo Económico
        </div>
        <div class="nodo-btn" onclick="flyToNodo('Parque de la Leyenda')" style="margin-bottom:4px; padding:5px 8px; border-radius:8px; cursor:pointer; transition:background 0.2s; display:flex; align-items:center; gap:6px;"
             onmouseover="this.style.background='#fdf0ef'" onmouseout="this.style.background='transparent'">
            <span style="color:#e07065; font-size:14px;">●</span> <span>🎵 Parque de la Leyenda</span>
        </div>
        <div class="nodo-btn" onclick="flyToNodo('Plaza Alfonso López')" style="margin-bottom:4px; padding:5px 8px; border-radius:8px; cursor:pointer; transition:background 0.2s; display:flex; align-items:center; gap:6px;"
             onmouseover="this.style.background='#edf4fb'" onmouseout="this.style.background='transparent'">
            <span style="color:#5b9bd5; font-size:14px;">●</span> <span>🏛️ Plaza Alfonso López</span>
        </div>
        <div class="nodo-btn" onclick="flyToNodo('Balneario Hurtado')" style="margin-bottom:4px; padding:5px 8px; border-radius:8px; cursor:pointer; transition:background 0.2s; display:flex; align-items:center; gap:6px;"
             onmouseover="this.style.background='#edf8f3'" onmouseout="this.style.background='transparent'">
            <span style="color:#43b581; font-size:14px;">●</span> <span>🌊 Balneario Hurtado</span>
        </div>
        <div class="nodo-btn" onclick="flyToNodo('Desfile de Piloneras')" style="margin-bottom:4px; padding:5px 8px; border-radius:8px; cursor:pointer; transition:background 0.2s; display:flex; align-items:center; gap:6px;"
             onmouseover="this.style.background='#fef6e8'" onmouseout="this.style.background='transparent'">
            <span style="color:#e8a838; font-size:14px;">●</span> <span>💃 Desfile de Piloneras</span>
        </div>
        <div class="nodo-btn" onclick="flyToNodo('Feria Ganadera')" style="margin-bottom:4px; padding:5px 8px; border-radius:8px; cursor:pointer; transition:background 0.2s; display:flex; align-items:center; gap:6px;"
             onmouseover="this.style.background='#f5f0fa'" onmouseout="this.style.background='transparent'">
            <span style="color:#9b7dc9; font-size:14px;">●</span> <span>🐄 Feria Ganadera</span>
        </div>
        <div style="border-top:1px solid #e2e8f0; padding-top:6px; margin-top:4px; font-size:10px; color:#718096;">
            <div style="font-weight:600;">Festival 2026:</div>
            <div style="color:#e8a838;">💰 ${total_2026['impacto_total_millones']:,}M COP</div>
            <div style="color:#43b581;">👥 {total_2026['visitantes_total']:,} visitantes</div>
            <div style="color:#5b9bd5;">🏨 {total_2026['ocupacion_hotelera_prom']}% ocupación</div>
        </div>
        <div style="margin-top:6px; font-size:8px; color:#a0aec0;">
            Fuente: CC Valledupar, SITUR, DANE
        </div>
    </div>
    <script>
    var nodosCoords = {{
{nodos_js_data}    }};
    function flyToNodo(nombre) {{
        var c = nodosCoords[nombre];
        if (!c) return;
        // Access the Leaflet map instance
        var mapEl = document.querySelector('.folium-map');
        if (!mapEl) return;
        var mapId = mapEl.id;
        var mapObj = window[mapId];
        if (!mapObj) return;
        mapObj.flyTo([c.lat, c.lon], 16, {{duration: 1.2}});
        // Try to open the marker popup after flying
        setTimeout(function() {{
            mapObj.eachLayer(function(layer) {{
                if (layer.getLatLng) {{
                    var ll = layer.getLatLng();
                    if (Math.abs(ll.lat - c.lat) < 0.0005 && Math.abs(ll.lng - c.lon) < 0.0005) {{
                        if (layer.getPopup && layer.getPopup()) {{
                            layer.openPopup();
                        }}
                    }}
                }}
            }});
        }}, 1300);
    }}
    // Move navigator and buttons inside map container for fullscreen support
    (function() {{
        function moveToMap() {{
            var mapEl = document.querySelector('.folium-map');
            if (!mapEl) {{ setTimeout(moveToMap, 200); return; }}
            var nav = document.getElementById('nodoNavigator');
            var btnA = document.getElementById('btnAirbnb');
            var btnG = document.getElementById('btnGauss');
            var panelA = document.getElementById('panelAirbnb');
            var panelG = document.getElementById('panelGauss');
            [nav, btnA, btnG, panelA, panelG].forEach(function(el) {{
                if (el) {{
                    mapEl.appendChild(el);
                    el.style.position = 'absolute';
                    L.DomEvent.disableScrollPropagation(el);
                    L.DomEvent.disableClickPropagation(el);
                }}
            }});
        }}
        if (document.readyState === 'complete') moveToMap();
        else window.addEventListener('load', moveToMap);
    }})();

    // ── Comparación multi-año: escucha los checkboxes del LayerControl ────────
    (function() {{
        var YEAR_PAL = {{
            "2021": "#718096", "2022": "#5b9bd5", "2023": "#43b581",
            "2024": "#e8a838", "2025": "#e07065", "2026": "#9b7dc9"
        }};
        // 2026 está activo por defecto (show=True en Python)
        var activeYears = ["2026"];

        function yearFromName(name) {{
            var m = (name || '').match(/(\d{{4}})/);
            return m ? m[1] : null;
        }}

        function renderComparacion(container) {{
            var anioPropio = container.getAttribute('data-anio');
            var color      = container.getAttribute('data-color');
            var datos      = JSON.parse(container.getAttribute('data-datos').replace(/&#39;/g, "'"));

            // Ocultar si hay menos de 2 años activos o si este año no está activo
            if (activeYears.length < 2 || activeYears.indexOf(anioPropio) === -1) {{
                container.innerHTML = '';
                return;
            }}

            var anos = activeYears.slice().sort();

            function fmtN(n)   {{ return n.toLocaleString('es-CO'); }}
            function fmtM(n)   {{ return '$' + n.toLocaleString('es-CO') + 'M'; }}
            function fmtCOP(n) {{ return '$' + n.toLocaleString('es-CO'); }}
            function fmtPct(n) {{ return n + '%'; }}

            function barraMetrica(clave, label, fmt, maxOv) {{
                var vals = {{}};
                anos.forEach(function(a) {{ vals[a] = datos[a][clave]; }});
                var mv = maxOv || Math.max.apply(null, anos.map(function(a){{return vals[a];}}) ) || 1;
                var h = '<div style="margin-bottom:9px;">';
                h += '<div style="font-size:10px;font-weight:600;color:#4a5568;margin-bottom:4px;">' + label + '</div>';
                anos.forEach(function(a) {{
                    var v   = vals[a];
                    var pct = Math.min(100, (v / mv) * 100).toFixed(1);
                    var ac  = YEAR_PAL[a] || '#718096';
                    var esA = (a === anioPropio);
                    var bgRow = esA ? ac + '18' : 'transparent';
                    var bL  = esA ? 'border-left:3px solid ' + ac + ';' : 'border-left:3px solid transparent;';
                    var fw  = esA ? '700' : '500';
                    var extra = '';
                    if (esA) {{
                        extra = '<span style="font-size:8px;color:' + ac + ';font-weight:700;white-space:nowrap;">◀ activo</span>';
                    }} else {{
                        var v0 = datos[anioPropio][clave];
                        if (v0 > 0) {{
                            var d  = ((v - v0) / v0 * 100).toFixed(1);
                            var ar = d > 0 ? '▲' : '▼';
                            var dc = d > 0 ? '#43b581' : '#e07065';
                            extra = '<span style="font-size:8px;color:' + dc + ';width:38px;text-align:right;display:inline-block;">' + ar + Math.abs(d) + '%</span>';
                        }}
                    }}
                    h += '<div style="display:flex;align-items:center;gap:5px;margin-bottom:2px;'
                       + 'background:' + bgRow + ';border-radius:4px;padding:2px 3px;' + bL + '">'
                       + '<span style="font-size:9px;font-weight:' + fw + ';color:' + ac + ';width:30px;">' + a + '</span>'
                       + '<div style="flex:1;background:#edf2f7;border-radius:4px;height:8px;overflow:hidden;">'
                       + '<div style="width:' + pct + '%;height:100%;background:' + ac + ';border-radius:4px;"></div>'
                       + '</div>'
                       + '<span style="font-size:9px;font-weight:' + fw + ';color:#2d3748;width:68px;text-align:right;">' + fmt(v) + '</span>'
                       + extra + '</div>';
                }});
                h += '</div>';
                return h;
            }}

            function procedencia() {{
                var h = '<div style="margin-bottom:8px;">';
                h += '<div style="font-size:10px;font-weight:600;color:#4a5568;margin-bottom:4px;">🌎 Procedencia dominante</div>';
                h += '<div style="display:flex;flex-wrap:wrap;gap:4px;">';
                var hayCambio = false;
                var prev = null;
                anos.forEach(function(a) {{
                    var proc = datos[a].procedencia_moda;
                    var ac   = YEAR_PAL[a] || '#718096';
                    var esA  = (a === anioPropio);
                    var cambio = (prev !== null && proc !== prev);
                    if (cambio) hayCambio = true;
                    var bg  = esA ? ac : ac + '22';
                    var fc  = esA ? '#fff' : ac;
                    var brd = esA ? '2px solid ' + ac : '1px solid ' + ac + '55';
                    h += '<span style="font-size:9px;font-weight:' + (esA?'700':'600') + ';'
                       + 'background:' + bg + ';color:' + fc + ';'
                       + 'padding:2px 8px;border-radius:10px;border:' + brd + ';">'
                       + a + ': ' + (cambio ? '⚠️ ' : '') + proc + '</span>';
                    prev = proc;
                }});
                h += '</div>';
                if (hayCambio) h += '<div style="font-size:8px;color:#e8a838;margin-top:2px;">⚠️ Cambio de procedencia dominante entre años seleccionados</div>';
                h += '</div>';
                return h;
            }}

            var titulo = '🔀 Comparando: ' + anos.join(' · ');
            var out = '<div style="background:#f8fafb;border-radius:10px;padding:12px;border:1px solid #e2e8f0;">'
                    + '<div style="font-size:11px;color:' + color + ';font-weight:700;'
                    + 'margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">'
                    + titulo + '</div>'
                    + barraMetrica('visitantes',            '👥 Visitantes',             fmtN)
                    + barraMetrica('ingresos_millones',     '💰 Ingresos (M COP)',       fmtM)
                    + barraMetrica('gasto_promedio',        '🛒 Gasto promedio (COP)',   fmtCOP)
                    + barraMetrica('empleos_temporales',    '👷 Empleos temporales',     fmtN)
                    + barraMetrica('ocupacion_hotelera',    '🏨 Ocupación hotelera',     fmtPct, 100)
                    + barraMetrica('precio_hospedaje_promedio', '💵 Precio hospedaje/noche', fmtCOP)
                    + procedencia()
                    + '</div>';
            container.innerHTML = out;
        }}

        function refreshAll() {{
            document.querySelectorAll('.comp-container').forEach(renderComparacion);
        }}

        function initListeners() {{
            var mapEl = document.querySelector('.folium-map');
            if (!mapEl) {{ setTimeout(initListeners, 300); return; }}
            var mapObj = window[mapEl.id];
            if (!mapObj) {{ setTimeout(initListeners, 300); return; }}

            mapObj.on('overlayadd', function(e) {{
                var y = yearFromName(e.name);
                if (y && activeYears.indexOf(y) === -1) activeYears.push(y);
                refreshAll();
            }});
            mapObj.on('overlayremove', function(e) {{
                var y = yearFromName(e.name);
                if (y) activeYears = activeYears.filter(function(x) {{ return x !== y; }});
                refreshAll();
            }});
            // Refrescar cuando se abre un popup (los containers se crean al abrir)
            mapObj.on('popupopen', function() {{ setTimeout(refreshAll, 60); }});
        }}

        if (document.readyState === 'complete') initListeners();
        else window.addEventListener('load', initListeners);
    }})();
    </script>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda_html))

    # Guardar
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "mapa_interactivo_valledupar.html")

    # Inject Lightbox HTML and JS
    lightbox_html = """
    <div id="lightboxModal" style="display:none; position:fixed; z-index:99999; left:0; top:0; width:100%; height:100%; background-color:rgba(0,0,0,0.85); backdrop-filter:blur(5px); justify-content:center; align-items:center; cursor:pointer;" onclick="this.style.display='none'">
        <span style="position:absolute; top:20px; right:30px; color:#fff; font-size:40px; font-weight:bold; cursor:pointer;">&times;</span>
        <img id="lightboxImg" src="" style="max-width:90%; max-height:90%; border-radius:8px; box-shadow:0 0 30px rgba(0,0,0,0.5);">
    </div>
    <script>
        function openLightbox(url) {
            document.getElementById('lightboxImg').src = url;
            document.getElementById('lightboxModal').style.display = 'flex';
        }
        window.openLightbox = openLightbox;
        // Listen to messages from iframe if popup is wrapped
        window.addEventListener('message', function(e) {
            if (e.data && e.data.type === 'openLightbox') {
                openLightbox(e.data.url);
            }
        });
    </script>
    """
    mapa.get_root().html.add_child(folium.Element(lightbox_html))

    # ── PUNTO EXTRA: Panel Airbnb vs Hotel integrado al mapa ──
    from estadistica.airbnb_vs_hotel import analizar_airbnb_vs_hotel
    resultado_ab = analizar_airbnb_vs_hotel()
    stats_a = resultado_ab['estadisticas']['airbnb']
    stats_h = resultado_ab['estadisticas']['hotel']
    sector_v = resultado_ab['sector_mas_volatil']
    dif_cv = abs(stats_a['cv_porcentaje'] - stats_h['cv_porcentaje'])

    # Generar tabla de rangos 2026
    d26 = resultado_ab['datos_2026']
    rango_a = d26['airbnb_max'] - d26['airbnb_min']
    rango_h = d26['hotel_max'] - d26['hotel_min']

    panel_airbnb_html = f'''
    <div id="btnAirbnb" onclick="openAirbnbPanel()"
         style="position:fixed; top:240px; left:10px; z-index:9998;
                background:#e07065; color:white;
                padding:8px 16px; border-radius:20px; cursor:pointer;
                font-family:'Segoe UI',sans-serif; font-size:11px; font-weight:600;
                box-shadow:0 3px 10px rgba(224,112,101,0.3); border:none;">
        ⭐ Airbnb vs Hotel
    </div>
    <style>
        @keyframes pulseBtn {{
            0%,100% {{ transform:scale(1); box-shadow:0 4px 12px rgba(224,112,101,0.35); }}
            50% {{ transform:scale(1.03); box-shadow:0 6px 18px rgba(224,112,101,0.5); }}
        }}
        @keyframes slideInRight {{
            from {{ transform:translateX(100%); opacity:0; }}
            to {{ transform:translateX(0); opacity:1; }}
        }}
        @keyframes fadeInUp {{
            from {{ transform:translateY(20px); opacity:0; }}
            to {{ transform:translateY(0); opacity:1; }}
        }}
        @keyframes growBar {{
            from {{ width:0%; }}
        }}
        @keyframes scaleIn {{
            from {{ transform:scale(0.7); opacity:0; }}
            to {{ transform:scale(1); opacity:1; }}
        }}
        #panelAirbnb::-webkit-scrollbar {{ width:6px; }}
        #panelAirbnb::-webkit-scrollbar-track {{ background:#f8fafb; }}
        #panelAirbnb::-webkit-scrollbar-thumb {{ background:#cbd5e0; border-radius:3px; }}
        .ab-section {{ opacity:0; transform:translateY(20px); }}
        .ab-section.visible {{ animation:fadeInUp 0.6s ease forwards; }}
        .ab-bar-fill {{ animation:growBar 1s ease forwards; }}
        .ab-stat-card {{ animation:scaleIn 0.5s ease forwards; }}
    </style>
    <div id="panelAirbnb" style="display:none; position:fixed; top:0; right:0; z-index:99998;
                width:420px; height:100vh; background:#ffffff;
                flex-direction:column; overflow-y:auto;
                box-shadow:-4px 0 24px rgba(0,0,0,0.10); border-left:1px solid #e2e8f0;
                font-family:'Segoe UI',Arial,sans-serif;">
        <div style="padding:16px 20px; background:#fdf0ef;
                    border-bottom:1px solid #e2e8f0; position:sticky; top:0; z-index:1;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0; color:#e07065; font-size:15px;">⭐ Airbnb vs Hotel</h2>
                    <p style="margin:2px 0 0; color:#718096; font-size:10px;">Análisis Airbnb vs Hotelería Tradicional</p>
                </div>
                <span onclick="closeAirbnbPanel()" style="color:#e07065; font-size:24px; cursor:pointer; padding:4px 8px; line-height:1;">&times;</span>
            </div>
        </div>
        <div style="padding:16px 20px;">
            <div class="ab-section" data-delay="100" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 12px; color:#2d3748; font-size:13px;">📈 1. Desviación Estándar (σ) – ¿Cuál tiene más "ruido"?</h3>
                <div style="display:flex; gap:10px;">
                    <div style="flex:1; background:#fdf0ef; border:1px solid #e0706544; border-radius:10px; padding:12px; text-align:center;">
                        <div style="font-size:10px; color:#e07065; font-weight:600;">🏠 AIRBNB</div>
                        <div style="font-size:22px; font-weight:700; color:#e07065; margin:4px 0;">σ = ${stats_a['desviacion_std']:,.0f}</div>
                        <div style="font-size:10px; color:#718096;">Mayor dispersión</div>
                    </div>
                    <div style="flex:1; background:#edf8f3; border:1px solid #43b58144; border-radius:10px; padding:12px; text-align:center;">
                        <div style="font-size:10px; color:#43b581; font-weight:600;">🏨 HOTEL</div>
                        <div style="font-size:22px; font-weight:700; color:#43b581; margin:4px 0;">σ = ${stats_h['desviacion_std']:,.0f}</div>
                        <div style="font-size:10px; color:#718096;">Menor dispersión</div>
                    </div>
                </div>
                <div style="text-align:center; margin-top:8px; font-size:11px; color:#e8a838;">⚠️ Airbnb tiene σ más alta → MÁS RUIDO en precios</div>
            </div>
            <div class="ab-section" data-delay="300" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">💰 2. Rango de Precios Festival 2026</h3>
                <table style="width:100%; border-collapse:collapse; font-size:11px; color:#2d3748;">
                    <tr style="background:#edf2f7;"><th style="padding:6px 8px; text-align:left; border-bottom:1px solid #e2e8f0; color:#718096;">Métrica</th><th style="padding:6px; text-align:right; color:#e07065; border-bottom:1px solid #e2e8f0;">Airbnb</th><th style="padding:6px; text-align:right; color:#43b581; border-bottom:1px solid #e2e8f0;">Hotel</th></tr>
                    <tr><td style="padding:5px 8px; border-bottom:1px solid #edf2f7;">Precio Mínimo</td><td style="padding:5px; text-align:right; border-bottom:1px solid #edf2f7;">${d26['airbnb_min']:,}</td><td style="padding:5px; text-align:right; border-bottom:1px solid #edf2f7;">${d26['hotel_min']:,}</td></tr>
                    <tr style="background:#f8fafb;"><td style="padding:5px 8px; border-bottom:1px solid #edf2f7;">Precio Máximo</td><td style="padding:5px; text-align:right; border-bottom:1px solid #edf2f7;">${d26['airbnb_max']:,}</td><td style="padding:5px; text-align:right; border-bottom:1px solid #edf2f7;">${d26['hotel_max']:,}</td></tr>
                    <tr><td style="padding:5px 8px; border-bottom:1px solid #edf2f7;">Mediana</td><td style="padding:5px; text-align:right; font-weight:600; color:#e07065; border-bottom:1px solid #edf2f7;">${d26['airbnb_mediana']:,}</td><td style="padding:5px; text-align:right; font-weight:600; color:#43b581; border-bottom:1px solid #edf2f7;">${d26['hotel_mediana']:,}</td></tr>
                    <tr style="background:#fdf0ef;"><td style="padding:5px 8px; font-weight:600;">RANGO (Max-Min)</td><td style="padding:5px; text-align:right; font-weight:600; color:#e07065;">${rango_a:,}</td><td style="padding:5px; text-align:right; font-weight:600; color:#43b581;">${rango_h:,}</td></tr>
                </table>
                <div style="text-align:center; margin-top:8px; font-size:11px; color:#e8a838;">Airbnb tiene un rango {rango_a/rango_h:.1f}x mayor → especulación en temporada alta</div>
            </div>
            <div class="ab-section" data-delay="500" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">📉 3. Coeficiente de Variación (CV%)</h3>
                <div style="display:flex; gap:10px; margin-bottom:8px;">
                    <div style="flex:1; text-align:center;"><div style="font-size:10px; color:#e07065;">AIRBNB</div><div style="font-size:28px; font-weight:700; color:#e07065;">{stats_a['cv_porcentaje']:.2f}%</div></div>
                    <div style="display:flex; align-items:center; font-size:20px; color:#a0aec0;">vs</div>
                    <div style="flex:1; text-align:center;"><div style="font-size:10px; color:#43b581;">HOTEL</div><div style="font-size:28px; font-weight:700; color:#43b581;">{stats_h['cv_porcentaje']:.2f}%</div></div>
                </div>
                <div style="display:flex; gap:4px; height:24px; border-radius:6px; overflow:hidden;">
                    <div class="ab-bar-fill" style="width:{stats_a['cv_porcentaje']/(stats_a['cv_porcentaje']+stats_h['cv_porcentaje'])*100:.0f}%; background:#e07065; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:600; color:white;">Airbnb</div>
                    <div class="ab-bar-fill" style="width:{stats_h['cv_porcentaje']/(stats_a['cv_porcentaje']+stats_h['cv_porcentaje'])*100:.0f}%; background:#43b581; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:600; color:white;">Hotel</div>
                </div>
            </div>
            <div class="ab-section" data-delay="700" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">📊 4. Crecimiento Mediana de Precios (2021-2026)</h3>
                <div style="display:flex; justify-content:center; gap:12px; margin-bottom:10px; font-size:11px;">
                    <label id="abToggleAirbnb" onclick="toggleAbLine('airbnb')" style="display:flex; align-items:center; gap:5px; cursor:pointer; padding:4px 12px; border-radius:6px; border:2px solid #e07065; background:#fdf0ef; transition:all 0.3s; user-select:none;">
                        <span style="width:18px; height:3px; background:#e07065; border-radius:2px; display:inline-block;"></span>
                        <span style="width:7px; height:7px; background:#e07065; border-radius:50%; display:inline-block;"></span>
                        <b style="color:#e07065;">Airbnb mediana</b>
                    </label>
                    <label id="abToggleHotel" onclick="toggleAbLine('hotel')" style="display:flex; align-items:center; gap:5px; cursor:pointer; padding:4px 12px; border-radius:6px; border:2px solid #5b9bd5; background:#edf4fb; transition:all 0.3s; user-select:none;">
                        <span style="width:18px; height:3px; background:#5b9bd5; border-radius:2px; display:inline-block;"></span>
                        <span style="width:7px; height:7px; background:#5b9bd5; border-radius:50%; display:inline-block;"></span>
                        <b style="color:#5b9bd5;">Hotel mediana</b>
                    </label>
                </div>
                <div id="abChartContainer" style="position:relative; height:220px; background:#ffffff; border-radius:8px; border:1px solid #e2e8f0; overflow:hidden;">
                    <svg id="abChartSvg" viewBox="0 0 380 200" style="width:100%; height:100%;"></svg>
                </div>
                <div id="abTooltip" style="display:none; position:fixed; z-index:99999; background:rgba(45,55,72,0.95); color:white; padding:8px 12px; border-radius:8px; font-size:11px; pointer-events:none; white-space:nowrap; box-shadow:0 4px 12px rgba(0,0,0,0.25);"></div>
                <div style="margin-top:8px; display:flex; justify-content:space-between; font-size:9px; color:#718096;">
                    <span>Crecimiento Airbnb: <b style="color:#e07065;">+{((resultado_ab['medianas_airbnb'][-1] - resultado_ab['medianas_airbnb'][0]) / resultado_ab['medianas_airbnb'][0] * 100):.0f}%</b> (5 años)</span>
                    <span>Crecimiento Hotel: <b style="color:#5b9bd5;">+{((resultado_ab['medianas_hotel'][-1] - resultado_ab['medianas_hotel'][0]) / resultado_ab['medianas_hotel'][0] * 100):.0f}%</b> (5 años)</span>
                </div>
            </div>
            <script>
            (function() {{
                var DA = {resultado_ab['medianas_airbnb']};
                var DH = {resultado_ab['medianas_hotel']};
                var YRS = {resultado_ab['anios']};
                var MAX_V = 500000;
                var showA = true, showH = true;
                var padL = 48, padR = 15, padT = 22, padB = 28;
                var W = 380, H = 200;
                var plotW = W - padL - padR;
                var plotH = H - padT - padB;

                function px(i) {{ return padL + (i / (YRS.length - 1)) * plotW; }}
                function py(v) {{ return padT + plotH - (v / MAX_V) * plotH; }}
                function fmt(v) {{ return '$' + (v / 1000).toFixed(0) + 'K'; }}

                function buildChart() {{
                    var svg = document.getElementById('abChartSvg');
                    if (!svg) {{ setTimeout(buildChart, 300); return; }}
                    svg.innerHTML = '';
                    var ns = 'http://www.w3.org/2000/svg';

                    // Grid
                    [0, 100000, 200000, 300000, 400000, 500000].forEach(function(v) {{
                        var y = py(v);
                        var ln = document.createElementNS(ns, 'line');
                        ln.setAttribute('x1', padL); ln.setAttribute('x2', W - padR);
                        ln.setAttribute('y1', y); ln.setAttribute('y2', y);
                        ln.setAttribute('stroke', '#e2e8f0'); ln.setAttribute('stroke-width', '0.8');
                        if (v > 0 && v < 500000) ln.setAttribute('stroke-dasharray', '3,3');
                        svg.appendChild(ln);
                        var t = document.createElementNS(ns, 'text');
                        t.setAttribute('x', padL - 4); t.setAttribute('y', y + 3);
                        t.setAttribute('text-anchor', 'end'); t.setAttribute('font-size', '8');
                        t.setAttribute('fill', '#a0aec0'); t.setAttribute('font-family', 'Segoe UI, sans-serif');
                        t.textContent = fmt(v);
                        svg.appendChild(t);
                    }});
                    // X labels
                    YRS.forEach(function(yr, i) {{
                        var t = document.createElementNS(ns, 'text');
                        t.setAttribute('x', px(i)); t.setAttribute('y', H - 6);
                        t.setAttribute('text-anchor', 'middle'); t.setAttribute('font-size', '9');
                        t.setAttribute('font-weight', '600'); t.setAttribute('fill', '#718096');
                        t.setAttribute('font-family', 'Segoe UI, sans-serif');
                        t.textContent = yr;
                        svg.appendChild(t);
                    }});

                    function drawSeries(data, color, id, vis) {{
                        var g = document.createElementNS(ns, 'g');
                        g.setAttribute('id', id);
                        g.style.opacity = vis ? '1' : '0';
                        g.style.transition = 'opacity 0.5s ease';
                        // Area fill
                        var ap = 'M ' + px(0) + ' ' + py(data[0]);
                        for (var i = 1; i < data.length; i++) ap += ' L ' + px(i) + ' ' + py(data[i]);
                        ap += ' L ' + px(data.length - 1) + ' ' + py(0) + ' L ' + px(0) + ' ' + py(0) + ' Z';
                        var area = document.createElementNS(ns, 'path');
                        area.setAttribute('d', ap); area.setAttribute('fill', color); area.setAttribute('opacity', '0.08');
                        g.appendChild(area);
                        // Line
                        var pts = data.map(function(v, i) {{ return px(i) + ',' + py(v); }}).join(' ');
                        var pl = document.createElementNS(ns, 'polyline');
                        pl.setAttribute('points', pts); pl.setAttribute('fill', 'none');
                        pl.setAttribute('stroke', color); pl.setAttribute('stroke-width', '2.5');
                        pl.setAttribute('stroke-linecap', 'round'); pl.setAttribute('stroke-linejoin', 'round');
                        pl.classList.add('ab-line-anim');
                        g.appendChild(pl);
                        // Dots + labels
                        data.forEach(function(v, i) {{
                            var cx = px(i), cy = py(v);
                            // Hover target
                            var ht = document.createElementNS(ns, 'circle');
                            ht.setAttribute('cx', cx); ht.setAttribute('cy', cy); ht.setAttribute('r', '12');
                            ht.setAttribute('fill', 'transparent'); ht.setAttribute('style', 'cursor:pointer;');
                            ht.setAttribute('data-tip', (id === 'lineAirbnb' ? '🏠 Airbnb' : '🏨 Hotel') + ' ' + YRS[i] + ': $' + v.toLocaleString('es-CO') + ' COP/noche');
                            ht.onmouseenter = function(e) {{
                                var tip = document.getElementById('abTooltip');
                                if (tip) {{ tip.textContent = this.getAttribute('data-tip'); tip.style.display = 'block'; tip.style.left = (e.clientX + 14) + 'px'; tip.style.top = (e.clientY - 38) + 'px'; }}
                            }};
                            ht.onmouseleave = function() {{ var tip = document.getElementById('abTooltip'); if (tip) tip.style.display = 'none'; }};
                            g.appendChild(ht);
                            // Visible dot
                            var c = document.createElementNS(ns, 'circle');
                            c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', '5');
                            c.setAttribute('fill', '#fff'); c.setAttribute('stroke', color); c.setAttribute('stroke-width', '2.5');
                            c.setAttribute('style', 'pointer-events:none;');
                            g.appendChild(c);
                            // Price label
                            var lbl = document.createElementNS(ns, 'text');
                            lbl.setAttribute('x', cx); lbl.setAttribute('y', cy - 10);
                            lbl.setAttribute('text-anchor', 'middle'); lbl.setAttribute('font-size', '8');
                            lbl.setAttribute('font-weight', '700'); lbl.setAttribute('fill', color);
                            lbl.setAttribute('font-family', 'Segoe UI, sans-serif');
                            lbl.textContent = fmt(v);
                            g.appendChild(lbl);
                        }});
                        svg.appendChild(g);
                        // Animate line drawing
                        setTimeout(function() {{
                            var len = pl.getTotalLength();
                            pl.style.strokeDasharray = len;
                            pl.style.strokeDashoffset = len;
                            pl.getBoundingClientRect();
                            pl.style.transition = 'stroke-dashoffset 1.5s ease';
                            pl.style.strokeDashoffset = '0';
                        }}, 100);
                    }}
                    drawSeries(DA, '#e07065', 'lineAirbnb', showA);
                    drawSeries(DH, '#5b9bd5', 'lineHotel', showH);
                }}

                window.toggleAbLine = function(which) {{
                    if (which === 'airbnb') {{
                        showA = !showA;
                        var g = document.getElementById('lineAirbnb');
                        var btn = document.getElementById('abToggleAirbnb');
                        if (g) g.style.opacity = showA ? '1' : '0';
                        if (btn) {{ btn.style.background = showA ? '#fdf0ef' : '#f7f7f7'; btn.style.borderColor = showA ? '#e07065' : '#cbd5e0'; btn.style.opacity = showA ? '1' : '0.45'; }}
                    }} else {{
                        showH = !showH;
                        var g = document.getElementById('lineHotel');
                        var btn = document.getElementById('abToggleHotel');
                        if (g) g.style.opacity = showH ? '1' : '0';
                        if (btn) {{ btn.style.background = showH ? '#edf4fb' : '#f7f7f7'; btn.style.borderColor = showH ? '#5b9bd5' : '#cbd5e0'; btn.style.opacity = showH ? '1' : '0.45'; }}
                    }}
                }};

                window._buildAbChart = buildChart;
                setTimeout(function() {{ var p = document.getElementById('panelAirbnb'); if (p && p.style.display !== 'none') buildChart(); }}, 1000);
            }})();
            </script>
            <div class="ab-section" data-delay="900" style="background:#fdf0ef; border-radius:12px; padding:16px; border:1px solid #e0706533; text-align:center;">
                <div style="font-size:12px; color:#e07065; font-weight:600; margin-bottom:6px;">⚠️ 5. CONCLUSIÓN: SECTOR CON MAYOR ESPECULACIÓN</div>
                <div style="font-size:28px; font-weight:700; color:#e07065; margin:8px 0;">▶ {sector_v.upper()} ◀</div>
                <div style="font-size:11px; color:#4a5568; line-height:1.5;">Diferencia de <b style="color:#e8a838;">{dif_cv:.2f} puntos porcentuales</b> en CV.<br>Los precios de <b style="color:#e07065;">{sector_v}</b> presentan <b style="color:#e07065;">MAYOR VOLATILIDAD</b><br>(especulación de precios) durante el Festival 2026.</div>
                <div style="margin-top:10px; padding-top:8px; border-top:1px solid #e2e8f0; font-size:9px; color:#a0aec0; line-height:1.4;">Fuente: RCN Noticias, RTA Noticias, CC Valledupar<br>Método: Desviación Estándar y Coeficiente de Variación sobre medianas 2021-2026</div>
            </div>
        </div>
    </div>
    <script>
    function openAirbnbPanel() {{
        var panel = document.getElementById('panelAirbnb');
        var btn = document.getElementById('btnAirbnb');
        btn.style.display = 'none';
        panel.style.display = 'flex';
        panel.style.animation = 'slideInRight 0.5s ease forwards';
        var sections = panel.querySelectorAll('.ab-section');
        sections.forEach(function(s) {{
            s.classList.remove('visible');
            s.style.opacity = '0';
            s.style.transform = 'translateY(20px)';
        }});
        sections.forEach(function(s) {{
            var delay = parseInt(s.getAttribute('data-delay')) || 0;
            setTimeout(function() {{
                s.classList.add('visible');
            }}, delay);
        }});
        // Trigger dynamic chart animation
        if (typeof window._buildAbChart === 'function') {{
            setTimeout(window._buildAbChart, 600);
        }}
    }}
    function closeAirbnbPanel() {{
        var panel = document.getElementById('panelAirbnb');
        panel.style.animation = 'slideInRight 0.4s ease reverse forwards';
        setTimeout(function() {{
            panel.style.display = 'none';
            document.getElementById('btnAirbnb').style.display = 'block';
        }}, 400);
    }}
    </script>
    '''
    mapa.get_root().html.add_child(folium.Element(panel_airbnb_html))

    # ── CAMPANA DE GAUSS: Panel integrado al mapa ──
    from estadistica.inferencial import calcular_probabilidad_superar_meta
    from data.datos_festival import DIST_NORMAL_PARAMS
    res_gauss = calcular_probabilidad_superar_meta()
    mu = DIST_NORMAL_PARAMS['media']
    sigma = DIST_NORMAL_PARAMS['desviacion']
    meta = DIST_NORMAL_PARAMS['meta']
    z_score = res_gauss['z_score']
    prob = res_gauss['prob_superar_porcentaje']
    # Serie histórica de ingresos del Parque de la Leyenda
    ingresos_hist = [DATOS["Parque de la Leyenda"][a]["ingresos_millones"] for a in ANIOS]

    # Build SVG bell curve points
    import math
    svg_points = []
    shade_points = []
    svg_w, svg_h = 360, 160
    x_min, x_max = mu - 3.5*sigma, mu + 3.5*sigma
    meta_svg_x = ((meta - x_min) / (x_max - x_min)) * svg_w
    for i in range(200):
        x_val = x_min + (x_max - x_min) * i / 199
        z = (x_val - mu) / sigma
        y_val = math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))
        sx = (i / 199) * svg_w
        sy = svg_h - (y_val / (1 / (sigma * math.sqrt(2 * math.pi)))) * (svg_h - 10)
        svg_points.append(f"{sx:.1f},{sy:.1f}")
        if x_val >= meta:
            shade_points.append(f"{sx:.1f},{sy:.1f}")

    curve_path = " ".join(svg_points)
    # Build shaded polygon for P(X > meta)
    shade_poly = ""
    if shade_points:
        first_x = shade_points[0].split(",")[0]
        last_x = shade_points[-1].split(",")[0]
        shade_poly = f"{first_x},{svg_h} " + " ".join(shade_points) + f" {last_x},{svg_h}"

    hist_bars = ""
    max_ing = max(ingresos_hist)
    for i, (a, v) in enumerate(zip(ANIOS, ingresos_hist)):
        pct = (v / max_ing) * 100
        color = "#e07065" if a == 2026 else "#5b9bd540"
        border = "border:1px solid #5b9bd5;" if a == 2026 else ""
        hist_bars += f'''<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:2px;">
            <div style="font-size:8px; color:#e8a838; font-weight:600;">${v:,}M</div>
            <div style="width:100%; background:#edf2f7; border-radius:3px; height:60px; display:flex; align-items:flex-end;">
                <div class="gauss-bar" style="width:100%; height:{pct:.0f}%; background:{color}; border-radius:3px; {border}"></div>
            </div>
            <div style="font-size:8px; color:#718096;">{a}</div>
        </div>'''

    panel_gauss_html = f'''
    <div id="btnGauss" onclick="openGaussPanel()"
         style="position:fixed; top:205px; left:10px; z-index:9998;
                background:#9b7dc9; color:white;
                padding:8px 16px; border-radius:20px; cursor:pointer;
                font-family:'Segoe UI',sans-serif; font-size:11px; font-weight:600;
                box-shadow:0 3px 10px rgba(155,125,201,0.3); border:none;">
        📊 Campana de Gauss
    </div>
    <div id="panelGauss" style="display:none; position:fixed; top:0; left:0; z-index:99998;
                width:440px; height:100vh; background:#ffffff;
                flex-direction:column; overflow-y:auto;
                box-shadow:4px 0 24px rgba(0,0,0,0.10); border-right:1px solid #e2e8f0;
                font-family:'Segoe UI',Arial,sans-serif;">
        <div style="padding:16px 20px; background:#f5f0fa;
                    border-bottom:1px solid #e2e8f0; position:sticky; top:0; z-index:1;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0; color:#9b7dc9; font-size:15px;">📊 Distribución Normal – Campana de Gauss</h2>
                    <p style="margin:2px 0 0; color:#718096; font-size:10px;">Parque de la Leyenda Vallenata – Proyección 2026</p>
                </div>
                <span onclick="closeGaussPanel()" style="color:#e07065; font-size:24px; cursor:pointer; padding:4px 8px; line-height:1;">&times;</span>
            </div>
        </div>
        <div style="padding:16px 20px;">
            <!-- Serie Histórica -->
            <div class="gauss-section" data-delay="100" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">📈 Serie Histórica de Ingresos (2021-2026)</h3>
                <div style="display:flex; gap:4px; align-items:flex-end;">{hist_bars}</div>
            </div>
            <!-- Parámetros -->
            <div class="gauss-section" data-delay="300" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">⚙️ Parámetros del Modelo</h3>
                <div style="display:flex; gap:8px;">
                    <div style="flex:1; background:#f5f0fa; border:1px solid #9b7dc944; border-radius:8px; padding:10px; text-align:center;">
                        <div style="font-size:9px; color:#718096;">Media (μ)</div>
                        <div style="font-size:20px; font-weight:700; color:#9b7dc9;">${mu:,}M</div>
                    </div>
                    <div style="flex:1; background:#edf4fb; border:1px solid #5b9bd544; border-radius:8px; padding:10px; text-align:center;">
                        <div style="font-size:9px; color:#718096;">Desv. Std (σ)</div>
                        <div style="font-size:20px; font-weight:700; color:#5b9bd5;">${sigma:,}M</div>
                    </div>
                    <div style="flex:1; background:#fef6e8; border:1px solid #e8a83844; border-radius:8px; padding:10px; text-align:center;">
                        <div style="font-size:9px; color:#718096;">Meta (X)</div>
                        <div style="font-size:20px; font-weight:700; color:#e8a838;">${meta:,}M</div>
                    </div>
                </div>
            </div>
            <!-- Campana SVG -->
            <div class="gauss-section" data-delay="500" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 8px; color:#2d3748; font-size:13px;">🔔 Campana de Gauss – Área Sombreada P(X &gt; {meta:,})</h3>
                <svg viewBox="0 0 {svg_w} {svg_h + 30}" style="width:100%; height:auto; background:#f0f4f8; border-radius:8px; padding:4px;">
                    <defs><linearGradient id="curveGrad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stop-color="#5b9bd5"/><stop offset="100%" stop-color="#9b7dc9"/>
                    </linearGradient></defs>
                    <polygon points="{shade_poly}" fill="#e0706566" stroke="none" class="gauss-shade"/>
                    <polyline points="{curve_path}" fill="none" stroke="url(#curveGrad)" stroke-width="2.5" class="gauss-curve"/>
                    <line x1="{meta_svg_x:.1f}" y1="5" x2="{meta_svg_x:.1f}" y2="{svg_h}" stroke="#e8a838" stroke-width="1.5" stroke-dasharray="4,3"/>
                    <line x1="{((mu - x_min)/(x_max - x_min))*svg_w:.1f}" y1="5" x2="{((mu - x_min)/(x_max - x_min))*svg_w:.1f}" y2="{svg_h}" stroke="#9b7dc9" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>
                    <text x="{meta_svg_x:.1f}" y="{svg_h + 15}" fill="#e8a838" font-size="9" text-anchor="middle" font-weight="bold">Meta ${meta:,}M</text>
                    <text x="{((mu - x_min)/(x_max - x_min))*svg_w:.1f}" y="{svg_h + 15}" fill="#9b7dc9" font-size="9" text-anchor="middle">μ=${mu:,}M</text>
                    <text x="{meta_svg_x + 30:.1f}" y="25" fill="#e07065" font-size="10" font-weight="bold">{prob:.2f}%</text>
                </svg>
                <div style="display:flex; justify-content:center; gap:16px; margin-top:6px; font-size:9px; color:#4a5568;">
                    <span><span style="display:inline-block; width:12px; height:3px; background:linear-gradient(90deg,#5b9bd5,#9b7dc9); border-radius:2px; vertical-align:middle;"></span> Distribución Normal</span>
                    <span><span style="display:inline-block; width:12px; height:8px; background:#e0706566; border-radius:2px; vertical-align:middle;"></span> P(X &gt; meta) = {prob:.2f}%</span>
                    <span style="color:#e8a838;">┊ Meta</span>
                    <span style="color:#9b7dc9;">┊ Media</span>
                </div>
            </div>
            <!-- Cálculos Paso a Paso -->
            <div class="gauss-section" data-delay="700" style="background:#f8fafb; border-radius:12px; padding:14px; margin-bottom:14px; border:1px solid #e2e8f0;">
                <h3 style="margin:0 0 10px; color:#2d3748; font-size:13px;">🧮 Cálculo Paso a Paso</h3>
                <div style="background:#f0f4f8; border-radius:8px; padding:12px; font-family:monospace; font-size:12px; color:#4a5568; line-height:1.8;">
                    <div><span style="color:#9b7dc9;">Paso 1:</span> Z = (X - μ) / σ</div>
                    <div style="padding-left:20px;">Z = ({meta:,} - {mu:,}) / {sigma}</div>
                    <div style="padding-left:20px;">Z = {meta - mu:,} / {sigma}</div>
                    <div style="padding-left:20px; color:#e8a838; font-weight:bold;">Z = {z_score:.4f}</div>
                    <div style="margin-top:8px;"><span style="color:#9b7dc9;">Paso 2:</span> P(X &gt; {meta:,}) = P(Z &gt; {z_score:.2f})</div>
                    <div style="padding-left:20px;">= 1 - Φ({z_score:.2f})</div>
                    <div style="padding-left:20px;">= 1 - {1 - prob/100:.6f}</div>
                    <div style="padding-left:20px; color:#e07065; font-weight:bold; font-size:14px;">= {prob/100:.6f} → {prob:.2f}%</div>
                </div>
            </div>
            <!-- Conclusión -->
            <div class="gauss-section" data-delay="900" style="background:#f5f0fa; border-radius:12px; padding:16px; border:1px solid #9b7dc933; text-align:center;">
                <div style="font-size:12px; color:#9b7dc9; font-weight:600; margin-bottom:6px;">📌 RESULTADO: PROBABILIDAD DE SUPERAR LA META</div>
                <div style="font-size:36px; font-weight:700; color:#e07065; margin:8px 0;">P = {prob:.2f}%</div>
                <div style="font-size:13px; color:#e8a838; font-weight:600; margin-bottom:6px;">{'POCO PROBABLE' if prob < 20 else 'MODERADAMENTE PROBABLE' if prob < 50 else 'PROBABLE'}</div>
                <div style="font-size:11px; color:#4a5568; line-height:1.5;">Un Z-score de <b style="color:#e8a838;">{z_score:.2f}</b> indica que la meta está <b style="color:#e07065;">{z_score:.1f} desviaciones estándar</b> por encima de la media histórica. Se necesitarían condiciones excepcionales para alcanzar ${meta:,}M.</div>
                <div style="margin-top:10px; padding-top:8px; border-top:1px solid #e2e8f0; font-size:9px; color:#a0aec0;">Modelo: Distribución Normal · Fuente: CC Valledupar · Datos: 2021-2026</div>
            </div>
        </div>
    </div>
    <script>
    function openGaussPanel() {{
        var panel = document.getElementById('panelGauss');
        document.getElementById('btnGauss').style.display = 'none';
        panel.style.display = 'flex';
        panel.style.animation = 'slideInLeft 0.5s ease forwards';
        var sections = panel.querySelectorAll('.gauss-section');
        sections.forEach(function(s) {{ s.classList.remove('visible'); s.style.opacity='0'; s.style.transform='translateY(20px)'; }});
        sections.forEach(function(s) {{
            var delay = parseInt(s.getAttribute('data-delay')) || 0;
            setTimeout(function() {{ s.classList.add('visible'); }}, delay);
        }});
    }}
    function closeGaussPanel() {{
        var panel = document.getElementById('panelGauss');
        panel.style.animation = 'slideInLeft 0.4s ease reverse forwards';
        setTimeout(function() {{ panel.style.display='none'; document.getElementById('btnGauss').style.display='block'; }}, 400);
    }}
    </script>
    <style>
        @keyframes slideInLeft {{ from {{ transform:translateX(-100%); opacity:0; }} to {{ transform:translateX(0); opacity:1; }} }}
        .gauss-section {{ opacity:0; transform:translateY(20px); }}
        .gauss-section.visible {{ animation:fadeInUp 0.6s ease forwards; }}
        .gauss-curve {{ stroke-dasharray:1000; stroke-dashoffset:1000; animation: drawCurve 2s ease forwards 0.5s; }}
        .gauss-shade {{ opacity:0; animation: fadeShade 1s ease forwards 1.5s; }}
        .gauss-bar {{ animation: growBar 0.8s ease forwards; }}
        @keyframes drawCurve {{ to {{ stroke-dashoffset:0; }} }}
        @keyframes fadeShade {{ to {{ opacity:1; }} }}
    </style>
    '''
    mapa.get_root().html.add_child(folium.Element(panel_gauss_html))

    mapa.save(filepath)
    print(f"\n  ✓ Mapa interactivo guardado: {filepath}")
    print(f"  ✓ Abra el archivo HTML en su navegador para interactuar")

    return mapa