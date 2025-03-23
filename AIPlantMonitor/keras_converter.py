import tensorflow as tf

# Load the Keras model from the current directory, replace 'model.h5' with your model filename
keras_model = tf.keras.models.load_model('./keras_model.h5')

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
tflite_model = converter.convert()

# Save the converted model to a file
with open('converted_model.tflite', 'wb') as f:
    f.write(tflite_model)
