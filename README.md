Sistema de Gestión de Horarios Académicos
Manual Técnico
1. Descripción del Proyecto
¿Qué hace el sistema?

Este es un sistema híbrido completo con Backend en C++ e Interfaz Gráfica en Python diseñado para la generación automatizada de horarios universitarios. Utiliza algoritmos de backtracking optimizados con heurísticas y teoría de grafos para asignar materias, grupos y profesores respetando restricciones complejas.
¿A quién va dirigido?

Está dirigido a coordinadores académicos y personal administrativo de la Universidad Politécnica de Victoria (o instituciones similares) encargados de la planificación semestral de cargas académicas.
Problema que resuelve (UTP)

Resuelve el University Timetabling Problem (Problema de Horarios Universitarios), automatizando la asignación de recursos (tiempo, profesores, grupos) para evitar:

    Conflictos de horario (mismo grupo con dos materias a la vez).

    Empalmes de profesores (un profesor en dos aulas a la vez).

    Sobrecarga de horas docentes.

2. Funcionalidades Principales

    Importación de Datos: Carga masiva de información académica desde archivos Excel (.xlsx).

    Validación de Datos: Detección automática de errores en la información de entrada antes del procesamiento.

    Generación Automática: Creación de horarios libres de conflictos mediante algoritmos computacionales.

    Visualización Organizada: Interfaz gráfica amigable para revisar los horarios generados.

    Exportación: Capacidad de guardar los resultados en formatos legibles y estructurados (JSON/Archivos).

3. Requerimientos del Sistema

Para el correcto funcionamiento y compilación del proyecto se requiere:

    Sistema Operativo: Linux (Recomendado) o Windows (vía WSL o MinGW).

    Lenguajes:

        C++: Estándar C++17 (Backend).

        Python: Versión 3.8 o superior (Frontend y Scripts).

    Librerías / Frameworks:

        C++: nlohmann/json (Manejo de JSON), CMake (Compilación).

        Python: Tkinter (GUI), pandas (Datos), openpyxl (Excel), networkx (Grafos), matplotlib (Visualización).

4. Instalación

Sigue estos pasos para configurar el entorno de desarrollo:
Paso 1: Clonar el repositorio
Bash

git clone <url-del-repositorio>
cd <nombre-del-carpeta>

Paso 2: Instalar dependencias de Python
Bash

pip install pandas openpyxl networkx matplotlib

Nota: Tkinter generalmente viene preinstalado con Python.
Paso 3: Compilar el Backend (C++)

El sistema incluye un script de compilación automática.
Bash

chmod +x compilar.sh
./compilar.sh

Paso 4: Cómo ejecutar el sistema

Tienes dos modos de operación:

A. Interfaz Gráfica (Recomendado para usuarios):
Bash

python ejecutar_interfaz.py

La interfaz te guiará paso a paso:

    Seleccionar archivo Excel.

    Validar datos.

    Generar horarios automáticamente.

    Visualizar y descargar resultados.

B. Línea de Comandos (Para desarrollo/debugging):
Bash

./build/horarios_backend input.json output.json

5. Estructura del Archivo Excel

El sistema espera un archivo Excel (.xlsx) con exactamente 3 hojas con los siguientes nombres y columnas obligatorias:
Hoja "Grupos"

Define los grupos de alumnos que requieren horario.
Cuatrimestre	Turno	Grupo
5	Matutino	ITI 5-1
5	Vespertino	ITI 5-2
Hoja "Materias"

Define la carga académica por cuatrimestre.
Cuatrimestre	Materia	Horas_Semana
5	Estructura de Datos	6
5	Diseño de Bases de Datos	5
Hoja "Profesores"

Define la planta docente y su disponibilidad.
Nombre	Materias_Imparte	Horas_Disponibles	Turno_Preferido
Dr. Said Polanco	Estructura de Datos;Algoritmos	20	Matutino
Dra. Karla Vázquez	Diseño de Bases de Datos;POO	18	Ambos
Reglas Importantes

    Separadores: Las materias que imparte un profesor se separan con punto y coma (;).

    Nombres: Deben coincidir exactamente entre las hojas de Materias y Profesores.

    Turnos: Valores aceptados: "Matutino", "Vespertino", "Ambos".

6. Arquitectura del Proyecto

El sistema sigue una arquitectura cliente-servidor local, donde Python actúa como cliente y C++ como motor de procesamiento.
Estructura de Carpetas y Archivos Clave

    src/cpp/: Backend (Núcleo de procesamiento)

        core/: Modelos de datos y estructura del grafo (grafo_conflictos.cpp).

        algoritmo/: Lógica de resolución (backtracking.cpp, heuristicas.cpp).

        main.cpp: Punto de entrada del ejecutable C++.

    src/interfaz/: Frontend

        Lógica de la ventana principal y comunicación con el backend.

    src/data/: Manejo de Datos

        lector_excel.py: Lectura y transformación de Excel a estructuras de Python.

        validador.py: Reglas de negocio para validar la entrada.

    src/visualization/: Análisis

        visualizador_grafo.py: Generación de diagramas de grafos con NetworkX.

    compilar.sh: Script de automatización de build con CMake.

7. Explicación del Algoritmo
Resumen del Problema

El sistema modela el problema como un Problema de Coloreo de Grafos combinado con Satisfacción de Restricciones (CSP).
Restricciones Manejadas

    Duras (Hard Constraints): No pueden violarse bajo ninguna circunstancia.

        Un grupo no puede tener dos clases a la vez.

        Un profesor no puede impartir dos clases a la vez.

        Un profesor solo imparte materias para las que está capacitado.

    Blandas (Soft Constraints): Se intenta cumplir pero no son obligatorias.

        Preferencia de turno del profesor.

Flujo del Algoritmo

    Construcción del Grafo:

        Nodos: Cada clase requerida (combinación Grupo-Materia).

        Aristas: Conflictos (misma hora requerida por compartir profesor o grupo).

    Pre-procesamiento:

        Cálculo del número cromático (Algoritmo Welsh-Powell) para estimar slots mínimos.

        Detección de cliques (grupos de conflictos mutuos).

    Backtracking:

        Asigna horarios (slots) recursivamente.

        Usa heurísticas (MRV - Minimum Remaining Values) para fallar rápido si no hay solución.

        Poda el árbol de búsqueda cuando se detecta una invalidez.

8. Uso del Sistema (Scripts de Ayuda)

Además de la interfaz principal, el proyecto incluye scripts de utilidad para desarrollo y pruebas:
Crear datos de prueba

Genera un Excel válido automáticamente para probar el sistema.
Bash

python crear_excel_ejemplo.py

Probar módulo de validación

Verifica que la lógica de lectura de Excel funcione.
Bash

python test_modulo.py

Análisis de Grafos

Ejecuta un análisis profundo de los conflictos y genera imágenes del grafo.
Bash

# Prueba completa con visualizaciones
python test_grafo.py

Salida esperada: Genera imágenes .png del grafo de conflictos y reportes de densidad.
Ejemplo de uso programático
Python

from src.data.lector_excel import leer_excel
from src.core.grafo_conflictos import GrafoConflictos
from src.visualization.visualizador_grafo import visualizar_grafo

# 1. Cargar
grupos, materias, profesores = leer_excel("datos_universidad.xlsx")
# 2. Procesar
grafo = GrafoConflictos()
grafo.construir_desde_datos(grupos, materias, profesores)
# 3. Visualizar
visualizar_grafo(grafo, "Grafo de Conflictos", "mi_grafo.png")

9. Manejo de Errores

El sistema implementa validaciones robustas para asegurar la integridad de los datos.
Errores Comunes de Excel (Módulo de Datos)

El sistema te alertará si encuentra:

    Cobertura insuficiente: Hay una materia que ningún profesor registrado puede impartir.

    Capacidad excedida: Las horas totales de las materias superan las horas disponibles de los profesores.

    Incompatibilidad de turnos: Un grupo matutino solo tiene profesores disponibles en turno vespertino.

    Duplicados: Nombres de profesores o grupos repetidos.

Errores de Ejecución

    Error: "nlohmann_json not found": El sistema usará la versión incluida en src/cpp/utils/json/include automáticamente.

    Error de visualización: Si test_grafo.py falla, asegúrate de tener instalado matplotlib (pip install matplotlib).

📊 Teoría de Grafos Aplicada (Detalle Técnico)
Resultados del Análisis

Con los datos de ejemplo estándar incluidos en el proyecto:

    36 nodos (asignaciones totales a programar)

    165 aristas (conflictos potenciales)

    67.3% de los conflictos son causados por disponibilidad de profesores.

    32.7% de los conflictos son por empalmes de grupo.

    Número cromático: 9 slots necesarios (Mínimo teórico de bloques de horario).

🎓 Proyecto Académico

Este es un proyecto de la materia Estructura de Datos que demuestra:

    Diseño de clases y objetos (POO).

    Uso eficiente de listas, diccionarios y grafos.

    Comunicación Inter-procesos (Python <-> C++).

    Ingeniería de Software aplicada a un problema real.

👨‍💻 Autor

Desarrollado para la Universidad Politécnica de Victoria.
