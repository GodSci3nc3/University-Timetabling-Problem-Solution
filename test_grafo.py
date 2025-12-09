"""
Script de prueba completo del módulo de Grafo de Conflictos.
Usa los datos del archivo Excel para construir y analizar el grafo.
"""

from src.data.lector_excel import leer_excel
from src.core.grafo_conflictos import GrafoConflictos
from src.core.analizador_grafo import (calcular_numero_cromatico_aproximado,
                                       verificar_factibilidad,
                                       encontrar_cliques,
                                       analizar_conflictos_por_tipo)
from src.visualization.visualizador_grafo import (visualizar_grafo,
                                                   visualizar_por_cuatrimestre,
                                                   generar_reporte_conflictos)


def main():
    """Función principal de prueba."""
    print("=" * 80)
    print("SISTEMA DE GESTIÓN DE HORARIOS ACADÉMICOS")
    print("Módulo de Grafo de Conflictos")
    print("=" * 80)
    print()
    
    # Paso 1: Cargar datos
    print("📂 CARGANDO DATOS...")
    print("-" * 80)
    try:
        grupos, materias, profesores = leer_excel("datos_universidad.xlsx")
        print(f"✓ Datos cargados: {len(grupos)} grupos, {len(materias)} materias, {len(profesores)} profesores")
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        return
    print()
    
    # Paso 2: Construir grafo
    print("🔨 CONSTRUYENDO GRAFO DE CONFLICTOS...")
    print("-" * 80)
    grafo = GrafoConflictos()
    grafo.construir_desde_datos(grupos, materias, profesores)
    print("✓ Grafo construido exitosamente")
    print()
    
    # Paso 3: Estadísticas del grafo
    print("📊 ESTADÍSTICAS DEL GRAFO")
    print("-" * 80)
    stats = grafo.obtener_estadisticas()
    
    print(f"Nodos totales: {stats['num_nodos']}")
    print(f"Aristas totales: {stats['num_aristas']}")
    print(f"Grado promedio: {stats['grado_promedio']:.2f}")
    print(f"Grado máximo: {stats['grado_maximo']}")
    print(f"Grado mínimo: {stats['grado_minimo']}")
    print(f"Densidad del grafo: {stats['densidad']:.4f}")
    
    print(f"\nDistribución por cuatrimestre:")
    for cuatri, num_nodos in sorted(stats['nodos_por_cuatrimestre'].items()):
        print(f"  • Cuatrimestre {cuatri}: {num_nodos} asignaciones")
    print()
    
    # Paso 4: Análisis de conflictos
    print("⚡ ANÁLISIS DE CONFLICTOS")
    print("-" * 80)
    analisis = analizar_conflictos_por_tipo(grafo)
    print(f"Total de conflictos: {analisis['total']}")
    print(f"  • Conflictos por mismo grupo: {analisis['conflictos_grupo']} ({analisis['porcentaje_grupo']:.1f}%)")
    print(f"  • Conflictos por mismo profesor: {analisis['conflictos_profesor']} ({analisis['porcentaje_profesor']:.1f}%)")
    print()
    
    # Paso 5: Nodos más conflictivos
    print("🔥 TOP 10 ASIGNACIONES MÁS CONFLICTIVAS")
    print("-" * 80)
    nodos_conflictivos = grafo.obtener_nodos_mas_conflictivos(10)
    
    for i, (nodo, grado) in enumerate(nodos_conflictivos, 1):
        print(f"{i}. {nodo} - {grado} conflictos")
    print()
    
    # Paso 6: Número cromático
    print("🎨 ANÁLISIS DE COLOREO")
    print("-" * 80)
    num_cromatico = calcular_numero_cromatico_aproximado(grafo)
    print(f"Número cromático aproximado: {num_cromatico}")
    print(f"Interpretación: Se necesitan al menos {num_cromatico} slots de tiempo diferentes")
    print()
    
    # Paso 7: Verificar factibilidad
    print("✓ VERIFICACIÓN DE FACTIBILIDAD")
    print("-" * 80)
    
    # Verificar para turno matutino (35 slots)
    slots_matutino = 35
    es_factible_mat, razon_mat = verificar_factibilidad(grafo, slots_matutino)
    print(f"Turno Matutino ({slots_matutino} slots): {razon_mat}")
    
    # Verificar para turno vespertino (35 slots)
    slots_vespertino = 35
    es_factible_vesp, razon_vesp = verificar_factibilidad(grafo, slots_vespertino)
    print(f"Turno Vespertino ({slots_vespertino} slots): {razon_vesp}")
    
    # Verificar para ambos turnos (70 slots)
    slots_ambos = 70
    es_factible_ambos, razon_ambos = verificar_factibilidad(grafo, slots_ambos)
    print(f"Ambos Turnos ({slots_ambos} slots): {razon_ambos}")
    print()
    
    # Paso 8: Encontrar cliques
    print("🔺 CLIQUES ENCONTRADOS (grupos mutuamente conflictivos)")
    print("-" * 80)
    cliques = encontrar_cliques(grafo, max_cliques=5)
    
    if cliques:
        print(f"Se encontraron {len(cliques)} cliques de tamaño 3:")
        for i, clique in enumerate(cliques[:5], 1):
            nodos_str = ", ".join([str(n) for n in clique])
            print(f"{i}. {{{nodos_str}}}")
    else:
        print("No se encontraron cliques de tamaño 3")
    print()
    
    # Paso 9: Generar visualizaciones
    print("📊 GENERANDO VISUALIZACIONES...")
    print("-" * 80)
    
    # Grafo completo
    visualizar_grafo(grafo, 
                    titulo="Grafo de Conflictos Completo",
                    guardar_como="grafo_completo.png")
    
    # Grafos por cuatrimestre
    cuatrimestres = sorted(set(nodo.cuatrimestre for nodo in grafo.nodos))
    for cuatri in cuatrimestres:
        visualizar_por_cuatrimestre(grafo, cuatri, 
                                   guardar_como=f"grafo_cuatrimestre_{cuatri}.png")
    
    print()
    
    # Paso 10: Generar reporte
    print("📄 GENERANDO REPORTE DETALLADO...")
    print("-" * 80)
    generar_reporte_conflictos(grafo, "reporte_grafo_completo.txt")
    print()
    
    # Resumen final
    print("=" * 80)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\nArchivos generados:")
    print("  • grafo_completo.png - Visualización del grafo completo")
    for cuatri in cuatrimestres:
        print(f"  • grafo_cuatrimestre_{cuatri}.png - Grafo del cuatrimestre {cuatri}")
    print("  • reporte_grafo_completo.txt - Reporte detallado de conflictos")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
