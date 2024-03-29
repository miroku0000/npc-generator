import os
import subprocess
import shutil

def move_files(input_dir, output_dir, subdir_name):
    # Create the subdirectory under the output directory if it doesn't exist
    sub_dir_path = os.path.join(output_dir, subdir_name)
    if not os.path.exists(sub_dir_path):
        os.makedirs(sub_dir_path)

    # Iterate through all files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            # Move JSON files to the subdirectory under the output directory
            src_json = os.path.join(input_dir, file_name)
            dest_json = os.path.join(sub_dir_path, file_name)
            shutil.move(src_json, dest_json)

            # Move corresponding PNG files to the same directory
            png_file_name = os.path.splitext(file_name)[0] + '.png'
            src_png = os.path.join(input_dir, png_file_name)
            dest_png = os.path.join(sub_dir_path, png_file_name)
            if os.path.exists(src_png):
                shutil.move(src_png, dest_png)

print("Starting upscale all")
curated_directory = os.path.join(os.getcwd(), "currated")

for root, dirs, files in os.walk(curated_directory):
    for directory in dirs:
        if "_" in directory and "nsfw" not in directory:
            print("Processing:", directory)
            subdir_path = os.path.join(root, directory)
            print("subdir_path:", subdir_path)
            for file in os.listdir(subdir_path):
                if file.endswith(".json"):
                    json_file_path = os.path.join(subdir_path, file)
                    command = [
                        "python",
                        "generatenpcfromjson.py",
                        "-json",
                        json_file_path
                    ]
                    print(" ".join(command))
                    subprocess.run(command)
                    
                    # Find the corresponding PNG file
                    png_file_path = os.path.splitext(json_file_path)[0] + ".png"
                    if os.path.exists(png_file_path):
                        os.remove(png_file_path)
                    if os.path.exists(json_file_path):
                        os.remove(json_file_path)
            # Move files after processing all files in the directory
            input_directory = 'highres'
            sub_directory = directory
            move_files(input_directory, input_directory, sub_directory)
