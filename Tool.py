from PIL import Image
import os
from pyfiglet import figlet_format, FontNotFound, FigletFont
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# --- Text-to-ASCII Conversion ---
def text_to_ascii(text, font="standard", color=Fore.WHITE, scale=1):
    """
    Convert text to ASCII art using pyfiglet with custom font, color, and scaling.
    """
    try:
        ascii_art = figlet_format(text, font=font)
        # Scale the ASCII art
        scaled_art = scale_ascii_art(ascii_art, scale)
        return f"{color}{scaled_art}{Style.RESET_ALL}"
    except FontNotFound:
        return "Error: Invalid font name. Please choose a valid font."
    except ImportError:
        return "Error: pyfiglet is not installed. Install it using 'pip install pyfiglet'."

# --- Scale ASCII Art ---
def scale_ascii_art(ascii_art, scale):
    """
    Scale ASCII art by duplicating characters horizontally and vertically.
    """
    if scale < 1:
        scale = 1  # Minimum scale is 1x
    lines = ascii_art.split("\n")
    scaled_lines = []
    for line in lines:
        # Scale horizontally
        scaled_line = "".join([char * scale for char in line])
        # Scale vertically by repeating the line
        scaled_lines.extend([scaled_line] * scale)
    return "\n".join(scaled_lines)

# --- List Available Fonts ---
def list_fonts():
    """
    List all available fonts supported by pyfiglet.
    """
    try:
        fonts = FigletFont.getFonts()
        print("\nAvailable Fonts:")
        for i, font in enumerate(fonts, 1):
            print(f"{i}. {font}")
        return fonts
    except Exception as e:
        return f"Error listing fonts: {str(e)}"

# --- Image-to-ASCII Conversion ---
def image_to_ascii(image_path, output_width=100, scale=1):
    """
    Convert an image to ASCII art with scaling.
    """
    ascii_chars = "@%#*+=-:. "
    try:
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        width, height = img.size
        ratio = height / width / 2
        new_width = output_width * scale
        new_height = int(output_width * ratio * scale)
        img = img.resize((new_width, new_height))
        pixels = img.getdata()
        ascii_str = "".join([ascii_chars[pixel // 25] for pixel in pixels])
        ascii_img = "\n".join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
        return ascii_img
    except Exception as e:
        return f"Image Error: {str(e)}"

# --- Terminal Interface ---
def main_menu():
    while True:
        print("\n" + "="*40)
        print("ASCII ART GENERATOR".center(40))
        print("="*40)
        print("1. Convert text to ASCII")
        print("2. Convert image to ASCII")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            text = input("Enter text to convert to ASCII: ")
            
            # List fonts and let the user choose one
            fonts = list_fonts()
            try:
                font_choice = int(input("Choose a font number (default is 1): ").strip()) - 1
                font = fonts[font_choice] if 0 <= font_choice < len(fonts) else "standard"
            except (ValueError, IndexError):
                font = "standard"
            
            # Let the user choose a color
            print("\nAvailable Colors:")
            print("1. White")
            print("2. Red")
            print("3. Green")
            print("4. Blue")
            print("5. Yellow")
            print("6. Magenta")
            print("7. Cyan")
            print("8. Black (may not be visible on dark terminals)")
            color_choice = input("Choose a color number (default is 1): ").strip()
            colors = {
                "1": Fore.WHITE,
                "2": Fore.RED,
                "3": Fore.GREEN,
                "4": Fore.BLUE,
                "5": Fore.YELLOW,
                "6": Fore.MAGENTA,
                "7": Fore.CYAN,
                "8": Fore.BLACK,  # Fixed missing comma here
            }
            color = colors.get(color_choice, Fore.WHITE)
            
            # Let the user choose a scale
            try:
                scale = int(input("Enter scale factor (default is 1): ").strip())
                scale = max(1, scale)  # Ensure scale is at least 1
            except ValueError:
                scale = 1
            
            # Generate ASCII art
            ascii_art = text_to_ascii(text, font, color, scale)
            print("\nGenerated ASCII Art:\n")
            print(ascii_art)
            
        elif choice == "2":
            path = input("Enter image path: ").strip()
            if not os.path.exists(path):
                print("File not found! Please check the path.")
                continue
            try:
                output_width = int(input("Enter output width (in characters): ").strip() or 100)
            except ValueError:
                print("Invalid width! Using default width of 100.")
                output_width = 100
            
            # Let the user choose a scale
            try:
                scale = int(input("Enter scale factor (default is 1, 2 for bigger art): ").strip())
                scale = max(1, scale)  # Ensure scale is at least 1
            except ValueError:
                scale = 1
            
            print("\nConverting...")
            ascii_art = image_to_ascii(path, output_width, scale)
            print("\nGenerated ASCII Art:\n")
            print(ascii_art)
            
        elif choice == "3":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice! Please enter 1-3")

if __name__ == "__main__":
    main_menu()