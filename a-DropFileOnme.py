import os
import sys

def main():
    if len(sys.argv) == 2:
        gif_path = sys.argv[1]
    else:
        gif_path = input("Drag and drop the GIF file here: ")

    # Check the file extension to determine which script to use
    file_extension = os.path.splitext(gif_path)[1].lower()

    if file_extension == ".gif":
        print("Choose the action:")
        print("1. Looping animation")
        print("2. Play once and freeze animation")
        print("3. Resize the GIF")

        animation_choice = input("Your choice: ")

        if animation_choice == "3":
            new_dimensions = input("Enter new dimensions (format: widthxheight, e.g., '1920x1200'): ")
            # Call the resize_gif function from conversion.py
            from conversion import resize_gif
            resize_gif(gif_path, new_dimensions)
        else:
            # Call the create_bootanimation_zip function from conversion.py
            from conversion import create_bootanimation_zip
            create_bootanimation_zip(gif_path, animation_choice)
    elif file_extension == ".zip":
        # Call the create_gif_from_bootanimation function from extract.py
        from extract import create_gif_from_bootanimation
        create_gif_from_bootanimation(gif_path)
    else:
        print("Invalid file format. Please provide a GIF or bootanimation.zip file.")

if __name__ == "__main__":
    main()
