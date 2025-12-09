"""
Configuración del Sistema de Gestión de Horarios Académicos.
Define constantes y funciones para generar slots de tiempo.
"""

from typing import List
from .modelos import Slot

# Días de la semana laborales
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# Definición de turnos con sus horarios
TURNOS = {
    "Matutino": {
        "inicio": "07:00",
        "fin": "14:00"
    },
    "Vespertino": {
        "inicio": "14:00",
        "fin": "21:00"
    }
}

# Slots horarios para turno Matutino (7 bloques de 1 hora)
SLOTS_MATUTINO = [
    ("07:00", "08:00"),
    ("08:00", "09:00"),
    ("09:00", "10:00"),
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("12:00", "13:00"),
    ("13:00", "14:00")
]

# Slots horarios para turno Vespertino (7 bloques de 1 hora)
SLOTS_VESPERTINO = [
    ("14:00", "15:00"),
    ("15:00", "16:00"),
    ("16:00", "17:00"),
    ("17:00", "18:00"),
    ("18:00", "19:00"),
    ("19:00", "20:00"),
    ("20:00", "21:00")
]


def get_all_slots(turno: str) -> List[Slot]:
    """
    Genera todos los slots posibles para un turno dado.
    
    Args:
        turno: Nombre del turno ("Matutino" o "Vespertino")
    
    Returns:
        Lista de objetos Slot (5 días × 7 horas = 35 slots)
    
    Raises:
        ValueError: Si el turno no es válido
    """
    if turno not in ["Matutino", "Vespertino"]:
        raise ValueError(f"Turno inválido: {turno}. Debe ser 'Matutino' o 'Vespertino'")
    
    # Seleccionar los slots según el turno
    slots_horarios = SLOTS_MATUTINO if turno == "Matutino" else SLOTS_VESPERTINO
    
    # Generar todos los slots combinando días y horarios
    slots = []
    for dia in DIAS_SEMANA:
        for hora_inicio, hora_fin in slots_horarios:
            slot = Slot(
                dia=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                turno=turno
            )
            slots.append(slot)
    
    return slots
