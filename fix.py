#!/usr/local/bin/python3

import os

def replace_string_in_file(file_path, search_string, replace_string):
    try:
        # Read in the file with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(search_string, replace_string)

        # Write the file out again
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(filedata)
    except UnicodeDecodeError:
        print(f"Skipping file (not a text file or encoding issue): {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

def search_and_replace_in_directory(directory, search_string, replace_string):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                replace_string_in_file(file_path, search_string, replace_string)

# Define the search and replace strings
search_string = "if self.safety_checker is None"
replace_string = "if True"

# Replace string in all Python files starting from the current directory
search_and_replace_in_directory('.', search_string, replace_string)

# Execute the compileall command
os.system("python -m compileall .")
