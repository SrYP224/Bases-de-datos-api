import requests
from requests.auth import HTTPBasicAuth

def mostrar_menu():
    print("\n=== MENÚ DE GESTIÓN DE USUARIOS ===")
    print("1. Ver todos los usuarios")
    print("2. Crear nuevo usuario")
    print("3. Buscar usuario por ID")
    print("4. Eliminar usuario")
    print("5. Salir")
    return input("\nSeleccione una opción (1-5): ")

def obtener_usuarios():
    response = requests.get('http://localhost:5000/usuarios')
    if response.status_code == 200:
        usuarios = response.json()
        print("\nUsuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")



def crear_usuario():
    nombre = input("\nIngrese el nombre del nuevo usuario: ")
    response = requests.post(
        'http://localhost:5000/crear',  # Cambié /usuarios por /crear
        json={"nombre": nombre},
        auth=HTTPBasicAuth('admin', 'admin123')
    )
    if response.status_code == 201:
        print("Usuario creado:", response.json())
    else:
        print("Error al crear usuario:", response.json())




def buscar_usuario():
    id = input("\nIngrese el ID del usuario a buscar: ")
    response = requests.get(f'http://localhost:5000/buscar/{id}')  # RUTA CORREGIDA
    if response.status_code == 200:
        usuario = response.json()
        print(f"Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al buscar usuario:", response.json())

def eliminar_usuario():
    id = input("\nIngrese el ID del usuario a eliminar: ")
    response = requests.delete(
        f'http://localhost:5000/eliminar/{id}',  # RUTA CORREGIDA
        auth=HTTPBasicAuth('admin', 'admin123')
    )
    if response.status_code == 200:
        print("Usuario eliminado:", response.json())
    else:
        print("Error al eliminar usuario:", response.json())

def main():
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            obtener_usuarios()
        elif opcion == '2':
            crear_usuario()
        elif opcion == '3':
            buscar_usuario()
        elif opcion == '4':
            eliminar_usuario()
        elif opcion == '5':
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == '__main__':
    main()
