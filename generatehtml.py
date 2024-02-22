import os
from collections import defaultdict

# Define the directory for reading the data and for writing the HTML files
data_directory = "output"
output_directory = "output"

# Ensure the output directory exists, create if it does not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize nested defaultdict structures for storing image paths
images_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
races_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

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
                    races_metadata[race][occupation][gender].append(relative_path)

# Function to generate HTML content for each category (occupation or race)
# Adjusted generate_html function for Flexbox layout
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
            gap: 10px; /* Adjust gap between images */
        }}
        .image {{
            flex: 1 0 10%; /* Adjust this to change how many images per row, 20% for 5 images per row */
            box-sizing: border-box;
        }}
        img {{
            width: 100%;
            height: auto;
            max-width: 200px; /* Adjust max width of images */
            max-height: 200px; /* Adjust max height of images */
        }}
        .hidden {{
            display: none;
        }}
    </style>
    <script>
        function filterImages(filterType, value) {{
            let images = document.querySelectorAll('div.image');
            images.forEach((image) => {{
                if (filterType === 'all') {{
                    image.classList.remove('hidden');
                }} else {{
                    if (image.classList.contains(value)) {{
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
    <h1>{title}</h1>
    <button onclick="filterImages('all', 'all')">Show All</button>
    <button onclick="filterImages('gender', 'male')">Male</button>
    <button onclick="filterImages('gender', 'female')">Female</button>
    <div class="container">
    """

    # Generate image divs with links inside the container
    for category in data:
        for gender in data[category]:
            for image_relative_path in data[category][gender]:
                html_content += f"""
                <div class='image {category} {gender}'>
                    <a href='{image_relative_path}' target='_blank'>
                        <img src='{image_relative_path}' alt='{category} {gender}' class='{gender}'>
                    </a>
                    <br>{category.capitalize()}, {gender.capitalize()}
                </div>
                """

    html_content += """
    </div>
    </body>
    </html>
    """

    return html_content



# Create index.html content
index_content = "<html><head><title>Index Page</title></head><body><h1>Index Page</h1><h2>Occupations</h2><ul>"

# Generate HTML files for each occupation and race, update index.html content
for occupation in images_metadata:
    filename = f"occupation_{occupation.replace(' ', '_').lower()}.html"
    with open(os.path.join(output_directory, filename), "w") as file:
        file.write(generate_html(occupation, images_metadata[occupation], "occupation"))
    index_content += f"<li><a href='{filename}'>{occupation}</a></li>"

index_content += "</ul><h2>Races</h2><ul>"

for race in races_metadata:
    filename = f"race_{race.replace(' ', '_').lower()}.html"
    with open(os.path.join(output_directory, filename), "w") as file:
        file.write(generate_html(race, races_metadata[race], "race"))
    index_content += f"<li><a href='{filename}'>{race}</a></li>"

index_content += "</ul></body></html>"

# Write the index.html file to the output directory
with open(os.path.join(output_directory, "index.html"), "w") as file:
    file.write(index_content)

print("HTML files and index.html have been generated in the 'output' directory.")
