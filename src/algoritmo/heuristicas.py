"""
Heurísticas para optimizar el algoritmo de backtracking.
Implementa MRV, Degree Heuristic y LCV para reducir el espacio de búsqueda.
"""

from typing import List, Tuple, Dict, Any
from ..core.modelos import Grupo, Materia, Profesor, Slot
from ..core.grafo_conflictos import GrafoConflictos, NodoAsignacion
from ..core.config import get_all_slots


def ordenar_por_mrv(
    asignaciones_pendientes: List[Tuple],
    estado: Dict,
    grupos: List[Grupo]
) -> List[Tuple]:
    """
    MRV (Minimum Remaining Values): Ordena asignaciones por número de slots disponibles.
    
    Coloca primero las asignaciones con MENOS slots disponibles (más restringidas).
    Esto implementa la estrategia "fail-fast": detectar callejones sin salida temprano.
    
    Args:
        asignaciones_pendientes: Lista de (grupo, materia, horas_restantes, profesores)
        estado: Estado actual del algoritmo
        grupos: Lista de todos los grupos
    
    Returns:
        Lista ordenada de asignaciones (más restringida primero)
    """
    def contar_slots_disponibles(asignacion: Tuple) -> int:
        """Cuenta cuántos slots están disponibles para una asignación."""
        grupo_obj, materia, horas_restantes, profesores = asignacion
        
        # Obtener todos los slots del turno del grupo
        slots_turno = get_all_slots(grupo_obj.turno)
        
        # Contar slots realmente disponibles
        slots_disponibles = 0
        horario = estado['horario']
        
        for slot in slots_turno:
            # Verificar si el slot está libre para el grupo
            if grupo_obj.nombre in horario:
                if slot.dia in horario[grupo_obj.nombre]:
                    slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
                    if slot_key in horario[grupo_obj.nombre][slot.dia]:
                        if horario[grupo_obj.nombre][slot.dia][slot_key] is not None:
                            continue  # Slot ocupado
            
            slots_disponibles += 1
        
        return slots_disponibles
    
    # Ordenar por número de slots disponibles (ascendente)
    return sorted(asignaciones_pendientes, key=contar_slots_disponibles)


def ordenar_por_degree(
    asignaciones_pendientes: List[Tuple],
    grafo: GrafoConflictos
) -> List[Tuple]:
    """
    Degree Heuristic: Ordena asignaciones por número de conflictos en el grafo.
    
    Coloca primero las asignaciones con MÁS conflictos (mayor grado en el grafo).
    Útil como criterio de desempate cuando MRV da el mismo valor.
    
    Args:
        asignaciones_pendientes: Lista de asignaciones
        grafo: Grafo de conflictos
    
    Returns:
        Lista ordenada por grado (más conflictos primero)
    """
    def obtener_grado(asignacion: Tuple) -> int:
        """Obtiene el grado del nodo en el grafo de conflictos."""
        grupo_obj, materia, _, _ = asignacion
        
        # Crear nodo correspondiente
        nodo = NodoAsignacion(
            grupo_nombre=grupo_obj.nombre,
            materia_nombre=materia.nombre,
            cuatrimestre=materia.cuatrimestre
        )
        
        # Obtener grado del grafo
        if nodo in grafo.nodos:
            return grafo.obtener_grado(nodo)
        return 0
    
    # Ordenar por grado (descendente)
    return sorted(asignaciones_pendientes, key=obtener_grado, reverse=True)


def seleccionar_mejor_slot(
    slots_disponibles: List[Slot],
    horario: Dict,
    grupo: Grupo,
    materia: Materia,
    estado: Dict
) -> List[Slot]:
    """
    LCV (Least Constraining Value): Ordena slots por cuánto restringen futuras asignaciones.
    
    Elige primero los slots que MENOS restrinjan las decisiones futuras.
    Esto maximiza las opciones para asignaciones posteriores.
    
    Args:
        slots_disponibles: Lista de slots candidatos
        horario: Horario actual
        grupo: Grupo a asignar
        materia: Materia a asignar
        estado: Estado actual
    
    Returns:
        Lista de slots ordenada (menos restrictivo primero)
    """
    def calcular_restriccion(slot: Slot) -> int:
        """
        Calcula cuántas futuras asignaciones se restringirían con este slot.
        Valor más bajo = menos restrictivo = mejor.
        """
        restriccion = 0
        
        # Factor 1: Slots ya ocupados en ese día para el grupo
        if grupo.nombre in horario:
            if slot.dia in horario[grupo.nombre]:
                ocupados = sum(1 for v in horario[grupo.nombre][slot.dia].values() if v is not None)
                restriccion += ocupados * 2  # Penalizar días ya ocupados
        
        # Factor 2: Horas tempranas son más valiosas (menos restricción)
        hora = int(slot.hora_inicio.split(':')[0])
        if hora < 10:  # Horas tempranas
            restriccion -= 3
        elif hora > 18:  # Horas tardías
            restriccion += 3
        
        # Factor 3: Preferir días con menos carga
        dias_carga = {}
        if grupo.nombre in horario:
            for dia, slots_dia in horario[grupo.nombre].items():
                carga = sum(1 for v in slots_dia.values() if v is not None)
                dias_carga[dia] = carga
        
        carga_dia_actual = dias_carga.get(slot.dia, 0)
        restriccion += carga_dia_actual
        
        return restriccion
    
    # Ordenar por restricción (ascendente = menos restrictivo primero)
    return sorted(slots_disponibles, key=calcular_restriccion)


def aplicar_heuristicas_combinadas(
    asignaciones_pendientes: List[Tuple],
    estado: Dict,
    grafo: GrafoConflictos,
    grupos: List[Grupo]
) -> List[Tuple]:
    """
    Aplica MRV y Degree Heuristic combinadas.
    
    Primero ordena por MRV (menos slots disponibles).
    En caso de empate, usa Degree (más conflictos).
    
    Args:
        asignaciones_pendientes: Lista de asignaciones
        estado: Estado actual
        grafo: Grafo de conflictos
        grupos: Lista de grupos
    
    Returns:
        Lista ordenada con heurísticas combinadas
    """
    # Primero aplicar MRV
    ordenadas_mrv = ordenar_por_mrv(asignaciones_pendientes, estado, grupos)
    
    # Luego aplicar Degree como desempate
    # (En caso de que MRV dé el mismo valor)
    ordenadas_final = ordenar_por_degree(ordenadas_mrv, grafo)
    
    return ordenadas_final
