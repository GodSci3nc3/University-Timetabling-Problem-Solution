"""
Lector de archivos Excel para el Sistema de Gestión de Horarios.
Carga datos de grupos, materias y profesores desde un archivo .xlsx.
"""

import os
from typing import Tuple, List
import pandas as pd
from ..core.modelos import Grupo, Materia, Profesor


def leer_excel(ruta_archivo: str) -> Tuple[List[Grupo], List[Materia], List[Profesor]]:
    """
    Lee un archivo Excel con datos de la universidad y crea objetos del modelo.
    
    El archivo debe contener 3 hojas:
    - "Grupos": Cuatrimestre | Turno | Grupo
    - "Materias": Cuatrimestre | Materia | Horas_Semana
    - "Profesores": Nombre | Materias_Imparte | Horas_Disponibles | Turno_Preferido
    
    Args:
        ruta_archivo: Ruta al archivo .xlsx
    
    Returns:
        Tupla con (lista_grupos, lista_materias, lista_profesores)
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato del archivo es incorrecto
    """
    # Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe")
    
    try:
        # Leer todas las hojas del Excel
        excel_data = pd.read_excel(ruta_archivo, sheet_name=None)
        
        # Validar que existan las 3 hojas requeridas
        hojas_requeridas = ["Grupos", "Materias", "Profesores"]
        hojas_faltantes = [h for h in hojas_requeridas if h not in excel_data]
        
        if hojas_faltantes:
            raise ValueError(f"Faltan las siguientes hojas en el Excel: {', '.join(hojas_faltantes)}")
        
        # Cargar cada hoja
        df_grupos = excel_data["Grupos"]
        df_materias = excel_data["Materias"]
        df_profesores = excel_data["Profesores"]
        
        # Procesar grupos
        grupos = _procesar_grupos(df_grupos)
        
        # Procesar materias
        materias = _procesar_materias(df_materias, grupos)
        
        # Procesar profesores
        profesores = _procesar_profesores(df_profesores)
        
        return grupos, materias, profesores
        
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Error al leer el archivo Excel: {str(e)}")


def _procesar_grupos(df: pd.DataFrame) -> List[Grupo]:
    """
    Procesa el DataFrame de grupos y crea objetos Grupo.
    
    Args:
        df: DataFrame con columnas [Cuatrimestre, Turno, Grupo]
    
    Returns:
        Lista de objetos Grupo
    """
    grupos = []
    
    for _, row in df.iterrows():
        grupo = Grupo(
            cuatrimestre=int(row['Cuatrimestre']),
            turno=str(row['Turno']).strip(),
            nombre=str(row['Grupo']).strip()
        )
        grupos.append(grupo)
    
    return grupos


def _procesar_materias(df: pd.DataFrame, grupos: List[Grupo]) -> List[Materia]:
    """
    Procesa el DataFrame de materias y crea objetos Materia.
    Asigna automáticamente los grupos que cursan cada materia según el cuatrimestre.
    
    Args:
        df: DataFrame con columnas [Cuatrimestre, Materia, Horas_Semana]
        grupos: Lista de grupos ya procesados
    
    Returns:
        Lista de objetos Materia
    """
    materias = []
    
    for _, row in df.iterrows():
        cuatrimestre = int(row['Cuatrimestre'])
        
        # Encontrar grupos que cursan esta materia (mismo cuatrimestre)
        grupos_cursantes = [g for g in grupos if g.cuatrimestre == cuatrimestre]
        
        materia = Materia(
            nombre=str(row['Materia']).strip(),
            cuatrimestre=cuatrimestre,
            horas_semana=int(row['Horas_Semana']),
            grupos_que_cursan=grupos_cursantes
        )
        materias.append(materia)
    
    return materias


def _procesar_profesores(df: pd.DataFrame) -> List[Profesor]:
    """
    Procesa el DataFrame de profesores y crea objetos Profesor.
    Parsea la columna "Materias_Imparte" que contiene materias separadas por ";".
    Parsea la columna "Disponibilidad_Horaria" (opcional) con formato:
    "Lunes:07:00-14:00;Martes:07:00-14:00" o simplemente usa Turno_Preferido
    
    Args:
        df: DataFrame con columnas [Nombre, Materias_Imparte, Horas_Disponibles, 
                                     Turno_Preferido, Disponibilidad_Horaria (opcional)]
    
    Returns:
        Lista de objetos Profesor
    """
    profesores = []
    
    for _, row in df.iterrows():
        materias_str = str(row['Materias_Imparte'])
        materias_imparte = [m.strip() for m in materias_str.split(';') if m.strip()]
        
        disponibilidad = {}
        if 'Disponibilidad_Horaria' in row and pd.notna(row['Disponibilidad_Horaria']):
            disp_str = str(row['Disponibilidad_Horaria']).strip()
            if disp_str and disp_str.lower() != 'nan':
                for dia_rango in disp_str.split(';'):
                    if ':' in dia_rango:
                        partes = dia_rango.split(':')
                        if len(partes) >= 2:
                            dia = partes[0].strip()
                            rangos_horarios = ':'.join(partes[1:])
                            
                            if dia not in disponibilidad:
                                disponibilidad[dia] = []
                            
                            for rango in rangos_horarios.split(','):
                                if '-' in rango:
                                    inicio, fin = rango.split('-')
                                    disponibilidad[dia].append((inicio.strip(), fin.strip()))
        
        profesor = Profesor(
            nombre=str(row['Nombre']).strip(),
            materias_imparte=materias_imparte,
            horas_disponibles=int(row['Horas_Disponibles']),
            turno_preferido=str(row['Turno_Preferido']).strip(),
            disponibilidad_horaria=disponibilidad
        )
        profesores.append(profesor)
    
    return profesores
