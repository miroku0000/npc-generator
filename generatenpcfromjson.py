import os
import random
import argparse
import glob
import shutil
import json

def remove_empty_subdirs(dir_path):
    # Walk through all subdirectories in the given directory
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for dir_name in dirs:
            # Construct the full path to the directory
            full_dir_path = os.path.join(root, dir_name)
            # Check if the directory is empty
            if not os.listdir(full_dir_path):
                # Remove the empty directory
                os.rmdir(full_dir_path)
                print(f"Removed empty directory: {full_dir_path}")

def createPicture(desc, steps=16, width=512, height=512, seed=""):
    """
    Generates a picture given a description. It will be in the output directory

    :param desc: string containing a description to give the LLM for picture generation
    :param seed: Optionally, providing the seed will get you a known result.    
    """
    cmd = f'python createhighres.py "{desc}" --steps {steps} --width {width} --height {height}'
    if seed:
        print(f"Using seed {seed}")
        cmd += f" --seed {seed}"
    os.system(cmd)

def generate_npc_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    desc = data.get('prompt', '')
    width = 1024 #data.get('width', 512)
    height = 1024 #data.get('height', 512)
    steps = 32 #data.get('steps', 16)
    seed = data.get('seed', '')

    createPicture(desc, steps, width, height, seed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate NPC images.")
    parser.add_argument("-json", type=str, help="Path to JSON file containing NPC parameters.")
    args = parser.parse_args()

    if args.json:
        generate_npc_from_json(args.json)
    else:
        print("Please provide a JSON file containing NPC parameters using the -json option.")
