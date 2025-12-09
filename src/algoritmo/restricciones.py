"""
Validación de restricciones para el algoritmo de backtracking.
Implementa restricciones duras (obligatorias) y blandas (preferencias).
"""

from typing import Tuple, Dict, Any, List
from ..core.modelos import Grupo, Materia, Profesor, Slot
from ..core.config import DIAS_SEMANA


def validar_restricciones_duras(
    horario: Dict,
    grupo: Grupo,
    materia: Materia,
    profesor: Profesor,
    slot: Slot,
    estado: Dict
) -> Tuple[bool, str]:
    """
    Verifica si asignar (materia, profesor) al grupo en el slot es válido.
    
    Restricciones duras verificadas:
    1. Profesor no está ocupado en ese slot
    2. Grupo no tiene otra clase en ese slot
    3. Slot está en el turno correcto del grupo
    4. Profesor tiene horas disponibles suficientes
    
    Args:
        horario: Matriz 3D de asignaciones actuales
        grupo: Grupo al que se asigna
        materia: Materia a asignar
        profesor: Profesor que impartirá
        slot: Slot de tiempo
        estado: Estado actual del algoritmo
    
    Returns:
        Tupla (es_valido, razon)
    """
    # Restricción 1: Verificar que el slot esté en el turno correcto
    if slot.turno != grupo.turno:
        return False, f"Slot {slot} no corresponde al turno {grupo.turno} del grupo {grupo.nombre}"
    
    # Restricción 2: Verificar que el grupo no tenga otra clase en ese slot
    if grupo.nombre in horario:
        if slot.dia in horario[grupo.nombre]:
            slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
            if slot_key in horario[grupo.nombre][slot.dia]:
                asignacion_existente = horario[grupo.nombre][slot.dia][slot_key]
                if asignacion_existente is not None:
                    return False, f"Grupo {grupo.nombre} ya tiene {asignacion_existente['materia']} en {slot}"
    
    # Restricción 3: Verificar que el profesor no esté ocupado en ese slot
    profesor_ocupado = estado.get('profesor_ocupado', {})
    if profesor.nombre in profesor_ocupado:
        if slot.dia in profesor_ocupado[profesor.nombre]:
            slot_key = f"{slot.hora_inicio}-{slot.hora_fin}"
            if slot_key in profesor_ocupado[profesor.nombre][slot.dia]:
                return False, f"Profesor {profesor.nombre} ya está ocupado en {slot}"
    
    # Restricción 4: Verificar que el profesor tenga horas disponibles
    horas_asignadas = estado.get('horas_asignadas_profesor', {}).get(profesor.nombre, 0)
    if horas_asignadas >= profesor.horas_disponibles:
        return False, f"Profesor {profesor.nombre} no tiene horas disponibles ({horas_asignadas}/{profesor.horas_disponibles})"
    
    # Restricción 5: Verificar compatibilidad de turno del profesor
    if profesor.turno_preferido not in ["Ambos", slot.turno]:
        return False, f"Profesor {profesor.nombre} prefiere turno {profesor.turno_preferido}, no {slot.turno}"
    
    return True, "Válido"


def calcular_score_calidad(horario: Dict, grupo_nombre: str) -> int:
    """
    Calcula el score de calidad del horario para un grupo.
    Considera restricciones blandas (preferencias).
    
    Score más alto = mejor calidad
    
    Penalizaciones:
    - Huecos entre clases: -10 puntos por hueco
    - Días sobrecargados: -5 puntos si >4 horas en un día
    
    Bonificaciones:
    - Clases agrupadas: +5 puntos por clases consecutivas
    
    Args:
        horario: Matriz 3D de asignaciones
        grupo_nombre: Nombre del grupo a evaluar
    
    Returns:
        Score de calidad (int)
    """
    if grupo_nombre not in horario:
        return 0
    
    score = 0
    horario_grupo = horario[grupo_nombre]
    
    # Evaluar cada día
    for dia in DIAS_SEMANA:
        if dia not in horario_grupo:
            continue
        
        # Obtener slots ocupados del día ordenados
        slots_ocupados = []
        for slot_key, asignacion in horario_grupo[dia].items():
            if asignacion is not None:
                hora_inicio = slot_key.split('-')[0]
                slots_ocupados.append(hora_inicio)
        
        if not slots_ocupados:
            continue
        
        slots_ocupados.sort()
        
        # Penalizar huecos entre clases
        huecos = 0
        for i in range(len(slots_ocupados) - 1):
            hora_actual = int(slots_ocupados[i].split(':')[0])
            hora_siguiente = int(slots_ocupados[i + 1].split(':')[0])
            
            # Si hay más de 1 hora de diferencia, es un hueco
            if hora_siguiente - hora_actual > 1:
                huecos += 1
        
        score -= huecos * 10
        
        # Penalizar días sobrecargados (más de 4 horas)
        if len(slots_ocupados) > 4:
            score -= 5
        
        # Bonificar clases consecutivas
        consecutivas = 0
        for i in range(len(slots_ocupados) - 1):
            hora_actual = int(slots_ocupados[i].split(':')[0])
            hora_siguiente = int(slots_ocupados[i + 1].split(':')[0])
            
            if hora_siguiente - hora_actual == 1:
                consecutivas += 1
        
        score += consecutivas * 5
    
    return score


def verificar_solucion_completa(horario: Dict, materias: List[Materia]) -> Tuple[bool, List[str]]:
    """
    Verifica que una solución esté completa y sea válida.
    
    Args:
        horario: Horario generado
        materias: Lista de materias que deben estar asignadas
    
    Returns:
        Tupla (es_completa, errores)
    """
    errores = []
    
    # Verificar que cada materia tenga todas sus horas asignadas
    for materia in materias:
        for grupo in materia.grupos_que_cursan:
            horas_asignadas = 0
            
            if grupo.nombre in horario:
                for dia in horario[grupo.nombre].values():
                    for asignacion in dia.values():
                        if asignacion and asignacion['materia'] == materia.nombre:
                            horas_asignadas += 1
            
            if horas_asignadas < materia.horas_semana:
                errores.append(
                    f"Materia {materia.nombre} para grupo {grupo.nombre}: "
                    f"{horas_asignadas}/{materia.horas_semana} horas asignadas"
                )
    
    es_completa = len(errores) == 0
    return es_completa, errores
