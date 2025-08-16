# SVG QR Code Generator with Logo Support

A Python library and command-line tool for generating QR codes in SVG format with optional logo embedding support.

## Features

- ✅ Generate QR codes in SVG format
- ✅ Add custom logos to QR codes
- ✅ Customizable colors (foreground and background)
- ✅ Adjustable size and border settings
- ✅ High error correction for logo compatibility
- ✅ Command-line interface and Python API
- ✅ Support for various data types (URLs, text, vCard, WiFi, etc.)

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required dependencies:

```bash
pip install qrcode[pil] Pillow svglib reportlab
```

## Quick Start

### Command Line Usage

```bash
# Basic QR code
python qr_generator.py "https://github.com" -o my_qr.svg

# QR code with logo
python qr_generator.py "https://example.com" -o branded_qr.svg -l logo.png

# Custom colors and size
python qr_generator.py "Hello World" -o custom_qr.svg --fill-color "#FF6B6B" --back-color "#F8F9FA" --box-size 12

# WiFi QR code
python qr_generator.py "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;" -o wifi_qr.svg
```

### Python API Usage

```python
from qr_generator import SVGQRGenerator

# Create generator instance
generator = SVGQRGenerator()

# Basic QR code
svg_content = generator.generate_qr_svg(
    data="https://example.com",
    output_path="basic_qr.svg"
)

# QR code with logo
svg_content = generator.generate_qr_svg(
    data="Your data here",
    output_path="logo_qr.svg",
    logo_path="your_logo.png",
    fill_color="#2E86AB",
    back_color="#F5F5F5",
    logo_size_ratio=0.2
)
```

## Command Line Options

```
positional arguments:
  data                  Data to encode in the QR code

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output SVG file path
  -l LOGO, --logo LOGO  Path to logo image file
  --fill-color FILL_COLOR
                        QR code color (default: black)
  --back-color BACK_COLOR
                        Background color (default: white)
  --box-size BOX_SIZE   Box size (default: 10)
  --border BORDER       Border size (default: 4)
  --logo-size LOGO_SIZE
                        Logo size ratio (0.1-0.3 recommended, default: 0.2)
```

## Supported Data Types

### URLs
```bash
python qr_generator.py "https://example.com" -o url_qr.svg
```

### Plain Text
```bash
python qr_generator.py "Hello, World!" -o text_qr.svg
```

### WiFi Credentials
```bash
python qr_generator.py "WIFI:T:WPA;S:NetworkName;P:Password;;" -o wifi_qr.svg
```

### Contact Information (vCard)
```bash
python qr_generator.py "BEGIN:VCARD
VERSION:3.0
FN:John Doe
ORG:Company
TEL:+1234567890
EMAIL:john@example.com
END:VCARD" -o contact_qr.svg
```

### SMS
```bash
python qr_generator.py "SMS:+1234567890:Hello from QR code!" -o sms_qr.svg
```

### Email
```bash
python qr_generator.py "mailto:someone@example.com?subject=Hello&body=Message" -o email_qr.svg
```

## Logo Guidelines

For best results when adding logos:

1. **Logo Size**: Keep logo size ratio between 0.1 and 0.3 (10%-30% of QR code)
2. **File Formats**: PNG, JPG, GIF supported (PNG with transparency recommended)
3. **Resolution**: Higher resolution logos work better
4. **Simple Designs**: Logos with simple designs and clear contrast work best
5. **Error Correction**: The library uses high error correction to accommodate logos

## Color Formats

Supported color formats:
- Named colors: `"red"`, `"blue"`, `"green"`, etc.
- Hex colors: `"#FF0000"`, `"#00FF00"`, `"#0000FF"`
- RGB: `"rgb(255, 0, 0)"`

## Examples

Run the examples script to see various use cases:

```bash
python examples.py
```

This will generate several example QR codes in the `examples/` folder:
- Basic QR code
- QR code with logo (if logo file exists)
- Custom styled QR code
- Text QR code

## API Reference

### SVGQRGenerator Class

#### `__init__()`
Initialize the QR code generator.

#### `create_qr_code(data, error_correction, box_size, border, fill_color, back_color)`
Create a basic QR code image.

**Parameters:**
- `data` (str): Data to encode
- `error_correction`: Error correction level (default: HIGH)
- `box_size` (int): Size of each module (default: 10)
- `border` (int): Border size in modules (default: 4)
- `fill_color` (str): QR code color (default: 'black')
- `back_color` (str): Background color (default: 'white')

#### `add_logo_to_qr(qr_img, logo_path, logo_size_ratio)`
Add a logo to the center of a QR code.

**Parameters:**
- `qr_img`: PIL Image of the QR code
- `logo_path` (str): Path to logo image file
- `logo_size_ratio` (float): Logo size as ratio of QR code size (default: 0.2)

#### `generate_qr_svg(data, output_path, logo_path, fill_color, back_color, box_size, border, logo_size_ratio)`
Generate a complete QR code in SVG format.

**Parameters:**
- `data` (str): Data to encode
- `output_path` (str, optional): Path to save SVG file
- `logo_path` (str, optional): Path to logo image
- `fill_color` (str): QR code color (default: 'black')
- `back_color` (str): Background color (default: 'white')
- `box_size` (int): Size of each module (default: 10)
- `border` (int): Border size (default: 4)
- `logo_size_ratio` (float, optional): Logo size ratio (default: 0.2)

**Returns:** SVG content as string

## File Structure

```
qr/
├── qr_generator.py     # Main QR code generator
├── examples.py         # Example usage scripts
├── README.md          # This documentation
└── examples/          # Generated example files (created by examples.py)
```

## Tips and Best Practices

1. **Testing**: Always test your QR codes with multiple QR code readers
2. **Size**: For printing, use larger box sizes (15-20) for better scanning
3. **Contrast**: Ensure good contrast between fill and background colors
4. **Logo Placement**: Logos are automatically centered and sized appropriately
5. **Error Correction**: High error correction is used by default for logo support

## Troubleshooting

### Common Issues

**"Logo file not found"**
- Check the logo file path is correct
- Ensure the file exists and is readable

**"QR code not scanning"**
- Try reducing logo size ratio
- Increase error correction level
- Test with different QR code readers

**"SVG not displaying correctly"**
- Ensure SVG viewer supports embedded images
- Try opening in a web browser

## License

This project is open source. Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
