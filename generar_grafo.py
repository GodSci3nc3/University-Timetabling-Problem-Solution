#!/usr/bin/env python3
"""
Script para generar visualización del grafo de conflictos.
Uso: python3 generar_grafo.py [archivo_excel]
"""

import sys
from src.data.lector_excel import leer_excel
from src.core.grafo_conflictos import GrafoConflictos
from src.visualization.visualizador_grafo import visualizar_grafo, generar_reporte_conflictos


def main():
    # Archivo de datos por defecto
    archivo_excel = 'datos_disponibilidad.xlsx'
    
    if len(sys.argv) > 1:
        archivo_excel = sys.argv[1]
    
    print(f"📊 Generando grafo de conflictos desde: {archivo_excel}")
    print("=" * 60)
    
    # Leer datos
    print("1. Leyendo datos del Excel...")
    grupos, materias, profesores = leer_excel(archivo_excel)
    print(f"   ✓ {len(grupos)} grupos, {len(materias)} materias, {len(profesores)} profesores")
    
    # Construir grafo
    print("\n2. Construyendo grafo de conflictos...")
    grafo = GrafoConflictos()
    grafo.construir_desde_datos(grupos, materias, profesores)
    
    stats = grafo.obtener_estadisticas()
    print(f"   ✓ Grafo construido:")
    print(f"     - Nodos: {stats['num_nodos']}")
    print(f"     - Aristas: {stats['num_aristas']}")
    print(f"     - Grado promedio: {stats['grado_promedio']:.2f}")
    print(f"     - Densidad: {stats['densidad']:.4f}")
    
    # Generar visualización
    print("\n3. Generando visualización...")
    nombre_imagen = 'grafo_conflictos.png'
    visualizar_grafo(grafo, 
                    titulo="Grafo de Conflictos - Sistema de Horarios",
                    guardar_como=nombre_imagen,
                    mostrar=False)
    
    # Generar reporte
    print("\n4. Generando reporte de conflictos...")
    nombre_reporte = 'reporte_conflictos.txt'
    generar_reporte_conflictos(grafo, archivo_salida=nombre_reporte)
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado:")
    print(f"   📈 Imagen del grafo: {nombre_imagen}")
    print(f"   📄 Reporte textual: {nombre_reporte}")
    print("=" * 60)


if __name__ == "__main__":
    main()
