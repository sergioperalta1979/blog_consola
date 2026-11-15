# blog/datos.py
# Datos base del blog y persistencia: carga y guardado de los posts en posts.json.
# Importa de modelos.py (que importa de validaciones.py); ninguno importa de este módulo.

import json
from pathlib import Path

from blog.modelos import post_desde_diccionario

# El archivo posts.json está en la carpeta raíz del proyecto (una arriba de blog/).
# Con Path la ruta funciona igual aunque el programa se ejecute desde otra carpeta.
RUTA_POSTS = Path(__file__).resolve().parent.parent / "posts.json"

# Diccionario con los datos del autor de los posts iniciales
perfil_autor = {
    "nombre": "Ana López",
    "bio": "Desarrolladora web y creadora de contenido sobre programación.",
    "especialidad": "Python y Django",
    "redes_sociales": ["@ana_dev", "@ana_python"]
}

# Set de etiquetas del blog: "Python" está repetida y el set la guarda una sola vez
etiquetas_blog = {"Python", "Django", "Web", "Backend", "Python"}

# Posts iniciales (se usan solo si todavía no existe posts.json).
# Los posts 1, 2 y 3 son correctos; los posts 4 y 5 tienen errores a propósito
# para probar la opción "Validar posts": el 4 tiene el contenido vacío y el 5 tiene
# "tags" como texto y no como lista.
datos_iniciales = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "contenido": "En este post veremos cómo empezar a programar con Python.",
        "autor": perfil_autor,
        "tags": ["Python", "Principiantes"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Qué es Django",
        "contenido": "Django es un framework web creado con Python.",
        "autor": perfil_autor,
        "tags": ["Python", "Django", "Web"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Organizando datos con listas",
        "contenido": "Las listas permiten guardar varios elementos en una sola variable.",
        "autor": perfil_autor,
        "tags": ["Python", "Listas"],
        "estado": "archivado"
    },
    {
        "id": 4,
        "titulo": "Funciones en Python",
        "contenido": "",
        "autor": perfil_autor,
        "tags": ["Python", "Funciones"],
        "estado": "publicado"
    },
    {
        "id": 5,
        "titulo": "Manejo de errores",
        "contenido": "Cómo evitar que un programa se cierre por un dato incorrecto.",
        "autor": perfil_autor,
        "tags": "Python, Errores",
        "estado": "borrador"
    }
]


def _convertir_a_posts(lista_de_diccionarios):
    """Convierte una lista de diccionarios en objetos Post.
    Devuelve (posts, mensajes): los posts que se pudieron armar y un aviso por cada
    diccionario incompleto que se omitió."""
    posts = []
    mensajes = []
    for posicion, datos in enumerate(lista_de_diccionarios, 1):
        try:
            posts.append(post_desde_diccionario(datos))
        except ValueError as error:
            mensajes.append(f"Se omitió el elemento {posicion} de posts.json: {error}.")
    return posts, mensajes


def cargar_posts(ruta=RUTA_POSTS):
    """Carga los posts desde posts.json y los devuelve como objetos Post.
    Devuelve (posts, mensajes). Si el archivo no existe, está vacío o es inválido,
    no se cierra el programa: se avisa en los mensajes y se sigue."""
    # El archivo no existe: se usan los datos iniciales
    if not ruta.exists():
        posts, mensajes = _convertir_a_posts(datos_iniciales)
        mensajes.insert(0, "No se encontró posts.json: se cargaron los datos iniciales. "
                           "Usá la opción 6 para crear el archivo.")
        return posts, mensajes

    # Se lee el archivo como texto
    try:
        texto = ruta.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [], [f"No se pudo leer posts.json ({error}): el blog empieza sin posts."]

    # El archivo está vacío
    if texto.strip() == "":
        return [], ["posts.json está vacío: el blog empieza sin posts."]

    # El archivo tiene contenido que no es JSON válido
    try:
        contenido = json.loads(texto)
    except json.JSONDecodeError as error:
        return [], [f"posts.json tiene contenido inválido ({error.msg}, línea {error.lineno}): "
                    "el blog empieza sin posts. Si guardás, el archivo se reemplaza."]

    # Es JSON válido, pero tiene que ser una lista de posts
    if not isinstance(contenido, list):
        return [], ["posts.json no contiene una lista de posts: el blog empieza sin posts."]

    return _convertir_a_posts(contenido)


def guardar_posts(posts, ruta=RUTA_POSTS):
    """Guarda los posts en posts.json. Antes convierte cada objeto en un diccionario.
    Devuelve (True/False, mensaje)."""
    # JSON no sabe guardar objetos: cada post se convierte antes en un diccionario
    try:
        lista = [post.a_diccionario() for post in posts]
    except AttributeError:
        return False, ("No se guardó: se intentó guardar un objeto que no se puede "
                       "convertir en diccionario (le falta el método a_diccionario).")
    try:
        texto = json.dumps(lista, ensure_ascii=False, indent=2)
        ruta.write_text(texto + "\n", encoding="utf-8")
    except (OSError, TypeError) as error:
        return False, f"No se pudo guardar posts.json: {error}"
    return True, f"Se guardaron {len(lista)} posts en {ruta.name}."
