"""
Pantalla de generación - Muestra progreso mientras se ejecuta el algoritmo.
"""

import tkinter as tk
from tkinter import messagebox
import threading
from .estilos import COLORES, FUENTES
from src.core.grafo_conflictos import GrafoConflictos
from src.core.backend_cpp import BackendCppIntegration


class PantallaGenerando(tk.Frame):
    """Pantalla que muestra el progreso de generación de horarios."""
    
    def __init__(self, parent, app):
        """Inicializa la pantalla de generación."""
        super().__init__(parent, bg=COLORES['fondo'])
        self.app = app
        self.animando = False
        self.spinner_index = 0
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Contenedor centrado
        contenedor = tk.Frame(self, bg=COLORES['fondo'])
        contenedor.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Spinner
        self.label_spinner = tk.Label(
            contenedor,
            text="⏳",
            font=('Arial', 72),
            bg=COLORES['fondo']
        )
        self.label_spinner.pack(pady=20)
        
        # Texto principal
        tk.Label(
            contenedor,
            text="Generando horarios...",
            font=FUENTES['titulo'],
            bg=COLORES['fondo'],
            fg=COLORES['texto']
        ).pack(pady=10)
        
        # Texto de progreso
        self.label_progreso = tk.Label(
            contenedor,
            text="Iniciando...",
            font=FUENTES['normal'],
            bg=COLORES['fondo'],
            fg=COLORES['texto']
        )
        self.label_progreso.pack(pady=10)
    
    def al_mostrar(self):
        """Se llama cuando se muestra esta pantalla."""
        self.iniciar_generacion()
    
    def iniciar_generacion(self):
        """Inicia el proceso de generación en un thread separado."""
        self.animando = True
        self.animar_spinner()
        
        # Ejecutar generación en thread separado
        thread = threading.Thread(target=self.generar_horarios, daemon=True)
        thread.start()
    
    def animar_spinner(self):
        """Anima el spinner."""
        if not self.animando:
            return
        
        spinners = ['⏳', '⌛']
        self.spinner_index = (self.spinner_index + 1) % len(spinners)
        self.label_spinner.config(text=spinners[self.spinner_index])
        
        # Continuar animación
        self.after(500, self.animar_spinner)
    
    def actualizar_progreso(self, texto):
        """Actualiza el texto de progreso."""
        self.label_progreso.config(text=texto)
    
    def generar_horarios(self):
        """Genera los horarios usando el backend C++."""
        try:
            grupos = self.app.datos['grupos']
            materias = self.app.datos['materias']
            profesores = self.app.datos['profesores']
            
            self.actualizar_progreso("Construyendo grafo de conflictos...")
            grafo = GrafoConflictos()
            grafo.construir_desde_datos(grupos, materias, profesores)
            self.app.datos['grafo'] = grafo
            
            self.actualizar_progreso("Ejecutando backend C++...")
            backend = BackendCppIntegration()
            horario, stats = backend.ejecutar_backend(grupos, materias, profesores)
            
            # Guardar tanto el horario procesado como el resultado completo del backend
            self.app.datos['horario_generado'] = horario
            self.app.datos['resultado_backend'] = {'horario': horario, 'estadisticas': stats}
            self.app.datos['arbol_decisiones'] = None
            self.app.datos['estadisticas'] = stats
            
            if horario:
                self.actualizar_progreso("Listo!")
                self.animando = False
                
                self.after(1000, lambda: self.app.mostrar_pantalla('resultados'))
            else:
                self.animando = False
                self.after(100, lambda: self.mostrar_error_sin_solucion())
                
        except Exception as e:
            self.animando = False
            self.after(100, lambda: self.mostrar_error(str(e)))
    
    def mostrar_error_sin_solucion(self):
        """Muestra mensaje de error cuando no hay solución."""
        messagebox.showerror(
            "No se encontró solución",
            "El algoritmo no pudo generar un horario válido.\n\n"
            "Posibles causas:\n"
            "• Restricciones demasiado estrictas\n"
            "• Insuficientes slots disponibles\n"
            "• Capacidad de profesores insuficiente\n\n"
            "Intenta ajustar los datos y vuelve a intentar."
        )
        self.app.mostrar_pantalla('validacion')
    
    def mostrar_error(self, mensaje):
        """Muestra mensaje de error genérico."""
        messagebox.showerror(
            "Error al generar horarios",
            f"Ocurrió un error durante la generación:\n\n{mensaje}"
        )
        self.app.mostrar_pantalla('validacion')
