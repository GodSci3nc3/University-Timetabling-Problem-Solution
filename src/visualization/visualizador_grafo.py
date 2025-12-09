"""
Visualizador de Grafo de Conflictos.
Genera visualizaciones del grafo usando networkx y matplotlib.
"""

import os
from typing import Optional
import matplotlib.pyplot as plt
import networkx as nx
from ..core.grafo_conflictos import GrafoConflictos, NodoAsignacion


# Paleta de colores para cuatrimestres
COLORES_CUATRIMESTRE = {
    1: '#FF6B6B',  # Rojo
    2: '#4ECDC4',  # Turquesa
    3: '#45B7D1',  # Azul
    4: '#FFA07A',  # Salmón
    5: '#98D8C8',  # Verde menta
    6: '#F7DC6F',  # Amarillo
    7: '#BB8FCE',  # Púrpura
    8: '#85C1E2',  # Azul claro
    9: '#F8B88B',  # Naranja
}


def visualizar_grafo(grafo: GrafoConflictos, titulo: str = "Grafo de Conflictos",
                     guardar_como: Optional[str] = None, mostrar: bool = False) -> None:
    """
    Visualiza el grafo de conflictos usando networkx y matplotlib.
    
    Args:
        grafo: Grafo de conflictos a visualizar
        titulo: Título del gráfico
        guardar_como: Ruta donde guardar la imagen (None para no guardar)
        mostrar: Si True, muestra la imagen en pantalla
    """
    # Crear grafo de networkx
    G = nx.Graph()
    
    # Agregar nodos
    for nodo in grafo.nodos:
        G.add_node(str(nodo), cuatrimestre=nodo.cuatrimestre)
    
    # Agregar aristas
    for nodo1 in grafo.nodos:
        for nodo2 in grafo.obtener_vecinos(nodo1):
            G.add_edge(str(nodo1), str(nodo2))
    
    # Configurar figura
    plt.figure(figsize=(16, 12))
    
    # Layout del grafo (spring layout para distribución automática)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Colorear nodos por cuatrimestre
    colores_nodos = [COLORES_CUATRIMESTRE.get(G.nodes[nodo]['cuatrimestre'], '#CCCCCC') 
                     for nodo in G.nodes()]
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, 
                          node_color=colores_nodos,
                          node_size=800,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)
    
    # Dibujar aristas
    nx.draw_networkx_edges(G, pos,
                          edge_color='#E74C3C',
                          width=1.5,
                          alpha=0.4)
    
    # Dibujar etiquetas
    labels = {str(nodo): f"{nodo.grupo_nombre}\n{nodo.materia_nombre[:15]}..." 
              if len(nodo.materia_nombre) > 15 
              else f"{nodo.grupo_nombre}\n{nodo.materia_nombre}"
              for nodo in grafo.nodos}
    
    nx.draw_networkx_labels(G, pos,
                           labels,
                           font_size=7,
                           font_weight='bold')
    
    # Título y estadísticas
    stats = grafo.obtener_estadisticas()
    plt.title(f"{titulo}\n"
             f"Nodos: {stats['num_nodos']} | Aristas: {stats['num_aristas']} | "
             f"Grado promedio: {stats['grado_promedio']:.2f}",
             fontsize=16, fontweight='bold', pad=20)
    
    # Leyenda de cuatrimestres
    cuatrimestres_presentes = sorted(set(nodo.cuatrimestre for nodo in grafo.nodos))
    leyenda_elementos = [plt.Line2D([0], [0], marker='o', color='w', 
                                   markerfacecolor=COLORES_CUATRIMESTRE.get(c, '#CCC'),
                                   markersize=10, label=f'{c}° Cuatrimestre')
                        for c in cuatrimestres_presentes]
    
    plt.legend(handles=leyenda_elementos, loc='upper left', fontsize=10)
    
    plt.axis('off')
    plt.tight_layout()
    
    # Guardar si se especifica ruta
    if guardar_como:
        plt.savefig(guardar_como, dpi=300, bbox_inches='tight')
        print(f"✓ Grafo guardado en: {guardar_como}")
    
    # Mostrar si se solicita
    if mostrar:
        plt.show()
    else:
        plt.close()


def visualizar_por_cuatrimestre(grafo: GrafoConflictos, cuatrimestre: int,
                                guardar_como: Optional[str] = None) -> None:
    """
    Visualiza solo los nodos de un cuatrimestre específico.
    
    Args:
        grafo: Grafo de conflictos completo
        cuatrimestre: Número del cuatrimestre a visualizar
        guardar_como: Ruta donde guardar la imagen
    """
    # Filtrar nodos del cuatrimestre
    nodos_filtrados = {nodo for nodo in grafo.nodos if nodo.cuatrimestre == cuatrimestre}
    
    # Crear subgrafo
    G = nx.Graph()
    
    for nodo in nodos_filtrados:
        G.add_node(str(nodo))
    
    for nodo1 in nodos_filtrados:
        for nodo2 in grafo.obtener_vecinos(nodo1):
            if nodo2 in nodos_filtrados:
                G.add_edge(str(nodo1), str(nodo2))
    
    # Configurar figura
    plt.figure(figsize=(14, 10))
    
    # Layout
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Dibujar
    nx.draw_networkx_nodes(G, pos,
                          node_color=COLORES_CUATRIMESTRE.get(cuatrimestre, '#CCC'),
                          node_size=1000,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)
    
    nx.draw_networkx_edges(G, pos,
                          edge_color='#E74C3C',
                          width=2,
                          alpha=0.5)
    
    # Etiquetas más grandes para subgrafo
    labels = {str(nodo): f"{nodo.grupo_nombre}\n{nodo.materia_nombre}"
              for nodo in nodos_filtrados}
    
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')
    
    plt.title(f"Grafo de Conflictos - {cuatrimestre}° Cuatrimestre\n"
             f"Nodos: {len(nodos_filtrados)} | Aristas: {G.number_of_edges()}",
             fontsize=16, fontweight='bold', pad=20)
    
    plt.axis('off')
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=300, bbox_inches='tight')
        print(f"✓ Grafo del cuatrimestre {cuatrimestre} guardado en: {guardar_como}")
    else:
        plt.show()


def generar_reporte_conflictos(grafo: GrafoConflictos, archivo_salida: Optional[str] = None) -> str:
    """
    Genera un reporte textual detallado de los conflictos del grafo.
    
    Args:
        grafo: Grafo de conflictos
        archivo_salida: Ruta donde guardar el reporte (None para solo retornar)
    
    Returns:
        String con el reporte completo
    """
    lineas = []
    lineas.append("=" * 80)
    lineas.append("REPORTE DE CONFLICTOS DEL GRAFO")
    lineas.append("=" * 80)
    lineas.append("")
    
    # Estadísticas generales
    stats = grafo.obtener_estadisticas()
    lineas.append("ESTADÍSTICAS GENERALES")
    lineas.append("-" * 80)
    lineas.append(f"Nodos totales: {stats['num_nodos']}")
    lineas.append(f"Aristas totales: {stats['num_aristas']}")
    lineas.append(f"Grado promedio: {stats['grado_promedio']:.2f}")
    lineas.append(f"Grado máximo: {stats['grado_maximo']}")
    lineas.append(f"Grado mínimo: {stats['grado_minimo']}")
    lineas.append(f"Densidad del grafo: {stats['densidad']:.4f}")
    lineas.append("")
    
    # Distribución por cuatrimestre
    lineas.append("DISTRIBUCIÓN POR CUATRIMESTRE")
    lineas.append("-" * 80)
    for cuatri, num_nodos in sorted(stats['nodos_por_cuatrimestre'].items()):
        lineas.append(f"Cuatrimestre {cuatri}: {num_nodos} asignaciones")
    lineas.append("")
    
    # Nodos más conflictivos
    lineas.append("TOP 10 ASIGNACIONES MÁS CONFLICTIVAS")
    lineas.append("-" * 80)
    nodos_conflictivos = grafo.obtener_nodos_mas_conflictivos(10)
    
    for i, (nodo, grado) in enumerate(nodos_conflictivos, 1):
        lineas.append(f"{i}. {nodo} - {grado} conflictos")
    
    lineas.append("")
    lineas.append("=" * 80)
    
    reporte = "\n".join(lineas)
    
    # Guardar si se especifica archivo
    if archivo_salida:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(reporte)
        print(f"✓ Reporte guardado en: {archivo_salida}")
    
    return reporte
