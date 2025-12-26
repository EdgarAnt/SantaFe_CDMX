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
print("Procesando todas las rutas...")

# Cargar rutas existentes
with open('rutas_coordenadas.json', 'r') as f:
    rutas9c = json.load(f)

with open('rutas76_coordenadas.json', 'r') as f:
    rutas76 = json.load(f)

rutas76a = procesar_kml('doc_ruta76a.kml')
rutas110 = procesar_kml('doc_ruta110.kml')

# Procesar rutas nuevas
rutas110b = procesar_kml('doc_ruta110b.kml')
print(f"Ruta 110-B: {len(rutas110b)} direcciones")
for ruta in rutas110b:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")

rutas110c = procesar_kml('doc_ruta110c.kml')
print(f"Ruta 110-C: {len(rutas110c)} direcciones")
for ruta in rutas110c:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")

rutas112 = procesar_kml('doc_ruta112.kml')
print(f"Ruta 112: {len(rutas112)} direcciones")
for ruta in rutas112:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")

# Crear estructura de datos completa
rutasData = {
    '9c': rutas9c,
    '76': rutas76,
    '76a': rutas76a,
    '110': rutas110,
    '110b': rutas110b,
    '110c': rutas110c,
    '112': rutas112
}

# Convertir a formato JavaScript
js_code = 'const rutasData = ' + json.dumps(rutasData, separators=(',', ':')) + ';'

with open('rutas_data.js', 'w') as f:
    f.write(js_code)

print("\nArchivo rutas_data.js actualizado con todas las rutas")
print(f"Total de rutas: 9C, 76, 76A, 110, 110-B, 110-C, 112")
