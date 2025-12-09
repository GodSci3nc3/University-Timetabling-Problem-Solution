"""
Analizador de Grafo de Conflictos.
Implementa algoritmos para analizar el grafo y estimar la factibilidad del problema.
"""

from typing import List, Tuple, Set
from .grafo_conflictos import GrafoConflictos, NodoAsignacion


def calcular_numero_cromatico_aproximado(grafo: GrafoConflictos) -> int:
    """
    Calcula una aproximación del número cromático del grafo.
    
    El número cromático es el mínimo número de colores (slots de tiempo)
    necesarios para colorear el grafo sin que nodos adyacentes compartan color.
    
    Usa el algoritmo greedy de coloreo (Welsh-Powell).
    
    Args:
        grafo: Grafo de conflictos
    
    Returns:
        Número aproximado de colores necesarios
    """
    if len(grafo.nodos) == 0:
        return 0
    
    # Ordenar nodos por grado descendente (Welsh-Powell)
    nodos_ordenados = sorted(grafo.nodos, 
                            key=lambda n: grafo.obtener_grado(n), 
                            reverse=True)
    
    # Asignar colores
    colores: dict[NodoAsignacion, int] = {}
    
    for nodo in nodos_ordenados:
        # Encontrar colores usados por vecinos
        colores_vecinos = {colores.get(vecino) for vecino in grafo.obtener_vecinos(nodo)
                          if vecino in colores}
        
        # Asignar el primer color disponible
        color = 0
        while color in colores_vecinos:
            color += 1
        
        colores[nodo] = color
    
    # El número cromático es el máximo color usado + 1
    return max(colores.values()) + 1 if colores else 0


def encontrar_cliques(grafo: GrafoConflictos, max_cliques: int = 10) -> List[Set[NodoAsignacion]]:
    """
    Encuentra cliques (conjuntos de nodos mutuamente conectados) en el grafo.
    
    Un clique representa un conjunto de asignaciones que todas tienen conflicto
    entre sí, por lo que necesitan slots diferentes.
    
    Args:
        grafo: Grafo de conflictos
        max_cliques: Número máximo de cliques a retornar
    
    Returns:
        Lista de cliques encontrados
    """
    cliques = []
    
    # Algoritmo simple: buscar triángulos (cliques de tamaño 3)
    lista_nodos = list(grafo.nodos)
    
    for i in range(len(lista_nodos)):
        for j in range(i + 1, len(lista_nodos)):
            for k in range(j + 1, len(lista_nodos)):
                nodo1, nodo2, nodo3 = lista_nodos[i], lista_nodos[j], lista_nodos[k]
                
                # Verificar si forman un triángulo
                if (nodo2 in grafo.obtener_vecinos(nodo1) and
                    nodo3 in grafo.obtener_vecinos(nodo1) and
                    nodo3 in grafo.obtener_vecinos(nodo2)):
                    
                    cliques.append({nodo1, nodo2, nodo3})
                    
                    if len(cliques) >= max_cliques:
                        return cliques
    
    return cliques


def verificar_factibilidad(grafo: GrafoConflictos, num_slots_disponibles: int) -> Tuple[bool, str]:
    """
    Verifica si es factible asignar horarios con los slots disponibles.
    
    Args:
        grafo: Grafo de conflictos
        num_slots_disponibles: Número de slots disponibles (ej: 35 para un turno)
    
    Returns:
        Tupla (es_factible, razon)
    """
    # Calcular número cromático aproximado
    num_cromatico = calcular_numero_cromatico_aproximado(grafo)
    
    if num_cromatico <= num_slots_disponibles:
        return True, f"Factible: se necesitan ~{num_cromatico} slots y hay {num_slots_disponibles} disponibles"
    else:
        deficit = num_cromatico - num_slots_disponibles
        return False, f"No factible: se necesitan ~{num_cromatico} slots pero solo hay {num_slots_disponibles} (déficit: {deficit})"


def analizar_conflictos_por_tipo(grafo: GrafoConflictos) -> dict:
    """
    Analiza los conflictos del grafo clasificándolos por tipo.
    
    Returns:
        Diccionario con estadísticas de conflictos por tipo
    """
    conflictos_grupo = 0
    conflictos_profesor = 0
    
    # Contar aristas ya procesadas para evitar duplicados
    aristas_procesadas = set()
    
    for nodo1 in grafo.nodos:
        for nodo2 in grafo.obtener_vecinos(nodo1):
            # Evitar contar la misma arista dos veces
            arista = tuple(sorted([str(nodo1), str(nodo2)]))
            if arista in aristas_procesadas:
                continue
            aristas_procesadas.add(arista)
            
            # Clasificar el tipo de conflicto
            if nodo1.grupo_nombre == nodo2.grupo_nombre:
                conflictos_grupo += 1
            else:
                conflictos_profesor += 1
    
    total = conflictos_grupo + conflictos_profesor
    
    return {
        'conflictos_grupo': conflictos_grupo,
        'conflictos_profesor': conflictos_profesor,
        'total': total,
        'porcentaje_grupo': (conflictos_grupo / total * 100) if total > 0 else 0,
        'porcentaje_profesor': (conflictos_profesor / total * 100) if total > 0 else 0
    }
