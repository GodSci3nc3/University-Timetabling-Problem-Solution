"""
Estilos y constantes para la interfaz gráfica.
Define colores, fuentes y funciones helper para crear widgets con estilo consistente.
"""

import tkinter as tk
from tkinter import ttk

# Paleta de colores del diseño
COLORES = {
    'primario': '#6B46C1',      # Morado
    'secundario': '#9F7AEA',    # Morado claro
    'exito': '#48BB78',         # Verde
    'error': '#F56565',         # Rojo
    'fondo': '#F7FAFC',         # Gris muy claro
    'texto': '#2D3748',         # Gris oscuro
    'blanco': '#FFFFFF',
    'gris_claro': '#E2E8F0'
}

# Configuraciones de fuentes (tamaños aumentados para mejor legibilidad)
# Se usa Ubuntu como fuente moderna y legible (disponible en Linux por defecto)
# Fallback a sans-serif si no está disponible
FUENTES = {
    'titulo': ('Ubuntu', 26, 'bold'),
    'subtitulo': ('Ubuntu', 18, 'bold'),
    'normal': ('Ubuntu', 12),
    'pequeña': ('Ubuntu', 10),
    'boton': ('Ubuntu', 12, 'bold'),
    'tabla': ('Ubuntu', 9)
}


def boton_primario(parent, texto, comando, **kwargs):
    """
    Crea un botón con estilo primario (morado).
    
    Args:
        parent: Widget padre
        texto: Texto del botón
        comando: Función a ejecutar al hacer clic
        **kwargs: Argumentos adicionales para el botón
    
    Returns:
        Widget Button configurado
    """
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=COLORES['primario'],
        fg=COLORES['blanco'],
        font=FUENTES['boton'],
        relief=tk.FLAT,
        padx=20,
        pady=10,
        cursor='hand2',
        **kwargs
    )


def boton_secundario(parent, texto, comando, **kwargs):
    """Crea un botón con estilo secundario (morado claro)."""
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=COLORES['secundario'],
        fg=COLORES['blanco'],
        font=FUENTES['boton'],
        relief=tk.FLAT,
        padx=20,
        pady=10,
        cursor='hand2',
        **kwargs
    )


def frame_tarjeta(parent, **kwargs):
    """
    Crea un frame con estilo de tarjeta (fondo blanco).
    
    Args:
        parent: Widget padre
        **kwargs: Argumentos adicionales
    
    Returns:
        Frame configurado
    """
    return tk.Frame(
        parent,
        bg=COLORES['blanco'],
        relief=tk.RAISED,
        borderwidth=1,
        **kwargs
    )


def label_titulo(parent, texto, **kwargs):
    """Crea un label con estilo de título."""
    return tk.Label(
        parent,
        text=texto,
        font=FUENTES['titulo'],
        bg=kwargs.get('bg', COLORES['fondo']),
        fg=COLORES['texto'],
        **{k: v for k, v in kwargs.items() if k != 'bg'}
    )


def label_subtitulo(parent, texto, **kwargs):
    """Crea un label con estilo de subtítulo."""
    return tk.Label(
        parent,
        text=texto,
        font=FUENTES['subtitulo'],
        bg=kwargs.get('bg', COLORES['fondo']),
        fg=COLORES['texto'],
        **{k: v for k, v in kwargs.items() if k != 'bg'}
    )


def configurar_estilo_treeview():
    """
    Configura el estilo global para widgets Treeview.
    Debe llamarse una vez al iniciar la aplicación.
    """
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configurar Treeview
    style.configure(
        'Treeview',
        background=COLORES['blanco'],
        foreground=COLORES['texto'],
        fieldbackground=COLORES['blanco'],
        font=FUENTES['normal']
    )
    
    style.configure(
        'Treeview.Heading',
        background=COLORES['primario'],
        foreground=COLORES['blanco'],
        font=FUENTES['boton']
    )
    
    # Tags para filas especiales
    style.map('Treeview', background=[('selected', COLORES['secundario'])])
