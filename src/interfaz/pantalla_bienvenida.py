"""
Pantalla de bienvenida - Carga de archivo Excel.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from .estilos import COLORES, FUENTES, boton_primario, label_titulo
from src.data.lector_excel import leer_excel


class PantallaBienvenida(tk.Frame):
    """Pantalla inicial para cargar el archivo Excel."""
    
    def __init__(self, parent, app):
        """
        Inicializa la pantalla de bienvenida.
        
        Args:
            parent: Widget padre
            app: Instancia de la aplicación principal
        """
        super().__init__(parent, bg=COLORES['fondo'])
        self.app = app
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Barra superior
        barra_superior = tk.Frame(self, bg=COLORES['primario'], height=60)
        barra_superior.pack(fill=tk.X)
        barra_superior.pack_propagate(False)
        
        tk.Label(
            barra_superior,
            text="Matriz de horarios",
            font=FUENTES['titulo'],
            bg=COLORES['primario'],
            fg=COLORES['blanco']
        ).pack(pady=15)
        
        # Contenedor central
        contenedor = tk.Frame(self, bg=COLORES['fondo'])
        contenedor.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Título
        label_titulo(contenedor, "Bienvenido al Sistema de Horarios").pack(pady=20)
        
        # Instrucciones
        instrucciones = tk.Label(
            contenedor,
            text="Para generar tus horarios, inserta un documento .xlsx que contenga:\n\n"
                 "• Número de grados\n"
                 "• Número de grupos por grado (Ej. 4-1, 4-2)\n"
                 "• Número y nombre de materias por grupo\n"
                 "• Horas de clase por semana de cada materia\n"
                 "• Nombre de Profesores con sus respectivas horas disponibles",
            font=FUENTES['normal'],
            bg=COLORES['fondo'],
            fg=COLORES['texto'],
            justify=tk.LEFT
        )
        instrucciones.pack(pady=20)
        
        # Área de selección de archivo
        area_seleccion = tk.Frame(
            contenedor,
            bg=COLORES['secundario'],
            width=400,
            height=200
        )
        area_seleccion.pack(pady=30)
        area_seleccion.pack_propagate(False)
        
        # Hacer clickeable toda el área
        area_seleccion.bind('<Button-1>', lambda e: self.seleccionar_archivo())
        
        tk.Label(
            area_seleccion,
            text="📁",
            font=('Arial', 48),
            bg=COLORES['secundario'],
            fg=COLORES['blanco']
        ).pack(expand=True)
        
        tk.Label(
            area_seleccion,
            text="Selecciona el archivo",
            font=FUENTES['subtitulo'],
            bg=COLORES['secundario'],
            fg=COLORES['blanco']
        ).pack()
        
        # Botón alternativo
        boton_primario(
            contenedor,
            "Seleccionar Archivo Excel",
            self.seleccionar_archivo
        ).pack(pady=20)
    
    def seleccionar_archivo(self):
        """Abre el diálogo para seleccionar archivo Excel."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            # Cargar datos
            grupos, materias, profesores = leer_excel(ruta)
            
            # Guardar en el estado de la aplicación
            self.app.datos['grupos'] = grupos
            self.app.datos['materias'] = materias
            self.app.datos['profesores'] = profesores
            self.app.datos['ruta_excel'] = ruta
            
            # Navegar a la siguiente pantalla
            self.app.mostrar_pantalla('validacion')
            
        except Exception as e:
            messagebox.showerror(
                "Error al cargar archivo",
                f"No se pudo cargar el archivo:\n\n{str(e)}\n\n"
                "Verifica que el archivo tenga el formato correcto."
            )
