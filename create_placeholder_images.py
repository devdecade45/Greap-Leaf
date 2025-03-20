import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create the previews directory if it doesn't exist
os.makedirs('images/previews', exist_ok=True)

# Define the image dimensions
width, height = 800, 500

# Define the images to create
images = [
    {
        'filename': 'diseases-preview.jpg',
        'title': 'Grape Diseases',
        'subtitle': 'Identification & Treatment',
        'bg_color': (156, 39, 176)  # Purple
    }
]

# Create each image
for img_info in images:
    filename = img_info['filename']
    title = img_info['title']
    subtitle = img_info['subtitle']
    bg_color = img_info['bg_color']
    
    # Create a new image with the specified background color
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add a gradient overlay
    for y in range(height):
        for x in range(width):
            # Create a radial gradient
            distance = ((x - width/2)**2 + (y - height/2)**2)**0.5
            max_distance = ((width/2)**2 + (height/2)**2)**0.5
            ratio = distance / max_distance
            
            # Darken the edges
            if x < width and y < height:  # Check bounds
                r, g, b = img.getpixel((x, y))
                factor = 1 - (ratio * 0.5)  # Darken by up to 50%
                r = int(r * factor)
                g = int(g * factor)
                b = int(b * factor)
                img.putpixel((x, y), (r, g, b))
    
    # Draw leaf disease patterns
    for _ in range(15):
        # Draw leaf shapes with disease spots
        leaf_x = random.randint(50, width-50)
        leaf_y = random.randint(50, height-50)
        leaf_size = random.randint(40, 80)
        
        # Leaf base color (green with variations)
        leaf_color = (
            random.randint(60, 120),  # R
            random.randint(140, 200),  # G
            random.randint(60, 120)   # B
        )
        
        # Draw a leaf shape (oval)
        draw.ellipse(
            (leaf_x - leaf_size, leaf_y - leaf_size//2, 
             leaf_x + leaf_size, leaf_y + leaf_size//2), 
            fill=leaf_color
        )
        
        # Add disease spots
        for _ in range(random.randint(3, 8)):
            spot_size = random.randint(5, 15)
            spot_x = random.randint(leaf_x - leaf_size + spot_size, leaf_x + leaf_size - spot_size)
            spot_y = random.randint(leaf_y - leaf_size//2 + spot_size, leaf_y + leaf_size//2 - spot_size)
            
            # Disease spot color (brown/black/yellow variations)
            spot_type = random.choice(['black_rot', 'leaf_blight', 'esca'])
            
            if spot_type == 'black_rot':
                spot_color = (random.randint(50, 80), random.randint(30, 60), random.randint(20, 40))
            elif spot_type == 'leaf_blight':
                spot_color = (random.randint(180, 220), random.randint(140, 180), random.randint(60, 100))
            else:  # esca
                spot_color = (random.randint(120, 160), random.randint(80, 120), random.randint(40, 80))
                
            draw.ellipse(
                (spot_x - spot_size, spot_y - spot_size, 
                 spot_x + spot_size, spot_y + spot_size), 
                fill=spot_color
            )
    
    # Add a semi-transparent overlay at the bottom for text
    overlay_height = 150
    for y in range(height - overlay_height, height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            # Gradually increase darkness toward the bottom
            darkness = (y - (height - overlay_height)) / overlay_height
            r = int(r * (1 - darkness * 0.8))
            g = int(g * (1 - darkness * 0.8))
            b = int(b * (1 - darkness * 0.8))
            img.putpixel((x, y), (r, g, b))
    
    # Add the title text
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width = draw.textlength(title, font=font)
    text_position = ((width - text_width) // 2, height - 120)
    
    # Draw text with a shadow effect
    shadow_offset = 3
    draw.text((text_position[0] + shadow_offset, text_position[1] + shadow_offset), title, font=font, fill=(0, 0, 0, 128))
    draw.text(text_position, title, font=font, fill=(255, 255, 255))
    
    # Add a subtitle
    try:
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        subtitle_font = ImageFont.load_default()
    
    subtitle_width = draw.textlength(subtitle, font=subtitle_font)
    subtitle_position = ((width - subtitle_width) // 2, height - 60)
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill=(255, 255, 255))
    
    # Save the image
    target_path = os.path.join('images/previews', filename)
    img.save(target_path)
    print(f"Created disease-specific image: {target_path}")

print("Disease image created successfully.") 