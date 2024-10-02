import streamlit as st
import logging
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Gemini API key
api_key = "AIzaSyDIU2KmhMTybjDvsIx6rwDYoicAzHGV3RA"
genai.configure(api_key=api_key)

# Streamlit Components
st.title("AlgoMentor 🧠🔍")
st.markdown('<style>h1{color: orange; text-align: center; margin-bottom: 0px;}</style>', unsafe_allow_html=True)
st.subheader('Socratic Learning Assistant for Sorting Algorithms 📚🤖')
st.markdown('<style>h3{text-align: center; margin-top: 0;}</style>', unsafe_allow_html=True)

# Streamlit Sidebar for User Input and Profile
with st.sidebar:
    # Add LinkedIn and GitHub links
    linkedin_url = "https://www.linkedin.com/in/malaiarasu-g-raj-38b695252/"
    github_url = "https://github.com/MalaiarasuGRaj"

    st.markdown(f"""
    Developed By:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color='orange'>**Malaiarasu GRaj**</font><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LinkedIn]({linkedin_url}) | [GitHub]({github_url})
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Input preferences section
    st.header("Input your preferences")

    # Initialize session state for topic and familiarity if not already present
    if 'topic' not in st.session_state:
        st.session_state.topic = "Sorting Algorithms"
    if 'familiarity' not in st.session_state:
        st.session_state.familiarity = "Select..."

    # Topic input field (default to Sorting Algorithms)
    st.session_state.topic = st.text_input("Topic/Subject:", value=st.session_state.topic, placeholder="Enter a topic...")

    # Familiarity level dropdown
    familiarity_options = ["Select...", "Beginner", "Intermediate", "Advanced"]
    st.session_state.familiarity = st.selectbox(
        "Familiarity Level:",
        familiarity_options,
        index=familiarity_options.index(st.session_state.familiarity)
    )

    # Generate content button
    generate_button = st.button("Generate Content")

# Function to generate content using Gemini API
def generate_content(topic, familiarity, user_question=None):
    # If there's no user question, return a welcome message
    if not user_question:
        return f"Welcome! Let's start exploring the topic of **{topic}**. Ask me any questions you have."

    # Otherwise, generate an AI response based on the user's question
    prompt = f"As a Socratic tutor, guide a {familiarity} level learner through the topic of '{topic}'. The learner asked: '{user_question}'."
    try:
        # Call Gemini API to generate content
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate content: {e}")
        return None

# Initialize session state for conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Handle content generation and conversation flow
if generate_button and st.session_state.topic and st.session_state.familiarity != "Select...":
    # Only add the initial message once
    if len(st.session_state.conversation) == 0:
        initial_message = generate_content(st.session_state.topic, st.session_state.familiarity)
        st.session_state.conversation.append(("AI", initial_message))

# Display the entire conversation (message history)
for speaker, message in st.session_state.conversation:
    if speaker == "AI":
        st.markdown(f"**AI**: {message}")
    else:
        st.markdown(f"**You**: {message}")

# Chat input box for user questions (only visible if the topic and familiarity are filled)
if st.session_state.topic and st.session_state.familiarity != "Select...":
    user_input = st.text_input("Ask your question:")

    # If the user submits a question, get AI's response and update the conversation
    if st.button("Submit"):
        if user_input:
            st.session_state.conversation.append(("You", user_input))
            ai_response = generate_content(st.session_state.topic, st.session_state.familiarity, user_input)
            st.session_state.conversation.append(("AI", ai_response))

            # Clear the user input in session state
            st.session_state['user_input'] = ""  # Ensure session state is reset properly

            # Display the updated conversation
            for speaker, message in st.session_state.conversation:
                if speaker == "AI":
                    st.markdown(f"**AI**: {message}")
                else:
                    st.markdown(f"**You**: {message}")

else:
    # Show error if inputs are missing or invalid
    if generate_button and (not st.session_state.topic or st.session_state.familiarity == "Select..."):
        st.error("Please enter the topic and select a familiarity level to proceed.")
