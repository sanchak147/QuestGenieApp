import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize your language model
llm = OpenAI()

# Define a function to generate questions
def generate_question(topic, difficulty):
    prompt_template = f"Generate a {difficulty} level technical question (coding question if possible) on the topic of {topic}."
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    question = chain.run(prompt_text=prompt_template)
    return question

# Define a function to provide feedback
def get_feedback(answer, question):
    prompt_template = f"Provide precise and professional feedback on the following answer: '{answer}' to the question: '{question}'. Highlight areas for improvement in 50 words."
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    feedback = chain.run(prompt_text=prompt_template)
    return feedback
st.set_page_config(page_title="Question and Answer Feedback")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: gray;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .stButton> button:hover{
    background-color: #ff4d4d;
    color:black;
    }
    .stTextArea > textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("QuestGenie 🧞")
st.markdown('''Your Q&A Feedback Buddy: Enter a topic 📖, choose difficulty🤔, get questions, and receive personalized feedback💡''')

# Text input for topic
topic = st.text_input("Enter the subject topic:")

# Dropdown for difficulty
difficulty = st.selectbox("Select the difficulty level:", ["Easy", "Medium", "Hard",'Very Hard','Expert'])

# Button to generate question
if st.button("Generate Question"):
    if topic:
        question = generate_question(topic, difficulty)
        st.session_state.question = question
        st.session_state.answer = None
        st.session_state.feedback = None
        st.write("Generated Question:", question)
    else:
        st.error("Please enter a subject topic.")

# Text area for answer
if 'question' in st.session_state:
    answer = st.text_area("Enter your answer:")

    # Button to get feedback
    if st.button("Get Feedback"):
        if answer:
            feedback = get_feedback(answer, st.session_state.question)
            st.session_state.answer = answer
            st.session_state.feedback = feedback
            st.write("Feedback:", feedback)
        else:
            st.error("Please enter your answer.")
