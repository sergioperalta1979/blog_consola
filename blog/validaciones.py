# blog/validaciones.py
# Reglas lógicas del sistema: revisa que los datos de un post tengan la estructura esperada.
# No importa nada de los otros módulos (los demás importan de acá), así se evitan
# los imports circulares.

# Tupla con los estados posibles de un post (datos fijos)
estados_post = ("borrador", "publicado", "archivado")

# Claves que todo post tiene que tener
CLAVES_OBLIGATORIAS = ("id", "titulo", "contenido", "autor", "tags", "estado")


def validar_post(datos, estados_validos=estados_post):
    """Revisa que los datos de un post (un diccionario) cumplan las reglas esperadas.
    Devuelve (True, "") si son válidos, o (False, mensaje) explicando el problema."""
    # El post tiene que ser un diccionario
    if not isinstance(datos, dict):
        return False, "el post no es un diccionario"

    # Tienen que existir todas las claves obligatorias
    for clave in CLAVES_OBLIGATORIAS:
        if clave not in datos:
            return False, f'falta la clave "{clave}"'

    # Título y contenido: tienen que ser texto y no estar vacíos
    titulo = datos.get("titulo")
    if not isinstance(titulo, str) or titulo.strip() == "":
        return False, "el título está vacío o no es texto"
    contenido = datos.get("contenido")
    if not isinstance(contenido, str) or contenido.strip() == "":
        return False, "el contenido está vacío o no es texto"

    # El autor tiene que ser un diccionario con la clave "nombre"
    autor = datos.get("autor")
    if not isinstance(autor, dict):
        return False, "el autor no es un diccionario"
    if "nombre" not in autor:
        return False, 'el autor no tiene la clave "nombre"'

    # Los tags tienen que estar guardados como lista
    if not isinstance(datos.get("tags"), list):
        return False, "tags debe ser una lista"

    # El estado tiene que ser uno de los estados válidos
    estado = datos.get("estado")
    if estado not in estados_validos:
        return False, f'el estado "{estado}" no está en {estados_validos}'

    return True, ""
