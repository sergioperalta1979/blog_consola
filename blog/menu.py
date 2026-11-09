# blog/menu.py
# Menú e interacción con el usuario: acá está todo el manejo de input().
# No importa nada de los otros módulos.


def mostrar_menu():
    """Muestra el menú y devuelve la opción elegida como número entero.
    Si el usuario escribe texto en lugar de un número, avisa y devuelve None."""
    print()
    print("--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")
    try:
        return int(input("Elige una opción: "))
    except ValueError:
        # int() falla si el texto no es un número: se avisa y el menú vuelve a mostrarse
        print("Opción inválida: ingresá un número del 1 al 5, no texto.")
        return None


def pedir_texto(mensaje):
    """Pide un texto al usuario y lo devuelve sin espacios al principio ni al final."""
    return input(mensaje).strip()
