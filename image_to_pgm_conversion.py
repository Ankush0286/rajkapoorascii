from PIL import Image
import sys


def img_to_p2(input_path, output_file):
    img_gray = Image.open(input_path).convert('L')
    width, height = img_gray.size
    pixels = list(img_gray.tobytes())
    
    try:
        with open(output_file, 'w') as f:
            f.write(f"P2\n{width} {height}\n255\n")
            for i, pix in enumerate(pixels):
                f.write(f"{pix} ")
                if (i + 1) % width == 0:
                    f.write("\n")
        return "File saved successfully."
    except Exception as e:
        return f"Error writing to file: {e}"

if __name__ == "__main__":
    input_file = "rajkapoor.jpg"
    output_file = "rajkapoor.pgm"
    print(img_to_p2(input_file, output_file))
