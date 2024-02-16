import os
import random
import argparse
import glob
import shutil
import random

def create_output_directory():
    # Define the directory path
    directory = "output"
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

def r(filename, folder="npcfiles"):
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
		return f"File '{filename}' not found."

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
		npcrace = npcrace = r("npcrace.txt")
	desc = r("npcheight.txt") + " " 
	desc = desc + r("npcattractiveness.txt") + " " 
	desc = desc + npcgender + " " 
	desc = desc + npcrace + " " 
	desc = desc + npcclass + "  with " 
	desc = desc + r("npceyedescription.txt") + " " 
	desc = desc + r("npceyeolor.txt") + " eyes"  
	desc = desc + ", " + mouth_a_an + " " +  mouth + "  mouth, "
	desc = desc + " a " + r("npcnose.txt") + " nose, and "
	desc = desc + r("npchairadjective.txt") + " "
	desc = desc + r("npchaircolor.txt") +" hair "
	desc = desc + "wearing a " + r("npcwaistcoatfit.txt") + " " +  topcolor + " " + r("npcwaistcoat.txt") +" waistcoat, "
	desc = desc + leggingscolor + " " + r("leggings.txt") + " leggings and " 
	desc = desc + shoescolor + " " + r("npcshoes.txt")
	npc={}
	npc["description"] = desc
	npc["race"] = npcrace
	npc["class"] = npcclass
	npc["gender"] = npcgender
	return npc

def createPicture(desc, seed):
	"""
    Generates a picture given a description. It will be in the output directory

    :param desc: string containing adescription to give the LLM for picture generation
    :param seed: Optionally, providing the seed will get you a known result.    
    """
	cmd='venv\\Scripts\\activate venv && python main.py ' + '"' + desc+ '"' + ' --steps 16 --width 512 --height 512'
	if seed:
		print("using seed " +str(seed))
		cmd = cmd + " --seed " + str(seed)
	os.system(cmd) 


parser=argparse.ArgumentParser(description="sample argument parser")
parser.add_argument("--npcrace", choices=['human','elf','dwarf','halfing','gnome','orc','random'], default='random')
parser.add_argument("--npcclass", default='random', choices=['druid','bard','wizard','barbarian','rogue','sorcerer','warlock','cleric','fighter','shopkeep','bartender','whore','innkeeper','random'])
parser.add_argument("--npcgender", default='random', choices=['male','female','random'])
parser.add_argument("--seed")
parser.add_argument("--folder")
parser.add_argument("--imagesperscenario",type=int, default = 4)
parser.add_argument("--scenarios", type=int, default = 4)

args=parser.parse_args()

create_output_directory()

# Randomly generate a prompt 4 times, or however many you specify in the scenarios parameter
# So, each time it will generate unique NPC characteristics
# randomly chosen if you do not specify them  	
for i in range(args.scenarios):
	npc = generatenpc(args.npcrace, args.npcclass , args.npcgender)
	desc = npc['description']
	npcrace = npc['race']
	npcclass = npc['class']
	npcgender= npc['gender']	
	prompt=r("npcprompts.txt") + " " + desc
	write_to_file('output\\prompt_' + npcgender +"_" + npcrace +"_" + npcclass+"_" + str(random.randint(10000000, 99999999))+".txt", prompt)
	print(prompt)
	# The following will create <imagesperscenario> images for each prompt
	for i in range(args.imagesperscenario):
		createPicture(desc,args.seed)
	if args.folder:
		folder="output\\" + args.folder
	else:
		folder="output\\" + npcgender+ "_" + npcrace + "_" + npcclass  
	movefiles("output/",folder, "*.png")
	movefiles("output/",folder, "*.txt")
	





