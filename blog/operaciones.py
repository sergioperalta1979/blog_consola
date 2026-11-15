# blog/operaciones.py
# Presentación de resultados: muestra por pantalla lo que calculan las clases.
# La lógica principal (listar, buscar, filtrar, crear y validar) vive ahora en la
# clase Blog de modelos.py; este módulo solo se ocupa de mostrar los resultados.


def mostrar_validaciones(resultados):
    """Muestra el resultado de validar los posts.
    Recibe la lista de (posición, es_válido, mensaje) que devuelve Blog.validar_posts()."""
    print("Validación de posts:")
    if len(resultados) == 0:
        print("No hay posts para validar.")
        return
    for posicion, es_valido, mensaje in resultados:
        if es_valido:
            print(f"Post {posicion}: válido")
        else:
            print(f"Post {posicion}: error - {mensaje}")
