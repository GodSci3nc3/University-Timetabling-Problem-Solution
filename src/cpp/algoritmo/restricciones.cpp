#include "restricciones.h"

std::pair<bool, std::string> validarRestriccionesDuras(
    const Horario& horario,
    const Grupo& grupo,
    const Materia& materia,
    const Profesor& profesor,
    const Slot& slot,
    const Estado& profesor_ocupado,
    const std::map<std::string, int>& horas_asignadas_profesor
) {
    if (slot.turno != grupo.turno) {
        return {false, "Slot no corresponde al turno del grupo"};
    }
    
    auto grupo_it = horario.find(grupo.nombre);
    if (grupo_it != horario.end()) {
        auto dia_it = grupo_it->second.find(slot.dia);
        if (dia_it != grupo_it->second.end()) {
            auto slot_it = dia_it->second.find(slot.getKey());
            if (slot_it != dia_it->second.end() && !slot_it->second.empty()) {
                return {false, "Grupo ya tiene clase en este slot"};
            }
        }
    }
    
    auto prof_it = profesor_ocupado.find(profesor.nombre);
    if (prof_it != profesor_ocupado.end()) {
        auto dia_it = prof_it->second.find(slot.dia);
        if (dia_it != prof_it->second.end()) {
            auto slot_it = dia_it->second.find(slot.getKey());
            if (slot_it != dia_it->second.end() && slot_it->second) {
                return {false, "Profesor ya esta ocupado en este slot"};
            }
        }
    }
    
    auto horas_it = horas_asignadas_profesor.find(profesor.nombre);
    int horas_actuales = (horas_it != horas_asignadas_profesor.end()) ? horas_it->second : 0;
    if (horas_actuales >= profesor.horas_disponibles) {
        return {false, "Profesor no tiene horas disponibles"};
    }
    
    if (profesor.turno_preferido != "Ambos" && profesor.turno_preferido != slot.turno) {
        return {false, "Turno no compatible con preferencia del profesor"};
    }
    
    if (!profesor.estaDisponibleEnSlot(slot.dia, slot.hora_inicio, slot.hora_fin)) {
        return {false, "Profesor no disponible en este horario"};
    }
    
    return {true, "Valido"};
}
