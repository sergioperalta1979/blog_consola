# main.py
# Archivo principal del sistema de blog por consola.
# Su trabajo es coordinar: carga los posts desde posts.json, crea el objeto Blog y
# llama al método que corresponde según la opción que elige el usuario.
# Para ejecutarlo, desde esta carpeta:  python main.py

from blog.datos import cargar_posts, guardar_posts
from blog.menu import mostrar_menu, pedir_texto, pedir_datos_post
from blog.modelos import Blog, Autor
from blog.operaciones import mostrar_validaciones

if __name__ == "__main__":
    # Al iniciar: se cargan los posts desde posts.json y se arma el Blog con ellos
    posts_cargados, mensajes = cargar_posts()
    for mensaje in mensajes:
        print(mensaje)
    blog = Blog(posts_cargados)

    # El programa sigue en marcha hasta que el usuario elige la opción 7
    while True:
        opcion = mostrar_menu()

        if opcion == 1:
            # Ver todos los posts
            blog.listar_posts()

        elif opcion == 2:
            # Buscar por título
            termino = pedir_texto("Buscar por titulo: ")
            if termino == "":
                print("La búsqueda no puede estar vacía.")
            else:
                encontrados = blog.buscar_por_titulo(termino)
                if len(encontrados) == 0:
                    print(f'No se encontraron posts con "{termino}" en el título.')
                else:
                    print(f'Resultados para "{termino}":')
                    blog.listar_posts(encontrados)

        elif opcion == 3:
            # Filtrar por tag
            tag = pedir_texto("Filtrar por tag: ")
            if tag == "":
                print("El tag no puede estar vacío.")
            else:
                encontrados = blog.filtrar_por_tag(tag)
                if len(encontrados) == 0:
                    print(f'No hay posts con el tag "{tag}".')
                else:
                    print(f"Posts con el tag {tag}:")
                    blog.listar_posts(encontrados)

        elif opcion == 4:
            # Crear un post nuevo: se piden los datos, se crea el objeto Post y se agrega al Blog
            datos = pedir_datos_post(blog.autor_por_defecto().nombre)
            try:
                # Si el autor ya existe en el blog se reutiliza; si no, se crea uno nuevo
                autor = blog.autor_por_defecto()
                if autor.nombre != datos["nombre_autor"]:
                    autor = Autor(datos["nombre_autor"])
                nuevo = blog.crear_post(datos["titulo"], datos["contenido"], autor,
                                        datos["tags"], datos["estado"])
                print(f"Post creado (id {nuevo.id}): {nuevo.resumen()}")
                print("Recordá guardarlo con la opción 6 (o se guarda solo al salir).")
            except ValueError as error:
                print(f"No se pudo crear el post: {error}.")

        elif opcion == 5:
            # Validar los posts
            mostrar_validaciones(blog.validar_posts())

        elif opcion == 6:
            # Guardar los posts en posts.json
            guardado, mensaje = guardar_posts(blog.obtener_posts())
            print(mensaje)
            if guardado:
                blog.modificado = False

        elif opcion == 7:
            # Salir: si hay cambios sin guardar, se guardan antes de cerrar
            if blog.modificado:
                guardado, mensaje = guardar_posts(blog.obtener_posts())
                print(mensaje)
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        elif opcion is not None:
            # Es un número, pero no es una opción del menú (si fue texto, ya se avisó)
            print("Opción inexistente: elegí un número del 1 al 7.")
