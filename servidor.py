from flask import Flask, jsonify, request, abort
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ]
}

# Simulación de usuarios para autenticación
usuarios_autenticados = {
    "admin": generate_password_hash("admin123")
}

# Decorador para autenticación básica
def autenticar(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username in usuarios_autenticados and
                            check_password_hash(usuarios_autenticados[auth.username], auth.password)):
            return jsonify({"mensaje": "Autenticación fallida"}), 401
        return f(*args, **kwargs)
    return decorador

@app.route('/')
def home():
    return "Home Lobby"

# Ruta para obtener los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para crear un nuevo usuario (acepta GET y POST)
@app.route('/crear', methods=['GET', 'POST'])

def crear_usuario():
    if request.method == 'GET':
        return jsonify({"mensaje": "Para crear un usuario, envía una solicitud POST con un nombre y autenticación básica."})

    # Verifica que sea una solicitud POST y procesa la creación del usuario
    nuevo_usuario = request.json
    if 'nombre' not in nuevo_usuario or not isinstance(nuevo_usuario['nombre'], str):
        return jsonify({"mensaje": "Nombre es requerido y debe ser una cadena"}), 400
    
    nuevo_id = len(base_datos["usuarios"]) + 1
    nuevo_usuario["id"] = nuevo_id
    base_datos["usuarios"].append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201

# Ruta para buscar un usuario por ID
@app.route('/buscar/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    return jsonify(usuario)

# Ruta para eliminar un usuario
@app.route('/eliminar/<int:id>', methods=['DELETE'])
@autenticar
def eliminar_usuario(id):
    usuario = next((u for u in base_datos["usuarios"] if u["id"] == id), None)
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    base_datos["usuarios"].remove(usuario)
    return jsonify({"mensaje": "Usuario eliminado"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
