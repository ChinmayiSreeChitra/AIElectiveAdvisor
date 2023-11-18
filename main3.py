import pandas as pd
import streamlit as st
import spacy
import openai

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Set up the OpenAI API key (replace with your actual API key)
api_key = ""
openai.api_key = api_key

if 'selected_course_for_description' not in st.session_state:
    st.session_state['selected_course_for_description'] = None

# Check if 'courses_for_comparison' exists in st.session_state, and initialize it if not
if 'courses_for_comparison' not in st.session_state:
    st.session_state['courses_for_comparison'] = []

# Now you can safely access st.session_state['courses_for_comparison']

# Define the list of prefixes
prefixes = ["ACCT", "AFAM", "AGNG", "AMST", "ANTH", "ARAB", "ART", "ARTE", "ASAM", "ASTR", "BIOL", "BUAD", "CAS",
            "CEDU", "CHEM", "CHIC", "CHIN", "CNSM", "COMD", "COMM", "COUN", "CPLT", "CPSC", "CRJU", "CTVA", "DANC",
            "ECON", "EDAD", "EDD", "EDEL", "EDSC", "EGCE", "EGEC", "EGGN", "EGME", "EGMT", "ENED", "ENGL", "ENST",
            "ESE", "ESM", "ETHN", "FIN", "FREN", "GEOG", "GEOL", "GRMN", "HCOM", "HIST", "HONR", "HSS", "HUSR", "IDT",
            "ISDS", "ITAL", "JAPN", "KNES", "KORE", "LBST", "LING", "LTAM", "MAED", "MATH", "MGMT", "MKTG", "MLNG",
            "MLSC", "MSW", "MUS", "MUSE", "NURS", "PERS", "PHIL", "PHYS", "PORT", "POSC", "PSYC", "PUBH", "READ",
            "RLST", "SCED", "SOCI", "SPAN", "SPED", "TESL", "THTR", "VIET", "WGST"]

# Load the Excel file just once into the session state to avoid reloading it on every rerun
if 'excel_data' not in st.session_state:
    st.session_state['excel_data'] = pd.read_excel('output_course_data.xlsx')

def get_classes_for_prefix(prefix):
    # Filter the DataFrame for rows containing the prefix
    df_filtered = st.session_state['excel_data'][st.session_state['excel_data']['Course Name'].str.startswith(prefix)]
    return df_filtered

st.title('AI ELECTIVE ADVISOR')

# Form for prefix selection
with st.form('prefix_form'):
    selected_prefix = st.selectbox('Select your prefix', prefixes)
    submitted = st.form_submit_button('Submit')

if submitted:
    # Filter the DataFrame for the selected prefix
    st.session_state['selected_classes'] = get_classes_for_prefix(selected_prefix)
    # Indicate that the "Select Classes Taken" button should be shown
    st.session_state['show_taken_button'] = True

# Display the list of classes using expanders
if 'selected_classes' in st.session_state and not st.session_state['selected_classes'].empty:
    for index, row in st.session_state['selected_classes'].iterrows():
        with st.expander(f"{row['Course Name']}"):
            st.markdown(f"""
            <div style="background-color: #f2f2f2; border-left: 5px solid #4CAF50; padding: 10px;">
                <h4 style="color: #5f2c82;">{row['Course Name']}</h4>
                <p style="margin: 0;"><strong>Course Number:</strong> {row['Course Number']}</p>
                <p style="margin-bottom: 10px;">{row['Description']}</p>
            </div>
            """, unsafe_allow_html=True)

# Button to trigger sidebar for selecting classes taken
if st.session_state.get('show_taken_button', False):
    if st.button('Select Classes Taken'):
        # Toggle the sidebar state
        st.session_state['open_sidebar'] = True

# If the sidebar is signaled to open, display the sidebar content
if st.session_state.get('open_sidebar', False):
    with st.sidebar:
        st.title("Selected Courses")
        if 'selected_classes' in st.session_state:
            course_names = st.session_state['selected_classes']['Course Name'].tolist()
            selected_courses = st.multiselect("Select the courses you have taken:", course_names)
            # When the user submits the selected courses, save it
            if st.button('Submit Selected Courses'):
                st.session_state['taken_courses'] = selected_courses
                if 'taken_courses' in st.session_state and st.session_state['taken_courses']:
                    # Filter out the taken courses
                    not_taken_courses = st.session_state['selected_classes'][
                        ~st.session_state['selected_classes']['Course Name'].isin(st.session_state['taken_courses'])
                    ]
                    # Display the courses not taken yet
                    st.write("Courses you have not taken yet:")
                    for course_name in not_taken_courses['Course Name']:
                        st.text(course_name)
                st.session_state['open_sidebar'] = True  # Close the sidebar

# Logic to display the course description in the sidebar
if st.session_state.get('open_sidebar', False):
    with st.sidebar:
        st.title("PreRequisites for the course you want to take")
        # Dropdown to select a course for viewing its description
        selected_course = st.selectbox("Select a course to see its description:",
                                       st.session_state['selected_classes']['Course Name'].tolist(),
                                       key='select_course_for_desc')
        # Button to submit the selected course and view description
        if st.button('Show Description'):
            # Find the course description
            full_description = st.session_state['selected_classes'].loc[
                st.session_state['selected_classes']['Course Name'] == selected_course, 'Description'].iloc[0]
            # Extract the part of the description starting from "Prerequisite"
            prerequisite_index = full_description.find("Prerequisite")
            if prerequisite_index != -1:
                # If the word "Prerequisite" is found, show the description from this point
                course_description = full_description[prerequisite_index:]
            else:
                # If the word "Prerequisite" is not found, show the full description
                course_description = "No prerequisite information found."
            st.write(course_description)
            # Keep the sidebar open for further actions
            st.session_state['open_sidebar_for_description'] = True

# New section for comparing courses using spaCy, ChatGPT, and BERT
if st.session_state.get('show_taken_button', False):
    st.title("Compare the Courses")

    # Create a list of course names based on the selected prefix
    if 'selected_classes' in st.session_state:
        course_names = st.session_state['selected_classes']['Course Name'].tolist()

    # Display checkboxes for each course
    selected_courses_for_comparison = st.multiselect(
        "Select courses to compare:", course_names, help="Select courses to compare."
    )

    if st.button('Submit Selected Courses for Comparison'):
        st.session_state['courses_for_comparison'] = selected_courses_for_comparison
        if 'courses_for_comparison' in st.session_state and st.session_state['courses_for_comparison']:
            # Show a message indicating that the user has selected courses for comparison
            st.success("Selected courses for comparison: {}".format(", ".join(selected_courses_for_comparison)))

            # Function to generate detailed recommendations for course descriptions using spaCy
            def generate_detailed_recommendations_spacy(course_descriptions):
                recommendations = {}
                for course_name, description in course_descriptions.items():
                    doc = nlp(description)
                    relevant_info = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "DATE"]
                    recommendations[course_name] = relevant_info
                return recommendations

            # Generate and display detailed reasons for course recommendations using spaCy
            selected_course_descriptions = {
                course: st.session_state['selected_classes'].loc[
                    st.session_state['selected_classes']['Course Name'] == course, 'Description'
                ].iloc[0]
                for course in st.session_state['courses_for_comparison']
            }

            recommendations_spacy = generate_detailed_recommendations_spacy(selected_course_descriptions)

            st.subheader("Recommendations using spaCy:")
            # Display the detailed reasons for course recommendations using spaCy
            for course, course_recommendations in recommendations_spacy.items():
                st.subheader(course)
                st.write("Detailed Reasons for Recommendation (spaCy):")
                if course_recommendations:
                    for info in course_recommendations:
                        st.write(f"- {info}")
                else:
                    st.write("No specific details found for this course (spaCy).")

            # Function to generate recommendations using ChatGPT
            def generate_recommendations_with_chatgpt(description):
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Generate recommendations for a course description: {description}\n\nRecommendations:",
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                return response.choices[0].text.strip()

            # Function to generate detailed recommendations for course descriptions using ChatGPT
            def generate_detailed_recommendations_chatgpt(course_descriptions):
                recommendations = {}
                for course_name, description in course_descriptions.items():
                    recommendations[course_name] = generate_recommendations_with_chatgpt(description)
                return recommendations

            # Generate and display detailed reasons for course recommendations using ChatGPT
            recommendations_chatgpt = generate_detailed_recommendations_chatgpt(selected_course_descriptions)

            st.subheader("Recommendations using ChatGPT:")
            # Display the detailed reasons for course recommendations using ChatGPT
            for course, course_recommendation in recommendations_chatgpt.items():
                st.subheader(course)
                st.write("Detailed Reasons for Recommendation (ChatGPT):")
                st.write(course_recommendation)

