from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)
file_path = './vacaciones.json'

def read_database():
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_database(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calendario')
def vacaciones_page():
    return render_template('calendario.html')

@app.route('/vacaciones', methods=['GET'])
def get_vacaciones():
    data = read_database()
    return jsonify(data)

@app.route('/vacaciones/<int:id>', methods=['GET'])
def get_vacacion(id):
    data = read_database()
    registro = next((item for item in data if item['id'] == id), None)
    if registro:
        return jsonify(registro)
    else:
        return 'Registro no encontrado', 404

@app.route('/vacaciones', methods=['POST'])
def add_vacacion():
    data = read_database()
    new_registro = {
        'id': data[-1]['id'] + 1 if data else 1,
        **request.json
    }
    data.append(new_registro)
    write_database(data)
    return jsonify(new_registro), 201

@app.route('/vacaciones/<int:id>', methods=['PUT'])
def update_vacacion(id):
    data = read_database()
    index = next((i for i, item in enumerate(data) if item['id'] == id), None)
    if index is not None:
        data[index] = {'id': id, **request.json}
        write_database(data)
        return jsonify(data[index])
    else:
        return 'Registro no encontrado', 404

@app.route('/vacaciones/<int:id>', methods=['DELETE'])
def delete_vacacion(id):
    data = read_database()
    new_data = [item for item in data if item['id'] != id]
    if len(new_data) != len(data):
        write_database(new_data)
        return '', 204
    else:
        return 'Registro no encontrado', 404

if __name__ == '__main__':
    app.run(port=3000)


if __name__ == '__main__':
    app.run(debug=True)
