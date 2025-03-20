import os
import sys
import webbrowser
import subprocess
import time

def main():
    """Main function to start the application"""
    print("Starting Grape Leaf Disease Detection Application...")
    
    # Check if Python is installed
    if not check_python():
        print("Python is not installed or not in PATH. Please install Python 3.7 or higher.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("Created 'uploads' directory.")
    
    # Start the Flask server
    try:
        print("Starting server...")
        server_process = subprocess.Popen([sys.executable, "app.py"], 
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # Wait for server to start
        time.sleep(2)
        
        # Open web browser
        print("Opening web browser...")
        webbrowser.open('http://localhost:5000')
        
        print("Application started successfully!")
        print("Press Ctrl+C to stop the server when you're done.")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
            print("Server stopped.")
    
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def check_python():
    """Check if Python is installed and is version 3.7 or higher"""
    try:
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 7:
            return True
        else:
            print(f"Python version {python_version.major}.{python_version.minor} detected.")
            print("Python 3.7 or higher is required.")
            return False
    except:
        return False

if __name__ == "__main__":
    main() 