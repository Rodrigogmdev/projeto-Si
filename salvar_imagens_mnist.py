from tensorflow.keras.datasets import mnist
from PIL import Image
import os

# Cria uma pasta para salvar as imagens
os.makedirs("mnist_imagens", exist_ok=True)

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Salva 10 imagens de treino
for i in range(10):
    img = Image.fromarray(train_images[i])
    img.save(f"mnist_imagens/digit_{train_labels[i]}_{i}.png")

print("Imagens salvas na pasta 'mnist_imagens'")
