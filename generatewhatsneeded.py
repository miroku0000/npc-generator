import os
import subprocess
import time

def count_files(directory):
    """
    Count the number of files in a directory, including all subdirectories.
    """
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

def find_directory_with_least_files(root_directory, search_pattern):
    """
    Find the subdirectory with the least number of files containing the search pattern.
    """
    subdirectories = [d for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d)) and search_pattern in d]
    min_total_files = float('inf')
    min_total_files_directory = None

    for subdir in subdirectories:
        subdir_path = os.path.join(root_directory, subdir)

        # Calculate the combined count for the subdirectory
        subdir_combined_count = count_files(subdir_path)
        output_combined_count = count_files(os.path.join("output", subdir)) if os.path.exists(os.path.join("output", subdir)) else 0
        total_count = subdir_combined_count + output_combined_count

        if total_count < min_total_files:
            min_total_files = total_count
            min_total_files_directory = subdir_path

    return min_total_files_directory

if __name__ == "__main__":
    root_directory = "npclibrary/npcs"  # Change this to your desired root directory
    output_directory = "output"
    search_pattern = "_"
    
    while True:
        result_directory = find_directory_with_least_files(root_directory, search_pattern)
        
        if result_directory:
            combined_directory = os.path.join(output_directory, result_directory[len("npclibrary/npcs/"):])

            npcs_combined_count = count_files(result_directory)
            output_combined_count = count_files(combined_directory) if os.path.exists(combined_directory) else 0
            total_combined_count = npcs_combined_count + output_combined_count
            
            print(result_directory)
            print(f"NPCs combined count: {npcs_combined_count}")
            print(f"Output combined count: {output_combined_count}")
            print(f"Total combined count: {total_combined_count}")

            s = result_directory[len("npclibrary/npcs/"):]
            gender = s.split("_")[0]
            race = s.split("_")[1]
            job = s.split("_")[2]
            print("Need more images of |" + gender + "| |" + race + "| |" + job + "|")

            # Constructing the command with the calculated values
            command = f'venv\\Scripts\\activate venv && python generatenpc.py --npcgender {gender} --npcrace {race} --npcclass "{job}" --imagesperscenario 1 --scenarios 20 --steps 32 --width 1024 --height 1024'

            # Executing the command
            subprocess.run(command, shell=True)

        else:
            print("No directories found containing pattern '{}'.".format(search_pattern))

        # Sleep for some time before repeating
        #time.sleep(1)  # Adjust the time interval as needed
