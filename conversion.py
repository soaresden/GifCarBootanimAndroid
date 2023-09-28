#conversion.py
import os
import zipfile
from PIL import Image
from PIL import ImageSequence

def resize_and_center(image, new_width, new_height):
    width, height = image.size
    ratio = min(new_width / width, new_height / height)
    resized_width = int(width * ratio)
    resized_height = int(height * ratio)
    resized_image = image.resize((resized_width, resized_height), Image.BILINEAR)
    x = (new_width - resized_width) // 2
    y = (new_height - resized_height) // 2
    background = Image.new("RGB", (new_width, new_height), (0, 0, 0))
    background.paste(resized_image, (x, y))
    return background

def resize_gif(gif_path, new_dimensions):
    if not os.path.exists(gif_path):
        print(f"The GIF file '{gif_path}' does not exist.")
        return

    try:
        new_width, new_height = map(int, new_dimensions.split("x"))
    except ValueError:
        print("Invalid dimensions format. Use the format 'widthxheight' (e.g., '1920x1200').")
        return

    with Image.open(gif_path) as gif:
        background = Image.new("RGB", (new_width, new_height), (0, 0, 0))
        resized_frames = []
        for frame in ImageSequence.Iterator(gif):
            resized_frame = resize_and_center(frame, new_width, new_height)
            resized_frames.append(resized_frame)

        base_filename = os.path.splitext(os.path.basename(gif_path))[0]
        resized_gif_name = f"{base_filename}_{new_width}x{new_height}.gif"
        resized_frames[0].save(resized_gif_name, save_all=True, append_images=resized_frames[1:], loop=0, duration=gif.info["duration"])
        print(f"The resized GIF has been successfully saved as '{resized_gif_name}'.")

def create_bootanimation_zip(gif_path, animation_choice):
    if not os.path.exists(gif_path):
        print(f"The GIF file '{gif_path}' does not exist.")
        return

    if animation_choice not in ["1", "2", "3"]:
        print("Invalid animation choice. Use 1 for a looping animation, 2 for a fixed animation, or 3 to resize the GIF.")
        return

    if animation_choice == "3":
        new_dimensions = input("Enter new dimensions (format: widthxheight, e.g., '1920x1200'): ")
        resize_gif(gif_path, new_dimensions)
    else:
        with Image.open(gif_path) as gif:
            width, height = gif.size
            frame_rate = gif.info.get("duration", 100)
            width = round(width)
            height = round(height)
            frame_rate = round(1000 / frame_rate)

        base_filename = os.path.splitext(os.path.basename(gif_path))[0]
        output_folder = "part0"
        os.makedirs(output_folder, exist_ok=True)

        with Image.open(gif_path) as gif:
            last_frame = None
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                frame_number = str(i + 1).zfill(3)
                frame.save(os.path.join(output_folder, f"b{frame_number}.png"))
                last_frame = frame

        if animation_choice == "2":
            last_frame_folder = "part1"
            os.makedirs(last_frame_folder, exist_ok=True)
            last_frame_number = len(os.listdir(output_folder)) + 1
            last_frame_number_str = str(last_frame_number).zfill(3)
            last_frame_copy_path = os.path.join(last_frame_folder, f"b{last_frame_number_str}.png")
            last_frame.save(last_frame_copy_path)

        output_zip_path = f"{base_filename}-loop.zip" if animation_choice == "1" else f"{base_filename}-fixed.zip"
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_STORED) as bootanimation_zip:
            desc_txt = f'{width} {height} {frame_rate}\np 1 0 {output_folder}\n'
            if animation_choice == "2":
                desc_txt += f'p 0 0 {last_frame_folder}\n'

            bootanimation_zip.writestr('desc.txt', desc_txt)

            for png_file in os.listdir(output_folder):
                if png_file.endswith(".png"):
                    bootanimation_zip.write(os.path.join(output_folder, png_file), os.path.join(output_folder, png_file))
            if animation_choice == "2":
                for png_file in os.listdir(last_frame_folder):
                    if png_file.endswith(".png"):
                        bootanimation_zip.write(os.path.join(last_frame_folder, png_file), os.path.join(last_frame_folder, png_file))

        for png_file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, png_file))
        if animation_choice == "2":
            for png_file in os.listdir(last_frame_folder):
                os.remove(os.path.join(last_frame_folder, png_file))
            os.rmdir(last_frame_folder)
        os.rmdir(output_folder)

        print(f"The bootanimation.zip file has been successfully created as '{output_zip_path}'.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        gif_path = input("Drag and drop the GIF file here: ")
    elif len(sys.argv) == 2:
        gif_path = sys.argv[1]
    else:
        print("Usage: python create_bootanimation.py [optional: gif_file_path]")
        sys.exit(1)

    print("Choose the animation type:")
    print("1. Looping animation")
    print("2. Play once and freeze animation")
    print("3. Resize the GIF")

    animation_choice = input("Your choice: ")

    create_bootanimation_zip(gif_path, animation_choice)