from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

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
    app.run(debug=True)
