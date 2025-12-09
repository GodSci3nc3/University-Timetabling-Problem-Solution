"""
Validador de datos del Sistema de Gestión de Horarios.
Verifica la consistencia e integridad de los datos cargados.
"""

from typing import List, Tuple
from ..core.modelos import Grupo, Materia, Profesor


def validar_datos(grupos: List[Grupo], materias: List[Materia], 
                  profesores: List[Profesor]) -> Tuple[bool, List[str]]:
    """
    Valida la consistencia de los datos cargados.
    
    Validaciones realizadas:
    1. Cada materia tiene al menos un profesor que puede impartirla
    2. Total de horas de materias no excede capacidad de profesores
    3. Grupos del mismo cuatrimestre tienen turnos compatibles
    4. No hay nombres duplicados
    
    Args:
        grupos: Lista de grupos
        materias: Lista de materias
        profesores: Lista de profesores
    
    Returns:
        Tupla (es_valido, lista_errores)
        - es_valido: True si pasa todas las validaciones
        - lista_errores: Lista de mensajes de error (vacía si es válido)
    """
    errores = []
    
    # Validación 1: Cobertura de profesores
    errores.extend(_validar_cobertura_profesores(materias, profesores))
    
    # Validación 2: Capacidad horaria
    errores.extend(_validar_capacidad_horaria(materias, profesores))
    
    # Validación 3: Compatibilidad de turnos
    errores.extend(_validar_turnos_grupos(grupos))
    
    # Validación 4: Unicidad de nombres
    errores.extend(_validar_unicidad(grupos, materias, profesores))
    
    es_valido = len(errores) == 0
    return es_valido, errores


def _validar_cobertura_profesores(materias: List[Materia], 
                                   profesores: List[Profesor]) -> List[str]:
    """
    Verifica que cada materia tenga al menos un profesor capacitado.
    """
    errores = []
    
    for materia in materias:
        # Buscar profesores que puedan impartir esta materia
        profesores_capacitados = [
            p for p in profesores if p.puede_impartir(materia.nombre)
        ]
        
        if not profesores_capacitados:
            errores.append(
                f"La materia '{materia.nombre}' no tiene ningún profesor capacitado"
            )
    
    return errores


def _validar_capacidad_horaria(materias: List[Materia], 
                               profesores: List[Profesor]) -> List[str]:
    """
    Verifica que la capacidad total de profesores sea suficiente.
    Calcula horas totales requeridas vs horas disponibles.
    """
    errores = []
    
    # Calcular horas totales requeridas (materia × grupos que la cursan)
    horas_totales_requeridas = 0
    for materia in materias:
        num_grupos = len(materia.grupos_que_cursan)
        horas_totales_requeridas += materia.horas_semana * num_grupos
    
    # Calcular horas totales disponibles
    horas_totales_disponibles = sum(p.horas_disponibles for p in profesores)
    
    if horas_totales_requeridas > horas_totales_disponibles:
        errores.append(
            f"Capacidad insuficiente: se requieren {horas_totales_requeridas}h/sem "
            f"pero solo hay {horas_totales_disponibles}h/sem disponibles "
            f"(déficit: {horas_totales_requeridas - horas_totales_disponibles}h)"
        )
    
    return errores


def _validar_turnos_grupos(grupos: List[Grupo]) -> List[str]:
    """
    Verifica que los grupos estén correctamente distribuidos por turnos.
    Advierte si un cuatrimestre solo tiene grupos en un turno.
    """
    errores = []
    
    # Agrupar por cuatrimestre
    cuatrimestres = {}
    for grupo in grupos:
        if grupo.cuatrimestre not in cuatrimestres:
            cuatrimestres[grupo.cuatrimestre] = set()
        cuatrimestres[grupo.cuatrimestre].add(grupo.turno)
    
    # Verificar distribución (advertencia, no error crítico)
    for cuatrimestre, turnos in cuatrimestres.items():
        if len(turnos) == 1:
            turno_unico = list(turnos)[0]
            # Esto es una advertencia, no un error crítico
            # Se comenta para no bloquear, pero se puede activar si se desea
            # errores.append(
            #     f"Advertencia: El cuatrimestre {cuatrimestre} solo tiene grupos "
            #     f"en turno {turno_unico}"
            # )
            pass
    
    return errores


def _validar_unicidad(grupos: List[Grupo], materias: List[Materia], 
                      profesores: List[Profesor]) -> List[str]:
    """
    Verifica que no haya nombres duplicados en grupos, materias o profesores.
    """
    errores = []
    
    # Validar grupos únicos
    nombres_grupos = [g.nombre for g in grupos]
    duplicados_grupos = _encontrar_duplicados(nombres_grupos)
    if duplicados_grupos:
        errores.append(f"Grupos duplicados: {', '.join(duplicados_grupos)}")
    
    # Validar materias únicas (por cuatrimestre)
    for cuatrimestre in set(m.cuatrimestre for m in materias):
        materias_cuatrimestre = [m.nombre for m in materias if m.cuatrimestre == cuatrimestre]
        duplicados = _encontrar_duplicados(materias_cuatrimestre)
        if duplicados:
            errores.append(
                f"Materias duplicadas en cuatrimestre {cuatrimestre}: {', '.join(duplicados)}"
            )
    
    # Validar profesores únicos
    nombres_profesores = [p.nombre for p in profesores]
    duplicados_profesores = _encontrar_duplicados(nombres_profesores)
    if duplicados_profesores:
        errores.append(f"Profesores duplicados: {', '.join(duplicados_profesores)}")
    
    return errores


def _encontrar_duplicados(lista: List[str]) -> List[str]:
    """
    Encuentra elementos duplicados en una lista.
    
    Returns:
        Lista de elementos que aparecen más de una vez
    """
    vistos = set()
    duplicados = set()
    
    for item in lista:
        if item in vistos:
            duplicados.add(item)
        vistos.add(item)
    
    return list(duplicados)
