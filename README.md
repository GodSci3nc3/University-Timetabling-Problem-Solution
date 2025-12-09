# Sistema de Gestión de Horarios Académicos

Sistema completo con **Backend en C++** e **Interfaz Gráfica en Python** para generar horarios universitarios usando algoritmos de backtracking y teoría de grafos.

## Arquitectura

### Backend (C++)
- Modelos de datos
- Grafo de conflictos
- Algoritmo de backtracking con heurísticas
- Comunicación mediante JSON

### Frontend (Python)
- Interfaz gráfica con Tkinter
- Carga y validación de datos Excel
- Visualización de resultados
- Integración con backend C++

## Compilación

```bash
./compilar.sh
```

## Ejecución

### Interfaz Gráfica

```bash
python ejecutar_interfaz.py
```

### Backend C++ (Standalone)

```bash
./build/horarios_backend input.json output.json
```

La interfaz te guiará paso a paso:
1. Seleccionar archivo Excel
2. Validar datos
3. Generar horarios automáticamente
4. Visualizar y descargar resultados

### Opción 2: Línea de Comandos

#### 1. Instalar dependencias

```bash
pip install pandas openpyxl networkx matplotlib
```

### 2. Crear archivo Excel de ejemplo

```bash
python crear_excel_ejemplo.py
```

### 3. Probar módulo de datos

```bash
python test_modulo.py
```

### 4. Probar módulo de grafos

```bash
# Ejemplo didáctico simple
python ejemplo_grafo_simple.py

# Prueba completa con visualizaciones
python test_grafo.py
```

### 5. Uso en código

```python
from src.data.lector_excel import leer_excel
from src.data.validador import validar_datos
from src.core.grafo_conflictos import GrafoConflictos
from src.visualization.visualizador_grafo import visualizar_grafo

# Cargar datos
grupos, materias, profesores = leer_excel("datos_universidad.xlsx")

# Validar
es_valido, errores = validar_datos(grupos, materias, profesores)

if es_valido:
    print("✓ Datos válidos. Listo para generar horarios.")
else:
    for error in errores:
        print(f"✗ {error}")

# Construir grafo de conflictos
grafo = GrafoConflictos()
grafo.construir_desde_datos(grupos, materias, profesores)

# Visualizar
visualizar_grafo(grafo, "Grafo de Conflictos", "mi_grafo.png")
```

## 📊 Formato del Excel

El archivo debe tener **3 hojas**:

### Hoja "Grupos"
| Cuatrimestre | Turno      | Grupo    |
|--------------|------------|----------|
| 5            | Matutino   | ITI 5-1  |
| 5            | Vespertino | ITI 5-2  |

### Hoja "Materias"
| Cuatrimestre | Materia                | Horas_Semana |
|--------------|------------------------|--------------|
| 5            | Estructura de Datos    | 6            |
| 5            | Diseño de Bases de Datos | 5          |

### Hoja "Profesores"
| Nombre           | Materias_Imparte                    | Horas_Disponibles | Turno_Preferido |
|------------------|-------------------------------------|-------------------|-----------------|
| Dr. Said Polanco | Estructura de Datos;Algoritmos      | 20                | Matutino        |
| Dra. Karla Vázquez | Diseño de Bases de Datos;POO      | 18                | Ambos           |

**Nota**: Las materias se separan con punto y coma (;)

## ✅ Validaciones Implementadas

### Módulo de Datos
1. **Cobertura de profesores**: Cada materia tiene al menos un profesor capacitado
2. **Capacidad horaria**: Total de horas no excede capacidad de profesores
3. **Compatibilidad de turnos**: Grupos correctamente distribuidos
4. **Unicidad**: No hay nombres duplicados

### Módulo de Grafos
1. **Detección de conflictos**: Identifica conflictos por grupo y por profesor
2. **Número cromático**: Calcula slots mínimos necesarios (algoritmo Welsh-Powell)
3. **Análisis de cliques**: Encuentra grupos mutuamente conflictivos
4. **Verificación de factibilidad**: Determina si es posible asignar con slots disponibles

## 📊 Teoría de Grafos Aplicada

### Modelo del Grafo
- **Nodos**: Cada nodo = (grupo, materia) que debe asignarse
- **Aristas**: Representan conflictos entre asignaciones
- **Coloreo**: Asignar slots (colores) sin que nodos conectados compartan slot

### Tipos de Conflictos
1. **Mismo Grupo**: Un grupo no puede tener 2 clases simultáneamente
2. **Mismo Profesor**: Un profesor no puede estar en 2 lugares a la vez

### Resultados del Análisis
Con los datos de ejemplo:
- **36 nodos** (asignaciones)
- **165 aristas** (conflictos)
- **67.3%** conflictos por profesor
- **32.7%** conflictos por grupo
- **Número cromático**: 9 slots necesarios

## 🎓 Proyecto Académico

Este es un proyecto de la materia **Estructura de Datos** que demuestra:
- Diseño de clases y objetos (POO)
- Uso de listas y diccionarios
- Validación de datos
- Manejo de archivos con pandas

## 👨‍💻 Autor

Desarrollado para la Universidad Politécnica de Victoria
