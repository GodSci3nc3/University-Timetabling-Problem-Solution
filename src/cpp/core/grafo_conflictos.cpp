#include "grafo_conflictos.h"
#include <algorithm>

NodoAsignacion::NodoAsignacion(const std::string& g, const std::string& m, int c)
    : grupo_nombre(g), materia_nombre(m), cuatrimestre(c) {}

bool NodoAsignacion::operator<(const NodoAsignacion& other) const {
    if (grupo_nombre != other.grupo_nombre)
        return grupo_nombre < other.grupo_nombre;
    if (materia_nombre != other.materia_nombre)
        return materia_nombre < other.materia_nombre;
    return cuatrimestre < other.cuatrimestre;
}

bool NodoAsignacion::operator==(const NodoAsignacion& other) const {
    return grupo_nombre == other.grupo_nombre && 
           materia_nombre == other.materia_nombre &&
           cuatrimestre == other.cuatrimestre;
}

std::string NodoAsignacion::toString() const {
    return "(" + grupo_nombre + ", " + materia_nombre + ")";
}

GrafoConflictos::GrafoConflictos() {}

void GrafoConflictos::construirMapeoProfesores(const std::vector<Profesor>& profesores) {
    for (const auto& profesor : profesores) {
        for (const auto& materia : profesor.materias_imparte) {
            profesores_por_materia[materia].push_back(profesor.nombre);
        }
    }
}

bool GrafoConflictos::compartenProfesor(const std::string& mat1, const std::string& mat2) const {
    auto it1 = profesores_por_materia.find(mat1);
    auto it2 = profesores_por_materia.find(mat2);
    
    if (it1 == profesores_por_materia.end() || it2 == profesores_por_materia.end())
        return false;
    
    const auto& profs1 = it1->second;
    const auto& profs2 = it2->second;
    
    for (const auto& p1 : profs1) {
        if (std::find(profs2.begin(), profs2.end(), p1) != profs2.end())
            return true;
    }
    
    return false;
}

bool GrafoConflictos::tieneConflicto(const NodoAsignacion& n1, const NodoAsignacion& n2) const {
    if (n1.grupo_nombre == n2.grupo_nombre)
        return true;
    
    if (compartenProfesor(n1.materia_nombre, n2.materia_nombre))
        return true;
    
    return false;
}

void GrafoConflictos::construirDesdeDatos(const std::vector<Grupo>& grupos,
                                          const std::vector<Materia>& materias,
                                          const std::vector<Profesor>& profesores) {
    construirMapeoProfesores(profesores);
    
    for (const auto& materia : materias) {
        for (const auto& grupo_nombre : materia.grupos_que_cursan) {
            NodoAsignacion nodo(grupo_nombre, materia.nombre, materia.cuatrimestre);
            agregarNodo(nodo);
        }
    }
    
    std::vector<NodoAsignacion> lista_nodos(nodos.begin(), nodos.end());
    for (size_t i = 0; i < lista_nodos.size(); i++) {
        for (size_t j = i + 1; j < lista_nodos.size(); j++) {
            if (tieneConflicto(lista_nodos[i], lista_nodos[j])) {
                agregarArista(lista_nodos[i], lista_nodos[j]);
            }
        }
    }
}

void GrafoConflictos::agregarNodo(const NodoAsignacion& nodo) {
    nodos.insert(nodo);
    if (aristas.find(nodo) == aristas.end()) {
        aristas[nodo] = std::set<NodoAsignacion>();
    }
}

void GrafoConflictos::agregarArista(const NodoAsignacion& n1, const NodoAsignacion& n2) {
    aristas[n1].insert(n2);
    aristas[n2].insert(n1);
}

std::set<NodoAsignacion> GrafoConflictos::obtenerVecinos(const NodoAsignacion& nodo) const {
    auto it = aristas.find(nodo);
    if (it != aristas.end()) {
        return it->second;
    }
    return std::set<NodoAsignacion>();
}

int GrafoConflictos::obtenerGrado(const NodoAsignacion& nodo) const {
    return obtenerVecinos(nodo).size();
}

size_t GrafoConflictos::getNumAristas() const {
    size_t total = 0;
    for (const auto& pair : aristas) {
        total += pair.second.size();
    }
    return total / 2;
}
