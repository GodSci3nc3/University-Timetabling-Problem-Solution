#ifndef JSON_IO_H
#define JSON_IO_H

#include "../core/modelos.h"
#include "../core/grafo_conflictos.h"
#include "../algoritmo/backtracking.h"
#include "json/include/json.hpp"
#include <string>
#include <vector>

using json = nlohmann::json;

struct DatosEntrada {
    std::vector<Grupo> grupos;
    std::vector<Materia> materias;
    std::vector<Profesor> profesores;
};

DatosEntrada leerJSON(const std::string& archivo);
void escribirJSON(const std::string& archivo, const ResultadoBacktracking& resultado);

#endif
