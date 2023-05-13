#Integrating OpenAI with Streamlit: With Example  Source Code Explainer 4/29/2023 --Author Ajit Dash
import streamlit as st
import openai
import os  

if 'history' not in st.session_state:
            st.session_state.history = []

if 'output_history' not in st.session_state:
            st.session_state.output_history = []


#Option # 1 - Using Streamlit secrets
#This is the easiest way using Streamlit secrets : 
#How to create steps

#A.Create a folder within your director where you have the code name as “.streamlit “

#B.Create a file name as “ secrets.toml” under the folder “.streamlit “

#C. Assign the key in the “ secrets.toml”
#Path = '363e5eaaaaaabbbbbccccc'
#Flow will look like this : projectfolder\streamlit\.streamlit (NOTE MAKE SURE ".streamlit" THIS NEED TO BE IN THE PROJECT FOLDER) 
#When you call the key within your code use this :  openai.api_key = st.secrets['path']


# os.getenv("OPENAI_API_KEY") = st.secrets['OPENAI_API_KEY'] 



# option#2 : Environmental variable 

#using option#2 env variable 
# openai.api_key = st.secrets['OPENAI_API_KEY']

# st.write("Secret Key", st.secrets["OPENAI_API_KEY"])

# st.write(
#     "Has environment variables been set:",
#     os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
# )

# openai.api_key_path = 'OPENAI_API_KEY.env'

# option#3 hard code the key 
#openai.api_key = 'xxxxxxxxxxxxxxxxxxxx'

#CHECK THE BLOG HOW TO HIDE YOUR KEY 
#"more details you will find in the blog:  "

# Define Streamlit app layout
st.title("Prompted Chat")

                          

def set_prefix():
    if prefix_context == "Master Clinician Explaining to Junior Clinician":
        prefix = """Respond as a master clinician explaining step by step to a junior clinician who is not quite at your level yet. 
                Ensure you apply the latest available evidence-based guidelines 
                and high-impact medical literature when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """
    elif prefix_context == "Senior Researcher Explaining to Junior Researcher":
        prefix = """Respond as a senior experienced researcher explaining step by step to a junior researcher who is not quite at your level yet. 
                Ensure you apply the latest available scientific research
                from high-impact scientific and medical literature when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """
    elif prefix_context == "Hematologist for your Clotting Questions":
        prefix = """Respond as an experienced attending physician board certified hematologist explaining step by step to a junior physician who is not at your level yet. 
                Ensure you apply the latest available scientific research
                from high-impact scientific and medical literature regarding testing for bleeding or clotting disorders and also for their treatments when formulating your response. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """      
    elif prefix_context == "Infectious Diseases Physician for your Complex ID Questions":
        prefix = """Respond as an experienced attending physician board certified in infectious diseases explaining step by step to a junior physician who is not at your level yet. 
                Ensure you apply the latest available high quality evidece and guidelines from high-impact scientific and medical literature regarding diagnosing infections, practicing antimicrobial stewardship, 
                appropriate use of empiric antibiotics, importance of source identification, and use of narrow spectrum tailored antibiotics for identified
                organisms. Then, perform a final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """                 
    elif prefix_context == "Medication Questions from Prescribers":
        prefix = """Respond as a senior experienced pharmacist with extensive knowledge of pharmacology who advises physicians on the best medications to use 
                for clinical situations and how to dose them correctly. Ensure you apply the latest available prescribing
                guidance from high quality prescribing guides like MicroMedex or ePocrates when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response."""
    elif prefix_context == "Patient Safety Expert Assesses Risks":
        prefix = """As a patient safety expert, you are asked to assess the risks of a particular clinical situation. Idenitify all failure modes, 
                consequences, and how they might be avoided."""
    elif prefix_context == "Just a Chat with ChatGPT":
        prefix = """Respond as a human having a conversation with ChatGPT."""
    else:
        prefix = ""
    return prefix

prefix_context = st.radio("Pick your setting:", 
                          ("Master Clinician Explaining to Junior Clinician", "Senior Researcher Explaining to Junior Researcher", 
                           "Hematologist for your Clotting Questions", "Infectious Diseases Physician for your Complex ID Questions", "Medication Questions from Prescribers", 
                           "Patient Safety Expert Assesses Risks", "Just a Chat with ChatGPT", "Your Option to Set a Context for the Conversation"))

prefix = set_prefix()
if prefix_context == "Your Option to Set a Context for the Conversation":
    prefix = st.sidebar.text_area("Enter your custom context..., eg., respond like a pirate.", height=100)


def clear_text():
    st.session_state["my_ask"] = ""



# Define function to explain code using OpenAI Codex
@st.cache_data
def answer_using_prefix(prefix, my_ask):
    history_context = "Use these preceding questions to help set context: \n" + "\n".join(st.session_state.history) + "now, for the current question: \n"
    completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
    model = 'gpt-3.5-turbo',
    messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': prefix + history_context + my_ask}
    ],
    temperature = temperature,   
    )
    # st.write(history_context + prefix + my_ask)
    return completion # Change how you access the message content
    
    
    
    
    # model_engine = "gpt-3.5-turbo" # Change to the desired OpenAI model
    # prompt = f"{prefix} + \n\n{my_ask}"
    # response = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     prompt=prompt,
    #     max_tokens=tokens,
    #     n=1,
    #     stop=None,
    #     temperature=temperature,
    # )
    # return response.choices[0].text

# Temperature and token slider
temperature = st.sidebar.slider(
    "Temperature - focused/conservative to creative/risky",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1
)
# tokens = st.sidebar.slider(
#     "Tokens",
#     min_value=64,
#     max_value=4096,
#     value=2048,
#     step=64
# )
# Define Streamlit app behavior
my_ask = st.text_area('Ask away!', height=100, key="my_ask")


# if len(history) > 10:
#     del history[0]
    

# prefix = set_prefix()
if st.button("Enter"):

    st.session_state.history.append(my_ask)
    output_text = answer_using_prefix(prefix, my_ask)

    # st.write("Answer", output_text)
    
    # st.write(st.session_state.history)
    st.write(f'Me: {my_ask}')
    st.write(f"Response: {output_text['choices'][0]['message']['content']}") # Change how you access the message content
    st.session_state.output_history.append((output_text['choices'][0]['message']['content']))


if st.sidebar.button("Clear Memory of Current Conversation"):
    st.session_state.history = []
    st.write("History Cleared)")

st.button("Clear Input Field", on_click=clear_text)

if st.button("Show prompt details"):
    st.write(f'Current Prompt: {prefix} + {my_ask} \n\n')



st.sidebar.write("Current Input History", st.session_state.history)
st.sidebar.write("Current Output History", st.session_state.output_history)
# st.write(f'My Current Question: {my_ask}')

