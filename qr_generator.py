#!/usr/bin/env python3
"""
SVG QR Code Generator with Optional Logo Support

This module provides functionality to generate QR codes in SVG format
with optional logo embedding capability.
"""

import qrcode
from PIL import Image, ImageDraw
import io
import base64
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
import sys


class SVGQRGenerator:
    """
    A class to generate SVG QR codes with optional logo embedding.
    """
    
    def __init__(self):
        self.qr = None
        self.logo_size_ratio = 0.2  # Logo will be 20% of QR code size by default
        
    def create_qr_code(self, data, error_correction=qrcode.ERROR_CORRECT_H,
                       box_size=10, border=4, fill_color='black', back_color='white'):
        """
        Create a QR code with the specified parameters.
        
        Args:
            data (str): The data to encode in the QR code
            error_correction: Error correction level (default: HIGH for logo support)
            box_size (int): Size of each box in pixels
            border (int): Border size in boxes
            fill_color (str): Color of the QR code modules
            back_color (str): Background color
        """
        self.qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR Code
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        # Create image with specified colors
        img = self.qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        )
        
        return img
    
    def add_logo_to_qr(self, qr_img, logo_path, logo_size_ratio=None):
        """
        Add a logo to the center of the QR code.
        
        Args:
            qr_img: PIL Image of the QR code
            logo_path (str): Path to the logo image
            logo_size_ratio (float): Ratio of logo size to QR code size
            
        Returns:
            PIL Image with logo embedded
        """
        if logo_size_ratio is None:
            logo_size_ratio = self.logo_size_ratio
            
        try:
            # Ensure images use RGBA so we can composite with alpha
            qr_img = qr_img.convert('RGBA')

            # Open and process logo (keep alpha)
            logo = Image.open(logo_path).convert('RGBA')

            # Calculate logo size
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * logo_size_ratio)

            # Resize logo maintaining aspect ratio
            logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Padding around logo so it doesn't touch QR modules
            padding = max(int(logo_size * 0.08), 8)
            bg_w = logo.size[0] + padding * 2
            bg_h = logo.size[1] + padding * 2

            # Create a transparent background and draw a white rounded rect for contrast
            logo_bg = Image.new('RGBA', (bg_w, bg_h), (255, 255, 255, 0))
            try:
                # Draw rounded rectangle (opaque white)
                radius = max(6, int(min(bg_w, bg_h) * 0.12))
                draw = ImageDraw.Draw(logo_bg)
                draw.rounded_rectangle([0, 0, bg_w, bg_h], radius=radius, fill=(255, 255, 255, 255))
            except Exception:
                # Fallback: plain rectangle
                draw = ImageDraw.Draw(logo_bg)
                draw.rectangle([0, 0, bg_w, bg_h], fill=(255, 255, 255, 255))

            # Paste the logo centered on the background using its alpha channel as mask
            logo_x = (bg_w - logo.size[0]) // 2
            logo_y = (bg_h - logo.size[1]) // 2
            logo_bg.paste(logo, (logo_x, logo_y), logo)

            # Paste onto QR image using alpha compositing to preserve transparency
            qr_img_copy = qr_img.copy()
            qr_w, qr_h = qr_img_copy.size
            pos_x = (qr_w - bg_w) // 2
            pos_y = (qr_h - bg_h) // 2

            qr_img_copy.paste(logo_bg, (pos_x, pos_y), logo_bg)

            # Return to RGB (no alpha) for downstream processing
            return qr_img_copy.convert('RGB')

        except Exception as e:
            print(f"Error adding logo: {e}")
            return qr_img
    
    def pil_to_svg(self, pil_image, svg_path=None):
        """
        Convert PIL image to SVG format.
        
        Args:
            pil_image: PIL Image object
            svg_path (str, optional): Path to save SVG file
            
        Returns:
            str: SVG content as string
        """
        # Convert PIL image to base64
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        img_data = base64.b64encode(buffer.getvalue()).decode()
        
        # Get image dimensions
        width, height = pil_image.size
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" 
     viewBox="0 0 {width} {height}">
    <image width="{width}" height="{height}" 
           xlink:href="data:image/png;base64,{img_data}"/>
</svg>'''
        
        # Save to file if path provided
        if svg_path:
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"SVG saved to: {svg_path}")
        
        return svg_content
    
    def generate_qr_svg(self, data, output_path=None, logo_path=None,
                       fill_color='black', back_color='white',
                       box_size=10, border=4, logo_size_ratio=None):
        """
        Generate a complete QR code in SVG format with optional logo.
        
        Args:
            data (str): Data to encode
            output_path (str, optional): Path to save SVG file
            logo_path (str, optional): Path to logo image
            fill_color (str): QR code color
            back_color (str): Background color
            box_size (int): Size of each module
            border (int): Border size
            logo_size_ratio (float, optional): Logo size ratio
            
        Returns:
            str: SVG content
        """
        # Create QR code
        qr_img = self.create_qr_code(
            data=data,
            fill_color=fill_color,
            back_color=back_color,
            box_size=box_size,
            border=border
        )
        
        # Add logo if provided
        if logo_path and Path(logo_path).exists():
            qr_img = self.add_logo_to_qr(qr_img, logo_path, logo_size_ratio)
        elif logo_path:
            print(f"Warning: Logo file not found: {logo_path}")
        
        # Convert to SVG
        svg_content = self.pil_to_svg(qr_img, output_path)
        
        return svg_content


def main():
    """Command line interface for the QR code generator."""
    parser = argparse.ArgumentParser(description='Generate SVG QR codes with optional logo')
    parser.add_argument('data', help='Data to encode in the QR code')
    parser.add_argument('-o', '--output', help='Output SVG file path')
    parser.add_argument('-l', '--logo', help='Path to logo image file')
    parser.add_argument('--fill-color', default='black', help='QR code color (default: black)')
    parser.add_argument('--back-color', default='white', help='Background color (default: white)')
    parser.add_argument('--box-size', type=int, default=10, help='Box size (default: 10)')
    parser.add_argument('--border', type=int, default=4, help='Border size (default: 4)')
    parser.add_argument('--logo-size', type=float, default=0.2, 
                       help='Logo size ratio (0.1-0.3 recommended, default: 0.2)')
    
    args = parser.parse_args()
    
    # Validate logo size ratio
    if not 0.05 <= args.logo_size <= 0.4:
        print("Warning: Logo size ratio should be between 0.05 and 0.4 for best results")
    
    # Create generator
    generator = SVGQRGenerator()
    
    try:
        # Generate QR code
        svg_content = generator.generate_qr_svg(
            data=args.data,
            output_path=args.output,
            logo_path=args.logo,
            fill_color=args.fill_color,
            back_color=args.back_color,
            box_size=args.box_size,
            border=args.border,
            logo_size_ratio=args.logo_size
        )
        
        # If no output file specified, print to stdout
        if not args.output:
            print("SVG Content:")
            print(svg_content)
            
        print(f"Successfully generated QR code for: {args.data}")
        
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
