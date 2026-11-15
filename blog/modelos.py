# blog/modelos.py
# Clases del sistema: Autor, Post y Blog.
# Cada clase sabe convertirse a diccionario (para guardarse en JSON) y hay
# funciones para hacer el camino inverso: reconstruir objetos desde un diccionario.
# Solo importa de validaciones.py (nunca al revés), para evitar imports circulares.

from blog.validaciones import validar_post, estados_post


class Autor:
    """Una persona autora del blog."""

    def __init__(self, nombre, bio="", especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        # Cada autor tiene su propia lista de redes (no se comparte entre autores)
        if redes_sociales is None:
            redes_sociales = []
        self.redes_sociales = redes_sociales

    def a_diccionario(self):
        """Convierte el autor en un diccionario compatible con JSON."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": list(self.redes_sociales),
        }


class Post:
    """Una publicación del blog. Su autor es un objeto de la clase Autor."""

    def __init__(self, id, titulo, contenido, autor, tags, estado):
        # La composición: el autor tiene que ser una instancia de Autor, no un texto
        if not isinstance(autor, Autor):
            raise TypeError("el autor de un post tiene que ser una instancia de la clase Autor")
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor
        self.tags = tags
        self.estado = estado

    def a_diccionario(self):
        """Convierte el post (y su autor) en un diccionario compatible con JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.a_diccionario(),
            "tags": self.tags,
            "estado": self.estado,
        }

    def resumen(self):
        """Devuelve una línea de texto con el título, el autor y el estado."""
        return f"{self.titulo} | Autor: {self.autor.nombre} | Estado: {self.estado}"

    def tiene_titulo(self, termino):
        """Devuelve True si el título contiene el término (sin importar mayúsculas)."""
        return isinstance(self.titulo, str) and termino.lower() in self.titulo.lower()

    def tiene_tag(self, tag):
        """Devuelve True si el post tiene ese tag (sin importar mayúsculas)."""
        # Solo se recorre si "tags" es realmente una lista
        if not isinstance(self.tags, list):
            return False
        for t in self.tags:
            if isinstance(t, str) and t.lower() == tag.lower():
                return True
        return False

    def validar(self):
        """Valida el post usando las reglas de validaciones.py.
        Devuelve (True, "") o (False, mensaje)."""
        return validar_post(self.a_diccionario())


def autor_desde_diccionario(datos):
    """Reconstruye un Autor desde un diccionario. Si faltan datos, avisa con ValueError."""
    if not isinstance(datos, dict):
        raise ValueError("los datos del autor no son un diccionario")
    if "nombre" not in datos:
        raise ValueError('falta la clave "nombre" del autor')
    return Autor(
        datos["nombre"],
        datos.get("bio", ""),
        datos.get("especialidad", ""),
        datos.get("redes_sociales", []),
    )


def post_desde_diccionario(datos):
    """Reconstruye un Post desde un diccionario. Si faltan datos, avisa con ValueError."""
    if not isinstance(datos, dict):
        raise ValueError("el post no es un diccionario")
    for clave in ("id", "titulo", "contenido", "autor", "tags", "estado"):
        if clave not in datos:
            raise ValueError(f'falta la clave "{clave}"')
    autor = autor_desde_diccionario(datos["autor"])
    return Post(datos["id"], datos["titulo"], datos["contenido"], autor, datos["tags"], datos["estado"])


class Blog:
    """El blog completo: guarda la lista de posts y centraliza la lógica principal."""

    def __init__(self, posts=None):
        # Lista de objetos Post
        if posts is None:
            posts = []
        self.posts = posts
        # Se pone en True cuando hay cambios sin guardar en posts.json
        self.modificado = False

    def obtener_posts(self):
        """Devuelve una copia de la lista con todos los posts cargados."""
        return list(self.posts)

    def listar_posts(self, lista=None):
        """Muestra título, autor y estado de los posts. Sin parámetro, muestra todos."""
        if lista is None:
            lista = self.posts
        if len(lista) == 0:
            print("No hay posts para mostrar.")
            return
        print("Posts disponibles:")
        for post in lista:
            print(f"- {post.resumen()}")

    def buscar_por_titulo(self, termino):
        """Devuelve los posts cuyo título contiene el término (sin importar mayúsculas)."""
        resultados = []
        for post in self.posts:
            if post.tiene_titulo(termino):
                resultados.append(post)
        return resultados

    def filtrar_por_tag(self, tag):
        """Devuelve los posts que tienen ese tag (sin importar mayúsculas)."""
        resultados = []
        for post in self.posts:
            if post.tiene_tag(tag):
                resultados.append(post)
        return resultados

    def siguiente_id(self):
        """Devuelve el próximo id libre: el mayor id numérico + 1."""
        mayor = 0
        for post in self.posts:
            if isinstance(post.id, int) and post.id > mayor:
                mayor = post.id
        return mayor + 1

    def autor_por_defecto(self):
        """Devuelve el autor del primer post, o un autor genérico si todavía no hay posts."""
        if len(self.posts) > 0:
            return self.posts[0].autor
        return Autor("Autor sin nombre")

    def crear_post(self, titulo, contenido, autor, tags, estado):
        """Crea un Post nuevo, lo agrega al blog y lo devuelve.
        Si hay campos vacíos o inválidos, avisa con ValueError y no agrega nada."""
        if not isinstance(titulo, str) or titulo.strip() == "":
            raise ValueError("el título no puede estar vacío")
        if not isinstance(contenido, str) or contenido.strip() == "":
            raise ValueError("el contenido no puede estar vacío")
        if estado not in estados_post:
            raise ValueError(f'el estado "{estado}" no es válido: usá {estados_post}')
        nuevo = Post(self.siguiente_id(), titulo.strip(), contenido.strip(), autor, tags, estado)
        self.posts.append(nuevo)
        self.modificado = True
        return nuevo

    def validar_posts(self):
        """Valida todos los posts. Devuelve una lista de (posición, es_válido, mensaje)."""
        resultados = []
        for posicion, post in enumerate(self.posts, 1):
            es_valido, mensaje = post.validar()
            resultados.append((posicion, es_valido, mensaje))
        return resultados

    def a_lista_de_diccionarios(self):
        """Convierte todos los posts en una lista de diccionarios compatible con JSON."""
        lista = []
        for post in self.posts:
            lista.append(post.a_diccionario())
        return lista
