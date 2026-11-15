# blog/menu.py
# Menú e interacción con el usuario: acá está todo el manejo de input().

from blog.datos import etiquetas_blog


def mostrar_menu():
    """Muestra el menú y devuelve la opción elegida como número entero.
    Si el usuario escribe texto en lugar de un número, avisa y devuelve None."""
    print()
    print("--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")
    try:
        return int(input("Elige una opción: "))
    except ValueError:
        # int() falla si el texto no es un número: se avisa y el menú vuelve a mostrarse
        print("Opción inválida: ingresá un número del 1 al 7, no texto.")
        return None


def pedir_texto(mensaje):
    """Pide un texto al usuario y lo devuelve sin espacios al principio ni al final."""
    return input(mensaje).strip()


def pedir_datos_post(nombre_autor_sugerido):
    """Pide por consola los datos de un post nuevo y los devuelve en un diccionario.
    Si el autor se deja vacío, se usa el sugerido. Los tags se escriben separados por comas."""
    print("--- NUEVO POST ---")
    titulo = pedir_texto("Título: ")
    contenido = pedir_texto("Contenido: ")
    nombre_autor = pedir_texto(f"Autor (Enter para usar a {nombre_autor_sugerido}): ")
    if nombre_autor == "":
        nombre_autor = nombre_autor_sugerido
    print("Etiquetas sugeridas:", ", ".join(sorted(etiquetas_blog)))
    texto_tags = pedir_texto("Tags separados por comas (se puede dejar vacío): ")
    tags = []
    for tag in texto_tags.split(","):
        if tag.strip() != "":
            tags.append(tag.strip())
    estado = pedir_texto("Estado (borrador, publicado o archivado) [borrador]: ").lower()
    if estado == "":
        estado = "borrador"
    return {
        "titulo": titulo,
        "contenido": contenido,
        "nombre_autor": nombre_autor,
        "tags": tags,
        "estado": estado,
    }
