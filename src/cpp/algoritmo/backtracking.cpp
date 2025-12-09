#include "backtracking.h"
#include "restricciones.h"
#include "../core/config.h"
#include <algorithm>
#include <chrono>
#include <iostream>

ResultadoBacktracking::ResultadoBacktracking() : exito(false) {}

BacktrackingSolver::BacktrackingSolver(const std::vector<Grupo>& g,
                                       const std::vector<Materia>& m,
                                       const std::vector<Profesor>& p,
                                       const GrafoConflictos& grafo_conflictos)
    : grupos(g), materias(m), profesores(p), grafo(grafo_conflictos) {}

void BacktrackingSolver::inicializarEstado() {
    horario.clear();
    profesor_ocupado.clear();
    horas_asignadas_profesor.clear();
    horas_asignadas_materia.clear();
    
    for (const auto& profesor : profesores) {
        horas_asignadas_profesor[profesor.nombre] = 0;
    }
    
    for (const auto& materia : materias) {
        for (const auto& grupo_nombre : materia.grupos_que_cursan) {
            horas_asignadas_materia[grupo_nombre][materia.nombre] = 0;
        }
    }
}

void BacktrackingSolver::construirAsignacionesPendientes() {
    asignaciones_pendientes.clear();
    
    for (const auto& materia : materias) {
        for (const auto& grupo_nombre : materia.grupos_que_cursan) {
            Grupo* grupo_ptr = nullptr;
            for (const auto& g : grupos) {
                if (g.nombre == grupo_nombre) {
                    grupo_ptr = const_cast<Grupo*>(&g);
                    break;
                }
            }
            
            if (!grupo_ptr) continue;
            if (!grupo_ptr) continue;
            
            std::vector<Profesor> profesores_capacitados;
            for (const auto& profesor : profesores) {
                if (profesor.puedeImpartir(materia.nombre)) {
                    profesores_capacitados.push_back(profesor);
                }
            }
            
            AsignacionPendiente asig(*grupo_ptr, materia, materia.horas_semana, profesores_capacitados);
            asignaciones_pendientes.push_back(asig);
        }
    }
}

void BacktrackingSolver::hacerAsignacion(const Grupo& grupo, const Materia& materia,
                                        const Profesor& profesor, const Slot& slot) {
    std::string valor = materia.nombre + "|" + profesor.nombre;
    horario[grupo.nombre][slot.dia][slot.getKey()][":valor"] = valor;
    profesor_ocupado[profesor.nombre][slot.dia][slot.getKey()] = true;
    horas_asignadas_profesor[profesor.nombre]++;
    horas_asignadas_materia[grupo.nombre][materia.nombre]++;
}

void BacktrackingSolver::deshacerAsignacion(const Grupo& grupo, const Materia& materia,
                                           const Profesor& profesor, const Slot& slot) {
    horario[grupo.nombre][slot.dia][slot.getKey()].erase(":valor");
    if (horario[grupo.nombre][slot.dia][slot.getKey()].empty()) {
        horario[grupo.nombre][slot.dia].erase(slot.getKey());
    }
    profesor_ocupado[profesor.nombre][slot.dia].erase(slot.getKey());
    horas_asignadas_profesor[profesor.nombre]--;
    horas_asignadas_materia[grupo.nombre][materia.nombre]--;
}

bool BacktrackingSolver::esSolucionCompleta() const {
    for (const auto& materia : materias) {
        for (const auto& grupo_nombre : materia.grupos_que_cursan) {
            auto grupo_it = horas_asignadas_materia.find(grupo_nombre);
            if (grupo_it == horas_asignadas_materia.end()) return false;
            
            auto materia_it = grupo_it->second.find(materia.nombre);
            if (materia_it == grupo_it->second.end()) return false;
            
            if (materia_it->second < materia.horas_semana) return false;
        }
    }
    return true;
}

bool BacktrackingSolver::intentarAsignar(const AsignacionPendiente& asignacion,
                                        const std::string& nodo_padre_id, int profundidad) {
    const auto& grupo = asignacion.grupo;
    const auto& materia = asignacion.materia;
    
    int horas_necesarias = materia.horas_semana;
    auto grupo_it = horas_asignadas_materia.find(grupo.nombre);
    if (grupo_it != horas_asignadas_materia.end()) {
        auto materia_it = grupo_it->second.find(materia.nombre);
        if (materia_it != grupo_it->second.end()) {
            horas_necesarias -= materia_it->second;
        }
    }
    
    if (horas_necesarias <= 0) return true;
    
    auto slots_turno = getAllSlots(grupo.turno);
    auto slots_ordenados = seleccionarMejorSlot(slots_turno, horario, grupo);
    
    for (const auto& slot : slots_ordenados) {
        for (const auto& profesor : asignacion.profesores_disponibles) {
            auto [valido, razon] = validarRestriccionesDuras(
                horario, grupo, materia, profesor, slot,
                profesor_ocupado, horas_asignadas_profesor
            );
            
            if (valido) {
                hacerAsignacion(grupo, materia, profesor, slot);
                
                if (horas_asignadas_materia[grupo.nombre][materia.nombre] >= materia.horas_semana) {
                    return true;
                }
                
                if (intentarAsignar(asignacion, nodo_padre_id, profundidad + 1)) {
                    return true;
                }
                
                deshacerAsignacion(grupo, materia, profesor, slot);
            }
        }
    }
    
    return false;
}

bool BacktrackingSolver::backtrackRecursivo(size_t indice, const std::string& nodo_padre_id, int profundidad) {
    if (indice >= asignaciones_pendientes.size()) {
        return esSolucionCompleta();
    }
    
    const auto& asignacion = asignaciones_pendientes[indice];
    
    if (intentarAsignar(asignacion, nodo_padre_id, profundidad)) {
        return backtrackRecursivo(indice + 1, nodo_padre_id, profundidad + 1);
    }
    
    return false;
}

ResultadoBacktracking BacktrackingSolver::resolver() {
    ResultadoBacktracking resultado;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    inicializarEstado();
    construirAsignacionesPendientes();
    
    std::cout << "Iniciando backtracking..." << std::endl;
    std::cout << "Asignaciones pendientes: " << asignaciones_pendientes.size() << std::endl;
    
    bool exito = backtrackRecursivo(0, "raiz", 1);
    
    auto fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duracion = fin - inicio;
    
    resultado.exito = exito;
    resultado.horario = horario;
    resultado.estadisticas["tiempo_total"] = duracion.count();
    resultado.estadisticas["nodos_explorados"] = static_cast<double>(arbol.getTotalNodos());
    
    if (exito) {
        std::cout << "Solucion encontrada!" << std::endl;
    } else {
        std::cout << "No se encontro solucion" << std::endl;
    }
    
    return resultado;
}
