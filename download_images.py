import os
import urllib.request
import ssl

# Create a context that doesn't verify SSL certificates
ssl._create_default_https_context = ssl._create_unverified_context

# Create the previews directory if it doesn't exist
os.makedirs('images/previews', exist_ok=True)

# Define the image URLs and their target filenames
images = [
    {
        'url': 'https://images.unsplash.com/photo-1464638681273-0962e9b53566?ixlib=rb-4.0.3',
        'filename': 'about-preview.jpg',
        'description': 'Vineyard landscape for About Us'
    },
    {
        'url': 'https://images.unsplash.com/photo-1573062337052-54ad1468bb5e?ixlib=rb-4.0.3',
        'filename': 'detection-preview.jpg',
        'description': 'Close-up of grape leaves for Disease Detection'
    },
    # Skip the ones that were already downloaded successfully
    # {
    #     'url': 'https://images.unsplash.com/photo-1596957901846-a0722f546502',
    #     'filename': 'diseases-preview.jpg',
    #     'description': 'Grape clusters for Diseases Information'
    # },
    # {
    #     'url': 'https://images.unsplash.com/photo-1516810714657-e654b97f1d80',
    #     'filename': 'contact-preview.jpg',
    #     'description': 'Vineyard workers for Contact Us'
    # }
]

# Download each image
for image in images:
    target_path = os.path.join('images/previews', image['filename'])
    
    # Skip if the file already exists
    if os.path.exists(target_path):
        print(f"File {target_path} already exists. Skipping.")
        continue
    
    print(f"Downloading {image['description']} to {target_path}...")
    try:
        urllib.request.urlretrieve(image['url'], target_path)
        print(f"Successfully downloaded {image['filename']}")
    except Exception as e:
        print(f"Error downloading {image['filename']}: {e}")

print("Download process completed.") 