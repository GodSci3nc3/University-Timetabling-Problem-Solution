#include <iostream>
#include <string>
#include "core/modelos.h"
#include "core/grafo_conflictos.h"
#include "core/config.h"
#include "algoritmo/backtracking.h"
#include "utils/json_io.h"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Uso: " << argv[0] << " <archivo_entrada.json> <archivo_salida.json>" << std::endl;
        return 1;
    }
    
    std::string archivo_entrada = argv[1];
    std::string archivo_salida = argv[2];
    
    try {
        std::cout << "Leyendo datos de entrada desde " << archivo_entrada << "..." << std::endl;
        DatosEntrada datos = leerJSON(archivo_entrada);
        
        std::cout << "Grupos cargados: " << datos.grupos.size() << std::endl;
        std::cout << "Materias cargadas: " << datos.materias.size() << std::endl;
        std::cout << "Profesores cargados: " << datos.profesores.size() << std::endl;
        
        std::cout << "\nConstruyendo grafo de conflictos..." << std::endl;
        GrafoConflictos grafo;
        grafo.construirDesdeDatos(datos.grupos, datos.materias, datos.profesores);
        
        std::cout << "Nodos en el grafo: " << grafo.getNumNodos() << std::endl;
        std::cout << "Aristas en el grafo: " << grafo.getNumAristas() << std::endl;
        
        std::cout << "\nResolviendo con backtracking..." << std::endl;
        BacktrackingSolver solver(datos.grupos, datos.materias, datos.profesores, grafo);
        ResultadoBacktracking resultado = solver.resolver();
        
        std::cout << "\nEscribiendo resultados en " << archivo_salida << "..." << std::endl;
        escribirJSON(archivo_salida, resultado);
        
        if (resultado.exito) {
            std::cout << "\nTiempo de ejecucion: " << resultado.estadisticas["tiempo_total"] 
                      << " segundos" << std::endl;
            std::cout << "Nodos explorados: " << resultado.estadisticas["nodos_explorados"] << std::endl;
        }
        
        std::cout << "\nProceso completado exitosamente." << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
