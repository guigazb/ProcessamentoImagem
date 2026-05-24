from PIL import Image

def convert_jpg_to_pgm_p2(input_path, output_path):
    # Load image and convert to grayscale
    img = Image.open(input_path).convert('L')
    width, height = img.size
    pixels = list(img.getdata())
    
    # Write P2 PGM file
    with open(output_path, 'w') as f:
        f.write(f"P2\n{width} {height}\n255\n")
        for i, pixel in enumerate(pixels):
            f.write(str(pixel) + " ")
            if (i + 1) % width == 0:
                f.write("\n")

# Example usage
convert_jpg_to_pgm_p2('demolidor.jpeg', 'output.pgm')
