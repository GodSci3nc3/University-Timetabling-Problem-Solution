#!/bin/bash
# Script para compilar el backend en C++

set -e

echo "=== Compilando Backend C++ ==="
echo ""

# Crear directorio build si no existe
if [ ! -d "build" ]; then
    echo "Creando directorio build..."
    mkdir -p build
fi

# Ir al directorio build
cd build

# Ejecutar CMake
echo "Configurando con CMake..."
cmake ..

# Compilar
echo "Compilando..."
make -j$(nproc)

echo ""
echo "✓ Compilación exitosa!"
echo "Ejecutable generado: build/horarios_backend"
echo ""
echo "Uso: ./build/horarios_backend <input.json> <output.json>"
