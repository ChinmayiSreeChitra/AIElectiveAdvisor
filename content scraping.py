import requests
from bs4 import BeautifulSoup
import re

# List of coid numbers
coid_numbers = [
    540413, 540423, 540414, 540421, 540415, 540676, 540409, 540407, 540410,
    540408, 540416, 540420, 541020, 540412, 540417, 540411, 540418, 540424,
    541009, 541043, 540419, 541010, 540930, 540422, 540425, 540974, 540701
]

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
                                print(f"Course Name: {course_name}")
                                print(f"Course number: {course_number}")
                                print(f"Description: {part}")
                                print("\n")
                                course_name = None
                                course_number = None

    else:
        print(f"Failed to retrieve the page for coid {coid}. Status code:", response.status_code)
