import pandas as pd

# Subset of the provided dictionary of career options
career_options = {
    "ACCT": ["Accountant", "Financial Analyst", "Auditor"],
    "AFAM": ["Historian of African American Studies", "Professor of African Studies", "Cultural Anthropologist"],
    "AGNG": ["Gerontologist", "Senior Services Manager", "Aging Policy Analyst"],
    "AMST": ["American Studies Professor", "Cultural Critic", "Public Policy Analyst"],
    "ANTH": ["Cultural Anthropologist", "Forensic Anthropologist", "Museum Curator"],
    "ARAB": ["Arabic Translator", "Middle Eastern Studies Professor", "Foreign Affairs Analyst"],
    "ART": ["Fine Artist", "Art Historian", "Art Gallery Director"],
    "ARTE": ["Art Educator", "Museum Education Director", "Art Therapist"],
    "ASAM": ["Asian American Studies Professor", "Community Advocate", "Ethnic Studies Researcher"],
    "ASTR": ["Astronomer", "Astrophysicist", "Space Mission Analyst"],
    "BIOL": ["Biologist", "Ecologist", "Genetic Counselor"],
    "BUAD": ["Business Administrator", "Operations Manager", "Entrepreneur"],
    "CAS": ["Communication Arts Specialist", "Media Coordinator", "Public Relations Specialist"],
    "CEDU": ["Curriculum Developer", "Educational Consultant", "Academic Advisor"],
    "CHEM": ["Chemist", "Pharmaceutical Researcher", "Toxicologist"],
    "CHIC": ["Chicano Studies Professor", "Community Outreach Coordinator", "Cultural Historian"],
    "CHIN": ["Chinese Language Instructor", "Translator", "International Business Consultant"],
    "CNSM": ["Consumer Sciences Specialist", "Family Financial Advisor", "Nutrition Manager"],
    "COMD": ["Speech-Language Pathologist", "Audiologist", "Communication Disorders Researcher"],
    "COMM": ["Communications Officer", "Broadcast Journalist", "Media Planner"],
    "COUN": ["Counselor", "Mental Health Therapist", "School Counselor"],
    "CPLT": ["Comparative Literature Professor", "Literary Critic", "Editor"],
    "CPSC": ["Computer Scientist", "Software Developer", "Information Security Analyst"],
    "CRJU": ["Criminal Justice Official", "Forensic Analyst", "Probation Officer"],
    "CTVA": ["Cinematographer", "Film Director", "Television Producer"],
    "DANC": ["Professional Dancer", "Choreographer", "Dance Instructor"],
    "ECON": ["Economist", "Financial Consultant", "Market Analyst"],
    "EDAD": ["School Administrator", "Educational Policy Developer", "Dean"],
    "EDD": ["Doctor of Education", "Educational Researcher", "Chief Academic Officer"],
    "EDEL": ["Elementary School Teacher", "Educational Program Developer", "Reading Specialist"],
    "EDSC": ["Secondary School Teacher", "Educational Consultant", "Curriculum Specialist"],
    "EGCE": ["Civil Engineer", "Urban Planner", "Environmental Consultant"],
    "EGEC": ["Electrical Engineer", "Control Systems Engineer", "Communications Engineer"],
    "EGGN": ["General Engineer", "Project Manager", "Systems Analyst"],
    "EGME": ["Mechanical Engineer", "Design Engineer", "Thermal Systems Engineer"],
    "EGMT": ["Management Engineer", "Industrial Engineer", "Quality Control Analyst"],
    "ENED": ["Engineering Educator", "STEM Program Coordinator", "Technical Trainer"],
    "ENGL": ["English Teacher", "Author", "Editor"],
    "ENST": ["Environmental Scientist", "Conservationist", "Sustainability Coordinator"],
    "ESE": ["Environmental Systems Engineer", "Renewable Energy Consultant", "Waste Management Specialist"],
    "ESM": ["Emergency Services Manager", "Disaster Response Coordinator", "Public Safety Director"],
    "ETHN": ["Ethnic Studies Professor", "Diversity Officer", "Human Rights Advocate"],
    "FIN": ["Financial Analyst", "Investment Banker", "Personal Financial Advisor"],
    "FREN": ["French Teacher", "Translator", "International Relations Specialist"],
    "GEOG": ["Geographer", "Urban Planner", "GIS Specialist"],
    "GEOL": ["Geologist", "Environmental Consultant", "Paleontologist"],
    "GRMN": ["German Language Instructor", "Translator", "Cultural Attaché"],
    "HCOM": ["Health Communications Specialist", "Patient Advocate", "Healthcare Marketing Coordinator"],
    "HIST": ["Historian", "Archivist", "Museum Curator"],
    "HONR": ["Research Scholar", "Academic Advisor", "Program Coordinator"],
    "HSS": ["Health and Social Services Manager", "Public Health Administrator", "Community Health Coordinator"],
    "HUSR": ["Human Services Professional", "Case Manager", "Social Work Administrator"],
    "IDT": ["Instructional Designer", "Educational Technologist", "Training Developer"],
    "ISDS": ["Information Systems Analyst", "Data Scientist", "IT Project Manager"],
    "ITAL": ["Italian Teacher", "Cultural Ambassador", "Travel Consultant"],
    "JAPN": ["Japanese Translator", "Cultural Liaison", "Foreign Language Educator"],
    "KNES": ["Kinesiologist", "Athletic Trainer", "Physical Education Teacher"],
    "KORE": ["Korean Language Instructor", "Translator", "Cultural Advisor"],
    "LBST": ["Labor Studies Professor", "Union Organizer", "Labor Relations Specialist"],
    "LING": ["Linguist", "Language Technologist", "Speech Analyst"],
    "LTAM": ["Latin American Studies Scholar", "Diplomat", "International NGO Worker"],
    "MAED": ["Mathematics Educator", "Curriculum Coordinator", "Educational Researcher"],
    "MATH": ["Mathematician", "Data Analyst", "Actuary"],
    "MGMT": ["Manager", "Business Consultant", "Operations Director"],
    "MKTG": ["Marketing Specialist", "Brand Manager", "Market Research Analyst"],
    "MLNG": ["Multilingual Educator", "Language Program Coordinator", "Diplomatic Services Officer"],
    "MLSC": ["Military Science Instructor", "Security Analyst", "Defense Strategist"],
    "MSW": ["Master of Social Work", "Clinical Social Worker", "Social Policy Analyst"],
    "MUS": ["Musician", "Music Teacher", "Music Director"],
    "MUSE": ["Museum Educator", "Exhibit Designer", "Cultural Preservationist"],
    "NURS": ["Registered Nurse", "Nurse Practitioner", "Clinical Nurse Specialist"],
    "PERS": ["Persian Language Instructor", "Middle Eastern Studies Expert", "Cultural Advisor"],
    "PHIL": ["Philosopher", "Ethics Consultant", "Critical Thinker"],
    "PHYS": ["Physicist", "Lab Technician", "Research Scientist"],
    "PORT": ["Portuguese Language Teacher", "Translator", "Cultural Affairs Coordinator"],
    "POSC": ["Political Scientist", "Public Policy Analyst", "Legislative Assistant"],
    "PSYC": ["Psychologist", "Mental Health Counselor", "Behavioral Scientist"],
    "PUBH": ["Public Health Professional", "Epidemiologist", "Health Policy Analyst"],
    "READ": ["Reading Specialist", "Literacy Coach", "Educational Consultant"],
    "RLST": ["Religious Studies Professor", "Chaplain", "Ethics Officer"],
    "SCED": ["Science Educator", "Research Scientist", "Environmental Educator"],
    "SOCI": ["Sociologist", "Demographer", "Community Developer"],
    "SPAN": ["Spanish Teacher", "Interpreter", "International Business Consultant"],
    "SPED": ["Special Education Teacher", "Learning Disabilities Specialist", "Behavioral Interventionist"],
    "TESL": ["TESOL Instructor", "English as a Second Language Teacher", "Language Program Director"],
    "THTR": ["Theater Director", "Actor", "Drama Teacher"],
    "VIET": ["Vietnamese Language Teacher", "Cultural Ambassador", "Immigration Consultant"],
    "WGST": ["Women's and Gender Studies Professor", "Diversity Coordinator", "Nonprofit Advocate"]

}

# Convert the dictionary into a DataFrame
career_options_df = pd.DataFrame.from_dict(career_options, orient='index', columns=['Career 1', 'Career 2', 'Career 3'])

# Reset the index to turn the dictionary keys into a column of the DataFrame
career_options_df.reset_index(inplace=True)
career_options_df.rename(columns={'index': 'Prefix'}, inplace=True)

# Define the path for the CSV file
csv_file_path = 'career_options.csv'

# Save the DataFrame to a CSV file
career_options_df.to_csv(csv_file_path, index=False)

# This will save the file 'career_options_subset.csv' in the current working directory.
