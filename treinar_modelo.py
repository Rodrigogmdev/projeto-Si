from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Carregar dados MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# One-hot encode das classes
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Cria modelo simples
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinar modelo
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

print("\n===========================================\n")
# Avaliar acurácia final no conjunto de teste
loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Acurácia final no conjunto de teste: {accuracy * 100:.2f}%")
print("\n===========================================\n")

# Salvar modelo
model.save('modelo_mnist.h5')
print("Modelo treinado e salvo em modelo_mnist.h5")
