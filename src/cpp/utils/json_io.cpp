#include "json_io.h"
#include <fstream>
#include <iostream>

DatosEntrada leerJSON(const std::string& archivo) {
    std::ifstream f(archivo);
    if (!f.is_open()) {
        throw std::runtime_error("No se puede abrir el archivo: " + archivo);
    }
    
    json j;
    f >> j;
    
    DatosEntrada datos;
    
    for (const auto& g : j["grupos"]) {
        Grupo grupo(
            g["cuatrimestre"].get<int>(),
            g["turno"].get<std::string>(),
            g["nombre"].get<std::string>()
        );
        datos.grupos.push_back(grupo);
    }
    
    for (const auto& m : j["materias"]) {
        Materia materia(
            m["nombre"].get<std::string>(),
            m["cuatrimestre"].get<int>(),
            m["horas_semana"].get<int>()
        );
        datos.materias.push_back(materia);
    }
    
    for (const auto& p : j["profesores"]) {
        std::vector<std::string> materias_imparte;
        for (const auto& mat : p["materias_imparte"]) {
            materias_imparte.push_back(mat.get<std::string>());
        }
        
        Profesor profesor(
            p["nombre"].get<std::string>(),
            materias_imparte,
            p["horas_disponibles"].get<int>(),
            p["turno_preferido"].get<std::string>()
        );
        
        if (p.contains("disponibilidad_horaria") && !p["disponibilidad_horaria"].is_null()) {
            for (const auto& [dia, rangos] : p["disponibilidad_horaria"].items()) {
                std::vector<std::pair<std::string, std::string>> rangos_dia;
                for (const auto& rango : rangos) {
                    if (rango.is_array() && rango.size() == 2) {
                        rangos_dia.push_back({
                            rango[0].get<std::string>(),
                            rango[1].get<std::string>()
                        });
                    }
                }
                if (!rangos_dia.empty()) {
                    profesor.disponibilidad_horaria[dia] = rangos_dia;
                }
            }
        }
        
        datos.profesores.push_back(profesor);
    }
    
    for (auto& materia : datos.materias) {
        for (const auto& grupo : datos.grupos) {
            if (grupo.cuatrimestre == materia.cuatrimestre) {
                materia.agregarGrupo(grupo.nombre);
            }
        }
    }
    
    return datos;
}

void escribirJSON(const std::string& archivo, const ResultadoBacktracking& resultado) {
    json j;
    
    j["exito"] = resultado.exito;
    
    j["horario"] = json::object();
    for (const auto& [grupo_nombre, dias] : resultado.horario) {
        j["horario"][grupo_nombre] = json::object();
        for (const auto& [dia, slots] : dias) {
            j["horario"][grupo_nombre][dia] = json::object();
            for (const auto& [slot_key, datos_slot] : slots) {
                if (!datos_slot.empty()) {
                    auto it = datos_slot.find(":valor");
                    if (it != datos_slot.end()) {
                        const std::string& valor = it->second;
                        size_t pos = valor.find('|');
                        if (pos != std::string::npos) {
                            std::string materia = valor.substr(0, pos);
                            std::string profesor = valor.substr(pos + 1);
                            
                            j["horario"][grupo_nombre][dia][slot_key] = {
                                {"materia", materia},
                                {"profesor", profesor}
                            };
                        }
                    }
                }
            }
        }
    }
    
    j["estadisticas"] = resultado.estadisticas;
    
    std::ofstream f(archivo);
    if (!f.is_open()) {
        throw std::runtime_error("No se puede escribir el archivo: " + archivo);
    }
    
    f << j.dump(2);
    f.close();
}
