cmake_minimum_required(VERSION 3.10)
project(SistemaHorarios VERSION 1.0 LANGUAGES CXX)

# Configurar C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Flags de compilación
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2")

# Buscar librerías necesarias
find_package(nlohmann_json 3.2.0 QUIET)

# Si no se encuentra nlohmann_json, usar versión incluida
if(NOT nlohmann_json_FOUND)
    message(STATUS "nlohmann_json no encontrado, usando versión incluida")
    include_directories(${CMAKE_SOURCE_DIR}/src/cpp/utils/json/include)
endif()

# Directorios de include
include_directories(
    ${CMAKE_SOURCE_DIR}/src/cpp
    ${CMAKE_SOURCE_DIR}/src/cpp/core
    ${CMAKE_SOURCE_DIR}/src/cpp/algoritmo
    ${CMAKE_SOURCE_DIR}/src/cpp/utils
)

# Archivos fuente
set(SOURCES
    src/cpp/main.cpp
    src/cpp/core/modelos.cpp
    src/cpp/core/grafo_conflictos.cpp
    src/cpp/core/config.cpp
    src/cpp/algoritmo/backtracking.cpp
    src/cpp/algoritmo/restricciones.cpp
    src/cpp/algoritmo/heuristicas.cpp
    src/cpp/algoritmo/arbol_decisiones.cpp
    src/cpp/utils/json_io.cpp
)

# Ejecutable principal
add_executable(horarios_backend ${SOURCES})

# Linkear librería JSON si se encontró
if(nlohmann_json_FOUND)
    target_link_libraries(horarios_backend nlohmann_json::nlohmann_json)
endif()

# Configuración de instalación
install(TARGETS horarios_backend DESTINATION bin)

# Mensaje de ayuda
message(STATUS "=== Sistema de Gestión de Horarios ===")
message(STATUS "Compilar con: cmake -B build && cmake --build build")
message(STATUS "Ejecutar con: ./build/horarios_backend <input.json> <output.json>")
