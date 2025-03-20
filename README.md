# Grape Leaf Disease Detection

A web application for detecting diseases in grape leaves using Convolutional Neural Networks (CNN).

## Features

- **Disease Detection**: Upload images of grape leaves to detect diseases
- **Multiple Disease Recognition**: Identifies Black Rot, Esca (Black Measles), Leaf Blight, and Healthy leaves
- **Detailed Information**: Provides comprehensive information about each disease and treatment options
- **User-Friendly Interface**: Easy-to-use web interface with responsive design
- **Interactive Results**: View confidence levels and detailed disease information
- **Drag-and-Drop Upload**: Simple image upload with drag-and-drop functionality
- **Responsive Design**: Works on desktop and mobile devices
- **Automatic Model Training**: Trains a new model if one doesn't exist

## Diseases Detected

1. **Black Rot**: A fungal disease that causes dark, circular lesions on grape leaves
2. **Esca (Black Measles)**: A complex fungal disease that causes tiger-stripe patterns on leaves
3. **Leaf Blight (Isariopsis Leaf Spot)**: Causes small, brown spots with yellow halos that can expand
4. **Healthy Leaves**: Identification of healthy grape leaves

## Installation

### Prerequisites

- Python 3.7 or higher
- TensorFlow 2.x
- Flask
- OpenCV
- NumPy
- Werkzeug
- Pillow
- Scikit-learn
- Matplotlib

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/grape-leaf-disease-detection.git
   cd grape-leaf-disease-detection
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```
   
   Alternatively, on Windows, you can double-click the `run.bat` file.

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Navigate to the "Disease Detection" page
2. Upload an image of a grape leaf by clicking on the upload area or dragging and dropping an image
3. Click the "Detect Disease" button
4. View the results, including the detected disease, confidence level, and treatment recommendations
5. For more information about specific diseases, visit the "Diseases" page

## Dataset Structure

The application expects a dataset with the following structure:
```
grape_dataset/
├── train/
│   ├── Black_rot/
│   ├── Esca_(Black_Measles)/
│   ├── Healthy/
│   └── Leaf_blight_(Isariopsis_Leaf_Spot)/
└── test/
    ├── Black_rot/
    ├── Esca_(Black_Measles)/
    ├── Healthy/
    └── Leaf_blight_(Isariopsis_Leaf_Spot)/
```

Each directory should contain images of grape leaves with the corresponding condition.

## Project Structure

- `app.py`: Main Flask application with disease detection model
- `run.py`: Application launcher with setup and checks
- `run.bat`: Windows batch file to run the application
- `requirements.txt`: List of required Python packages
- `grape_disease_model.h5`: Pre-trained CNN model
- `index.html`, `about.html`, etc.: Web pages
- `script.js`: JavaScript for frontend functionality
- `styles.css`: CSS styles for the web interface
- `images/`: Directory containing images used in the web interface
- `uploads/`: Directory for storing uploaded images

## Model Information

The disease detection model is a Convolutional Neural Network (CNN) trained on a dataset of grape leaf images. The model achieves over 95% accuracy in identifying the four different classes (Black Rot, Esca, Leaf Blight, and Healthy leaves).

The model architecture includes:
- Multiple convolutional layers with ReLU activation
- MaxPooling layers for downsampling
- Dropout layers to prevent overfitting
- Dense layers for classification

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The dataset used for training the model is based on the [Plant Village Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- Special thanks to all contributors who have helped with the development of this project 