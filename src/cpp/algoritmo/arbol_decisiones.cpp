#include "arbol_decisiones.h"

NodoArbol::NodoArbol(const std::string& id, const std::string& tipo, int prof)
    : id(id), tipo(tipo), estado("explorando"), profundidad(prof) {}

ArbolDecisiones::ArbolDecisiones() 
    : nodo_raiz_id(""), nodo_actual_id(""), contador_nodos(0) {
    nodo_raiz_id = agregarNodo("raiz", 0, {{"descripcion", "Estado inicial"}});
    nodo_actual_id = nodo_raiz_id;
}

std::string ArbolDecisiones::agregarNodo(const std::string& tipo, int profundidad,
                                        const std::map<std::string, std::string>& datos,
                                        const std::string& padre_id) {
    std::string nuevo_id = "nodo_" + std::to_string(contador_nodos++);
    
    NodoArbol nuevo_nodo(nuevo_id, tipo, profundidad);
    nuevo_nodo.datos = datos;
    nuevo_nodo.padre_id = padre_id;
    
    nodos[nuevo_id] = nuevo_nodo;
    
    if (!padre_id.empty() && nodos.find(padre_id) != nodos.end()) {
        nodos[padre_id].hijos_ids.push_back(nuevo_id);
    }
    
    nodo_actual_id = nuevo_id;
    return nuevo_id;
}

void ArbolDecisiones::marcarExito(const std::string& nodo_id) {
    if (nodos.find(nodo_id) != nodos.end()) {
        nodos[nodo_id].estado = "exito";
    }
}

void ArbolDecisiones::marcarFallo(const std::string& nodo_id) {
    if (nodos.find(nodo_id) != nodos.end()) {
        nodos[nodo_id].estado = "fallo";
    }
}
