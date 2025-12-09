#ifndef MODELOS_H
#define MODELOS_H

#include <string>
#include <vector>
#include <map>

class Grupo {
public:
    int cuatrimestre;
    std::string turno;
    std::string nombre;
    
    Grupo(int cuatri, const std::string& t, const std::string& n);
    std::string toString() const;
};

class Materia {
public:
    std::string nombre;
    int cuatrimestre;
    int horas_semana;
    std::vector<std::string> grupos_que_cursan;
    
    Materia(const std::string& n, int cuatri, int horas);
    void agregarGrupo(const std::string& grupo_nombre);
    std::string toString() const;
};

class Profesor {
public:
    std::string nombre;
    std::vector<std::string> materias_imparte;
    int horas_disponibles;
    std::string turno_preferido;
    std::map<std::string, std::vector<std::pair<std::string, std::string>>> disponibilidad_horaria;
    int horas_asignadas;
    
    Profesor(const std::string& n, const std::vector<std::string>& materias,
             int horas_disp, const std::string& turno_pref);
    
    bool puedeImpartir(const std::string& materia) const;
    bool tieneDisponibilidad(int horas) const;
    bool estaDisponibleEnSlot(const std::string& dia, const std::string& hora_inicio, 
                              const std::string& hora_fin) const;
    std::string toString() const;
};

class Slot {
public:
    std::string dia;
    std::string hora_inicio;
    std::string hora_fin;
    std::string turno;
    
    Slot(const std::string& d, const std::string& hi, 
         const std::string& hf, const std::string& t);
    
    std::string toString() const;
    std::string getKey() const;
};

class Asignacion {
public:
    std::string grupo_nombre;
    std::string materia_nombre;
    std::string profesor_nombre;
    Slot slot;
    
    Asignacion(const std::string& g, const std::string& m,
               const std::string& p, const Slot& s);
    
    std::string toString() const;
};

#endif
