#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json

# Parsear el archivo KML de la ruta 76
tree = ET.parse('doc_ruta76.kml')
root = tree.getroot()

# Namespace de KML
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Diccionario para almacenar las rutas
rutas76 = []

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

        rutas76.append({
            'nombre': nombre,
            'coordenadas': coordenadas
        })

# Guardar como JSON
with open('rutas76_coordenadas.json', 'w', encoding='utf-8') as f:
    json.dump(rutas76, f, ensure_ascii=False, indent=2)

print(f"Se extrajeron {len(rutas76)} rutas de la línea 76:")
for ruta in rutas76:
    print(f"  - {ruta['nombre']}: {len(ruta['coordenadas'])} puntos")
