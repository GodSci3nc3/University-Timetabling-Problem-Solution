#include "modelos.h"
#include <algorithm>
#include <sstream>

Grupo::Grupo(int cuatri, const std::string& t, const std::string& n)
    : cuatrimestre(cuatri), turno(t), nombre(n) {}

std::string Grupo::toString() const {
    return nombre + " (" + turno + ")";
}

Materia::Materia(const std::string& n, int cuatri, int horas)
    : nombre(n), cuatrimestre(cuatri), horas_semana(horas) {}

void Materia::agregarGrupo(const std::string& grupo_nombre) {
    grupos_que_cursan.push_back(grupo_nombre);
}

std::string Materia::toString() const {
    return nombre + " (" + std::to_string(horas_semana) + "h/sem)";
}

Profesor::Profesor(const std::string& n, const std::vector<std::string>& materias,
                   int horas_disp, const std::string& turno_pref)
    : nombre(n), materias_imparte(materias), horas_disponibles(horas_disp),
      turno_preferido(turno_pref), horas_asignadas(0) {}

bool Profesor::puedeImpartir(const std::string& materia) const {
    return std::find(materias_imparte.begin(), materias_imparte.end(), materia) 
           != materias_imparte.end();
}

bool Profesor::tieneDisponibilidad(int horas) const {
    return (horas_asignadas + horas) <= horas_disponibles;
}

bool Profesor::estaDisponibleEnSlot(const std::string& dia, const std::string& hora_inicio,
                                    const std::string& hora_fin) const {
    if (disponibilidad_horaria.empty()) {
        return true;
    }
    
    auto it = disponibilidad_horaria.find(dia);
    if (it == disponibilidad_horaria.end()) {
        return false;
    }
    
    int hora_slot_inicio = std::stoi(hora_inicio.substr(0, 2));
    int hora_slot_fin = std::stoi(hora_fin.substr(0, 2));
    
    for (const auto& rango : it->second) {
        int hora_rango_inicio = std::stoi(rango.first.substr(0, 2));
        int hora_rango_fin = std::stoi(rango.second.substr(0, 2));
        
        if (hora_slot_inicio >= hora_rango_inicio && hora_slot_fin <= hora_rango_fin) {
            return true;
        }
    }
    
    return false;
}

std::string Profesor::toString() const {
    return nombre + " (" + std::to_string(horas_asignadas) + "/" + 
           std::to_string(horas_disponibles) + "h)";
}

Slot::Slot(const std::string& d, const std::string& hi, 
           const std::string& hf, const std::string& t)
    : dia(d), hora_inicio(hi), hora_fin(hf), turno(t) {}

std::string Slot::toString() const {
    return dia + " " + hora_inicio + "-" + hora_fin;
}

std::string Slot::getKey() const {
    return hora_inicio + "-" + hora_fin;
}

Asignacion::Asignacion(const std::string& g, const std::string& m,
                       const std::string& p, const Slot& s)
    : grupo_nombre(g), materia_nombre(m), profesor_nombre(p), slot(s) {}

std::string Asignacion::toString() const {
    return grupo_nombre + " - " + materia_nombre + " - " + 
           profesor_nombre + " @ " + slot.toString();
}
