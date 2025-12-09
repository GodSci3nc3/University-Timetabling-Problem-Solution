"""
Pantalla de validación - Muestra tabla de validación de datos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .estilos import COLORES, FUENTES, boton_primario, boton_secundario
from src.data.generador_tabla import generar_tabla_validacion
from src.data.validador import validar_datos


class PantallaValidacion(tk.Frame):
    """Pantalla que muestra la tabla de validación de datos."""
    
    def __init__(self, parent, app):
        """Inicializa la pantalla de validación."""
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
        
        # Contenedor principal
        contenedor = tk.Frame(self, bg=COLORES['fondo'])
        contenedor.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        # Subtítulo
        tk.Label(
            contenedor,
            text="Tabla generada a partir de la información del archivo.\n"
                 "Verifica y continúa con el proceso para generar tus horarios",
            font=FUENTES['normal'],
            bg=COLORES['fondo'],
            fg=COLORES['texto']
        ).pack(pady=10)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(contenedor, bg=COLORES['blanco'])
        frame_tabla.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Crear Treeview
        columnas = ('Materias', 'Grupos', 'Horas_Materia', 'Horas_Semana', 'Resta')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=20)
        
        # Configurar columnas
        self.tree.heading('Materias', text='Materias y Horas asignadas')
        self.tree.heading('Grupos', text='Grupos')
        self.tree.heading('Horas_Materia', text='Horas por materia')
        self.tree.heading('Horas_Semana', text='Horas por semana')
        self.tree.heading('Resta', text='Resta')
        
        for col in columnas:
            self.tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar tags para estilos
        self.tree.tag_configure('encabezado', background=COLORES['primario'], foreground=COLORES['blanco'])
        self.tree.tag_configure('grupo', background=COLORES['secundario'], foreground=COLORES['blanco'])
        
        # Frame de botones
        frame_botones = tk.Frame(contenedor, bg=COLORES['fondo'])
        frame_botones.pack(pady=20)
        
        boton_secundario(frame_botones, "Cancelar", self.cancelar).pack(side=tk.LEFT, padx=10)
        boton_primario(frame_botones, "Continuar →", self.continuar).pack(side=tk.LEFT, padx=10)
    
    def al_mostrar(self):
        """Se llama cuando se muestra esta pantalla."""
        self.poblar_tabla()
    
    def poblar_tabla(self):
        """Puebla la tabla con los datos cargados."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener datos
        materias = self.app.datos['materias']
        grupos = self.app.datos['grupos']
        
        if not materias or not grupos:
            return
        
        # Generar tabla de validación
        tabla = generar_tabla_validacion(materias, grupos)
        
        # Poblar árbol
        for cuatrimestre, grupos_dict in tabla.items():
            # Insertar encabezado de cuatrimestre
            self.tree.insert('', tk.END, values=(cuatrimestre, '', '', '', ''), tags=('encabezado',))
            
            for grupo_nombre, lista_materias in grupos_dict.items():
                # Insertar grupo
                self.tree.insert('', tk.END, values=(f"  {grupo_nombre}", '', '', '', ''), tags=('grupo',))
                
                # Insertar materias
                for info in lista_materias:
                    self.tree.insert('', tk.END, values=(
                        f"    {info['materia']}",
                        '',
                        info['horas_materia'],
                        info['horas_semana'],
                        info['resta']
                    ))
    
    def cancelar(self):
        """Regresa a la pantalla de bienvenida."""
        self.app.mostrar_pantalla('bienvenida')
    
    def continuar(self):
        """Valida los datos y continúa."""
        grupos = self.app.datos['grupos']
        materias = self.app.datos['materias']
        profesores = self.app.datos['profesores']
        
        # Validar datos
        es_valido, errores = validar_datos(grupos, materias, profesores)
        
        if not es_valido:
            mensaje_error = "Se encontraron los siguientes errores:\n\n"
            mensaje_error += "\n".join(f"• {error}" for error in errores[:5])
            if len(errores) > 5:
                mensaje_error += f"\n\n... y {len(errores) - 5} errores más"
            
            messagebox.showerror("Errores de validación", mensaje_error)
            return
        
        # Si es válido, continuar a generación
        self.app.mostrar_pantalla('generando')
