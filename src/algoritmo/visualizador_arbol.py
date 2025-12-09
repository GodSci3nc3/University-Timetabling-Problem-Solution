"""
Visualización del árbol de decisiones del backtracking.
Genera imágenes PNG usando GraphViz para mostrar el proceso de búsqueda.
"""

from typing import Optional
from graphviz import Digraph
from .arbol_decisiones import ArbolDecisiones


def visualizar_arbol_backtracking(
    arbol: ArbolDecisiones,
    output_path: str = "arbol_backtracking",
    formato: str = "png",
    max_nodos: Optional[int] = None
) -> None:
    """
    Genera visualización del árbol de decisiones usando GraphViz.
    
    Código de colores:
    - Verde: Decisión que llevó a solución (éxito)
    - Rojo: Decisión que hizo backtrack (fallo)
    - Amarillo: Conflicto detectado (poda)
    - Azul: Raíz o solución final
    - Gris: Nodo explorando
    
    Args:
        arbol: Árbol de decisiones
        output_path: Ruta base del archivo de salida (sin extensión)
        formato: Formato de salida ('png', 'pdf', 'svg')
        max_nodos: Máximo de nodos a visualizar (None = todos)
    """
    # Crear grafo dirigido
    dot = Digraph(comment='Árbol de Backtracking')
    dot.attr(rankdir='TB')  # Top to Bottom
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='8')
    
    # Determinar qué nodos mostrar
    nodos_a_mostrar = list(arbol.nodos.keys())
    if max_nodos and len(nodos_a_mostrar) > max_nodos:
        # Mostrar solo los primeros max_nodos
        nodos_a_mostrar = nodos_a_mostrar[:max_nodos]
        print(f"⚠️  Mostrando solo {max_nodos} de {len(arbol.nodos)} nodos")
    
    # Agregar nodos
    for nodo_id in nodos_a_mostrar:
        nodo = arbol.nodos[nodo_id]
        
        # Determinar color según estado y tipo
        if nodo.tipo == 'raiz':
            color = 'lightblue'
            label = "INICIO"
        elif nodo.tipo == 'conflicto':
            color = 'yellow'
            razon = nodo.datos.get('razon', 'Conflicto')
            label = f"❌ CONFLICTO\\n{razon[:30]}..."
        elif nodo.tipo == 'decision':
            if nodo.estado == 'exito':
                color = 'lightgreen'
                label_prefix = "✓"
            elif nodo.estado == 'fallo':
                color = 'lightcoral'
                label_prefix = "✗"
            else:
                color = 'lightgray'
                label_prefix = "?"
            
            # Crear label con información de la decisión
            grupo = nodo.datos.get('grupo', '')
            materia = nodo.datos.get('materia', '')[:20]
            profesor = nodo.datos.get('profesor', '')[:15]
            slot = nodo.datos.get('slot', '')
            
            label = f"{label_prefix} {grupo}\\n{materia}\\n{slot}\\nProf: {profesor}"
        else:
            color = 'white'
            label = str(nodo.tipo)
        
        # Agregar nodo al grafo
        dot.node(
            str(nodo_id),
            label,
            fillcolor=color
        )
    
    # Agregar aristas
    for nodo_id in nodos_a_mostrar:
        nodo = arbol.nodos[nodo_id]
        
        for hijo_id in nodo.hijos_ids:
            if hijo_id in nodos_a_mostrar:
                # Color de arista según estado del hijo
                hijo = arbol.nodos[hijo_id]
                if hijo.estado == 'exito':
                    edge_color = 'green'
                    edge_style = 'bold'
                elif hijo.estado == 'fallo':
                    edge_color = 'red'
                    edge_style = 'dashed'
                else:
                    edge_color = 'black'
                    edge_style = 'solid'
                
                dot.edge(
                    str(nodo_id),
                    str(hijo_id),
                    color=edge_color,
                    style=edge_style
                )
    
    # Agregar leyenda
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Leyenda', fontsize='12', style='filled', color='lightgray')
        legend.node('leg_exito', '✓ Éxito', fillcolor='lightgreen', shape='box')
        legend.node('leg_fallo', '✗ Backtrack', fillcolor='lightcoral', shape='box')
        legend.node('leg_conflicto', '❌ Conflicto', fillcolor='yellow', shape='box')
    
    # Renderizar
    try:
        dot.render(output_path, format=formato, cleanup=True)
        print(f"✓ Árbol de backtracking guardado en: {output_path}.{formato}")
    except Exception as e:
        print(f"✗ Error al generar visualización: {e}")
        print("  Asegúrate de tener GraphViz instalado en el sistema")


def visualizar_camino_solucion(
    arbol: ArbolDecisiones,
    output_path: str = "camino_solucion",
    formato: str = "png"
) -> None:
    """
    Visualiza solo el camino que llevó a la solución.
    
    Args:
        arbol: Árbol de decisiones
        output_path: Ruta base del archivo
        formato: Formato de salida
    """
    # Obtener camino de solución
    camino = arbol.obtener_camino_solucion()
    
    if not camino:
        print("⚠️  No hay camino de solución para visualizar")
        return
    
    # Crear grafo
    dot = Digraph(comment='Camino de Solución')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
    dot.attr('edge', color='green', style='bold', fontname='Arial')
    
    # Agregar solo nodos del camino
    for i, nodo_id in enumerate(camino):
        nodo = arbol.nodos[nodo_id]
        
        if nodo.tipo == 'raiz':
            label = f"INICIO\\nProfundidad: {nodo.profundidad}"
            color = 'lightblue'
        elif nodo.tipo == 'decision':
            grupo = nodo.datos.get('grupo', '')
            materia = nodo.datos.get('materia', '')
            profesor = nodo.datos.get('profesor', '')
            slot = nodo.datos.get('slot', '')
            
            label = f"Paso {i}\\n{grupo}\\n{materia}\\n{slot}\\n{profesor}"
            color = 'lightgreen'
        else:
            label = str(nodo.tipo)
            color = 'white'
        
        dot.node(str(nodo_id), label, fillcolor=color)
    
    # Agregar aristas entre nodos consecutivos del camino
    for i in range(len(camino) - 1):
        dot.edge(str(camino[i]), str(camino[i + 1]))
    
    # Renderizar
    try:
        dot.render(output_path, format=formato, cleanup=True)
        print(f"✓ Camino de solución guardado en: {output_path}.{formato}")
    except Exception as e:
        print(f"✗ Error al generar visualización: {e}")
