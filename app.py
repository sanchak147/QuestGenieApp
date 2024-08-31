import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize your language model
llm = OpenAI(openai_api_key=openai_api_key)

# Initialize session state for progress tracking
if 'questions_attempted' not in st.session_state:
    st.session_state.questions_attempted = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'page' not in st.session_state:
    st.session_state.page = "QuestGenie"  # Default page

# Define a function to generate questions
def generate_question(topic, difficulty, question_type=None):
    if question_type:
        prompt_template = f"Generate a {difficulty} level {question_type} question on the topic of {topic}."
    else:
        prompt_template = f"Generate a {difficulty} level technical question (coding question if possible) on the topic of {topic}."
    
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    question = chain.run(prompt_text=prompt_template)
    return question

# Define a function to generate a hint
def generate_hint(question):
    prompt_template = f"Provide a hint for the following question: '{question}'. Make the hint informative but not give away the entire answer."
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    hint = chain.run(prompt_text=prompt_template)
    return hint

# Define a function to provide feedback
def get_feedback(answer, question):
    normalized_answer = answer.strip().lower()
    if normalized_answer in ["don't know", "no", "-", "n/a", "none", "idk"]:
        prompt_template = f"User doesn't know the answer to the question: '{question}'. Respond with encouragement, explain that it's okay not to know, and provide the correct answer along with some tips on how to learn this topic."
    else:
        prompt_template = f"Provide precise and professional feedback on the following answer: '{answer}' to the question: '{question}'. If the answer is wrong, tell it directly. Highlight areas for improvement in 50 words, if there is scope provide the correct code."
    
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    feedback = chain.run(prompt_text=prompt_template)
    
    # Update progress tracking
    st.session_state.questions_attempted += 1
    if "correct" in feedback.lower():
        st.session_state.correct_answers += 1
    
    return feedback

def generate_code(question):
    prompt_template = f"Write an optimal code solution in Python for the following problem: '{question}'. Provide the code with comments explaining each step."
    prompt = PromptTemplate(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    optimal_code = chain.run(prompt_text=prompt_template)
    return optimal_code

# Streamlit UI Setup
st.set_page_config(page_title="QuestGenie 🧞")

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
    .stButton > button:hover {
        background-color: #ff4d4d;
        color: black;
    }
    .stTextArea > label > div {
        display: flex;
        align-items: center;
    }
    .stTextArea > div > textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
        resize: vertical;  /* Allow the textarea to grow vertically */
        min-height: 100px;  /* Minimum height for the textarea */
        max-height: 400px;  /* Maximum height for the textarea */
        overflow: auto;  /* Allow scrolling if content exceeds max height */
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Styling with HTML and CSS
st.sidebar.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #2C3E50;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content .stButton > button {
        background-color: #3498DB;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .sidebar .sidebar-content .stButton > button:hover {
        background-color: #2980B9;
    }
    .sidebar .sidebar-content .stTextInput > div > input,
    .sidebar .sidebar-content .stSelectbox > div {
        border-radius: 5px;
        border: 1px solid #3498DB;
        padding: 10px;
    }
    .sidebar .sidebar-content .centered-button {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for hint button and CodeGuru
with st.sidebar:
    st.markdown('<h2 style="color: white;">Options</h2>', unsafe_allow_html=True)
    
    if st.button("💡 Show Hint"):
        if 'question' not in st.session_state:
            st.warning("Please generate a question first before requesting a hint.")
        else:
            with st.spinner('Generating Hint....'):
                hint = generate_hint(st.session_state.question)
                st.session_state.hint = hint
                st.success('Hint Generated !')
    
    if st.button("🧑‍💻 Generate Code with Codeguru"):
        if 'question' not in st.session_state:
            st.warning("Please generate a question first before requesting code.")
        else:
            with st.spinner('Guru is preparing Guru Bachan....'):
                optimal_code = generate_code(st.session_state.question)
                st.session_state.optimal_code = optimal_code
                st.success('Code Generated !')
    
    # Navigation between pages
    if st.session_state.page == "QuestGenie":
        go_to_codeguru = st.button("Go to CodeGuru 🧑‍💻")
    else:
        back_to_questgenie = st.button("Back to QuestGenie 🧞")

# Handle navigation button actions
if 'go_to_codeguru' in locals() and go_to_codeguru:
    st.session_state.page = "CodeGuru"
if 'back_to_questgenie' in locals() and back_to_questgenie:
    st.session_state.page = "QuestGenie"

# Conditional title and content display based on the page
if st.session_state.page == "QuestGenie":
    st.title("QuestGenie 🧞")
    st.markdown('''Your Q&A Feedback Buddy: Enter a topic 📖, choose difficulty🤔, get questions, and receive personalized feedback💡''')
    
    # QuestGenie page content here
    topic = st.text_input("Enter the subject topic:")
    topics_with_types = {
        "Python": ["Syntax", "Real-World Problems using Codex", "Core"],
        "Machine Learning": ["Theory", "Coding", "Real-World Applications using Code"],
        "Statistics": ['Theory','Coding in Python','Real-World Problems Using Code']
    }

    if topic in topics_with_types:
        question_type = st.selectbox("Select the type of question:", topics_with_types[topic])
    else:
        question_type = None

    difficulty = st.selectbox("Select the difficulty level:", ["Easy", "Medium", "Hard", "Very Hard", "Expert"])

    if st.button("Generate Question"):
        if topic:
            question = generate_question(topic, difficulty)
            st.session_state.question = question
            st.session_state.hint = None
            st.session_state.answer = None
            st.session_state.feedback = None
            st.session_state.optimal_code = None

        else:
            st.error("Please enter a subject topic.")

    if 'question' in st.session_state:
        st.write("Generated Question:", st.session_state.question)

        if 'hint' in st.session_state and st.session_state.hint:
            with st.expander("Hint"):
                st.write(st.session_state.hint)
        if 'optimal_code' in st.session_state and st.session_state.optimal_code:
            with st.expander('Guru Bachan'):
                st.code(st.session_state.optimal_code, language='python')

    if 'question' in st.session_state:
        answer = st.text_area("Enter your answer:")

        if st.button("Get Feedback"):
            if answer:
                feedback = get_feedback(answer, st.session_state.question)
                st.session_state.answer = answer
                st.session_state.feedback = feedback
                st.write("Feedback:", feedback)
            else:
                st.error("Please enter your answer.")

    if st.session_state.questions_attempted > 0:
        progress = st.session_state.correct_answers / st.session_state.questions_attempted
        st.write(f"Progress: {st.session_state.correct_answers}/{st.session_state.questions_attempted} correct answers")
        st.progress(progress)

else:  # CodeGuru Page
    st.title("CodeGuru 🧑‍💻")
    st.markdown("Enter your problem statement below and select the programming language to generate the optimal code solution.")

    code_input = st.text_area("Enter your prompt:")
    language = st.selectbox("Select the programming language:", ["Python", "Java", "C++", "JavaScript"])
    
    if st.button("Generate Code"):
        if code_input:
            with st.spinner('Generating optimal code...'):
                # You can modify the generate_code function to accept the language if needed
                optimal_code = generate_code(code_input)
                st.session_state.optimal_code = optimal_code
                st.success('Code Generated!')
                st.code(optimal_code, language=language.lower())
        else:
            st.error("Please enter a prompt.")


# Footer with app version and copyright
st.markdown(f"""
    <div class="footer-text">
        <p style="text-align: center;">QuestGenie Version 1.1.2 | &copy; 2024 sanchak147</p>
    </div>
""", unsafe_allow_html=True)
