import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import time
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__, static_folder='.', static_url_path='')

# Define constants
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'grape_disease_model.h5'
IMG_SIZE = 256  # The size expected by the model
DATASET_PATH = 'grape_dataset'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Load the model
model = None

def load_keras_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("Model loaded successfully!")
        return True
        else:
            print(f"Model file '{MODEL_PATH}' not found. Training a new model...")
            train_model()
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to preprocess the image for prediction
def preprocess_image(file_path):
    try:
    img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

# Define class labels
class_labels = ["Black_rot", "Esca_(Black_Measles)", "Healthy", "Leaf_blight_(Isariopsis_Leaf_Spot)"]

# Function to train the model
def train_model():
    global model
    
    # Define data generators with data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation data
    valid_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'train'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical',
        shuffle=True
    )
    
    # Load validation data
    valid_generator = valid_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'test'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    
    # Build the model
    model = Sequential([
        # First convolutional block
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Second convolutional block
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Third convolutional block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Flatten and fully connected layers
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(len(class_labels), activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train the model
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // 32,
        epochs=15,  # Reduced for faster training
        validation_data=valid_generator,
        validation_steps=valid_generator.samples // 32
    )
    
    # Save the model
    model.save(MODEL_PATH)
    print("Model trained and saved successfully!")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/home.html')
def home():
    return send_from_directory('.', 'home.html')

@app.route('/about.html')
def about():
    return send_from_directory('.', 'about.html')

@app.route('/detection.html')
def detection():
    return send_from_directory('.', 'detection.html')

@app.route('/diseases.html')
def diseases():
    return send_from_directory('.', 'diseases.html')

@app.route('/contact.html')
def contact():
    return send_from_directory('.', 'contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Check if model is loaded
        global model
        if model is None:
            if not load_keras_model():
                return jsonify({'error': 'Model could not be loaded'}), 500
        
        try:
            # Add a small delay to simulate processing time for better UX
            time.sleep(1)
            
            # Preprocess the image
            processed_image = preprocess_image(file_path)
            
            if processed_image is None:
                return jsonify({'error': 'Failed to process the image'}), 500
            
            # Make prediction
            predictions = model.predict(processed_image)
            predicted_class_index = np.argmax(predictions[0])
            predicted_class = class_labels[predicted_class_index]
            confidence = float(predictions[0][predicted_class_index])
            
            # Get disease information
            disease_info = get_disease_info(predicted_class)
            
            # Return the prediction
            return jsonify({
                'prediction': predicted_class,
                'confidence': confidence,
                'all_probabilities': {class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))},
                'disease_info': disease_info
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format. Allowed formats: png, jpg, jpeg'}), 400

# Function to get disease information
def get_disease_info(disease):
    disease_info = {
        'Black_rot': {
            'scientific_name': 'Guignardia bidwellii',
            'symptoms': 'Circular lesions with dark borders and tan centers on leaves. Fruit develops black rot.',
            'treatment': 'Remove infected plant material. Apply fungicides containing captan, myclobutanil, or mancozeb.'
        },
        'Esca_(Black_Measles)': {
            'scientific_name': 'Complex of fungi including Phaeomoniella chlamydospora',
            'symptoms': 'Tiger-stripe patterns on leaves with yellow or reddish-brown areas between green veins.',
            'treatment': 'No cure available. Remove severely infected vines. Use clean pruning tools and protect wounds.'
        },
        'Leaf_blight_(Isariopsis_Leaf_Spot)': {
            'scientific_name': 'Pseudocercospora vitis',
            'symptoms': 'Small, irregular reddish-brown spots with yellow halos that can merge and cause defoliation.',
            'treatment': 'Remove fallen leaves. Apply fungicides containing copper, mancozeb, or azoxystrobin.'
        },
        'Healthy': {
            'scientific_name': 'N/A',
            'symptoms': 'No visible symptoms. Leaves are green, intact, and free from spots or discoloration.',
            'treatment': 'Continue regular vineyard maintenance and monitoring.'
        }
    }
    
    return disease_info.get(disease, {
        'scientific_name': 'Unknown',
        'symptoms': 'Unknown',
        'treatment': 'Consult with a viticulture specialist.'
    })

# Handle contact form submissions
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        # In a real application, you would process this data (e.g., send an email, store in database)
        print(f"Contact form submission: {data}")
        return jsonify({'success': True, 'message': 'Your message has been sent successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Handle newsletter subscriptions
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        email = data.get('email')
        # In a real application, you would add this email to your newsletter list
        print(f"Newsletter subscription: {email}")
        return jsonify({'success': True, 'message': 'You have been subscribed to our newsletter!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Load the model when the app starts
    load_keras_model()
    app.run(debug=True, host='0.0.0.0', port=5000) 