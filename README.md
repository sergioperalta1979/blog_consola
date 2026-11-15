# Blog por consola

Sistema de blog que se usa desde la terminal. Permite ver los posts, buscar por título, filtrar por tag, crear posts nuevos, validarlos y guardarlos en un archivo JSON para que sigan ahí la próxima vez que se abra el programa.

Esta versión usa **programación orientada a objetos** (clases `Autor`, `Post` y `Blog`) y **persistencia con JSON** (`posts.json`). Sigue organizada en módulos y paquetes.

Los datos son de ejemplo (una autora ficticia y cinco posts). Los posts 4 y 5 tienen errores a propósito para probar la opción de validación.

## Cómo ejecutarlo

Requisitos: tener Python 3 instalado. No hace falta instalar ninguna librería.

1. Abrir una terminal en la carpeta `blog_consola` (la que contiene `main.py`).
2. Ejecutar:

   ```
   python main.py
   ```

3. Elegir una opción escribiendo su número (1 a 7).

**El archivo que se ejecuta es `main.py`**, desde la carpeta raíz del proyecto.

## Menú

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Crear nuevo post
5. Validar posts
6. Guardar posts en JSON
7. Salir
```

| Opción | Qué hace |
|---|---|
| 1 | Muestra todos los posts con su título, su autor y su estado |
| 2 | Pide una palabra y muestra los posts cuyo título la contiene (sin importar mayúsculas o minúsculas) |
| 3 | Pide un tag y muestra los posts que lo tienen (sin importar mayúsculas o minúsculas) |
| 4 | Pide los datos de un post nuevo (título, contenido, autor, tags y estado), lo crea y lo agrega al blog |
| 5 | Revisa cada post y dice cuáles son válidos y cuáles tienen errores |
| 6 | Guarda todos los posts en `posts.json` |
| 7 | Se despide y termina. Si hay posts nuevos sin guardar, los guarda antes de cerrar |

Si se escribe texto en lugar de un número, o un número que no está en el menú, el programa avisa y vuelve a mostrar el menú sin cerrarse. Si al crear un post se deja vacío el título o el contenido, avisa y no crea nada.

## Organización del proyecto

```
blog_consola/
│
├── main.py
├── README.md
├── posts.json
│
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── modelos.py
    ├── operaciones.py
    └── validaciones.py
```

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Archivo principal. Carga los posts, crea el objeto `Blog` y llama al método que corresponde según la opción elegida. Está protegido con `if __name__ == "__main__":` |
| `posts.json` | Archivo donde se guardan los posts entre una ejecución y otra |
| `blog/__init__.py` | Hace que la carpeta `blog/` sea un paquete de Python |
| `blog/modelos.py` | Las clases `Autor`, `Post` y `Blog`, y las funciones que reconstruyen objetos desde diccionarios |
| `blog/datos.py` | Persistencia: `cargar_posts()` y `guardar_posts()`. También tiene los datos iniciales de ejemplo |
| `blog/menu.py` | Menú y manejo de `input()` |
| `blog/operaciones.py` | Muestra por pantalla el resultado de las validaciones |
| `blog/validaciones.py` | Reglas de validación de un post y los estados posibles |

## Las clases

| Clase | Qué representa | Responsabilidad |
|---|---|---|
| `Autor` | Una persona autora | Guarda `nombre`, `bio`, `especialidad` y `redes_sociales`. Sabe convertirse en diccionario (`a_diccionario()`) |
| `Post` | Una publicación | Guarda `id`, `titulo`, `contenido`, `autor`, `tags` y `estado`. Su `autor` es **una instancia de `Autor`**, no un texto (si no, da un error). Sabe convertirse en diccionario, mostrar un resumen, decir si tiene un título o un tag y validarse |
| `Blog` | El blog completo | Tiene una lista de objetos `Post` y centraliza la lógica: `listar_posts()`, `buscar_por_titulo()`, `filtrar_por_tag()`, `crear_post()`, `validar_posts()`, `obtener_posts()` y `a_lista_de_diccionarios()` |

## Cómo se guarda y se carga la información

JSON no puede guardar objetos de Python directamente, así que hay una conversión en cada sentido:

- **Al guardar** (opción 6, o al salir con cambios): cada `Post` se convierte en un diccionario con `a_diccionario()` (y su `Autor` también), y la lista completa se escribe en `posts.json` con el módulo `json`.
- **Al cargar** (al iniciar el programa): se lee `posts.json`, se obtiene una lista de diccionarios y cada uno se convierte de nuevo en un objeto `Post` con su `Autor` (`post_desde_diccionario()`). Con esos objetos se arma el `Blog`.

El archivo `posts.json` está en la carpeta raíz del proyecto y el programa lo encuentra aunque se ejecute desde otra carpeta.

Si hay problemas con el archivo, el programa no se cierra: avisa y sigue.

| Situación | Qué hace el programa |
|---|---|
| `posts.json` no existe | Usa los datos iniciales de ejemplo y avisa que se puede crear el archivo con la opción 6 |
| `posts.json` está vacío | Empieza con un blog sin posts y avisa |
| `posts.json` tiene contenido inválido, o no es una lista | Empieza con un blog sin posts y avisa qué pasó |
| Un post del archivo está incompleto (por ejemplo, le falta una clave) | Omite ese post, avisa cuál fue y carga los demás |
| Se intenta guardar algo que no se puede convertir en diccionario | No guarda y explica el problema |

## Qué cambió respecto al checkpoint anterior

- Antes los posts y el autor eran **diccionarios** y la lógica eran **funciones** sueltas. Ahora son **objetos** (`Post`, `Autor`) y la lógica principal está en los métodos de la clase `Blog`.
- Se agregó `blog/modelos.py` con las clases.
- Los datos ya no están fijos en el código: se **cargan y guardan en `posts.json`** (`blog/datos.py` ahora se ocupa de la persistencia).
- El menú pasó de 5 a 7 opciones: se sumaron **Crear nuevo post** y **Guardar posts en JSON**.
- `blog/operaciones.py` ya no tiene las funciones de listar, buscar y filtrar (pasaron a `Blog`) y quedó solo para mostrar resultados.
- `blog/validaciones.py` ahora define los estados válidos y sigue validando, pero sobre los datos de un post en forma de diccionario. Así se puede usar tanto con los objetos (`Post.validar()`) como al cargar el JSON.

### Cómo se conectan los módulos

Los imports van en una sola dirección, así que no hay imports circulares:

```
validaciones.py  <--  modelos.py  <--  datos.py  <--  menu.py  <--  main.py
                                                  <--  operaciones.py (sin imports)  <--  main.py
```

## Qué valida `validar_post()`

Que el post sea un diccionario; que tenga las claves `id`, `titulo`, `contenido`, `autor`, `tags` y `estado`; que el título y el contenido no estén vacíos; que el autor sea un diccionario con la clave `nombre`; que los tags sean una lista; y que el estado sea uno de `estados_post` (`borrador`, `publicado` o `archivado`).
