import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist

print("Iniciando script de teste...")

# Carrega o modelo treinado
modelo = tf.keras.models.load_model("modelo_mnist.h5")
print("Modelo carregado com sucesso.")

# Carrega os dados MNIST para teste
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = x_test.astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1)
print(f"Dados de teste carregados: {x_test.shape[0]} imagens")

# Faz predição nos primeiros 5 exemplos
pred = modelo.predict(x_test[:5])
pred_classes = np.argmax(pred, axis=1)

print("Predições:", pred_classes)
print("Rótulos reais:", y_test[:5])
