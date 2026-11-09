# blog/validaciones.py
# Reglas lógicas del sistema: revisa que un post tenga la estructura esperada.
# Solo importa de datos.py (nunca al revés), para evitar imports circulares.

from blog.datos import estados_post

# Claves que todo post tiene que tener
CLAVES_OBLIGATORIAS = ("id", "titulo", "contenido", "autor", "tags", "estado")


def validar_post(post, estados_validos=estados_post):
    """Revisa que un post cumpla las reglas esperadas.
    Devuelve (True, "") si es válido, o (False, mensaje) explicando el problema.
    Los estados válidos se reciben por parámetro (por defecto, los de estados_post)."""
    # El post tiene que ser un diccionario
    if not isinstance(post, dict):
        return False, "el post no es un diccionario"

    # Tienen que existir todas las claves obligatorias
    for clave in CLAVES_OBLIGATORIAS:
        if clave not in post:
            return False, f'falta la clave "{clave}"'

    # Título y contenido: tienen que ser texto y no estar vacíos
    titulo = post.get("titulo")
    if not isinstance(titulo, str) or titulo.strip() == "":
        return False, "el título está vacío o no es texto"
    contenido = post.get("contenido")
    if not isinstance(contenido, str) or contenido.strip() == "":
        return False, "el contenido está vacío o no es texto"

    # El autor tiene que ser un diccionario con la clave "nombre"
    autor = post.get("autor")
    if not isinstance(autor, dict):
        return False, "el autor no es un diccionario"
    if "nombre" not in autor:
        return False, 'el autor no tiene la clave "nombre"'

    # Los tags tienen que estar guardados como lista
    if not isinstance(post.get("tags"), list):
        return False, "tags debe ser una lista"

    # El estado tiene que ser uno de los estados válidos
    estado = post.get("estado")
    if estado not in estados_validos:
        return False, f'el estado "{estado}" no está en {estados_validos}'

    return True, ""
