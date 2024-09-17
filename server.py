from flask import Flask, jsonify, request
import processing


app = Flask(__name__)

@app.route('/api/load', methods=['POST'])
def load():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Please provide the number of files usign a POST request.'}), 400
    n_str = data.get('n')
    if n_str is None:
        return jsonify({'error': 'Please provide the number of files.'}), 400
    if not str(n_str).isnumeric():
        return jsonify({'error': 'The number of files is not a numeric value.'}), 400
    n = int(n_str)
    if not n in [1, 2]:
        return jsonify({'error': 'The number of files must be 1 or 2.'}), 400
    try:
        response = processing.load(n)
    except Exception:
        return jsonify({'error': 'Internal error.'}), 400
    return jsonify(response)


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Please provide the samples for prediction using a POST request.'}), 400
    
    try:
        response = processing.predict(data)
    except Exception:
        return jsonify({'error': 'Internal error.'}), 400
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
