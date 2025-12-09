#ifndef RESTRICCIONES_H
#define RESTRICCIONES_H

#include "../core/modelos.h"
#include <map>
#include <string>
#include <tuple>

using Horario = std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>;
using Estado = std::map<std::string, std::map<std::string, std::map<std::string, bool>>>;

std::pair<bool, std::string> validarRestriccionesDuras(
    const Horario& horario,
    const Grupo& grupo,
    const Materia& materia,
    const Profesor& profesor,
    const Slot& slot,
    const Estado& profesor_ocupado,
    const std::map<std::string, int>& horas_asignadas_profesor
);

#endif
