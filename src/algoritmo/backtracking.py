"""
Algoritmo de Backtracking para resolver el University Timetabling Problem.
Implementa búsqueda recursiva con poda y heurísticas para eficiencia.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from copy import deepcopy

from ..core.modelos import Grupo, Materia, Profesor
from ..core.grafo_conflictos import GrafoConflictos
from ..core.config import get_all_slots, DIAS_SEMANA

from .restricciones import validar_restricciones_duras, verificar_solucion_completa
from .heuristicas import aplicar_heuristicas_combinadas, seleccionar_mejor_slot
from .arbol_decisiones import ArbolDecisiones


def resolver_backtracking(
    grupos: List[Grupo],
    materias: List[Materia],
    profesores: List[Profesor],
    grafo: GrafoConflictos
) -> Tuple[Optional[Dict], ArbolDecisiones, Dict[str, Any]]:
    """
    Resuelve el problema de horarios usando backtracking con heurísticas.
    
    Este es el motor central del sistema. Explora el espacio de soluciones
    de manera sistemática, podando ramas que no pueden llevar a soluciones válidas.
    
    Args:
        grupos: Lista de grupos
        materias: Lista de materias
        profesores: Lista de profesores
        grafo: Grafo de conflictos
    
    Returns:
        Tupla (horario_completo, arbol_decisiones, estadisticas)
        - horario_completo: None si no hay solución
        - arbol_decisiones: Árbol con el proceso de búsqueda
        - estadisticas: Métricas del algoritmo
    """
    print("🚀 Iniciando algoritmo de Backtracking...")
    print("=" * 70)
    
    tiempo_inicio = time.time()
    
    # Inicializar estado
    estado = _inicializar_estado(grupos, materias, profesores)
    
    # Crear árbol de decisiones
    arbol = ArbolDecisiones()
    arbol.agregar_nodo('raiz', {'descripcion': 'Estado inicial'})
    
    print(f"📊 Asignaciones a realizar: {len(estado['asignaciones_pendientes'])}")
    print(f"📊 Slots disponibles por turno: 35 (5 días × 7 horas)")
    print()
    
    # Ejecutar backtracking recursivo
    print("🔍 Explorando espacio de soluciones...")
    resultado = _backtrack_recursivo(estado, 0, arbol, grafo, grupos)
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    # Generar estadísticas
    nodos_con_hijos = sum(1 for n in arbol.nodos.values() if n.hijos_ids)
    total_hijos = sum(len(n.hijos_ids) for n in arbol.nodos.values())
    factor_ramificacion = total_hijos / nodos_con_hijos if nodos_con_hijos > 0 else 0
    
    estadisticas = {
        'tiempo_total': tiempo_total,
        'nodos_explorados': len(arbol.nodos),
        'backtracks_realizados': sum(1 for n in arbol.nodos.values() if n.estado == 'fallo'),
        'profundidad_maxima': max((n.profundidad for n in arbol.nodos.values()), default=0),
        'nodos_por_segundo': len(arbol.nodos) / tiempo_total if tiempo_total > 0 else 0,
        'factor_ramificacion': factor_ramificacion,
        'tasa_exito': 100.0 if resultado else 0.0,
        'longitud_solucion': len(arbol.obtener_camino_solucion()),
        'nodos_exito': sum(1 for n in arbol.nodos.values() if n.estado == 'exito'),
        'nodos_por_tipo': {}
    }
    
    if resultado:
        print("\n✅ ¡SOLUCIÓN ENCONTRADA!")
        print("=" * 70)
        
        # Marcar camino exitoso en el árbol
        if arbol.nodo_actual_id is not None:
            arbol.marcar_exito(arbol.nodo_actual_id)
    else:
        print("\n❌ No se encontró solución válida")
        print("=" * 70)
    
    return resultado, arbol, estadisticas


def _inicializar_estado(
    grupos: List[Grupo],
    materias: List[Materia],
    profesores: List[Profesor]
) -> Dict[str, Any]:
    """
    Inicializa el estado del algoritmo.
    
    Returns:
        Diccionario con:
        - horario: Matriz 3D vacía
        - profesor_ocupado: Tracking de ocupación de profesores
        - horas_asignadas_profesor: Horas ya asignadas a cada profesor
        - asignaciones_pendientes: Cola de asignaciones por hacer
    """
    # Inicializar horario vacío (matriz 3D)
    horario = {}
    for grupo in grupos:
        horario[grupo.nombre] = {}
        for dia in DIAS_SEMANA:
            horario[grupo.nombre][dia] = {}
            # Inicializar todos los slots del turno
            slots = get_all_slots(grupo.turno)
            for slot in slots:
                if slot.dia == dia:
                    slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
                    horario[grupo.nombre][dia][slot_key] = None
    
    # Tracking de profesores
    profesor_ocupado = {p.nombre: {dia: {} for dia in DIAS_SEMANA} for p in profesores}
    horas_asignadas_profesor = {p.nombre: 0 for p in profesores}
    
    # Crear lista de asignaciones pendientes
    asignaciones_pendientes = []
    for materia in materias:
        for grupo in materia.grupos_que_cursan:
            # Encontrar profesores que pueden impartir esta materia
            profesores_posibles = [
                p for p in profesores if p.puede_impartir(materia.nombre)
            ]
            
            # Agregar asignación pendiente
            asignaciones_pendientes.append((
                grupo,
                materia,
                materia.horas_semana,  # Horas restantes
                profesores_posibles
            ))
    
    return {
        'horario': horario,
        'profesor_ocupado': profesor_ocupado,
        'horas_asignadas_profesor': horas_asignadas_profesor,
        'asignaciones_pendientes': asignaciones_pendientes
    }


def _backtrack_recursivo(
    estado: Dict,
    profundidad: int,
    arbol: ArbolDecisiones,
    grafo: GrafoConflictos,
    grupos: List[Grupo]
) -> Optional[Dict]:
    """
    Función recursiva de backtracking.
    
    Explora el árbol de decisiones usando:
    - MRV: Selecciona la asignación más restringida
    - LCV: Prueba primero los slots menos restrictivos
    - Poda: Abandona ramas que violan restricciones
    
    Args:
        estado: Estado actual del algoritmo
        profundidad: Nivel de recursión
        arbol: Árbol de decisiones
        grafo: Grafo de conflictos
        grupos: Lista de grupos
    
    Returns:
        Horario completo si se encuentra solución, None si no
    """
    # CASO BASE: No hay más asignaciones pendientes
    if not estado['asignaciones_pendientes']:
        # Verificar que la solución esté completa
        return estado['horario']
    
    # Aplicar heurísticas: MRV + Degree
    asignaciones_ordenadas = aplicar_heuristicas_combinadas(
        estado['asignaciones_pendientes'],
        estado,
        grafo,
        grupos
    )
    
    # Tomar la asignación más restringida (MRV)
    grupo, materia, horas_restantes, profesores_posibles = asignaciones_ordenadas[0]
    
    # Obtener slots disponibles para el turno del grupo
    slots_turno = get_all_slots(grupo.turno)
    
    # Aplicar LCV: ordenar slots por menos restrictivos primero
    slots_ordenados = seleccionar_mejor_slot(
        slots_turno,
        estado['horario'],
        grupo,
        materia,
        estado
    )
    
    # EXPLORAR: Probar cada combinación de slot + profesor
    for slot in slots_ordenados:
        for profesor in profesores_posibles:
            # Validar restricciones duras
            es_valido, razon = validar_restricciones_duras(
                estado['horario'],
                grupo,
                materia,
                profesor,
                slot,
                estado
            )
            
            if not es_valido:
                # Registrar conflicto en el árbol (PODA)
                arbol.agregar_nodo(
                    'conflicto',
                    {
                        'grupo': grupo.nombre,
                        'materia': materia.nombre,
                        'profesor': profesor.nombre,
                        'slot': str(slot),
                        'razon': razon
                    },
                    padre_id=arbol.nodo_actual_id
                )
                continue  # Probar siguiente opción
            
            # DECISIÓN VÁLIDA: Registrar en el árbol
            nodo_decision_id = arbol.agregar_nodo(
                'decision',
                {
                    'grupo': grupo.nombre,
                    'materia': materia.nombre,
                    'profesor': profesor.nombre,
                    'slot': str(slot),
                    'horas_restantes': horas_restantes
                },
                padre_id=arbol.nodo_actual_id
            )
            
            # Hacer asignación temporal
            _hacer_asignacion(estado, grupo, materia, profesor, slot)
            
            # RECURSIÓN: Explorar con esta decisión
            resultado = _backtrack_recursivo(estado, profundidad + 1, arbol, grafo, grupos)
            
            if resultado is not None:
                # ¡ÉXITO! Propagar solución hacia arriba
                arbol.marcar_exito(nodo_decision_id)
                return resultado
            
            # BACKTRACK: Esta decisión no llevó a solución
            arbol.marcar_backtrack(nodo_decision_id)
            _deshacer_asignacion(estado, grupo, materia, profesor, slot)
    
    # Ninguna opción funcionó: retornar None (backtrack)
    return None


def _hacer_asignacion(
    estado: Dict,
    grupo: Grupo,
    materia: Materia,
    profesor: Profesor,
    slot
) -> None:
    """
    Realiza una asignación temporal en el estado.
    
    Actualiza:
    - Horario del grupo
    - Ocupación del profesor
    - Horas asignadas al profesor
    - Lista de asignaciones pendientes
    """
    # Actualizar horario
    slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
    estado['horario'][grupo.nombre][slot.dia][slot_key] = {
        'materia': materia.nombre,
        'profesor': profesor.nombre
    }
    
    # Marcar profesor como ocupado
    estado['profesor_ocupado'][profesor.nombre][slot.dia][slot_key] = True
    
    # Incrementar horas asignadas
    estado['horas_asignadas_profesor'][profesor.nombre] += 1
    
    # Actualizar asignaciones pendientes
    for i, (g, m, horas, profs) in enumerate(estado['asignaciones_pendientes']):
        if g.nombre == grupo.nombre and m.nombre == materia.nombre:
            horas_restantes = horas - 1
            if horas_restantes > 0:
                # Actualizar horas restantes
                estado['asignaciones_pendientes'][i] = (g, m, horas_restantes, profs)
            else:
                # Asignación completa, remover de pendientes
                estado['asignaciones_pendientes'].pop(i)
            break


def _deshacer_asignacion(
    estado: Dict,
    grupo: Grupo,
    materia: Materia,
    profesor: Profesor,
    slot
) -> None:
    """
    Deshace una asignación (backtrack).
    
    Revierte todos los cambios hechos por _hacer_asignacion.
    """
    # Limpiar horario
    slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
    estado['horario'][grupo.nombre][slot.dia][slot_key] = None
    
    # Liberar profesor
    if slot_key in estado['profesor_ocupado'][profesor.nombre][slot.dia]:
        del estado['profesor_ocupado'][profesor.nombre][slot.dia][slot_key]
    
    # Decrementar horas asignadas
    estado['horas_asignadas_profesor'][profesor.nombre] -= 1
    
    # Restaurar en asignaciones pendientes
    # Buscar si ya existe
    encontrado = False
    for i, (g, m, horas, profs) in enumerate(estado['asignaciones_pendientes']):
        if g.nombre == grupo.nombre and m.nombre == materia.nombre:
            # Incrementar horas restantes
            estado['asignaciones_pendientes'][i] = (g, m, horas + 1, profs)
            encontrado = True
            break
    
    if not encontrado:
        # Agregar de nuevo a pendientes
        profesores_posibles = [
            p for p in profs if p.nombre == profesor.nombre
        ] + [p for p in profs if p.nombre != profesor.nombre]
        
        estado['asignaciones_pendientes'].append((
            grupo,
            materia,
            1,  # 1 hora pendiente
            profesores_posibles
        ))
