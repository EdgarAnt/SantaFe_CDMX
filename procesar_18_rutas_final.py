#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json

def procesar_kml(archivo_kml):
    """Procesa un archivo KML y extrae las rutas"""
    tree = ET.parse(archivo_kml)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    rutas = []

    for placemark in root.findall('.//kml:Placemark', ns):
        nombre = placemark.find('kml:name', ns).text
        linestring = placemark.find('.//kml:LineString', ns)

        if linestring is not None:
            coords_text = linestring.find('kml:coordinates', ns).text.strip()
            coordenadas = []
            for linea in coords_text.split('\n'):
                linea = linea.strip()
                if linea:
                    partes = linea.split(',')
                    lng = float(partes[0])
                    lat = float(partes[1])
                    coordenadas.append([lat, lng])

            rutas.append({'nombre': nombre, 'coordenadas': coordenadas})

    return rutas

print("🚌 Procesando TODAS las 18 rutas finales...")

# Cargar rutas existentes
with open('rutas_coordenadas.json', 'r') as f:
    rutas9c = json.load(f)
with open('rutas76_coordenadas.json', 'r') as f:
    rutas76 = json.load(f)

# Procesar todas las rutas
rutas76a = procesar_kml('doc_ruta76a.kml')
rutas110 = procesar_kml('doc_ruta110.kml')
rutas110b = procesar_kml('doc_ruta110b.kml')
rutas110c = procesar_kml('doc_ruta110c.kml')
rutas112 = procesar_kml('doc_ruta112.kml')
rutas113b = procesar_kml('doc_n1.kml')
rutas115 = procesar_kml('doc_n2.kml')
rutas115a = procesar_kml('doc_n3.kml')
rutas116 = procesar_kml('doc_n4.kml')
rutas118 = procesar_kml('doc_n5.kml')
rutas119 = procesar_kml('doc_x1.kml')
rutas119b = procesar_kml('doc_x2.kml')
rutas120 = procesar_kml('doc_x3.kml')
rutas121a = procesar_kml('doc_x4.kml')

# Procesar rutas finales
rutas124 = procesar_kml('doc_final1.kml')
print(f"✓ 124: {len(rutas124)} direcciones - {sum(len(r['coordenadas']) for r in rutas124)} puntos")

rutas124a = procesar_kml('doc_final2.kml')
print(f"✓ 124-A: {len(rutas124a)} direcciones - {sum(len(r['coordenadas']) for r in rutas124a)} puntos")

# Crear estructura completa con TODAS las 18 rutas
rutasData = {
    '9c': rutas9c,
    '76': rutas76,
    '76a': rutas76a,
    '110': rutas110,
    '110b': rutas110b,
    '110c': rutas110c,
    '112': rutas112,
    '113b': rutas113b,
    '115': rutas115,
    '115a': rutas115a,
    '116': rutas116,
    '118': rutas118,
    '119': rutas119,
    '119b': rutas119b,
    '120': rutas120,
    '121a': rutas121a,
    '124': rutas124,
    '124a': rutas124a
}

# Convertir a JavaScript
js_code = 'const rutasData = ' + json.dumps(rutasData, separators=(',', ':')) + ';'
with open('rutas_data.js', 'w') as f:
    f.write(js_code)

print(f"\n✅ Archivo actualizado con {len(rutasData)} rutas totales")
print("📍 Rutas completas:")
print("   9C, 76, 76A, 110, 110-B, 110-C, 112, 113-B,")
print("   115, 115-A, 116, 118, 119, 119-B, 120, 121-A,")
print("   124, 124-A")
print(f"\n🎯 Total: {len(rutasData)} rutas con {len(rutasData) * 2} direcciones")
