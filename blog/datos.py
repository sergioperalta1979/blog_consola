# blog/datos.py
# Datos base del blog (continúan las estructuras de los módulos anteriores).
# Este módulo no importa nada de los otros: así se evitan los imports circulares.

# Diccionario con los datos del autor; "redes_sociales" es una lista anidada
perfil_autor = {
    "nombre": "Ana López",
    "bio": "Desarrolladora web y creadora de contenido sobre programación.",
    "especialidad": "Python y Django",
    "redes_sociales": ["@ana_dev", "@ana_python"]
}

# Tupla con los estados posibles de un post (datos fijos)
estados_post = ("borrador", "publicado", "archivado")

# Set de etiquetas del blog: "Python" está repetida y el set la guarda una sola vez
etiquetas_blog = {"Python", "Django", "Web", "Backend", "Python"}

# Lista de posts. Los posts 1, 2 y 3 están completos; los posts 4 y 5 tienen
# errores a propósito para probar la opción "Validar posts".
# En todos, "autor" usa el diccionario perfil_autor (autor anidado).
posts = [
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
        # Post incompleto: falta la clave "contenido"
        "id": 4,
        "titulo": "Funciones en Python",
        "autor": perfil_autor,
        "tags": ["Python", "Funciones"],
        "estado": "publicado"
    },
    {
        # Post con un dato de tipo incorrecto: "tags" es un texto y no una lista
        "id": 5,
        "titulo": "Manejo de errores",
        "contenido": "Cómo evitar que un programa se cierre por un dato incorrecto.",
        "autor": perfil_autor,
        "tags": "Python, Errores",
        "estado": "borrador"
    }
]
