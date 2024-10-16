import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained model for thorax X-ray classification
MODEL_PATH = "model/thorax_xray_model.h5"  # Adjust the model path if necessary
model = tf.keras.models.load_model(MODEL_PATH)

def analyze_image(file_path, condition):
    try:
        # Load and preprocess the image
        img = image.load_img(file_path, target_size=(224, 224))  # Adjust the size if needed
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0  # Normalize image data to [0, 1]

        # Predict the class of the X-ray image
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Create a readable output for the classification
        if predicted_class == 0:
            result = "The X-ray is normal. No abnormalities detected."
        else:
            result = "The X-ray indicates a potential issue. Further medical consultation is recommended."

        # Combine the image result with any user-provided medical conditions
        if condition:
            diagnosis = f"Based on the provided condition: '{condition}', the following analysis can be made: {result}"
        else:
            diagnosis = f"No additional conditions provided. The X-ray analysis: {result}"

        return {"diagnosis": diagnosis, "prediction_details": predictions.tolist()}
    
    except Exception as e:
        raise Exception(f"Error processing the image: {str(e)}")
