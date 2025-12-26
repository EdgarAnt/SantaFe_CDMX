#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json

def procesar_kml(archivo_kml):
    """Procesa un archivo KML y extrae las rutas"""
    tree = ET.parse(archivo_kml)
    root = tree.getroot()

    # Namespace de KML
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    rutas = []

    # Buscar todos los Placemark con LineString
    for placemark in root.findall('.//kml:Placemark', ns):
        nombre = placemark.find('kml:name', ns).text
        linestring = placemark.find('.//kml:LineString', ns)

        if linestring is not None:
            coords_text = linestring.find('kml:coordinates', ns).text.strip()

            # Convertir las coordenadas de texto a lista de [lat, lng]
            coordenadas = []
            for linea in coords_text.split('\n'):
                linea = linea.strip()
                if linea:
                    partes = linea.split(',')
                    lng = float(partes[0])
                    lat = float(partes[1])
                    coordenadas.append([lat, lng])

            rutas.append({
                'nombre': nombre,
                'coordenadas': coordenadas
            })

    return rutas

# Procesar todas las rutas
print("Procesando rutas...")

# Cargar rutas existentes (9C y 76)
with open('rutas_coordenadas.json', 'r') as f:
    rutas9c = json.load(f)

with open('rutas76_coordenadas.json', 'r') as f:
    rutas76 = json.load(f)

# Procesar nuevas rutas
rutas76a = procesar_kml('doc_ruta76a.kml')
print(f"Ruta 76A: {len(rutas76a)} direcciones")
for ruta in rutas76a:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")

rutas110 = procesar_kml('doc_ruta110.kml')
print(f"Ruta 110: {len(rutas110)} direcciones")
for ruta in rutas110:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")

# Crear estructura de datos completa
rutasData = {
    '9c': rutas9c,
    '76': rutas76,
    '76a': rutas76a,
    '110': rutas110
}

# Convertir a formato JavaScript
js_code = 'const rutasData = ' + json.dumps(rutasData, separators=(',', ':')) + ';'

with open('rutas_data.js', 'w') as f:
    f.write(js_code)

print("\nArchivo rutas_data.js actualizado con todas las rutas")
print(f"Total de rutas: 9C, 76, 76A, 110")
