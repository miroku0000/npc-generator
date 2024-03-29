import os
import subprocess
import time
import shutil

import os

def count_total_files(subdir, root_directories):
    total_files = 0
    for directory in root_directories:
        subdir_path = os.path.join(directory, subdir)
        if os.path.exists(subdir_path) and os.path.isdir(subdir_path) and "_" in subdir:
            total_files += len([file for file in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, file))])
    return total_files

def identify_subdir_with_least_files(npclibrary_dir, root_directories):
    min_total_files = float('inf')
    min_total_subdir = None
    for subdir in os.listdir(npclibrary_dir):
        if os.path.isdir(os.path.join(npclibrary_dir, subdir)) and "_" in subdir:
            total_files = count_total_files(subdir, root_directories)
            if total_files < min_total_files:
                min_total_files = total_files
                min_total_subdir = subdir
    return min_total_subdir

# Top-level directories
root_directories = ["currated", "output", "highres", "npclibrary/npcs"]

# Directory containing subdirectories to analyze
npclibrary_dir = "npclibrary/npcs"

    

if __name__ == "__main__":
    root_directory = "npclibrary/npcs"  # Change this to your desired root directory
    output_directory = "output"
    search_pattern = "_"
    
    while True:
        start_time = time.time()
        # Identify the subdirectory with the least total number of files
        result_directory = identify_subdir_with_least_files(npclibrary_dir, root_directories)
        print("Subdirectory with the least total number of files:", result_directory)

        if result_directory:
            combined_directory = os.path.join(output_directory, result_directory[len("npclibrary/npcs/"):])
            
            gender = result_directory.split("_")[0]
            race = result_directory.split("_")[1]
            job = result_directory.split("_")[2]
            print("Need more images of |" + gender + "| |" + race + "| |" + job + "|")

            # Constructing the command with the calculated values
            command = f'venv\\Scripts\\activate venv && python generatenpc.py --npcgender {gender} --npcrace {race} --npcclass "{job}" --imagesperscenario 1 --scenarios 20 --steps 16 --width 256 --height 256'

            # Measuring the time before executing the command
            command_start_time = time.time()

            # Executing the command
            subprocess.run(command, shell=True)

            # Measuring the time after executing the command
            command_end_time = time.time()

            # Calculating the duration for the command
            command_duration = command_end_time - command_start_time
            print(f"Time taken for command: {command_duration} seconds")

            print("Running qa")
            command = f'..\\venv\\Scripts\\activate venv && python qa.py'
            current_directory = os.getcwd()
            print(current_directory)
            subprocess.run(command, shell=True, cwd=os.path.join(current_directory, "moondream"))
                    
            # Executing the command
            subprocess.run(command, shell=True)
         

        else:
            print("No directories found containing pattern '{}'.".format(search_pattern))

        end_time = time.time()
        duration = end_time - start_time
        print(f"Total time taken: {duration} seconds")
        # Sleep for some time before repeating
        #time.sleep(1)  # Adjust the time interval as needed
