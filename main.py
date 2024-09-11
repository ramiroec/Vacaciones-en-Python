from flask import Flask, request, jsonify, render_template
import json

# Crear una instancia de Flask
app = Flask(__name__)

# Ruta al archivo JSON que simula la base de datos
file_path = './vacaciones.json'

# Función para leer los datos del archivo JSON
def read_database():
    with open(file_path, 'r') as file:
        # Leer y devolver los datos como un diccionario de Python
        data = json.load(file)
    return data

# Función para escribir datos en el archivo JSON
def write_database(data):
    with open(file_path, 'w') as file:
        # Guardar los datos en el archivo con indentación para mayor legibilidad
        json.dump(data, file, indent=2)

# Ruta principal que renderiza la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para la página del calendario de vacaciones
@app.route('/calendario')
def vacaciones_page():
    return render_template('calendario.html')

# Ruta para obtener todas las vacaciones (GET)
@app.route('/vacaciones', methods=['GET'])
def get_vacaciones():
    # Leer datos de la "base de datos" y devolverlos en formato JSON
    data = read_database()
    return jsonify(data)

# Ruta para obtener una vacación específica por su ID (GET)
@app.route('/vacaciones/<int:id>', methods=['GET'])
def get_vacacion(id):
    # Leer los datos de la "base de datos"
    data = read_database()
    # Buscar el registro con el ID especificado
    registro = next((item for item in data if item['id'] == id), None)
    if registro:
        # Si se encuentra, devolver el registro
        return jsonify(registro)
    else:
        # Si no se encuentra, devolver un error 404
        return 'Registro no encontrado', 404

# Ruta para añadir una nueva vacación (POST)
@app.route('/vacaciones', methods=['POST'])
def add_vacacion():
    # Leer los datos existentes
    data = read_database()
    # Crear un nuevo registro con un ID único
    new_registro = {
        'id': data[-1]['id'] + 1 if data else 1,  # Asignar un ID basado en el último registro
        **request.json  # Combinar con los datos del cuerpo de la solicitud
    }
    # Añadir el nuevo registro a los datos existentes
    data.append(new_registro)
    # Guardar los datos actualizados
    write_database(data)
    # Devolver el nuevo registro y un código de estado 201
    return jsonify(new_registro), 201

# Ruta para actualizar una vacación existente (PUT)
@app.route('/vacaciones/<int:id>', methods=['PUT'])
def update_vacacion(id):
    # Leer los datos de la "base de datos"
    data = read_database()
    # Encontrar el índice del registro con el ID especificado
    index = next((i for i, item in enumerate(data) if item['id'] == id), None)
    if index is not None:
        # Actualizar el registro en la posición encontrada
        data[index] = {'id': id, **request.json}
        # Guardar los datos actualizados
        write_database(data)
        # Devolver el registro actualizado
        return jsonify(data[index])
    else:
        # Si no se encuentra, devolver un error 404
        return 'Registro no encontrado', 404

# Ruta para eliminar una vacación por su ID (DELETE)
@app.route('/vacaciones/<int:id>', methods=['DELETE'])
def delete_vacacion(id):
    # Leer los datos de la "base de datos"
    data = read_database()
    # Crear una nueva lista excluyendo el registro con el ID especificado
    new_data = [item for item in data if item['id'] != id]
    if len(new_data) != len(data):
        # Si se eliminó un registro, guardar los datos actualizados
        write_database(new_data)
        # Devolver una respuesta vacía con un código de estado 204
        return '', 204
    else:
        # Si no se eliminó nada, devolver un error 404
        return 'Registro no encontrado', 404

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(port=3000, debug=True)  # Iniciar la aplicación en el puerto 3000 con modo debug activado
