import os
import json
from collections import defaultdict

# Define the directory for reading the data and for writing the HTML files
data_directory = "output"
output_directory = "output"

# Ensure the output directory exists, create if it does not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Delete any existing HTML files in the output directory
for file in os.listdir(output_directory):
    if file.endswith(".html"):
        os.remove(os.path.join(output_directory, file))

# Initialize nested defaultdict structures for storing image paths and metadata
images_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
races_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

# Traverse through each folder in the data directory
for root, dirs, files in os.walk(data_directory):
    for dir_name in dirs:
        parts = dir_name.split("_")
        if len(parts) == 3:
            gender, race, occupation = parts
            current_dir_path = os.path.join(root, dir_name)
            
            # Process each PNG file and its corresponding JSON file in the directory
            for file_name in os.listdir(current_dir_path):
                if file_name.endswith(".png"):
                    json_filename = file_name.replace('.png', '.json')
                    json_path = os.path.join(current_dir_path, json_filename)
                    
                    # Read metadata from the JSON file
                    metadata = {}
                    if os.path.exists(json_path):
                        with open(json_path, 'r') as json_file:
                            metadata = json.load(json_file)
                    
                    # Include the image path in the metadata
                    metadata['path'] = os.path.join(dir_name, file_name)
                    metadata["race"]=race
                    metadata["gender"]=gender
                    metadata["occupation"]= occupation
                    images_metadata[occupation][race][gender].append(metadata)
                    races_metadata[race][occupation][gender].append(metadata)

# Function to generate HTML content for each category (occupation or race)
def generate_html(title, data, category_type):
    categories = list(data.keys())
    html_content = f"""
    <html>
    <head>
    <title>{title} Page</title>
    <style>
        .container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: start;
            gap: 10px;
        }}
        .image {{
            flex: 1 0 10%; /* More images per row */
            box-sizing: border-box;
            margin-bottom: 20px; /* Space for details button and additional info */
        }}
        img {{
            width: 100%;
            height: auto;
            max-width: 200px;
            max-height: 200px;
        }}
        .details, .details-button, .additional-info {{
            display: none; /* Initially hide details and button */
            width: 100%;
            text-align: center;
            margin-top: 5px;
        }}
        .details-button, .additional-info {{
            display: block; /* Show the button and additional info */
            cursor: pointer;
        }}
    </style>
    <script>
        let currentGender = '';
        let currentRace = '';

        function filterImages(filterType, value) {{
            if (filterType === 'gender') {{
                currentGender = value;
            }} else if (filterType === 'race') {{
                currentRace = value;
            }}

            let images = document.querySelectorAll('div.image');
            images.forEach((image) => {{
                let genderMatch = !currentGender || image.classList.contains(currentGender);
                let raceMatch = !currentRace || image.classList.contains(currentRace);

                image.style.display = genderMatch && raceMatch ? 'block' : 'none';
            }});
        }}

        function toggleDetails(id) {{
            let details = document.getElementById(id);
            details.style.display = details.style.display === 'block' ? 'none' : 'block';
        }}

        function resetFilters() {{
            currentGender = '';
            currentRace = '';
            filterImages('all', 'all');
        }}
    </script>
    </head>
    <body>
    <h1>{title}</h1>
    <button onclick="resetFilters()">Show All</button>
    <button onclick="filterImages('gender', 'male')">Male</button>
    <button onclick="filterImages('gender', 'female')">Female</button>
    """

    if category_type == "occupation":
        for race in categories:
            html_content += f"<button onclick=\"filterImages('race', '{race}')\">{race.capitalize()}</button>"
        html_content += "<button onclick=\"filterImages('race', 'all')\">Show All Races</button>"

    html_content += "<div class='container'>"
    detail_id = 0  # Unique ID for detail divs

    for category in data:
        for gender in data[category]:
            for metadata in data[category][gender]:
                race=metadata.get("race", "N/A")
                image_path = metadata["path"]
                seed = metadata.get("seed", "N/A")
                prompt = metadata.get("prompt", "N/A")
                model = metadata.get("model", "N/A")
                width = metadata.get("width", "N/A")
                height = metadata.get("height", "N/A")
                steps = metadata.get("steps", "N/A")
                occ=metadata.get("occupation", "N/A")
                additional_info = f"{gender.capitalize()}, {race.capitalize()}" if category_type == "occupation" else f"{gender.capitalize()}, {occ.capitalize()}"

                html_content += f"""
                <div class='image {category} {gender}'>
                    <div class='additional-info'>{additional_info}</div>
                    <a href='{image_path}' target='_blank'>
                        <img src='{image_path}' alt='Image'>
                    </a>
                    <button class='details-button' onclick='toggleDetails("details-{detail_id}")'>Details</button>
                    <div class='details' id='details-{detail_id}'>
                        <p>Seed: {seed}</p>
                        <p>Prompt: {prompt}</p>
                        <p>Model: {model}</p>
                        <p>Width: {width}px</p>
                        <p>Height: {height}px</p>
                        <p>Steps: {steps}</p>
                    </div>
                </div>
                """
                detail_id += 1

    html_content += "</div></body></html>"

    return html_content

# Start generating HTML files for each occupation and race, and compile index.html content
index_content = "<html><head><title>Index Page</title></head><body><h1>Index Page</h1><h2>Occupations</h2><ul>"

for occupation in images_metadata:
    display_name = occupation.replace('_', ' ').title()  # Capitalize the first letter of each word
    filename = f"occupation_{occupation.replace(' ', '_').lower()}.html"
    with open(os.path.join(output_directory, filename), "w") as file:
        file.write(generate_html(occupation, images_metadata[occupation], "occupation"))
    index_content += f"<li><a href='{filename}'>{display_name}</a></li>"

index_content += "</ul><h2>Races</h2><ul>"

for race in races_metadata:
    filename = f"race_{race.replace(' ', '_').lower()}.html"
    with open(os.path.join(output_directory, filename), "w") as file:
        file.write(generate_html(race, races_metadata[race], "race"))
    index_content += f"<li><a href='{filename}'>{race.capitalize()}</a></li>"

index_content += "</ul></body></html>"

# Write the index.html file to the output directory
with open(os.path.join(output_directory, "index.html"), "w") as file:
    file.write(index_content)

print("HTML files and index.html have been generated in the 'output' directory.")
