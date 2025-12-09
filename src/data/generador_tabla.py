"""
Generador de tabla de validación para la interfaz de usuario.
Crea estructuras de datos para mostrar la distribución de materias por grupo.
"""

from typing import Dict, List
from ..core.modelos import Materia, Grupo


def generar_tabla_validacion(materias: List[Materia], grupos: List[Grupo]) -> Dict:
    """
    Genera una tabla de validación que muestra la distribución de materias por grupo.
    
    Esta tabla se usa en la interfaz para verificar visualmente la carga horaria
    de cada grupo y detectar posibles inconsistencias.
    
    Args:
        materias: Lista de materias
        grupos: Lista de grupos
    
    Returns:
        Diccionario con estructura:
        {
            "Primer cuatrimestre": {
                "Grupo 1-1": [
                    {
                        "materia": "Algoritmos",
                        "horas_materia": 6,
                        "horas_semana": 6,
                        "resta": 0
                    }
                ]
            }
        }
    """
    tabla = {}
    
    # Obtener todos los cuatrimestres únicos
    cuatrimestres = sorted(set(g.cuatrimestre for g in grupos))
    
    for cuatrimestre in cuatrimestres:
        # Nombre legible del cuatrimestre
        nombre_cuatrimestre = _obtener_nombre_cuatrimestre(cuatrimestre)
        tabla[nombre_cuatrimestre] = {}
        
        # Obtener grupos de este cuatrimestre
        grupos_cuatrimestre = [g for g in grupos if g.cuatrimestre == cuatrimestre]
        
        for grupo in grupos_cuatrimestre:
            # Obtener materias de este cuatrimestre
            materias_cuatrimestre = [m for m in materias if m.cuatrimestre == cuatrimestre]
            
            # Crear lista de materias para este grupo
            lista_materias = []
            for materia in materias_cuatrimestre:
                info_materia = {
                    "materia": materia.nombre,
                    "horas_materia": materia.horas_semana,
                    "horas_semana": materia.horas_semana,
                    "resta": 0  # Inicialmente 0, se actualizará durante la asignación
                }
                lista_materias.append(info_materia)
            
            tabla[nombre_cuatrimestre][grupo.nombre] = lista_materias
    
    return tabla


def generar_resumen_carga(materias: List[Materia], grupos: List[Grupo]) -> Dict:
    """
    Genera un resumen de la carga horaria total por cuatrimestre y grupo.
    
    Args:
        materias: Lista de materias
        grupos: Lista de grupos
    
    Returns:
        Diccionario con resumen de horas por cuatrimestre y grupo
    """
    resumen = {}
    
    cuatrimestres = sorted(set(g.cuatrimestre for g in grupos))
    
    for cuatrimestre in cuatrimestres:
        nombre_cuatrimestre = _obtener_nombre_cuatrimestre(cuatrimestre)
        
        # Calcular horas totales de materias en este cuatrimestre
        materias_cuatrimestre = [m for m in materias if m.cuatrimestre == cuatrimestre]
        horas_totales = sum(m.horas_semana for m in materias_cuatrimestre)
        
        # Contar grupos
        grupos_cuatrimestre = [g for g in grupos if g.cuatrimestre == cuatrimestre]
        num_grupos = len(grupos_cuatrimestre)
        
        resumen[nombre_cuatrimestre] = {
            "num_materias": len(materias_cuatrimestre),
            "horas_por_grupo": horas_totales,
            "num_grupos": num_grupos,
            "horas_totales_requeridas": horas_totales * num_grupos
        }
    
    return resumen


def _obtener_nombre_cuatrimestre(numero: int) -> str:
    """
    Convierte el número de cuatrimestre a nombre legible.
    
    Args:
        numero: Número del cuatrimestre (1-9)
    
    Returns:
        Nombre del cuatrimestre (ej: "Primer cuatrimestre")
    """
    nombres = {
        1: "Primer cuatrimestre",
        2: "Segundo cuatrimestre",
        3: "Tercer cuatrimestre",
        4: "Cuarto cuatrimestre",
        5: "Quinto cuatrimestre",
        6: "Sexto cuatrimestre",
        7: "Séptimo cuatrimestre",
        8: "Octavo cuatrimestre",
        9: "Noveno cuatrimestre"
    }
    
    return nombres.get(numero, f"Cuatrimestre {numero}")
