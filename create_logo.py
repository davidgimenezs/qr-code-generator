#!/usr/bin/env python3
"""
Create a simple sample logo for testing the QR code generator.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_logo():
    """Create a simple sample logo image."""
    # Create a 200x200 image with transparent background
    size = 200
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle background
    circle_color = (66, 133, 244, 255)  # Google Blue
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], fill=circle_color)
    
    # Draw text "LOGO" in the center
    text = "LOGO"
    try:
        # Try to use a built-in font
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw white text
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save the logo
    img.save('sample_logo.png')
    print("Sample logo created: sample_logo.png")
    
    return 'sample_logo.png'

if __name__ == "__main__":
    create_sample_logo()
