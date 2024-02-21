import os
from collections import defaultdict

# Define the directory for reading the data and for writing the HTML files
data_directory = "output"
output_directory = "output"

# Ensure the output directory exists, create if it does not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize a nested defaultdict structure for storing image paths
images_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

# Traverse through each folder in the data directory
for root, dirs, files in os.walk(data_directory):
    for dir_name in dirs:
        parts = dir_name.split("_")
        if len(parts) == 3:
            gender, race, occupation = parts
            current_dir_path = os.path.join(root, dir_name)
            
            # Process each PNG file in the directory
            for file_name in os.listdir(current_dir_path):
                if file_name.endswith(".png"):
                    # Save the relative path from the output directory to the image
                    relative_path = os.path.join(dir_name, file_name)
                    images_metadata[occupation][race][gender].append(relative_path)

# Function to generate HTML content for each occupation
def generate_html(occupation, data):
    races = list(data.keys())
    html_content = f"""
    <html>
    <head>
    <title>{occupation}</title>
    <style>
        img {{ width: 200px; height: 200px; }}
        .hidden {{ display: none; }}
    </style>
    <script>
        function filterImages(filterType, value) {{
            let images = document.querySelectorAll('div.image');
            images.forEach((image) => {{
                if (filterType === 'race') {{
                    if (value === 'all' || image.classList.contains(value)) {{
                        image.classList.remove('hidden');
                    }} else {{
                        image.classList.add('hidden');
                    }}
                }} else if (filterType === 'gender') {{
                    if (value === 'all' || image.classList.contains(value)) {{
                        image.classList.remove('hidden');
                    }} else {{
                        image.classList.add('hidden');
                    }}
                }}
            }});
        }}
    </script>
    </head>
    <body>
    <h1>{occupation}</h1>
    <button onclick="filterImages('gender', 'all')">Show All</button>
    <button onclick="filterImages('gender', 'male')">Male</button>
    <button onclick="filterImages('gender', 'female')">Female</button>
    """

    # Buttons for filtering by race
    for race in races:
        html_content += f"<button onclick=\"filterImages('race', '{race}')\">{race.capitalize()}</button>"
    html_content += f"<button onclick=\"filterImages('race', 'all')\">Show All Races</button>"

    # Generate image divs
    for race in data:
        for gender in data[race]:
            for image_relative_path in data[race][gender]:
                html_content += f"<div class='image {race} {gender}'><img src='{image_relative_path}' alt='{race} {gender}'><br>{race.capitalize()}, {gender.capitalize()}</div>"

    html_content += """
    </body>
    </html>
    """

    return html_content

# Create index.html content
index_content = "<html><head><title>Index of Occupations</title></head><body><h1>Index of Occupations</h1><ul>"

# Write HTML files for each occupation to the output directory and update index.html content
for occupation in images_metadata:
    filename = f"{occupation.replace(' ', '_').lower()}.html"
    html_filename = os.path.join(output_directory, filename)
    with open(html_filename, "w") as file:
        file.write(generate_html(occupation, images_metadata[occupation]))
    index_content += f"<li><a href='{filename}'>{occupation}</a></li>"

index_content += "</ul></body></html>"

# Write the index.html file
index_filename = os.path.join(output_directory, "index.html")
with open(index_filename, "w") as file:
    file.write(index_content)

print("HTML files and index.html have been generated in the 'output' directory.")
