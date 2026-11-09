# blog/operaciones.py
# Operaciones principales del blog: listar, buscar por título, filtrar por tag
# y mostrar el resultado de las validaciones.
# Las funciones reciben los datos por parámetro: no dependen de variables globales.

from blog.validaciones import validar_post


def obtener_nombre_autor(post):
    """Devuelve el nombre del autor del post, o un aviso si el dato falta o está mal."""
    autor = post.get("autor")  # .get() evita el KeyError si no existe la clave
    if isinstance(autor, dict):
        return autor.get("nombre", "(autor sin nombre)")
    return "(autor inválido)"


def listar_posts(lista):
    """Muestra el título, el autor y el estado de cada post de la lista recibida."""
    if len(lista) == 0:
        print("No hay posts para mostrar.")
        return
    print("Posts disponibles:")
    for post in lista:
        if isinstance(post, dict):
            titulo = post.get("titulo", "(sin título)")
            estado = post.get("estado", "(sin estado)")
            print(f"- {titulo} | Autor: {obtener_nombre_autor(post)} | Estado: {estado}")
        else:
            print("- (post con formato inválido)")


def buscar_por_titulo(lista, termino):
    """Devuelve los posts cuyo título contiene el término (sin importar mayúsculas)."""
    termino = termino.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            titulo = post.get("titulo", "")
            # Solo se compara si el título es un texto
            if isinstance(titulo, str) and termino in titulo.lower():
                resultados.append(post)
    return resultados


def filtrar_por_tag(lista, tag):
    """Devuelve los posts que tienen ese tag en su lista de tags (sin importar mayúsculas)."""
    tag = tag.lower()
    resultados = []
    for post in lista:
        if isinstance(post, dict):
            tags_del_post = post.get("tags", [])
            # Solo se recorre si "tags" es realmente una lista
            if isinstance(tags_del_post, list):
                for t in tags_del_post:
                    if isinstance(t, str) and t.lower() == tag:
                        resultados.append(post)
                        break  # ya coincidió: no hace falta seguir con los demás tags
    return resultados


def mostrar_validaciones(lista):
    """Valida cada post de la lista y muestra cuáles son válidos y cuáles tienen errores."""
    print("Validación de posts:")
    for posicion, post in enumerate(lista, 1):
        es_valido, mensaje = validar_post(post)
        if es_valido:
            print(f"Post {posicion}: válido")
        else:
            print(f"Post {posicion}: error - {mensaje}")
