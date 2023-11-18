import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Read coid numbers from the input Excel file
input_df = pd.read_excel("/Users/channapragadachitra/Desktop/cpsc362/coid_numbers1.xlsx")

# List of coid numbers from the input DataFrame
coid_numbers = input_df["coid Numbers"].tolist()

# Create an empty list to store course data
course_data = []

# Iterate through the list of coid numbers
for coid in coid_numbers:
    # Generate the URL for each coid number
    url = f"https://catalog.fullerton.edu/preview_course_nopop.php?catoid=80&coid={coid}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Flag to indicate if the specific sentence has been found
    found_sentence = False

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <p> tags
        p_tags = soup.find_all('p')

        # Initialize variables to store course name and number
        course_name = None
        course_number = None

        # Extract and print the text from each <p> tag after finding the specific sentence
        for p in p_tags:
            text = p.get_text(strip=True)
            if 'CSUF is committed to ensuring equal accessibility to our users.Let us know about any accessibility problems you encounter using this website.' in text:
                found_sentence = True
                continue  # Skip the specific sentence's paragraph
            if found_sentence:
                # Split the text at a number in parentheses and add a two-line gap
                parts = re.split(r'(\(\d+\))', text)
                for part in parts:
                    part = part.strip()  # Remove leading and trailing whitespace
                    if part:
                        if re.match(r'\(\d+\)', part):  # If the part is a number in parentheses, it's a course number
                            course_number = part
                        else:
                            if course_name is None:
                                course_name = part
                            else:
                                course_data.append([course_name, course_number, part])
                                course_name = None
                                course_number = None

    else:
        print(f"Failed to retrieve the page for coid {coid}. Status code:", response.status_code)

# Create a DataFrame from the course data
output_df = pd.DataFrame(course_data, columns=["Course Name", "Course Number", "Description"])

# Export the DataFrame to an Excel file
output_df.to_excel("output_course_data.xlsx", index=False)

print("Data has been stored in 'output_course_data.xlsx'")
