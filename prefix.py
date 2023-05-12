#Integrating OpenAI with Streamlit: With Example  Source Code Explainer 4/29/2023 --Author Ajit Dash
import streamlit as st
import openai
import os  


#Option # 1 - Using Streamlit secrets
#This is the easiest way using Streamlit secrets : 
#How to create steps

#A.Create a folder within your director where you have the code name as “.streamlit “

#B.Create a file name as “ secrets.toml” under the folder “.streamlit “

#C. Assign the key in the “ secrets.toml”
#Path = '363e5eaaaaaabbbbbccccc'
#Flow will look like this : projectfolder\streamlit\.streamlit (NOTE MAKE SURE ".streamlit" THIS NEED TO BE IN THE PROJECT FOLDER) 
#When you call the key within your code use this :  openai.api_key = st.secrets['path']


openai.api_key_path = st.secrets['OPENAI_API_KEY'] 



# option#2 : Environmental variable 

#using option#2 env variable 
#openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key_path = 'key.env'

# option#3 hard code the key 
#openai.api_key = 'xxxxxxxxxxxxxxxxxxxx'

#CHECK THE BLOG HOW TO HIDE YOUR KEY 
#"more details you will find in the blog:  "

# Define Streamlit app layout
st.title("Prefixed Chat")
prefix_context = st.selectbox("Select Context", ["Medical Treatments", "Pathophysiology", "Patient Safety"])

def set_prefix():
    if prefix_context == "Medical Treatments":
        prefix = """According to the latest evidence-based guidelines 
                and high-impact medical literature, and by performing a 
                final step by step review of the response as an expert clinician, 
                please answer the following:"""
    elif prefix_context == "Pathophysiology":
        prefix = """According to the latest scientific 
                and high-impact medical literature, and by performing a 
                final step by step review of the response as a senior research scientist, 
                please answer the following:"""
    elif prefix_context == "Patient Safety":
        prefix = """According to the latest patient safety and quality improvement guidelines  
                and high-impact medical literature, and by performing a 
                final step by step review of the response as a patient safety expert, 
                please answer the following:"""
    else:
        prefix = ""
    return prefix


# Define function to explain code using OpenAI Codex
def answer_using_prefix(prefix, my_ask):
    model_engine = "text-davinci-003" # Change to the desired OpenAI model
    prompt = f"{prefix} + \n\n{my_ask}"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0].text

# Temperature and token slider
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1
)
tokens = st.sidebar.slider(
    "Tokens",
    min_value=64,
    max_value=4096,
    value=2048,
    step=64
)
# Define Streamlit app behavior
my_ask = st.text_input('My own question', 'Enter your own question here.')
prefix = set_prefix()
if st.button("Explain"):
    output_text = answer_using_prefix(prefix, my_ask)
    st.text_area("Code Explanation", output_text)