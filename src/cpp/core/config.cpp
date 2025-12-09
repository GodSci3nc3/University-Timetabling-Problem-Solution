#include "config.h"

std::vector<Slot> getAllSlots(const std::string& turno) {
    std::vector<Slot> slots;
    
    const auto& horarios = (turno == "Matutino") ? SLOTS_MATUTINO : SLOTS_VESPERTINO;
    
    for (const auto& dia : DIAS_SEMANA) {
        for (const auto& horario : horarios) {
            slots.emplace_back(dia, horario.first, horario.second, turno);
        }
    }
    
    return slots;
}
