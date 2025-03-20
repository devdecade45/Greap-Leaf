import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create the users directory if it doesn't exist
os.makedirs('images/users', exist_ok=True)

# Define the image dimensions (square profile images)
size = 200

# Define the users to create images for
users = [
    {
        'filename': 'user1.png',
        'initials': 'JD',
        'bg_color': (76, 175, 80)  # Green
    },
    {
        'filename': 'user2.png',
        'initials': 'MR',
        'bg_color': (33, 150, 243)  # Blue
    },
    {
        'filename': 'user3.png',
        'initials': 'TS',
        'bg_color': (156, 39, 176)  # Purple
    },
    {
        'filename': 'user4.png',
        'initials': 'AK',
        'bg_color': (255, 152, 0)  # Orange
    },
    {
        'filename': 'user5.png',
        'initials': 'PL',
        'bg_color': (0, 188, 212)  # Cyan
    }
]

# Create each image
for user in users:
    filename = user['filename']
    initials = user['initials']
    bg_color = user['bg_color']
    
    # Create a new image with the specified background color
    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add a subtle pattern
    for i in range(0, size, 10):
        # Draw diagonal lines
        line_color = (
            max(0, bg_color[0] - 20),
            max(0, bg_color[1] - 20),
            max(0, bg_color[2] - 20)
        )
        draw.line([(0, i), (i, 0)], fill=line_color, width=1)
        draw.line([(size, i), (i, size)], fill=line_color, width=1)
    
    # Add the initials text
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width = draw.textlength(initials, font=font)
    text_position = ((size - text_width) // 2, (size // 2) - 40)
    
    # Draw text with a shadow effect
    shadow_offset = 2
    draw.text((text_position[0] + shadow_offset, text_position[1] + shadow_offset), initials, font=font, fill=(0, 0, 0, 128))
    draw.text(text_position, initials, font=font, fill=(255, 255, 255))
    
    # Add a circular mask
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)
    
    # Create a new RGBA image
    img_rgba = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    img_rgba.paste(img, (0, 0), mask)
    
    # Save the image
    target_path = os.path.join('images/users', filename)
    img_rgba.save(target_path)
    print(f"Created user profile image: {target_path}")

print("User profile images created successfully.") 