#extract.py

import os
import zipfile
import shutil
from PIL import Image
from PIL import ImageSequence

def create_gif_from_bootanimation(bootanimation_zip_path):
    # Check if the zip file exists
    if not os.path.exists(bootanimation_zip_path):
        print(f"The file '{bootanimation_zip_path}' does not exist.")
        return

    # Create a folder for temporary extraction
    extraction_folder = "temp_extracted_frames"
    os.makedirs(extraction_folder, exist_ok=True)

    try:
        # Extract the bootanimation.zip file
        with zipfile.ZipFile(bootanimation_zip_path, 'r') as bootanimation_zip:
            bootanimation_zip.extractall(extraction_folder)
    except Exception as e:
        print(f"Error extracting files from '{bootanimation_zip_path}': {str(e)}")
        return

    # Read the frame rate from the first line of desc.txt
    desc_txt_path = os.path.join(extraction_folder, 'desc.txt')
    original_frame_rate = None

    if os.path.exists(desc_txt_path):
        try:
            with open(desc_txt_path, 'r', encoding='utf-8', errors='ignore') as desc_file:
                lines = desc_file.readlines()

            if lines and len(lines[0].split()) == 3:
                _, _, frame_rate = map(int, lines[0].split())
                original_frame_rate = round(1000 / frame_rate)
        except (ValueError, IndexError):
            print("Invalid data format in desc.txt.")

    # Find all part folders in the extraction folder
    part_folders = [os.path.join(extraction_folder, folder) for folder in os.listdir(extraction_folder) if os.path.isdir(os.path.join(extraction_folder, folder))]

    # Sort the part folders alphabetically
    part_folders.sort()

    # Create a list to hold the image frames
    frames = []

    for part_folder in part_folders:
        # Find all image files in the part folder and sort them alphabetically
        image_files = [os.path.join(part_folder, filename) for filename in sorted(os.listdir(part_folder)) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Open each image file and append it to the frames list
        for image_file in image_files:
            frame = Image.open(image_file)
            frames.append(frame)

    # Check if there are frames to create a GIF
    if frames:
        # Ask for the desired frame rate (speed)
        custom_frame_rate = input(f"Set custom frame rate (press Enter to keep original = {original_frame_rate}): ")
        if custom_frame_rate:
            try:
                custom_frame_rate = int(custom_frame_rate)
            except ValueError:
                print("Invalid frame rate. Using original frame rate.")
                custom_frame_rate = None

        # Use the custom frame rate if provided, otherwise use the original frame rate
        frame_rate = custom_frame_rate or original_frame_rate

        # Create a GIF file with frame rate in the file name
        frame_rate_str = f"fps{frame_rate}"
        gif_filename = os.path.splitext(os.path.basename(bootanimation_zip_path))[0] + f"-{frame_rate_str}.gif"
        gif_path = os.path.join(os.path.dirname(bootanimation_zip_path), gif_filename)
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=frame_rate)
        print(f"The GIF has been successfully recreated as '{gif_path}'.")
    else:
        print("No frames found to create a GIF.")

    # Clean up by removing the temporary extraction folder
    if os.path.exists(extraction_folder):
        try:
            shutil.rmtree(extraction_folder)
        except Exception as e:
            print(f"Error deleting temporary folder '{extraction_folder}': {str(e)}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        bootanimation_zip_path = input("Enter the path to the bootanimation.zip file: ")
    elif len(sys.argv) == 2:
        bootanimation_zip_path = sys.argv[1]
    else:
        print("Usage: python create_gif_from_bootanimation.py [optional: bootanimation_zip_path]")
        sys.exit(1)

    create_gif_from_bootanimation(bootanimation_zip_path)
