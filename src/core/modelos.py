"""
Modelos de datos del Sistema de Gestión de Horarios Académicos.
Define las clases principales del dominio.
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Grupo:
    """
    Representa un grupo de estudiantes.
    
    Attributes:
        cuatrimestre: Número del cuatrimestre (1-9)
        turno: Turno del grupo ("Matutino" o "Vespertino")
        nombre: Identificador del grupo (ej: "ITI 5-1")
    """
    cuatrimestre: int
    turno: str
    nombre: str
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.turno})"


@dataclass
class Materia:
    """
    Representa una materia del plan de estudios.
    
    Attributes:
        nombre: Nombre de la materia
        cuatrimestre: Cuatrimestre al que pertenece
        horas_semana: Horas semanales requeridas
        grupos_que_cursan: Lista de grupos que cursan esta materia
    """
    nombre: str
    cuatrimestre: int
    horas_semana: int
    grupos_que_cursan: List[Grupo] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.horas_semana}h/sem)"


@dataclass
class Profesor:
    """
    Representa un profesor de la universidad.
    
    Attributes:
        nombre: Nombre completo del profesor
        materias_imparte: Lista de materias que puede impartir
        horas_disponibles: Total de horas disponibles por semana
        turno_preferido: Turno de preferencia ("Matutino", "Vespertino" o "Ambos")
        disponibilidad_horaria: Dict con disponibilidad por día y rango horario
                               Formato: {"Lunes": [("07:00", "14:00")], ...}
                               Si está vacío, usa turno_preferido por compatibilidad
        horas_asignadas: Horas ya asignadas (se actualiza durante la generación)
    """
    nombre: str
    materias_imparte: List[str]
    horas_disponibles: int
    turno_preferido: str
    disponibilidad_horaria: dict = field(default_factory=dict)
    horas_asignadas: int = 0
    
    def puede_impartir(self, materia: str) -> bool:
        """Verifica si el profesor puede impartir una materia."""
        return materia in self.materias_imparte
    
    def tiene_disponibilidad(self, horas: int) -> bool:
        """Verifica si el profesor tiene disponibilidad para más horas."""
        return (self.horas_asignadas + horas) <= self.horas_disponibles
    
    def esta_disponible_en_slot(self, dia: str, hora_inicio: str, hora_fin: str) -> bool:
        """
        Verifica si el profesor está disponible en un slot específico.
        
        Args:
            dia: Día de la semana
            hora_inicio: Hora de inicio del slot (formato "HH:MM")
            hora_fin: Hora de fin del slot (formato "HH:MM")
        
        Returns:
            True si está disponible, False si no
        """
        if not self.disponibilidad_horaria:
            return True
        
        if dia not in self.disponibilidad_horaria:
            return False
        
        hora_slot_inicio = int(hora_inicio.split(':')[0])
        hora_slot_fin = int(hora_fin.split(':')[0])
        
        for rango_inicio, rango_fin in self.disponibilidad_horaria[dia]:
            hora_rango_inicio = int(rango_inicio.split(':')[0])
            hora_rango_fin = int(rango_fin.split(':')[0])
            
            if hora_slot_inicio >= hora_rango_inicio and hora_slot_fin <= hora_rango_fin:
                return True
        
        return False
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.horas_asignadas}/{self.horas_disponibles}h)"


@dataclass
class Slot:
    """
    Representa un bloque de tiempo en el horario.
    
    Attributes:
        dia: Día de la semana
        hora_inicio: Hora de inicio (formato "HH:MM")
        hora_fin: Hora de fin (formato "HH:MM")
        turno: Turno al que pertenece
    """
    dia: str
    hora_inicio: str
    hora_fin: str
    turno: str
    
    def __str__(self) -> str:
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin}"


@dataclass
class Asignacion:
    """
    Representa la asignación de una materia a un slot específico.
    
    Attributes:
        grupo: Grupo que recibe la clase
        materia: Materia que se imparte
        profesor: Profesor que imparte la clase
        slot: Slot de tiempo asignado
    """
    grupo: Grupo
    materia: Materia
    profesor: Profesor
    slot: Slot
    
    def __str__(self) -> str:
        return f"{self.grupo.nombre} - {self.materia.nombre} - {self.profesor.nombre} @ {self.slot}"
