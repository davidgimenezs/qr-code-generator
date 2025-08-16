#!/usr/bin/env python3
"""
Interactive usage guide for the SVG QR Code Generator
"""

from qr_generator import SVGQRGenerator
import os

def print_header():
    """Print the application header."""
    print("=" * 60)
    print("       SVG QR Code Generator - Interactive Guide")
    print("=" * 60)
    print()

def show_help():
    """Show command line help."""
    print("Command Line Usage Examples:")
    print("-" * 30)
    print("1. Basic QR code:")
    print("   python qr_generator.py \"Your data here\" -o output.svg")
    print()
    print("2. QR code with logo:")
    print("   python qr_generator.py \"Your data\" -o output.svg -l logo.png")
    print()
    print("3. Custom colors:")
    print("   python qr_generator.py \"Your data\" -o output.svg --fill-color \"#FF6B6B\" --back-color \"#F8F9FA\"")
    print()
    print("4. Large size for printing:")
    print("   python qr_generator.py \"Your data\" -o output.svg --box-size 15 --border 6")
    print()
    print("5. Complete help:")
    print("   python qr_generator.py --help")
    print()

def interactive_generator():
    """Interactive QR code generator."""
    print("Interactive QR Code Generator")
    print("-" * 30)
    
    try:
        # Get user input
        data = input("Enter the data to encode (URL, text, etc.): ").strip()
        if not data:
            print("No data entered. Exiting.")
            return
        
        output_file = input("Enter output filename (default: qr_code.svg): ").strip()
        if not output_file:
            output_file = "qr_code.svg"
        if not output_file.endswith('.svg'):
            output_file += '.svg'
        
        # Logo option
        use_logo = input("Add a logo? (y/n, default: n): ").strip().lower()
        logo_path = None
        if use_logo in ['y', 'yes']:
            logo_path = input("Enter logo file path: ").strip()
            if logo_path and not os.path.exists(logo_path):
                print(f"Warning: Logo file '{logo_path}' not found. Continuing without logo.")
                logo_path = None
        
        # Color options
        use_custom_colors = input("Use custom colors? (y/n, default: n): ").strip().lower()
        fill_color = 'black'
        back_color = 'white'
        
        if use_custom_colors in ['y', 'yes']:
            fill_color = input("Enter QR code color (default: black): ").strip() or 'black'
            back_color = input("Enter background color (default: white): ").strip() or 'white'
        
        # Size options
        use_custom_size = input("Customize size? (y/n, default: n): ").strip().lower()
        box_size = 10
        border = 4
        
        if use_custom_size in ['y', 'yes']:
            try:
                box_size = int(input("Enter box size (default: 10): ").strip() or "10")
                border = int(input("Enter border size (default: 4): ").strip() or "4")
            except ValueError:
                print("Invalid size values. Using defaults.")
                box_size = 10
                border = 4
        
        # Generate QR code
        print("\nGenerating QR code...")
        generator = SVGQRGenerator()
        
        svg_content = generator.generate_qr_svg(
            data=data,
            output_path=output_file,
            logo_path=logo_path,
            fill_color=fill_color,
            back_color=back_color,
            box_size=box_size,
            border=border
        )
        
        print(f"✅ QR code successfully generated: {output_file}")
        
        # Show scan instructions
        print("\nTo test your QR code:")
        print("1. Open the SVG file in a web browser")
        print("2. Use a QR code scanner app on your phone")
        print("3. The scanner should decode:", data[:50] + "..." if len(data) > 50 else data)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

def show_examples():
    """Show common QR code examples."""
    print("Common QR Code Examples:")
    print("-" * 25)
    
    examples = [
        ("Website URL", "https://example.com"),
        ("Email", "mailto:someone@example.com?subject=Hello&body=Message"),
        ("Phone number", "tel:+1234567890"),
        ("SMS", "SMS:+1234567890:Hello from QR code!"),
        ("WiFi Network", "WIFI:T:WPA;S:NetworkName;P:Password;;"),
        ("Plain text", "Hello, World! This is a QR code."),
        ("Contact (vCard)", "BEGIN:VCARD\\nVERSION:3.0\\nFN:John Doe\\nTEL:+1234567890\\nEMAIL:john@example.com\\nEND:VCARD")
    ]
    
    for i, (desc, data) in enumerate(examples, 1):
        print(f"{i}. {desc}:")
        print(f"   {data}")
        print()

def main_menu():
    """Show the main menu and handle user choices."""
    while True:
        print("\nChoose an option:")
        print("1. Generate QR code interactively")
        print("2. Show command line examples")
        print("3. Show common data examples")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            interactive_generator()
        elif choice == '2':
            show_help()
        elif choice == '3':
            show_examples()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

def main():
    """Main function."""
    print_header()
    print("This interactive guide will help you generate QR codes.")
    print("You can also use the command line interface for automation.")
    print()
    
    main_menu()

if __name__ == "__main__":
    main()
