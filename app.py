from flask import Flask, request, render_template, jsonify
from PIL import Image, ImageOps, UnidentifiedImageError
import numpy as np
import tensorflow as tf
import io
import os

app = Flask(__name__)
os.makedirs("static", exist_ok=True)

# Carrega o modelo uma única vez na inicialização do app
modelo = tf.keras.models.load_model("modelo_mnist.h5")

def preprocess_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('L')
    except UnidentifiedImageError:
        # Salva imagem inválida para debug
        with open("static/erro_debug.png", "wb") as f:
            f.write(image_bytes)
        raise ValueError("Arquivo enviado não é uma imagem válida.")

    # Inverte cores: fundo preto, desenho branco (padrão MNIST)
    img = ImageOps.invert(img)

    # Binariza a imagem (preto e branco)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    img = img.convert('L')

    # Corta a imagem para o conteúdo
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Redimensiona para 20x20 mantendo proporção
    img.thumbnail((20, 20), Image.Resampling.LANCZOS)

    # Cria imagem nova 28x28 preta e cola a imagem redimensionada centralizada
    new_img = Image.new('L', (28, 28), 0)
    left = (28 - img.width) // 2
    top = (28 - img.height) // 2
    new_img.paste(img, (left, top))

    # Converte para array normalizado
    arr = np.array(new_img) / 255.0

    # Salva imagem processada para visualização
    new_img.save('static/ultima_imagem_processada.png')

    # Ajusta shape para o modelo e tipo float32
    return arr.reshape(1, 28, 28, 1).astype(np.float32)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    print(f"Arquivo recebido: {file.filename if file else 'Nenhum arquivo'}")  # DEBUG

    if not file or not file.mimetype.startswith("image/"):
        return jsonify({"error": "Nenhuma imagem válida foi enviada."}), 400

    img_bytes = file.read()
    try:
        img_preproc = preprocess_image(img_bytes)
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a imagem: {e}"}), 400

    # Predição pelo modelo
    pred = modelo.predict(img_preproc)
    digit = int(np.argmax(pred))

    # Responde sempre JSON nesta rota (AJAX/fetch espera JSON)
    return jsonify({"predicao": digit})

if __name__ == "__main__":
    app.run(debug=True)
