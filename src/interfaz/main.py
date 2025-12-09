"""
Aplicación principal del Sistema de Gestión de Horarios.
Maneja la navegación entre pantallas y el estado compartido.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.interfaz.estilos import COLORES, configurar_estilo_treeview
from src.interfaz.pantalla_bienvenida import PantallaBienvenida
from src.interfaz.pantalla_validacion import PantallaValidacion
from src.interfaz.pantalla_generando import PantallaGenerando
from src.interfaz.pantalla_resultados import PantallaResultados


class AplicacionHorarios(tk.Tk):
    """
    Aplicación principal del sistema de horarios.
    Maneja la navegación entre pantallas y el estado compartido.
    """
    
    def __init__(self):
        """Inicializa la aplicación."""
        super().__init__()
        
        # Configuración de la ventana
        self.title("Sistema de Gestión de Horarios Académicos")
        self.geometry("1200x800")
        self.configure(bg=COLORES['fondo'])
        
        # Hacer la ventana responsive - permitir redimensionamiento mínimo
        self.minsize(900, 600)
        
        # Configurar estilos globales
        configurar_estilo_treeview()
        
        # Estado compartido entre pantallas
        self.datos = {
            'grupos': None,
            'materias': None,
            'profesores': None,
            'grafo': None,
            'horario_generado': None,
            'arbol_decisiones': None,
            'estadisticas': None,
            'ruta_excel': None
        }
        
        # Container para las pantallas
        self.container = tk.Frame(self, bg=COLORES['fondo'])
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Diccionario de pantallas
        self.pantallas = {}
        
        # Crear todas las pantallas
        self._crear_pantallas()
        
        # Mostrar pantalla inicial
        self.mostrar_pantalla('bienvenida')
    
    def _crear_pantallas(self):
        """Crea todas las pantallas de la aplicación."""
        # Pantalla de bienvenida
        self.pantallas['bienvenida'] = PantallaBienvenida(self.container, self)
        
        # Pantalla de validación
        self.pantallas['validacion'] = PantallaValidacion(self.container, self)
        
        # Pantalla de generación
        self.pantallas['generando'] = PantallaGenerando(self.container, self)
        
        # Pantalla de resultados
        self.pantallas['resultados'] = PantallaResultados(self.container, self)
        
        # Posicionar todas las pantallas en el mismo lugar
        for pantalla in self.pantallas.values():
            pantalla.grid(row=0, column=0, sticky='nsew')
        
        # Configurar grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
    def mostrar_pantalla(self, nombre):
        """
        Muestra una pantalla específica.
        
        Args:
            nombre: Nombre de la pantalla ('bienvenida', 'validacion', etc.)
        """
        if nombre not in self.pantallas:
            messagebox.showerror("Error", f"Pantalla '{nombre}' no encontrada")
            return
        
        # Traer la pantalla al frente
        pantalla = self.pantallas[nombre]
        pantalla.tkraise()
        
        # Si la pantalla tiene un método de inicialización, llamarlo
        if hasattr(pantalla, 'al_mostrar'):
            pantalla.al_mostrar()


def main():
    """Punto de entrada de la aplicación."""
    try:
        app = AplicacionHorarios()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{str(e)}")
        raise


if __name__ == "__main__":
    main()
