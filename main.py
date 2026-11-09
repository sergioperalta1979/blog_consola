# main.py
# Archivo principal del sistema de blog por consola.
# Su trabajo es coordinar: importa las piezas del paquete blog y llama a la
# función que corresponde según la opción que elige el usuario.
# Para ejecutarlo, desde esta carpeta:  python main.py

from blog.datos import posts
from blog.menu import mostrar_menu, pedir_texto
from blog.operaciones import (
    listar_posts,
    buscar_por_titulo,
    filtrar_por_tag,
    mostrar_validaciones,
)

if __name__ == "__main__":
    # El programa sigue en marcha hasta que el usuario elige la opción 5
    while True:
        opcion = mostrar_menu()

        if opcion == 1:
            # Ver todos los posts
            listar_posts(posts)

        elif opcion == 2:
            # Buscar por título
            termino = pedir_texto("Buscar por titulo: ")
            if termino == "":
                print("La búsqueda no puede estar vacía.")
            else:
                encontrados = buscar_por_titulo(posts, termino)
                if len(encontrados) == 0:
                    print(f'No se encontraron posts con "{termino}" en el título.')
                else:
                    print(f'Resultados para "{termino}":')
                    listar_posts(encontrados)

        elif opcion == 3:
            # Filtrar por tag
            tag = pedir_texto("Filtrar por tag: ")
            if tag == "":
                print("El tag no puede estar vacío.")
            else:
                encontrados = filtrar_por_tag(posts, tag)
                if len(encontrados) == 0:
                    print(f'No hay posts con el tag "{tag}".')
                else:
                    print(f"Posts con el tag {tag}:")
                    listar_posts(encontrados)

        elif opcion == 4:
            # Validar todos los posts
            mostrar_validaciones(posts)

        elif opcion == 5:
            # Salir del programa
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        elif opcion is not None:
            # Es un número, pero no es una opción del menú (si fue texto, ya se avisó)
            print("Opción inexistente: elegí un número del 1 al 5.")
