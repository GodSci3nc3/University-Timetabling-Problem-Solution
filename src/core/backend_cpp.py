"""
Módulo de integración con el backend C++.
Convierte datos Python a JSON, ejecuta el backend y retorna resultados.
"""

import json
import subprocess
import os
import tempfile
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

from .modelos import Grupo, Materia, Profesor


class BackendCppIntegration:
    """Integración con el backend C++ mediante JSON."""
    
    def __init__(self, backend_path: str = None):
        """
        Inicializa la integración.
        
        Args:
            backend_path: Ruta al ejecutable del backend.
                         Si es None, busca en build/horarios_backend
        """
        if backend_path is None:
            project_root = Path(__file__).parent.parent.parent
            backend_path = project_root / "build" / "horarios_backend"
        
        self.backend_path = Path(backend_path)
        
        if not self.backend_path.exists():
            raise FileNotFoundError(
                f"Backend C++ no encontrado en: {self.backend_path}\n"
                f"Ejecuta: ./compilar.sh para compilar el backend"
            )
    
    def convertir_a_json(self, grupos: List[Grupo], materias: List[Materia],
                        profesores: List[Profesor]) -> Dict:
        """Convierte los datos Python a formato JSON para el backend."""
        data = {
            "grupos": [],
            "materias": [],
            "profesores": []
        }
        
        for grupo in grupos:
            data["grupos"].append({
                "cuatrimestre": grupo.cuatrimestre,
                "turno": grupo.turno,
                "nombre": grupo.nombre
            })
        
        for materia in materias:
            data["materias"].append({
                "nombre": materia.nombre,
                "cuatrimestre": materia.cuatrimestre,
                "horas_semana": materia.horas_semana
            })
        
        for profesor in profesores:
            prof_data = {
                "nombre": profesor.nombre,
                "materias_imparte": profesor.materias_imparte,
                "horas_disponibles": profesor.horas_disponibles,
                "turno_preferido": profesor.turno_preferido
            }
            
            if profesor.disponibilidad_horaria:
                prof_data["disponibilidad_horaria"] = profesor.disponibilidad_horaria
            
            data["profesores"].append(prof_data)
        
        return data
    
    def ejecutar_backend(self, grupos: List[Grupo], materias: List[Materia],
                        profesores: List[Profesor]) -> Tuple[Optional[Dict], Dict[str, Any]]:
        """
        Ejecuta el backend C++ y retorna los resultados.
        
        Args:
            grupos: Lista de grupos
            materias: Lista de materias
            profesores: Lista de profesores
        
        Returns:
            Tupla (horario, estadisticas)
            - horario: Diccionario con el horario generado o None si falló
            - estadisticas: Métricas del algoritmo
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "input.json"
            output_file = Path(tmpdir) / "output.json"
            
            input_data = self.convertir_a_json(grupos, materias, profesores)
            
            with open(input_file, 'w') as f:
                json.dump(input_data, f, indent=2)
            
            try:
                result = subprocess.run(
                    [str(self.backend_path), str(input_file), str(output_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    raise RuntimeError(
                        f"El backend C++ falló con código {result.returncode}\n"
                        f"Salida: {result.stdout}\n"
                        f"Error: {result.stderr}"
                    )
                
                with open(output_file, 'r') as f:
                    output_data = json.load(f)
                
                exito = output_data.get("exito", False)
                horario = output_data.get("horario", {}) if exito else None
                estadisticas = output_data.get("estadisticas", {})
                
                return horario, estadisticas
                
            except subprocess.TimeoutExpired:
                raise TimeoutError("El backend C++ excedió el tiempo límite de 5 minutos")
            except FileNotFoundError:
                raise FileNotFoundError(f"No se pudo ejecutar: {self.backend_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al leer la salida del backend: {e}")


def resolver_con_backend_cpp(grupos: List[Grupo], materias: List[Materia],
                             profesores: List[Profesor]) -> Tuple[Optional[Dict], Dict[str, Any]]:
    """
    Función auxiliar para resolver horarios usando el backend C++.
    
    Args:
        grupos: Lista de grupos
        materias: Lista de materias
        profesores: Lista de profesores
    
    Returns:
        Tupla (horario, estadisticas)
    """
    backend = BackendCppIntegration()
    return backend.ejecutar_backend(grupos, materias, profesores)
