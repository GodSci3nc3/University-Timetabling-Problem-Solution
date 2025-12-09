"""
Script de prueba del algoritmo de Backtracking.
Ejecuta el algoritmo completo y genera visualizaciones.
"""

from src.data.lector_excel import leer_excel
from src.core.grafo_conflictos import GrafoConflictos
from src.algoritmo.backtracking import resolver_backtracking
from src.algoritmo.estadisticas import generar_estadisticas, imprimir_estadisticas, generar_reporte_texto
from src.algoritmo.visualizador_arbol import visualizar_arbol_backtracking, visualizar_camino_solucion
from src.algoritmo.restricciones import verificar_solucion_completa


def imprimir_horario(horario, grupo_nombre):
    """Imprime el horario de un grupo de forma legible."""
    print(f"\n📅 HORARIO: {grupo_nombre}")
    print("=" * 80)
    
    if grupo_nombre not in horario:
        print("  No hay horario para este grupo")
        return
    
    from src.core.config import DIAS_SEMANA
    
    for dia in DIAS_SEMANA:
        if dia not in horario[grupo_nombre]:
            continue
        
        print(f"\n{dia}:")
        print("-" * 80)
        
        slots_dia = horario[grupo_nombre][dia]
        slots_ordenados = sorted(slots_dia.keys())
        
        for slot_key in slots_ordenados:
            asignacion = slots_dia[slot_key]
            if asignacion:
                materia = asignacion['materia']
                profesor = asignacion['profesor']
                print(f"  {slot_key:15} | {materia:30} | {profesor}")


def main():
    """Función principal de prueba."""
    print("=" * 80)
    print("SISTEMA DE GESTIÓN DE HORARIOS ACADÉMICOS")
    print("Algoritmo de Backtracking con Heurísticas")
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
    
    # Paso 2: Construir grafo de conflictos
    print("🕸️  CONSTRUYENDO GRAFO DE CONFLICTOS...")
    print("-" * 80)
    grafo = GrafoConflictos()
    grafo.construir_desde_datos(grupos, materias, profesores)
    stats_grafo = grafo.obtener_estadisticas()
    print(f"✓ Grafo construido: {stats_grafo['num_nodos']} nodos, {stats_grafo['num_aristas']} aristas")
    print()
    
    # Paso 3: Ejecutar backtracking
    print("🚀 EJECUTANDO ALGORITMO DE BACKTRACKING...")
    print("=" * 80)
    
    horario, arbol, stats = resolver_backtracking(grupos, materias, profesores, grafo)
    
    # Paso 4: Mostrar resultados
    if horario:
        print("\n✅ ¡SOLUCIÓN ENCONTRADA!")
        print("=" * 80)
        
        # Verificar completitud
        es_completa, errores = verificar_solucion_completa(horario, materias)
        
        if es_completa:
            print("✓ La solución es completa y válida")
        else:
            print("⚠️  La solución tiene los siguientes problemas:")
            for error in errores[:5]:  # Mostrar máximo 5 errores
                print(f"  - {error}")
        
        # Mostrar horarios de algunos grupos
        print("\n📅 HORARIOS GENERADOS (muestra)")
        print("=" * 80)
        
        for grupo in grupos[:3]:  # Mostrar solo los primeros 3 grupos
            imprimir_horario(horario, grupo.nombre)
        
        if len(grupos) > 3:
            print(f"\n... y {len(grupos) - 3} grupos más")
        
    else:
        print("\n❌ NO SE ENCONTRÓ SOLUCIÓN")
        print("=" * 80)
        print("El problema puede ser:")
        print("  • Restricciones demasiado estrictas")
        print("  • Insuficientes slots disponibles")
        print("  • Capacidad de profesores insuficiente")
    
    # Paso 5: Mostrar estadísticas
    imprimir_estadisticas(stats)
    
    # Paso 6: Generar visualizaciones
    print("\n📊 GENERANDO VISUALIZACIONES...")
    print("-" * 80)
    
    # Árbol completo (limitado a 100 nodos para que sea legible)
    visualizar_arbol_backtracking(
        arbol,
        output_path="arbol_backtracking",
        max_nodos=100
    )
    
    # Camino de solución
    if horario:
        visualizar_camino_solucion(arbol, output_path="camino_solucion")
    
    # Exportar árbol a JSON
    arbol.exportar_json("arbol_decisiones.json")
    print("✓ Árbol exportado a JSON: arbol_decisiones.json")
    
    # Paso 7: Generar reporte
    print("\n📄 GENERANDO REPORTE...")
    print("-" * 80)
    generar_reporte_texto(stats, "reporte_backtracking.txt")
    
    print("\n" + "=" * 80)
    print("✓ PRUEBA COMPLETADA")
    print("=" * 80)
    print("\nArchivos generados:")
    print("  • arbol_backtracking.png - Visualización del árbol (primeros 100 nodos)")
    if horario:
        print("  • camino_solucion.png - Camino que llevó a la solución")
    print("  • arbol_decisiones.json - Árbol completo en formato JSON")
    print("  • reporte_backtracking.txt - Reporte de estadísticas")
    print()


if __name__ == "__main__":
    main()
