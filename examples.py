#!/usr/bin/env python3
"""
Example usage of the SVG QR Code Generator

This script demonstrates how to use the QR code generator both programmatically
and via command line.
"""

from qr_generator import SVGQRGenerator
from pathlib import Path


def example_basic_qr():
    """Generate a basic QR code without logo."""
    print("=== Basic QR Code Example ===")
    
    generator = SVGQRGenerator()
    
    # Generate QR code for a URL
    data = "https://github.com"
    output_path = "basic_qr.svg"
    
    svg_content = generator.generate_qr_svg(
        data=data,
        output_path=output_path,
        fill_color='#000000',
        back_color='#ffffff',
        box_size=10,
        border=4
    )
    
    print(f"Basic QR code generated: {output_path}")
    return output_path


def example_qr_with_logo():
    """Generate a QR code with logo (if logo file exists)."""
    print("\n=== QR Code with Logo Example ===")
    
    generator = SVGQRGenerator()
    
    # Generate QR code for contact info
    data = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
ORG:Example Company
TEL:+1234567890
EMAIL:john@example.com
URL:https://example.com
END:VCARD"""
    
    output_path = "contact_qr_with_logo.svg"
    logo_path = "logo.png"  # This would be your logo file
    
    # Check if logo exists
    if Path(logo_path).exists():
        svg_content = generator.generate_qr_svg(
            data=data,
            output_path=output_path,
            logo_path=logo_path,
            fill_color='#2E86AB',  # Blue color
            back_color='#F5F5F5',  # Light gray background
            box_size=12,
            border=4,
            logo_size_ratio=0.25
        )
        print(f"QR code with logo generated: {output_path}")
    else:
        # Generate without logo
        svg_content = generator.generate_qr_svg(
            data=data,
            output_path=output_path,
            fill_color='#2E86AB',
            back_color='#F5F5F5',
            box_size=12,
            border=4
        )
        print(f"QR code generated without logo (logo file not found): {output_path}")
    
    return output_path


def example_custom_styled_qr():
    """Generate a custom styled QR code."""
    print("\n=== Custom Styled QR Code Example ===")
    
    generator = SVGQRGenerator()
    
    # Generate QR code for WiFi connection
    wifi_data = "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;"
    output_path = "wifi_qr.svg"
    
    svg_content = generator.generate_qr_svg(
        data=wifi_data,
        output_path=output_path,
        fill_color='#8B5CF6',  # Purple
        back_color='#FEF3C7',  # Light yellow
        box_size=8,
        border=6
    )
    
    print(f"WiFi QR code generated: {output_path}")
    return output_path


def example_text_qr():
    """Generate a simple text QR code."""
    print("\n=== Text QR Code Example ===")
    
    generator = SVGQRGenerator()
    
    # Generate QR code for simple text
    text_data = "Hello, World! This is a QR code generated with Python!"
    output_path = "text_qr.svg"
    
    svg_content = generator.generate_qr_svg(
        data=text_data,
        output_path=output_path,
        fill_color='#DC2626',  # Red
        back_color='#FFFFFF',  # White
        box_size=10,
        border=4
    )
    
    print(f"Text QR code generated: {output_path}")
    return output_path


def main():
    """Run all examples."""
    print("SVG QR Code Generator Examples")
    print("=" * 40)
    
    try:
        # Create output directory if it doesn't exist
        Path("examples").mkdir(exist_ok=True)
        
        # Change to examples directory for output
        import os
        original_dir = os.getcwd()
        os.chdir("examples")
        
        # Run examples
        example_basic_qr()
        example_qr_with_logo()
        example_custom_styled_qr()
        example_text_qr()
        
        # Return to original directory
        os.chdir(original_dir)
        
        print("\n" + "=" * 40)
        print("All examples completed! Check the 'examples' folder for generated SVG files.")
        print("\nTo use from command line:")
        print("python qr_generator.py 'Your data here' -o output.svg")
        print("python qr_generator.py 'Your data here' -o output.svg -l logo.png")
        print("\nFor help:")
        print("python qr_generator.py --help")
        
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    main()
