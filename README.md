# Blog por consola

Sistema de blog que se usa desde la terminal. Permite ver los posts, buscar por título, filtrar por tag y validar la estructura de cada publicación. Es la versión organizada en módulos y paquetes del sistema que se venía construyendo en los módulos anteriores del curso de Python.

Los datos son de ejemplo (una autora ficticia y cinco posts). Los posts 4 y 5 tienen errores a propósito para probar la opción de validación.

## Cómo ejecutarlo

Requisitos: tener Python 3 instalado. No hace falta instalar ninguna librería.

1. Abrir una terminal en la carpeta `blog_consola` (la que contiene `main.py`).
2. Ejecutar:

   ```
   python main.py
   ```

3. Elegir una opción escribiendo su número (1 a 5).

**El archivo que se ejecuta es `main.py`**, y siempre desde la carpeta raíz del proyecto. Si se ejecuta desde otra carpeta pueden aparecer errores de importación.

## Menú

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Validar posts
5. Salir
```

| Opción | Qué hace |
|---|---|
| 1 | Muestra todos los posts con su título, su autor y su estado |
| 2 | Pide una palabra y muestra los posts cuyo título la contiene (sin importar mayúsculas o minúsculas) |
| 3 | Pide un tag y muestra los posts que lo tienen (sin importar mayúsculas o minúsculas) |
| 4 | Revisa cada post y dice cuáles son válidos y cuáles tienen errores |
| 5 | Muestra un mensaje de despedida y termina el programa |

Si se escribe texto en lugar de un número, o un número que no está en el menú, el programa avisa y vuelve a mostrar el menú sin cerrarse.

## Organización del proyecto

```
blog_consola/
│
├── main.py
├── README.md
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── operaciones.py
    └── validaciones.py
```

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Archivo principal. Importa las piezas del paquete y coordina el menú: llama a la función que corresponde según la opción elegida. Está protegido con `if __name__ == "__main__":` |
| `blog/__init__.py` | Hace que la carpeta `blog/` sea un paquete de Python |
| `blog/datos.py` | Datos base: `perfil_autor`, `estados_post`, `etiquetas_blog` y `posts` (el autor de cada post es el diccionario `perfil_autor`) |
| `blog/menu.py` | Menú y manejo de `input()`: `mostrar_menu()` y `pedir_texto()` |
| `blog/operaciones.py` | Operaciones del blog: `listar_posts()`, `buscar_por_titulo()`, `filtrar_por_tag()` y `mostrar_validaciones()` |
| `blog/validaciones.py` | Reglas de validación: `validar_post()` |

### Cómo se conectan los módulos

Los imports van en una sola dirección, así que no hay imports circulares:

```
datos.py  <--  validaciones.py  <--  operaciones.py  <--  main.py
menu.py  <--------------------------------------------------  main.py
```

## Qué valida `validar_post()`

Que el post sea un diccionario; que tenga las claves `id`, `titulo`, `contenido`, `autor`, `tags` y `estado`; que el título y el contenido no estén vacíos; que el autor sea un diccionario con la clave `nombre`; que los tags sean una lista; y que el estado sea uno de `estados_post` (`borrador`, `publicado` o `archivado`).
