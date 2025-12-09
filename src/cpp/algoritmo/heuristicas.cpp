#include "heuristicas.h"
#include <algorithm>

AsignacionPendiente::AsignacionPendiente(const Grupo& g, const Materia& m, 
                                         int h, const std::vector<Profesor>& profs)
    : grupo(g), materia(m), horas_restantes(h), profesores_disponibles(profs) {}

std::vector<Slot> seleccionarMejorSlot(
    const std::vector<Slot>& slots_disponibles,
    const std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>& horario,
    const Grupo& grupo
) {
    auto slots_ordenados = slots_disponibles;
    
    std::sort(slots_ordenados.begin(), slots_ordenados.end(),
        [&horario, &grupo](const Slot& s1, const Slot& s2) {
            int restriccion1 = 0;
            int restriccion2 = 0;
            
            auto grupo_it = horario.find(grupo.nombre);
            if (grupo_it != horario.end()) {
                auto dia1_it = grupo_it->second.find(s1.dia);
                if (dia1_it != grupo_it->second.end()) {
                    for (const auto& slot_pair : dia1_it->second) {
                        if (!slot_pair.second.empty()) restriccion1 += 2;
                    }
                }
                
                auto dia2_it = grupo_it->second.find(s2.dia);
                if (dia2_it != grupo_it->second.end()) {
                    for (const auto& slot_pair : dia2_it->second) {
                        if (!slot_pair.second.empty()) restriccion2 += 2;
                    }
                }
            }
            
            int hora1 = std::stoi(s1.hora_inicio.substr(0, 2));
            int hora2 = std::stoi(s2.hora_inicio.substr(0, 2));
            
            if (hora1 < 10) restriccion1 -= 3;
            else if (hora1 > 18) restriccion1 += 3;
            
            if (hora2 < 10) restriccion2 -= 3;
            else if (hora2 > 18) restriccion2 += 3;
            
            return restriccion1 < restriccion2;
        });
    
    return slots_ordenados;
}
