import pandas as pd
import streamlit as st
import spacy
from claude import claude_client
from claude import claude_wrapper

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

career_data = pd.read_csv('/Users/channapragadachitra/Desktop/cpsc362/career_options.csv')

if 'selected_course_for_description' not in st.session_state:
    st.session_state['selected_course_for_description'] = None

if 'excel_data' in st.session_state:
    st.session_state['excel_data']['Undergraduate Keyword'] = st.session_state['excel_data']['Description'].str.contains('undergraduate', case=False)
    st.session_state['excel_data']['Graduate Keyword'] = st.session_state['excel_data']['Description'].str.contains('Graduate-level', case=False)



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
    st.session_state['excel_data'] = pd.read_excel('/Users/channapragadachitra/Desktop/cpsc362/output_course_data.xlsx')

def get_classes_for_prefix(prefix):
    # Filter the DataFrame for rows containing the prefix
    df_filtered = st.session_state['excel_data'][st.session_state['excel_data']['Course Name'].str.startswith(prefix)]
    return df_filtered


# Function to get career options for a selected prefix
def get_career_options(selected_prefix):
    careers = []
    prefix_row = career_data[career_data['Prefix'] == selected_prefix]
    if not prefix_row.empty:
        careers.extend(prefix_row[['Career 1', 'Career 2', 'Career 3']].values[0])
    return careers


# Add some CSS styling for the title
st.markdown(
    """
    <style>
    .title-text {
        font-size: 36px;
        color: #5f2c82;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title-text">AI ELECTIVE ADVISOR</p>', unsafe_allow_html=True)


# Form for prefix selection
with st.form('prefix_form'):
    selected_prefix = st.selectbox('Select your prefix', prefixes)
    submitted = st.form_submit_button('Submit')

if submitted:
    # Filter the DataFrame for the selected prefix
    st.session_state['selected_classes'] = get_classes_for_prefix(selected_prefix)
    # Indicate that the "Select Classes Taken" button should be shown
    st.session_state['show_taken_button'] = True
    # Add a task to display career options in the sidebar
    st.session_state['display_careers'] = True

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
    if st.button('different operations for selecting classes'):
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


# New section for comparing courses
if st.session_state.get('show_taken_button', False):

    st.markdown(
        """
        <style>
        .title-text {
            font-size: 36px;
            color: #5f2c82;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="title-text">Compare the Courses</p>', unsafe_allow_html=True)

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

# Function to generate detailed recommendations for course recommendations
def generate_detailed_recommendations(course_descriptions):
    recommendations = {}
    for course_name, description in course_descriptions.items():
        # Implement your logic to generate detailed recommendations here
        # You can use NLP techniques like named entity recognition (NER) and sentence analysis
        # Replace the following code with your own recommendation generation logic
        doc = nlp(description)
        relevant_info = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "DATE"]
        recommendations[course_name] = relevant_info
    return recommendations

# Logic to generate and display detailed reasons for course recommendations
if 'courses_for_comparison' in st.session_state and st.session_state['courses_for_comparison']:
    selected_course_descriptions = {
        course: st.session_state['selected_classes'].loc[
            st.session_state['selected_classes']['Course Name'] == course, 'Description'
        ].iloc[0]
        for course in st.session_state['courses_for_comparison']
    }

    recommendations = generate_detailed_recommendations(selected_course_descriptions)

    # Display the detailed reasons for course recommendations
    for course, course_recommendations in recommendations.items():
        st.subheader(course)
        st.write("Detailed Reasons for Recommendation:")
        if course_recommendations:
            for info in course_recommendations:
                st.write(f"- {info}")
        else:
            st.write("No specific details found for this course.")



# New section for filtering classes by standing
if 'selected_classes' in st.session_state and not st.session_state['selected_classes'].empty:

    st.markdown(
        """
        <style>
        .title-text {
            font-size: 36px;
            color: #5f2c82;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="title-text">Filter Classes by Standing</p>', unsafe_allow_html=True)

    with st.form("standing_form"):
        standing_option = st.selectbox("Select Class Standing:", ["Undergraduate", "Graduate"])
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if standing_option == "Undergraduate":
            # Filter for undergraduate classes
            undergraduate_classes = st.session_state['selected_classes'][st.session_state['selected_classes']['Undergraduate Keyword']]
            st.write("Undergraduate Classes:")
            for index, row in undergraduate_classes.iterrows():
                st.markdown(f"""
                <div style="background-color: #f2f2f2; border-left: 5px solid #4CAF50; padding: 10px;">
                    <h4 style="color: #5f2c82;">{row['Course Name']}</h4>
                    <p style="margin: 0;"><strong>Course Number:</strong> {row['Course Number']}</p>
                    <p style="margin-bottom: 10px;">{row['Description']}</p>
                </div>
                """, unsafe_allow_html=True)

        elif standing_option == "Graduate":
            # Filter for graduate classes based on the "Graduate Keyword" column
            graduate_classes = st.session_state['selected_classes'][st.session_state['selected_classes']['Graduate Keyword']]
            st.write("Graduate Classes:")
            for index, row in graduate_classes.iterrows():
                st.markdown(f"""
                <div style="background-color: #f2f2f2; border-left: 5px solid #4CAF50; padding: 10px;">
                    <h4 style="color: #5f2c82;">{row['Course Name']}</h4>
                    <p style="margin: 0;"><strong>Course Number:</strong> {row['Course Number']}</p>
                    <p style="margin-bottom: 10px;">{row['Description']}</p>
                </div>
                """, unsafe_allow_html=True)

if st.session_state.get('display_careers', False):
    st.markdown(
        """
        <style>
        .title-text {
            font-size: 24px;
            color: #5f2c82;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="title-text">Careers Related to Selected Prefix</p>', unsafe_allow_html=True)

    selected_prefix_careers = get_career_options(selected_prefix)
    if selected_prefix_careers:
        st.write(f"Careers related to '{selected_prefix}':")
        for career in selected_prefix_careers:
            st.write(f"- {career}")
    else:
        st.write(f"No career information found for '{selected_prefix}'.")





# Define your SESSION_KEY for claude.ai (replace with your actual key)
SESSION_KEY = "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"

# Initialize the claude client and wrapper
client = claude_client.ClaudeClient(SESSION_KEY)
organizations = client.get_organizations()
claude_obj = claude_wrapper.ClaudeWrapper(client, organization_uuid=organizations[0]['uuid'])

# ... (your existing code)

# Section for interacting with the "claude.ai" agent
st.markdown('<p class="title-text">Interact with the Claude.ai Agent</p>', unsafe_allow_html=True)

# Text input for user to enter a prompt for the "claude.ai" agent
claude_prompt = st.text_input("Enter a prompt for the Claude.ai Agent:")

# Button to generate a response from the "claude.ai" agent
if st.button("Generate Claude.ai Response"):
    # Start a new conversation
    new_conversation_data = claude_obj.start_new_conversation("New Conversation", claude_prompt)
    conversation_uuid = new_conversation_data['uuid']

    # Get the response from the initial message
    initial_response = new_conversation_data['response']

    # Extract and format the relevant information from the initial response
    completion = initial_response.get("completion", "")
    model = initial_response.get("model", "")

    # Display the formatted response
    st.write("Initial Claude.ai Response:")
    st.write("Model Used: " + model)
    st.write("Response:")
    st.write(completion)

    # Send additional messages (if needed)
    response = claude_obj.send_message("How are you doing today!")

    # Check if the response is not None before iterating over it
    if response is not None:
        st.write("Additional Claude.ai Responses:")
        for msg in response:
            msg_completion = msg.get("completion", "")
            st.write(msg_completion)
