#!/usr/bin/env python3
"""
Script para ejecutar la interfaz gráfica del Sistema de Horarios.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.interfaz.main import main

if __name__ == "__main__":
    main()
