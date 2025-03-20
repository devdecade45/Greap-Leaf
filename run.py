import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import flask
        import tensorflow
        import numpy
        import cv2
        import werkzeug
        import PIL
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing package: {e}")
        return False

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Packages installed successfully.")

def check_dataset():
    """Check if the dataset directory exists"""
    dataset_path = 'grape_dataset'
    if not os.path.exists(dataset_path):
        print(f"Warning: Dataset directory '{dataset_path}' not found.")
        print("The application may still work for predictions if you have a trained model.")
    else:
        print(f"Dataset directory '{dataset_path}' found.")
        # Check if dataset has the expected structure
        train_path = os.path.join(dataset_path, 'train')
        test_path = os.path.join(dataset_path, 'test')
        
        if not os.path.exists(train_path) or not os.path.exists(test_path):
            print("Warning: Dataset does not have the expected train/test structure.")
        else:
            print("Dataset structure looks good.")

def create_uploads_dir():
    """Create uploads directory if it doesn't exist"""
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created '{uploads_dir}' directory.")
    else:
        print(f"'{uploads_dir}' directory already exists.")

def check_images_dir():
    """Check if images directory exists and create it if needed"""
    images_dir = 'images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created '{images_dir}' directory.")
    else:
        print(f"'{images_dir}' directory already exists.")
        
    # Check for subdirectories
    subdirs = ['diseases', 'team', 'previews']
    for subdir in subdirs:
        subdir_path = os.path.join(images_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
            print(f"Created '{subdir_path}' directory.")

def run_app():
    """Run the Flask application"""
    print("Starting the application...")
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    print("=== Grape Leaf Disease Detection Setup ===")
    
    # Check if requirements are installed
    if not check_requirements():
        choice = input("Do you want to install the required packages? (y/n): ")
        if choice.lower() == 'y':
            install_requirements()
        else:
            print("Cannot continue without required packages. Exiting.")
            sys.exit(1)
    
    # Check for dataset and directories
    check_dataset()
    create_uploads_dir()
    check_images_dir()
    
    # Run the application
    run_app() 