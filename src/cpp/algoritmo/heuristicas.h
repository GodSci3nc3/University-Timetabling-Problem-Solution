#ifndef HEURISTICAS_H
#define HEURISTICAS_H

#include "../core/modelos.h"
#include "../core/grafo_conflictos.h"
#include <vector>
#include <map>

struct AsignacionPendiente {
    Grupo grupo;
    Materia materia;
    int horas_restantes;
    std::vector<Profesor> profesores_disponibles;
    
    AsignacionPendiente(const Grupo& g, const Materia& m, int h, 
                       const std::vector<Profesor>& profs);
};

std::vector<Slot> seleccionarMejorSlot(
    const std::vector<Slot>& slots_disponibles,
    const std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>& horario,
    const Grupo& grupo
);

#endif
