#ifndef GRAFO_CONFLICTOS_H
#define GRAFO_CONFLICTOS_H

#include <string>
#include <set>
#include <map>
#include <vector>
#include <memory>
#include "modelos.h"

struct NodoAsignacion {
    std::string grupo_nombre;
    std::string materia_nombre;
    int cuatrimestre;
    
    NodoAsignacion(const std::string& g, const std::string& m, int c);
    
    bool operator<(const NodoAsignacion& other) const;
    bool operator==(const NodoAsignacion& other) const;
    std::string toString() const;
};

class GrafoConflictos {
private:
    std::set<NodoAsignacion> nodos;
    std::map<NodoAsignacion, std::set<NodoAsignacion>> aristas;
    std::map<std::string, std::vector<std::string>> profesores_por_materia;
    
    void construirMapeoProfesores(const std::vector<Profesor>& profesores);
    bool tieneConflicto(const NodoAsignacion& n1, const NodoAsignacion& n2) const;
    bool compartenProfesor(const std::string& mat1, const std::string& mat2) const;

public:
    GrafoConflictos();
    
    void construirDesdeDatos(const std::vector<Grupo>& grupos,
                             const std::vector<Materia>& materias,
                             const std::vector<Profesor>& profesores);
    
    void agregarNodo(const NodoAsignacion& nodo);
    void agregarArista(const NodoAsignacion& n1, const NodoAsignacion& n2);
    
    std::set<NodoAsignacion> obtenerVecinos(const NodoAsignacion& nodo) const;
    int obtenerGrado(const NodoAsignacion& nodo) const;
    
    size_t getNumNodos() const { return nodos.size(); }
    size_t getNumAristas() const;
    
    const std::set<NodoAsignacion>& getNodos() const { return nodos; }
    const std::map<std::string, std::vector<std::string>>& getProfesoresPorMateria() const {
        return profesores_por_materia;
    }
};

#endif
