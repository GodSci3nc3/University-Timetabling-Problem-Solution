"""
Pantalla de resultados - Visualización de horarios generados con 3 vistas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from .estilos import COLORES, FUENTES, boton_primario
from src.core.config import DIAS_SEMANA
from collections import defaultdict


class PantallaResultados(tk.Frame):
    """Pantalla que muestra los horarios generados en 3 vistas: Matriz ITI, ITI y Disponibilidad."""
    
    def __init__(self, parent, app):
        """Inicializa la pantalla de resultados."""
        super().__init__(parent, bg=COLORES['fondo'])
        self.app = app
        self.grupo_actual = 0
        self.grupos_lista = []
        self.profesor_actual = 0
        self.profesores_lista = []
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea los elementos de la interfaz con 3 pestañas."""
        # Configurar grid para que sea responsive
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Barra superior
        barra_superior = tk.Frame(self, bg=COLORES['primario'], height=60)
        barra_superior.grid(row=0, column=0, sticky='ew')
        barra_superior.pack_propagate(False)
        
        tk.Label(
            barra_superior,
            text="Resultados",
            font=FUENTES['titulo'],
            bg=COLORES['primario'],
            fg=COLORES['blanco']
        ).pack(pady=15)
        
        # Contenedor principal
        contenedor = tk.Frame(self, bg=COLORES['fondo'])
        contenedor.grid(row=1, column=0, sticky='nsew', padx=30, pady=20)
        contenedor.grid_rowconfigure(1, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)
        
        # Subtítulo
        tk.Label(
            contenedor,
            text="Vista de los horarios generados",
            font=FUENTES['normal'],
            bg=COLORES['fondo'],
            fg=COLORES['texto']
        ).grid(row=0, column=0, pady=10)
        
        # Notebook con pestañas
        self.notebook = ttk.Notebook(contenedor)
        self.notebook.grid(row=1, column=0, sticky='nsew', pady=10)
        
        # Crear las 3 pestañas
        self.tab_matriz = tk.Frame(self.notebook, bg=COLORES['fondo'])
        self.tab_horarios = tk.Frame(self.notebook, bg=COLORES['fondo'])
        self.tab_disponibilidad = tk.Frame(self.notebook, bg=COLORES['fondo'])
        
        self.notebook.add(self.tab_matriz, text='📊 Matriz ITI')
        self.notebook.add(self.tab_horarios, text='📅 Horarios por Grupo')
        self.notebook.add(self.tab_disponibilidad, text='⏰ Disponibilidad Profesores')
        
        # Crear contenido de cada pestaña
        self._crear_vista_matriz()
        self._crear_vista_horarios()
        self._crear_vista_disponibilidad()
        
        # Botón de descarga
        boton_primario(
            contenedor,
            "💾 Descargar Excel con 3 Hojas",
            self.descargar
        ).grid(row=2, column=0, pady=20)
    
    def _crear_vista_matriz(self):
        """Crea la vista de Matriz ITI (profesores vs materias)."""
        self.tab_matriz.grid_rowconfigure(1, weight=1)
        self.tab_matriz.grid_columnconfigure(0, weight=1)
        
        # Título explicativo
        tk.Label(
            self.tab_matriz,
            text="Matriz de asignación de horas por profesor y materia",
            font=FUENTES['normal'],
            bg=COLORES['fondo'],
            fg=COLORES['texto']
        ).grid(row=0, column=0, pady=10)
        
        # Frame para la tabla
        frame = tk.Frame(self.tab_matriz, bg=COLORES['blanco'])
        frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Treeview para matriz con scroll horizontal habilitado
        self.tree_matriz = ttk.Treeview(frame, show='tree headings', height=20)
        
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_matriz.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree_matriz.xview)
        self.tree_matriz.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree_matriz.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
    
    def _crear_vista_horarios(self):
        """Crea la vista de horarios por grupo."""
        self.tab_horarios.grid_rowconfigure(1, weight=1)
        self.tab_horarios.grid_columnconfigure(0, weight=1)
        
        # Navegador de grupos
        frame_nav = tk.Frame(self.tab_horarios, bg=COLORES['fondo'])
        frame_nav.grid(row=0, column=0, pady=10)
        
        tk.Button(
            frame_nav,
            text="◀",
            command=self.grupo_anterior,
            font=FUENTES['boton'],
            bg=COLORES['primario'],
            fg=COLORES['blanco'],
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        self.label_grupo = tk.Label(
            frame_nav,
            text="",
            font=FUENTES['subtitulo'],
            bg=COLORES['fondo'],
            fg=COLORES['texto'],
            width=30
        )
        self.label_grupo.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            frame_nav,
            text="▶",
            command=self.grupo_siguiente,
            font=FUENTES['boton'],
            bg=COLORES['primario'],
            fg=COLORES['blanco'],
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame para tabla
        frame = tk.Frame(self.tab_horarios, bg=COLORES['blanco'])
        frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        columnas = ['Horas'] + DIAS_SEMANA
        self.tree_horarios = ttk.Treeview(frame, columns=columnas, show='headings', height=15)
        
        for col in columnas:
            self.tree_horarios.heading(col, text=col)
            self.tree_horarios.column(col, width=150)
        
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_horarios.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree_horarios.xview)
        self.tree_horarios.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree_horarios.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
    
    def _crear_vista_disponibilidad(self):
        """Crea la vista de disponibilidad de profesores."""
        self.tab_disponibilidad.grid_rowconfigure(1, weight=1)
        self.tab_disponibilidad.grid_columnconfigure(0, weight=1)
        
        # Navegador de profesores
        frame_nav = tk.Frame(self.tab_disponibilidad, bg=COLORES['fondo'])
        frame_nav.grid(row=0, column=0, pady=10)
        
        tk.Button(
            frame_nav,
            text="◀",
            command=self.profesor_anterior,
            font=FUENTES['boton'],
            bg=COLORES['primario'],
            fg=COLORES['blanco'],
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        self.label_profesor = tk.Label(
            frame_nav,
            text="",
            font=FUENTES['subtitulo'],
            bg=COLORES['fondo'],
            fg=COLORES['texto'],
            width=30
        )
        self.label_profesor.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            frame_nav,
            text="▶",
            command=self.profesor_siguiente,
            font=FUENTES['boton'],
            bg=COLORES['primario'],
            fg=COLORES['blanco'],
            width=3
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame para tabla
        frame = tk.Frame(self.tab_disponibilidad, bg=COLORES['blanco'])
        frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        columnas = ['Horas'] + DIAS_SEMANA
        self.tree_disponibilidad = ttk.Treeview(frame, columns=columnas, show='headings', height=15)
        
        for col in columnas:
            self.tree_disponibilidad.heading(col, text=col)
            self.tree_disponibilidad.column(col, width=150)
        
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_disponibilidad.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree_disponibilidad.xview)
        self.tree_disponibilidad.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree_disponibilidad.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
    
    def al_mostrar(self):
        """Se llama cuando se muestra esta pantalla."""
        # Obtener listas
        grupos = self.app.datos['grupos']
        profesores = self.app.datos['profesores']
        
        self.grupos_lista = [g.nombre for g in grupos]
        self.profesores_lista = [p.nombre for p in profesores]
        
        self.grupo_actual = 0
        self.profesor_actual = 0
        
        # Llenar las 3 vistas
        self.mostrar_matriz()
        self.mostrar_horario_grupo()
        self.mostrar_disponibilidad_profesor()
    
    def mostrar_matriz(self):
        """Muestra la matriz de asignación profesores-materias."""
        # Limpiar árbol
        for item in self.tree_matriz.get_children():
            self.tree_matriz.delete(item)
        
        # Obtener horario del backend (estructura: {grupo: {dia: {slot: {materia, profesor}}}})
        horario = self.app.datos.get('horario_generado', {})
        
        if not horario:
            return
        
        # Agrupar por grupo-materia y profesor
        matriz = defaultdict(lambda: defaultdict(int))
        profesores_set = set()
        
        for grupo, dias_data in horario.items():
            for dia, slots_data in dias_data.items():
                for slot, asig_data in slots_data.items():
                    if asig_data:
                        materia = asig_data.get('materia', '')
                        profesor = asig_data.get('profesor', '')
                        
                        grupo_materia = f"{grupo} - {materia}"
                        matriz[grupo_materia][profesor] += 1
                        profesores_set.add(profesor)
        
        profesores_ordenados = sorted(profesores_set)
        
        # Configurar columnas con anchos generosos para mejor visibilidad
        columnas = ['Grupo-Materia', 'Total Horas'] + profesores_ordenados
        self.tree_matriz['columns'] = columnas
        
        for col in columnas:
            self.tree_matriz.heading(col, text=col)
            # Anchos amplios: 300 para grupo-materia, 100 para horas, 150 para cada profesor
            if col == 'Grupo-Materia':
                width = 300
            elif col == 'Total Horas':
                width = 100
            else:
                width = 150
            
            self.tree_matriz.column(col, width=width, minwidth=width, anchor='center')
        
        # Llenar datos
        for grupo_materia in sorted(matriz.keys()):
            horas_total = sum(matriz[grupo_materia].values())
            valores = [grupo_materia, horas_total]
            
            for prof in profesores_ordenados:
                horas = matriz[grupo_materia].get(prof, '')
                valores.append(horas if horas else '')
            
            self.tree_matriz.insert('', tk.END, values=valores)
    
    def mostrar_horario_grupo(self):
        """Muestra el horario del grupo actual."""
        if not self.grupos_lista:
            return
        
        # Limpiar tabla
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)
        
        # Actualizar label
        grupo_nombre = self.grupos_lista[self.grupo_actual]
        self.label_grupo.config(text=f"Grupo: {grupo_nombre}")
        
        # Obtener horario del backend (estructura: {grupo: {dia: {slot: {materia, profesor}}}})
        horario = self.app.datos.get('horario_generado', {})
        
        if not horario or grupo_nombre not in horario:
            return
        
        horario_grupo = horario[grupo_nombre]
        
        # Mapeo de días
        dia_map = {'Lunes': 'L', 'Martes': 'M', 'Miercoles': 'Mi', 'Miércoles': 'Mi', 'Jueves': 'J', 'Viernes': 'V'}
        
        # Organizar por slot
        slots_data = defaultdict(lambda: defaultdict(str))
        slots_set = set()
        
        for dia, slots in horario_grupo.items():
            dia_corto = dia_map.get(dia, dia[:2])
            for slot, asig in slots.items():
                slots_set.add(slot)
                if asig:
                    materia = asig.get('materia', '')
                    profesor = asig.get('profesor', '')
                    slots_data[slot][dia_corto] = f"{materia}\n{profesor}"
        
        # Ordenar slots
        def slot_key(s):
            hora = s.split('-')[0]
            h, m = hora.split(':')
            return int(h) * 60 + int(m)
        
        slots_ordenados = sorted(list(slots_set), key=slot_key)
        
        # Poblar tabla
        for slot in slots_ordenados:
            fila = [slot]
            
            for dia_corto in ['L', 'M', 'Mi', 'J', 'V']:
                fila.append(slots_data[slot].get(dia_corto, ''))
            
            self.tree_horarios.insert('', tk.END, values=fila)
    
    def mostrar_disponibilidad_profesor(self):
        """Muestra la disponibilidad del profesor actual."""
        if not self.profesores_lista:
            return
        
        # Limpiar tabla
        for item in self.tree_disponibilidad.get_children():
            self.tree_disponibilidad.delete(item)
        
        # Actualizar label
        profesor_nombre = self.profesores_lista[self.profesor_actual]
        self.label_profesor.config(text=f"Profesor: {profesor_nombre}")
        
        # Obtener horario del backend (estructura: {grupo: {dia: {slot: {materia, profesor}}}})
        horario = self.app.datos.get('horario_generado', {})
        
        if not horario:
            return
        
        # Mapeo de días
        dia_map = {'Lunes': 'L', 'Martes': 'M', 'Miercoles': 'Mi', 'Miércoles': 'Mi', 'Jueves': 'J', 'Viernes': 'V'}
        
        # Organizar por slot y día
        disponibilidad = defaultdict(lambda: defaultdict(str))
        slots_set = set()
        
        for grupo, dias_data in horario.items():
            for dia, slots in dias_data.items():
                dia_corto = dia_map.get(dia, dia[:2])
                for slot, asig in slots.items():
                    if asig and asig.get('profesor') == profesor_nombre:
                        slots_set.add(slot)
                        disponibilidad[slot][dia_corto] = grupo
        
        # Ordenar slots
        def slot_key(s):
            hora = s.split('-')[0]
            h, m = hora.split(':')
            return int(h) * 60 + int(m)
        
        slots_ordenados = sorted(list(slots_set), key=slot_key)
        
        # Poblar tabla
        for slot in slots_ordenados:
            fila = [slot]
            
            for dia_corto in ['L', 'M', 'Mi', 'J', 'V']:
                fila.append(disponibilidad[slot].get(dia_corto, ''))
            
            self.tree_disponibilidad.insert('', tk.END, values=fila)
    
    def grupo_anterior(self):
        """Navega al grupo anterior."""
        if self.grupo_actual > 0:
            self.grupo_actual -= 1
            self.mostrar_horario_grupo()
    
    def grupo_siguiente(self):
        """Navega al grupo siguiente."""
        if self.grupo_actual < len(self.grupos_lista) - 1:
            self.grupo_actual += 1
            self.mostrar_horario_grupo()
    
    def profesor_anterior(self):
        """Navega al profesor anterior."""
        if self.profesor_actual > 0:
            self.profesor_actual -= 1
            self.mostrar_disponibilidad_profesor()
    
    def profesor_siguiente(self):
        """Navega al profesor siguiente."""
        if self.profesor_actual < len(self.profesores_lista) - 1:
            self.profesor_actual += 1
            self.mostrar_disponibilidad_profesor()
    
    def descargar(self):
        """Descarga los horarios a un archivo Excel con las 3 hojas."""
        try:
            # Pedir ubicación de guardado
            ruta = filedialog.asksaveasfilename(
                title="Guardar horarios",
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")]
            )
            
            if not ruta:
                return
            
            # Usar el nuevo generador de Excel con 3 hojas
            from src.data.generador_excel_resultado import GeneradorExcelResultado
            
            # Preparar datos de entrada
            datos_entrada = {
                'grupos': {g.nombre: g for g in self.app.datos['grupos']},
                'materias': {m.nombre: m for m in self.app.datos['materias']},
                'profesores': {p.nombre: p for p in self.app.datos['profesores']}
            }
            
            # Obtener horario generado
            horario = self.app.datos.get('horario_generado', {})
            
            # Generar Excel
            generador = GeneradorExcelResultado(datos_entrada, horario)
            generador.generar(ruta)
            
            messagebox.showinfo(
                "Éxito",
                f"Horarios guardados exitosamente en:\n{ruta}\n\n"
                "El archivo contiene 3 hojas:\n"
                "• Matriz ITI: Asignación de profesores a materias\n"
                "• ITI: Horarios visuales por grupo\n"
                "• Disponibilidad: Disponibilidad de profesores"
            )
            
        except Exception as e:
            import traceback
            messagebox.showerror(
                "Error al guardar",
                f"No se pudieron guardar los horarios:\n\n{str(e)}\n\n"
                f"Detalles:\n{traceback.format_exc()}"
            )
