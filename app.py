from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

@app.route('/get_image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400

    filepath = os.path.join('uploads', filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Image not found'}), 404

    return send_file(filepath, mimetype='image/jpeg')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image received'}),  400

    image_data = data['image']
    if not image_data.startswith('data:image/'):
        return jsonify({'error': 'Invalid image format'}),  400

    # Remover o prefixo 'data:image/jpeg;base64,'
    prefix, image_data = image_data.split(',',  1)
    image_type = prefix.split('/')[1]

    # Decodificar a string Base64 para bytes
    image_bytes = base64.b64decode(image_data)

    # Gerar um nome de arquivo único
    filename = f"{os.path.join('uploads', f'image.{image_type}')}"

    # Salvar a imagem
    with open(filename, 'wb') as f:
        f.write(image_bytes)

    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}),  200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=5000, debug=True)
