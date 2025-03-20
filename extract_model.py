import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define constants
IMG_SIZE = 256
MODEL_PATH = 'grape_disease_model.h5'
DATASET_PATH = 'grape_dataset'

# Define class labels
class_labels = ["Black_rot", "Esca_(Black_Measles)", "Healthy", "Leaf_blight_(Isariopsis_Leaf_Spot)"]

def train_and_save_model():
    """
    Train a CNN model on the grape leaf disease dataset and save it
    """
    print("Starting model training...")
    
    # Define data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'train'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical'
    )
    
    # Load validation data
    validation_generator = test_datagen.flow_from_directory(
        os.path.join(DATASET_PATH, 'test'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical'
    )
    
    # Build the model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
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
    
    # Print model summary
    model.summary()
    
    # Train the model
    print("Training the model...")
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // 32,
        epochs=10,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // 32
    )
    
    # Save the model
    print(f"Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    print("Model saved successfully!")
    
    return model

if __name__ == "__main__":
    # Check if model already exists
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}. Delete it if you want to retrain.")
    else:
        # Train and save the model
        train_and_save_model() 