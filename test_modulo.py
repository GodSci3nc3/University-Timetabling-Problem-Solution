"""
Script de prueba del módulo de carga y validación de datos.
Demuestra el uso completo del sistema.
"""

import json
from src.data.lector_excel import leer_excel
from src.data.validador import validar_datos
from src.data.generador_tabla import generar_tabla_validacion, generar_resumen_carga


def main():
    """Función principal de prueba."""
    print("=" * 70)
    print("SISTEMA DE GESTIÓN DE HORARIOS ACADÉMICOS")
    print("Módulo de Carga y Validación de Datos")
    print("=" * 70)
    print()
    
    # Paso 1: Cargar datos desde Excel
    print("📂 Cargando datos desde 'datos_universidad.xlsx'...")
    try:
        grupos, materias, profesores = leer_excel("datos_universidad.xlsx")
        print(f"✓ Datos cargados exitosamente")
        print(f"  - Grupos: {len(grupos)}")
        print(f"  - Materias: {len(materias)}")
        print(f"  - Profesores: {len(profesores)}")
        print()
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        return
    
    # Paso 2: Mostrar resumen de datos cargados
    print("📊 RESUMEN DE DATOS CARGADOS")
    print("-" * 70)
    
    print("\n🎓 GRUPOS:")
    for grupo in grupos[:5]:  # Mostrar solo los primeros 5
        print(f"  • {grupo}")
    if len(grupos) > 5:
        print(f"  ... y {len(grupos) - 5} grupos más")
    
    print("\n📚 MATERIAS:")
    for materia in materias[:5]:
        print(f"  • {materia} - {len(materia.grupos_que_cursan)} grupos")
    if len(materias) > 5:
        print(f"  ... y {len(materias) - 5} materias más")
    
    print("\n👨‍🏫 PROFESORES:")
    for profesor in profesores:
        print(f"  • {profesor}")
        print(f"    Imparte: {', '.join(profesor.materias_imparte)}")
    print()
    
    # Paso 3: Validar datos
    print("🔍 VALIDANDO DATOS...")
    print("-" * 70)
    es_valido, errores = validar_datos(grupos, materias, profesores)
    
    if es_valido:
        print("✓ Todos los datos son válidos")
        print("✓ El sistema está listo para generar horarios")
    else:
        print("✗ Se encontraron los siguientes errores:")
        for i, error in enumerate(errores, 1):
            print(f"  {i}. {error}")
    print()
    
    # Paso 4: Generar tabla de validación
    print("📋 GENERANDO TABLA DE VALIDACIÓN...")
    print("-" * 70)
    tabla = generar_tabla_validacion(materias, grupos)
    
    # Mostrar tabla en formato legible
    for cuatrimestre, grupos_dict in tabla.items():
        print(f"\n{cuatrimestre.upper()}")
        for grupo_nombre, lista_materias in grupos_dict.items():
            print(f"\n  {grupo_nombre}:")
            for info in lista_materias:
                print(f"    • {info['materia']}: {info['horas_semana']}h/semana")
    print()
    
    # Paso 5: Generar resumen de carga
    print("📈 RESUMEN DE CARGA HORARIA")
    print("-" * 70)
    resumen = generar_resumen_carga(materias, grupos)
    
    for cuatrimestre, info in resumen.items():
        print(f"\n{cuatrimestre}:")
        print(f"  • Materias: {info['num_materias']}")
        print(f"  • Grupos: {info['num_grupos']}")
        print(f"  • Horas por grupo: {info['horas_por_grupo']}h/semana")
        print(f"  • Horas totales requeridas: {info['horas_totales_requeridas']}h/semana")
    
    print()
    print("=" * 70)
    print("✓ Prueba completada exitosamente")
    print("=" * 70)


if __name__ == "__main__":
    main()
