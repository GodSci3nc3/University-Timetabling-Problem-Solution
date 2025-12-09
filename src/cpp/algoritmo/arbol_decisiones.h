#ifndef ARBOL_DECISIONES_H
#define ARBOL_DECISIONES_H

#include <string>
#include <vector>
#include <map>

struct NodoArbol {
    std::string id;
    std::string tipo;
    std::string estado;
    int profundidad;
    std::map<std::string, std::string> datos;
    std::vector<std::string> hijos_ids;
    std::string padre_id;
    
    NodoArbol() : profundidad(0), estado("explorando") {}
    NodoArbol(const std::string& id, const std::string& tipo, int prof);
};

class ArbolDecisiones {
private:
    std::map<std::string, NodoArbol> nodos;
    std::string nodo_raiz_id;
    std::string nodo_actual_id;
    int contador_nodos;
    
public:
    ArbolDecisiones();
    
    std::string agregarNodo(const std::string& tipo, int profundidad,
                          const std::map<std::string, std::string>& datos,
                          const std::string& padre_id = "");
    
    void marcarExito(const std::string& nodo_id);
    void marcarFallo(const std::string& nodo_id);
    
    size_t getTotalNodos() const { return nodos.size(); }
    const std::map<std::string, NodoArbol>& getNodos() const { return nodos; }
};

#endif
