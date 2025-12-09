"""
Grafo de Conflictos para el University Timetabling Problem.
Modela las restricciones del problema usando teoría de grafos.
"""

from typing import Set, Dict, List, Tuple
from dataclasses import dataclass
from ..core.modelos import Grupo, Materia, Profesor


@dataclass(frozen=True)
class NodoAsignacion:
    """
    Representa un nodo en el grafo de conflictos.
    Cada nodo es una asignación (grupo, materia) que debe hacerse.
    
    Attributes:
        grupo_nombre: Nombre del grupo (ej: "ITI 5-1")
        materia_nombre: Nombre de la materia
        cuatrimestre: Cuatrimestre al que pertenece
    """
    grupo_nombre: str
    materia_nombre: str
    cuatrimestre: int
    
    def __str__(self) -> str:
        return f"({self.grupo_nombre}, {self.materia_nombre})"
    
    def __hash__(self) -> int:
        return hash((self.grupo_nombre, self.materia_nombre))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, NodoAsignacion):
            return False
        return (self.grupo_nombre == other.grupo_nombre and 
                self.materia_nombre == other.materia_nombre)


class GrafoConflictos:
    """
    Grafo que representa los conflictos en el problema de horarios.
    
    - Nodos: Asignaciones (grupo, materia)
    - Aristas: Conflictos entre asignaciones
    
    Tipos de conflictos:
    1. Mismo grupo: Un grupo no puede tener 2 clases simultáneamente
    2. Mismo profesor: Un profesor no puede estar en 2 lugares a la vez
    """
    
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.nodos: Set[NodoAsignacion] = set()
        # Lista de adyacencia: nodo -> conjunto de nodos en conflicto
        self.aristas: Dict[NodoAsignacion, Set[NodoAsignacion]] = {}
        # Mapeo de materia -> profesores que la imparten
        self.profesores_por_materia: Dict[str, List[str]] = {}
    
    def construir_desde_datos(self, grupos: List[Grupo], materias: List[Materia], 
                              profesores: List[Profesor]) -> None:
        """
        Construye el grafo completo desde los datos cargados.
        
        Args:
            grupos: Lista de grupos
            materias: Lista de materias
            profesores: Lista de profesores
        """
        # Paso 1: Construir mapeo de profesores por materia
        self._construir_mapeo_profesores(profesores)
        
        # Paso 2: Crear todos los nodos (una asignación por cada grupo-materia)
        for materia in materias:
            for grupo in materia.grupos_que_cursan:
                nodo = NodoAsignacion(
                    grupo_nombre=grupo.nombre,
                    materia_nombre=materia.nombre,
                    cuatrimestre=materia.cuatrimestre
                )
                self.agregar_nodo(nodo)
        
        # Paso 3: Detectar y agregar aristas de conflicto
        lista_nodos = list(self.nodos)
        for i in range(len(lista_nodos)):
            for j in range(i + 1, len(lista_nodos)):
                nodo1 = lista_nodos[i]
                nodo2 = lista_nodos[j]
                
                if self._tiene_conflicto(nodo1, nodo2):
                    self.agregar_arista(nodo1, nodo2)
    
    def _construir_mapeo_profesores(self, profesores: List[Profesor]) -> None:
        """Construye el mapeo de materia -> lista de profesores."""
        for profesor in profesores:
            for materia in profesor.materias_imparte:
                if materia not in self.profesores_por_materia:
                    self.profesores_por_materia[materia] = []
                self.profesores_por_materia[materia].append(profesor.nombre)
    
    def _tiene_conflicto(self, nodo1: NodoAsignacion, nodo2: NodoAsignacion) -> bool:
        """
        Verifica si dos nodos tienen conflicto.
        
        Returns:
            True si existe conflicto (deben conectarse con arista)
        """
        # Conflicto Tipo 1: Mismo grupo
        if nodo1.grupo_nombre == nodo2.grupo_nombre:
            return True
        
        # Conflicto Tipo 2: Mismo profesor
        if self._comparten_profesor(nodo1.materia_nombre, nodo2.materia_nombre):
            return True
        
        return False
    
    def _comparten_profesor(self, materia1: str, materia2: str) -> bool:
        """Verifica si dos materias pueden ser impartidas por el mismo profesor."""
        profesores1 = set(self.profesores_por_materia.get(materia1, []))
        profesores2 = set(self.profesores_por_materia.get(materia2, []))
        
        # Si tienen profesores en común, pueden tener conflicto
        return len(profesores1 & profesores2) > 0
    
    def agregar_nodo(self, nodo: NodoAsignacion) -> None:
        """Agrega un nodo al grafo."""
        self.nodos.add(nodo)
        if nodo not in self.aristas:
            self.aristas[nodo] = set()
    
    def agregar_arista(self, nodo1: NodoAsignacion, nodo2: NodoAsignacion) -> None:
        """
        Agrega una arista bidireccional entre dos nodos.
        Representa un conflicto entre dos asignaciones.
        """
        self.aristas[nodo1].add(nodo2)
        self.aristas[nodo2].add(nodo1)
    
    def obtener_vecinos(self, nodo: NodoAsignacion) -> Set[NodoAsignacion]:
        """Retorna el conjunto de nodos en conflicto con el nodo dado."""
        return self.aristas.get(nodo, set())
    
    def obtener_grado(self, nodo: NodoAsignacion) -> int:
        """Retorna el número de conflictos (grado) de un nodo."""
        return len(self.obtener_vecinos(nodo))
    
    def obtener_estadisticas(self) -> Dict:
        """
        Calcula estadísticas del grafo.
        
        Returns:
            Diccionario con métricas del grafo
        """
        num_nodos = len(self.nodos)
        num_aristas = sum(len(vecinos) for vecinos in self.aristas.values()) // 2
        
        grados = [self.obtener_grado(nodo) for nodo in self.nodos]
        grado_promedio = sum(grados) / num_nodos if num_nodos > 0 else 0
        grado_maximo = max(grados) if grados else 0
        grado_minimo = min(grados) if grados else 0
        
        # Nodos por cuatrimestre
        nodos_por_cuatrimestre = {}
        for nodo in self.nodos:
            cuatri = nodo.cuatrimestre
            nodos_por_cuatrimestre[cuatri] = nodos_por_cuatrimestre.get(cuatri, 0) + 1
        
        return {
            'num_nodos': num_nodos,
            'num_aristas': num_aristas,
            'grado_promedio': grado_promedio,
            'grado_maximo': grado_maximo,
            'grado_minimo': grado_minimo,
            'nodos_por_cuatrimestre': nodos_por_cuatrimestre,
            'densidad': (2 * num_aristas) / (num_nodos * (num_nodos - 1)) if num_nodos > 1 else 0
        }
    
    def obtener_nodos_mas_conflictivos(self, n: int = 5) -> List[Tuple[NodoAsignacion, int]]:
        """
        Retorna los n nodos con más conflictos.
        
        Returns:
            Lista de tuplas (nodo, grado) ordenadas por grado descendente
        """
        nodos_con_grado = [(nodo, self.obtener_grado(nodo)) for nodo in self.nodos]
        nodos_con_grado.sort(key=lambda x: x[1], reverse=True)
        return nodos_con_grado[:n]
