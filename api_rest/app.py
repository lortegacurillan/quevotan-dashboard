from flask import Flask, request, jsonify
from config import get_db

app = Flask(__name__)
db = get_db()
collection = db.documentosUnificados

def validate_request(req):
    # Aquí puedes añadir validaciones según tus necesidades
    if not req:
        return False
    return True

@app.route('/dato_unico', methods=['GET'])
def get_single_data():
    if not validate_request(request.args):
        return jsonify({"error": "Solicitud inválida"}), 400

    query_key = request.args.get('query_key')
    query_value = request.args.get('query_value')
    column = request.args.get('column')

    query = {query_key: query_value}

    if column:
        result = collection.find_one(query, {column: 1, '_id': 0})
    else:
        result = collection.find_one(query)

    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Dato no encontrado"}), 404

@app.route('/multiples_datos', methods=['GET'])
def get_multiple_data():
    if not validate_request(request.args):
        return jsonify({"error": "Solicitud inválida"}), 400

    query_key = request.args.get('query_key')
    query_value = request.args.get('query_value')
    column = request.args.get('column')

    query = {query_key: query_value}

    if column:
        results = collection.find(query, {column: 1, '_id': 0})
    else:
        results = collection.find(query)

    results_list = list(results)
    if results_list:
        return jsonify(results_list), 200
    else:
        return jsonify({"error": "Datos no encontrados"}), 404

if __name__ == '__main__':
    app.run(debug=True)
