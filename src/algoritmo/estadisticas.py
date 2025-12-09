"""
Generación de estadísticas del proceso de backtracking.
Analiza el árbol de decisiones para obtener métricas de rendimiento.
"""

from typing import Dict, Any
from .arbol_decisiones import ArbolDecisiones


def generar_estadisticas(
    arbol: ArbolDecisiones,
    tiempo_ejecucion: float
) -> Dict[str, Any]:
    """
    Genera estadísticas detalladas del proceso de backtracking.
    
    Args:
        arbol: Árbol de decisiones del backtracking
        tiempo_ejecucion: Tiempo total en segundos
    
    Returns:
        Diccionario con métricas del algoritmo
    """
    # Obtener estadísticas básicas del árbol
    stats_arbol = arbol.obtener_estadisticas()
    
    # Calcular métricas adicionales
    nodos_explorados = stats_arbol['total_nodos']
    backtracks = stats_arbol['nodos_fallo']
    profundidad_max = stats_arbol['profundidad_maxima']
    
    # Eficiencia
    nodos_por_segundo = nodos_explorados / tiempo_ejecucion if tiempo_ejecucion > 0 else 0
    
    # Factor de ramificación promedio
    nodos_con_hijos = sum(1 for n in arbol.nodos.values() if n.hijos_ids)
    total_hijos = sum(len(n.hijos_ids) for n in arbol.nodos.values())
    factor_ramificacion = total_hijos / nodos_con_hijos if nodos_con_hijos > 0 else 0
    
    # Tasa de éxito
    nodos_decision = stats_arbol['nodos_por_tipo'].get('decision', 0)
    tasa_exito = (stats_arbol['nodos_exito'] / nodos_decision * 100) if nodos_decision > 0 else 0
    
    # Camino de solución
    camino_solucion = arbol.obtener_camino_solucion()
    longitud_solucion = len(camino_solucion)
    
    return {
        # Métricas básicas
        'nodos_explorados': nodos_explorados,
        'backtracks_realizados': backtracks,
        'profundidad_maxima': profundidad_max,
        'tiempo_total': tiempo_ejecucion,
        
        # Eficiencia
        'nodos_por_segundo': nodos_por_segundo,
        'factor_ramificacion': factor_ramificacion,
        'tasa_exito': tasa_exito,
        
        # Solución
        'longitud_solucion': longitud_solucion,
        'nodos_exito': stats_arbol['nodos_exito'],
        
        # Distribución por tipo
        'nodos_por_tipo': stats_arbol['nodos_por_tipo']
    }


def imprimir_estadisticas(stats: Dict[str, Any]) -> None:
    """
    Imprime las estadísticas de forma legible.
    
    Args:
        stats: Diccionario de estadísticas
    """
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS DEL BACKTRACKING")
    print("=" * 70)
    
    print("\n🔍 EXPLORACIÓN:")
    print(f"  • Nodos explorados: {stats['nodos_explorados']:,}")
    print(f"  • Backtracks realizados: {stats['backtracks_realizados']:,}")
    print(f"  • Profundidad máxima: {stats['profundidad_maxima']}")
    
    print("\n⚡ EFICIENCIA:")
    print(f"  • Tiempo total: {stats['tiempo_total']:.2f}s")
    print(f"  • Nodos por segundo: {stats['nodos_por_segundo']:.0f}")
    print(f"  • Factor de ramificación: {stats['factor_ramificacion']:.2f}")
    print(f"  • Tasa de éxito: {stats['tasa_exito']:.1f}%")
    
    print("\n✅ SOLUCIÓN:")
    print(f"  • Longitud del camino: {stats['longitud_solucion']}")
    print(f"  • Nodos en camino exitoso: {stats['nodos_exito']}")
    
    print("\n📋 DISTRIBUCIÓN POR TIPO:")
    for tipo, cantidad in stats['nodos_por_tipo'].items():
        print(f"  • {tipo.capitalize()}: {cantidad}")
    
    print("\n" + "=" * 70)


def generar_reporte_texto(stats: Dict[str, Any], archivo_salida: str) -> None:
    """
    Genera un reporte de estadísticas en formato texto.
    
    Args:
        stats: Diccionario de estadísticas
        archivo_salida: Ruta del archivo de salida
    """
    lineas = []
    lineas.append("=" * 70)
    lineas.append("REPORTE DE ESTADÍSTICAS - ALGORITMO DE BACKTRACKING")
    lineas.append("=" * 70)
    lineas.append("")
    
    lineas.append("MÉTRICAS DE EXPLORACIÓN")
    lineas.append("-" * 70)
    lineas.append(f"Nodos explorados: {stats['nodos_explorados']:,}")
    lineas.append(f"Backtracks realizados: {stats['backtracks_realizados']:,}")
    lineas.append(f"Profundidad máxima alcanzada: {stats['profundidad_maxima']}")
    lineas.append("")
    
    lineas.append("MÉTRICAS DE EFICIENCIA")
    lineas.append("-" * 70)
    lineas.append(f"Tiempo total de ejecución: {stats['tiempo_total']:.3f} segundos")
    lineas.append(f"Nodos explorados por segundo: {stats['nodos_por_segundo']:.0f}")
    lineas.append(f"Factor de ramificación promedio: {stats['factor_ramificacion']:.2f}")
    lineas.append(f"Tasa de éxito de decisiones: {stats['tasa_exito']:.2f}%")
    lineas.append("")
    
    lineas.append("INFORMACIÓN DE LA SOLUCIÓN")
    lineas.append("-" * 70)
    lineas.append(f"Longitud del camino de solución: {stats['longitud_solucion']}")
    lineas.append(f"Nodos marcados como exitosos: {stats['nodos_exito']}")
    lineas.append("")
    
    lineas.append("DISTRIBUCIÓN DE NODOS POR TIPO")
    lineas.append("-" * 70)
    for tipo, cantidad in stats['nodos_por_tipo'].items():
        lineas.append(f"{tipo.capitalize()}: {cantidad}")
    lineas.append("")
    
    lineas.append("=" * 70)
    
    # Guardar archivo
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    
    print(f"✓ Reporte guardado en: {archivo_salida}")
