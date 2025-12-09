#ifndef BACKTRACKING_H
#define BACKTRACKING_H

#include "../core/modelos.h"
#include "../core/grafo_conflictos.h"
#include "arbol_decisiones.h"
#include "heuristicas.h"
#include <map>
#include <vector>
#include <memory>

struct ResultadoBacktracking {
    bool exito;
    std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>> horario;
    std::map<std::string, double> estadisticas;
    
    ResultadoBacktracking();
};

class BacktrackingSolver {
private:
    std::vector<Grupo> grupos;
    std::vector<Materia> materias;
    std::vector<Profesor> profesores;
    GrafoConflictos grafo;
    ArbolDecisiones arbol;
    
    std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>> horario;
    std::map<std::string, std::map<std::string, std::map<std::string, bool>>> profesor_ocupado;
    std::map<std::string, int> horas_asignadas_profesor;
    std::map<std::string, std::map<std::string, int>> horas_asignadas_materia;
    
    std::vector<AsignacionPendiente> asignaciones_pendientes;
    
    void inicializarEstado();
    void construirAsignacionesPendientes();
    bool backtrackRecursivo(size_t indice, const std::string& nodo_padre_id, int profundidad);
    bool intentarAsignar(const AsignacionPendiente& asignacion, const std::string& nodo_padre_id, int profundidad);
    void hacerAsignacion(const Grupo& grupo, const Materia& materia, const Profesor& profesor, const Slot& slot);
    void deshacerAsignacion(const Grupo& grupo, const Materia& materia, const Profesor& profesor, const Slot& slot);
    bool esSolucionCompleta() const;

public:
    BacktrackingSolver(const std::vector<Grupo>& g, const std::vector<Materia>& m,
                      const std::vector<Profesor>& p, const GrafoConflictos& grafo_conflictos);
    
    ResultadoBacktracking resolver();
};

#endif
