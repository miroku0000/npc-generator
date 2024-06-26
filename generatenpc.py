import os
import random
import argparse
import glob
import shutil
import random
import os
import glob
import re

import os

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



def write_prompt_to_text_files(directory, prompt):
    # Search for all .png files in the specified directory
    png_files = glob.glob(os.path.join(directory, '*.png'))
    for png_file in png_files:
        # Generate the new filename by adding "_prompt.txt" to the original file name
        base_name = os.path.basename(png_file)  # Get the base name of the file
        new_filename = os.path.splitext(base_name)[0] + "_prompt.txt"  # Remove .png extension and add "_prompt.txt"
        new_filepath = os.path.join(directory, new_filename)  # Create the full path for the new file
        # Write the prompt to the new text file
        with open(new_filepath, 'w') as text_file:
            text_file.write(prompt) 
        print(f"Prompt written to {new_filepath}")

def create_output_directory(directory="output"):
    # Define the directory path
    # Check if the directory already exists
    if not os.path.exists(directory):
        # Create the directory if it doesn't exist
        os.makedirs(directory)
        print(f"Directory '{directory}' was created.")
    else:
        print(f"Directory '{directory}' already exists.")

def write_to_file(file_path, text):
    """
    Opens a text file and writes the specified text to it.
    
    :param file_path: The path to the file.
    :param text: The text to write to the file.
    """
    with open(file_path, 'w') as file:
        file.write(text)

def movefiles(source_directory="output/",destination_directory="output/default", pattern="*.png"):
    """
    Moves all files of a given pattern to another directory.
    
    :param source_directory: The path to directory containing the files you want to move.
    :param destination_directory: The directory to move the files to
    """
    # Create the destination directory if it does not exist
    if not os.path.exists(destination_directory):
    	os.makedirs(destination_directory)
    todo_files = glob.glob(os.path.join(source_directory, pattern))
    for file_path in todo_files:
	    destination_path = os.path.join(destination_directory, os.path.basename(file_path))
	    shutil.move(file_path, destination_path)

def column(s,n):
	"""
	Given a string s  with | as a separater, return the nth field
	For example is s= foo|bar, column(s,0) returns foo and column(s,1) returns bar
	:param s: a string containing | separated fields
	:param n: the number of the column you want returned starting at 0
	"""
	return s.split("|")[n]

def r(filename, default="", folder="npcfiles",):
	"""
	Reads a text file an retuns a random line from it.

	:param filename: The name of a text file.
	"""
	try:
		with open(folder + "/" + filename, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			if lines:
				return random.choice(lines).strip()
			else:
				return "File is empty."
	except FileNotFoundError:
		return default

def generatenpc(npcrace="", npcclass="", npcgender=""):
	"""
    Generates a random npc.

    :param npcrace: string containing a race you want or the empty string for it to be randomly chosen.
    :param npcclass: string containing a class you want or the empty string for it to be randomly chosen.
    :param npcgender: string containing a gender you want or the empty string for it to be randomly chosen.
    
    """
	randomgender = r("npcgender.txt")
	if not npcgender or 'random' in npcgender:
		npcgender = column(randomgender,0)
	randommouth = r("npcmouths.txt")
	mouth_a_an = column(randommouth,1)
	mouth = column(randommouth,0)
	randomclothescolors=r("npcclothescolors.txt")
	topcolor = column(randomclothescolors,0)
	leggingscolor = column(randomclothescolors,1)
	shoescolor = column(randomclothescolors,2)

	if not npcclass or 'random' in npcclass:
		npcclass = r("npcclass.txt")
	if not npcrace or 'random' in npcrace:
		therace  = r("npcrace.txt","human")
	else:
		therace = npcrace
	theclass = npcclass.lower()
	theclass = r(theclass+".txt",theclass) + " "
	therace = r(therace.lower() + ".txt", therace.lower()) 
	theclass = theclass + r(npcclass +"weapon.txt","") + " "
	theclass = theclass + r(npcclass+"activities.txt","") 
 	
	desc = r("npcheight.txt") + " " 
	desc = desc + r("npcattractiveness.txt") + " " 
	desc = desc + npcgender + " " 
	desc = desc + therace + " " 
	desc = desc + theclass + " with " 
	desc = desc + r("npceyedescription.txt") + " " 
	desc = desc + r("npceyeolor.txt") + " eyes"  
	desc = desc + ", " + mouth_a_an + " " +  mouth + " mouth, "
	desc = desc + "a " + r("npcnose.txt") + " nose, and "
	desc = desc + r("npchairadjective.txt") + " "
	desc = desc + r("npchaircolor.txt") +" hair "
	desc = desc + "wearing a " + r("npcwaistcoatfit.txt") + " " +  topcolor + " " + r("npcwaistcoat.txt") + " "+ r("npctops.txt")+", "
	desc = desc + leggingscolor + " " + r("leggings.txt") + " leggings and " 
	desc = desc + shoescolor + " " + r("npcshoes.txt")
	npc={}
	if "female" in npcgender:
		desc = desc.replace("their","her")
	else:
		if "male" in npcgender:
			desc = desc.replace("their","his")
	# Replace 2 or more spaces with a single space
	npc["description"] = re.sub(r'\s+', ' ', desc)
	npc["description"] = npc["description"].replace(",","")
	npc["race"] = npcrace
	npc["class"] = npcclass
	npc["gender"] = npcgender
	return npc

def createPicture(desc,steps=16, width=512, height=512, seed=""):
	"""
    Generates a picture given a description. It will be in the output directory

    :param desc: string containing adescription to give the LLM for picture generation
    :param seed: Optionally, providing the seed will get you a known result.    
    """
	cmd='python main.py ' + '"' + desc+ '"' + " --steps " + str(steps) + " --width " +str(width) + " --height " +  str(height)
	#cmd='venv\\Scripts\\activate venv && python main.py ' + '"' + desc+ '"' + " --steps " + str(steps) + " --width " +str(width) + " --height " +  str(height)
	if seed:
		print("using seed " +str(seed))
		cmd = cmd + " --seed " + str(seed)
	os.system(cmd) 
parser=argparse.ArgumentParser(description="sample argument parser")
parser.add_argument("--npcrace", choices=['human','elf','dwarf','halfling','gnome','orc','tabaxi','tiefling', 'random'], default='random')
parser.add_argument("--npcclass", default='random')
parser.add_argument("--npcgender", default='random', choices=['male','female','random'])
parser.add_argument("--seed")
parser.add_argument("--folder")
parser.add_argument("--imagesperscenario",type=int, default = 4)
parser.add_argument("--scenarios", type=int, default = 4)
parser.add_argument("--width", type=int, default=512)
parser.add_argument("--height", type=int, default=512)
parser.add_argument("--steps", type=int, default=16)


args=parser.parse_args()


remove_empty_subdirs("output")
create_output_directory("output")
create_output_directory("output/misc")
folder="output/misc/"
movefiles("output/",folder, "*.png")
movefiles("output/",folder, "*.json")

# Randomly generate a prompt 4 times, or however many you specify in the scenarios parameter
# So, each time it will generate unique NPC characteristics
# randomly chosen if you do not specify them  	
for i in range(args.scenarios):
	print("Generating scenario =" + str(i+1) + " of " + str(args.scenarios) + " scenarios") 
	npc = generatenpc(args.npcrace, args.npcclass , args.npcgender)
	desc = npc['description']
	npcrace = npc['race']
	npcclass = npc['class'].lower()	
	npcgender= npc['gender']	
	prompt=r("npcprompts.txt") + " " + desc
	#write_to_file( os.path.join(output,prompt_' + npcgender +"_" + npcrace +"_" + npcclass+"_" + str(random.randint(10000000, 99999999))+".txt", prompt))
	print(prompt)
	# The following will create <imagesperscenario> images for each prompt
	for j in range(args.imagesperscenario):
		print("generating image " + str(j+1) + " of " + str(args.imagesperscenario) + " for scenario " + str(i+1))
		#createPicture(desc,args.args.seed)
		createPicture(desc, args.steps, args.width, args.height)
	if args.folder:
		folder=os.path.join("output", args.folder)
		#folder="output\\" + args.folder
	else:
		folder=os.path.join("output",npcgender+ "_" + npcrace + "_" + npcclass)  
		#folder="output\\" + npcgender+ "_" + npcrace + "_" + npcclass  
	#write_prompt_to_text_files("output/", prompt)
	movefiles("output",folder, "*.png")
	movefiles("output",folder, "*.json")
	
