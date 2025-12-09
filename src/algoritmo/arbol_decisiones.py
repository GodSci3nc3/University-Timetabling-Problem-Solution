"""
Estructura de árbol de decisiones para registrar el proceso de backtracking.
Permite visualizar y analizar el espacio de búsqueda explorado.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import json


@dataclass
class NodoArbol:
    """
    Representa un nodo en el árbol de decisiones del backtracking.
    
    Attributes:
        id: Identificador único del nodo
        tipo: 'decision', 'conflicto', 'solucion', 'backtrack'
        datos: Información de la asignación o conflicto
        padre_id: ID del nodo padre (None para raíz)
        hijos_ids: Lista de IDs de nodos hijos
        estado: 'explorando', 'exito', 'fallo'
        profundidad: Nivel en el árbol
    """
    id: int
    tipo: str  # 'decision', 'conflicto', 'solucion', 'backtrack'
    datos: Dict[str, Any]
    padre_id: Optional[int] = None
    hijos_ids: List[int] = field(default_factory=list)
    estado: str = 'explorando'  # 'explorando', 'exito', 'fallo'
    profundidad: int = 0


class ArbolDecisiones:
    """
    Árbol que registra todas las decisiones tomadas durante el backtracking.
    
    Permite:
    - Visualizar el proceso de búsqueda
    - Analizar qué caminos se exploraron
    - Identificar dónde ocurrieron backtracks
    - Generar estadísticas del algoritmo
    """
    
    def __init__(self):
        """Inicializa un árbol vacío."""
        self.nodos: Dict[int, NodoArbol] = {}
        self.siguiente_id = 0
        self.raiz_id: Optional[int] = None
        self.nodo_actual_id: Optional[int] = None
    
    def agregar_nodo(
        self,
        tipo: str,
        datos: Dict[str, Any],
        padre_id: Optional[int] = None
    ) -> int:
        """
        Agrega un nuevo nodo al árbol.
        
        Args:
            tipo: Tipo de nodo ('decision', 'conflicto', etc.)
            datos: Información del nodo
            padre_id: ID del padre (None para raíz)
        
        Returns:
            ID del nodo creado
        """
        nodo_id = self.siguiente_id
        self.siguiente_id += 1
        
        # Determinar profundidad
        profundidad = 0
        if padre_id is not None and padre_id in self.nodos:
            profundidad = self.nodos[padre_id].profundidad + 1
        
        # Crear nodo
        nodo = NodoArbol(
            id=nodo_id,
            tipo=tipo,
            datos=datos,
            padre_id=padre_id,
            profundidad=profundidad
        )
        
        self.nodos[nodo_id] = nodo
        
        # Actualizar padre
        if padre_id is not None and padre_id in self.nodos:
            self.nodos[padre_id].hijos_ids.append(nodo_id)
        
        # Actualizar raíz si es el primer nodo
        if self.raiz_id is None:
            self.raiz_id = nodo_id
        
        # Actualizar nodo actual
        self.nodo_actual_id = nodo_id
        
        return nodo_id
    
    def marcar_backtrack(self, nodo_id: int) -> None:
        """
        Marca un nodo como fallido (backtrack).
        
        Args:
            nodo_id: ID del nodo a marcar
        """
        if nodo_id in self.nodos:
            self.nodos[nodo_id].estado = 'fallo'
    
    def marcar_exito(self, nodo_id: int) -> None:
        """
        Marca un nodo como exitoso (parte de la solución).
        Propaga el éxito hacia arriba en el árbol.
        
        Args:
            nodo_id: ID del nodo a marcar
        """
        if nodo_id not in self.nodos:
            return
        
        # Marcar este nodo
        self.nodos[nodo_id].estado = 'exito'
        
        # Propagar hacia arriba
        padre_id = self.nodos[nodo_id].padre_id
        if padre_id is not None:
            self.marcar_exito(padre_id)
    
    def obtener_camino_solucion(self) -> List[int]:
        """
        Obtiene el camino desde la raíz hasta la solución.
        
        Returns:
            Lista de IDs de nodos en el camino exitoso
        """
        if self.raiz_id is None:
            return []
        
        camino = []
        
        def recorrer(nodo_id: int):
            if nodo_id not in self.nodos:
                return
            
            nodo = self.nodos[nodo_id]
            if nodo.estado == 'exito':
                camino.append(nodo_id)
                for hijo_id in nodo.hijos_ids:
                    recorrer(hijo_id)
        
        recorrer(self.raiz_id)
        return camino
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Calcula estadísticas del árbol.
        
        Returns:
            Diccionario con métricas
        """
        total_nodos = len(self.nodos)
        nodos_exito = sum(1 for n in self.nodos.values() if n.estado == 'exito')
        nodos_fallo = sum(1 for n in self.nodos.values() if n.estado == 'fallo')
        
        profundidad_maxima = max((n.profundidad for n in self.nodos.values()), default=0)
        
        # Contar por tipo
        tipos = {}
        for nodo in self.nodos.values():
            tipos[nodo.tipo] = tipos.get(nodo.tipo, 0) + 1
        
        return {
            'total_nodos': total_nodos,
            'nodos_exito': nodos_exito,
            'nodos_fallo': nodos_fallo,
            'profundidad_maxima': profundidad_maxima,
            'nodos_por_tipo': tipos
        }
    
    def exportar_json(self, ruta: str) -> None:
        """
        Exporta el árbol a formato JSON.
        
        Args:
            ruta: Ruta del archivo de salida
        """
        datos = {
            'raiz_id': self.raiz_id,
            'nodos': {
                nodo_id: {
                    'id': nodo.id,
                    'tipo': nodo.tipo,
                    'datos': nodo.datos,
                    'padre_id': nodo.padre_id,
                    'hijos_ids': nodo.hijos_ids,
                    'estado': nodo.estado,
                    'profundidad': nodo.profundidad
                }
                for nodo_id, nodo in self.nodos.items()
            }
        }
        
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
