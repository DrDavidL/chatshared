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
st.title("Prefixed Chat")
prefix_context = st.radio("Pick your persona:", ("Master Clinician", "Medical Scientist", "Medications", "Patient Safety Expert"))

def set_prefix():
    if prefix_context == "Master Clinician":
        prefix = """Take on the role of a master clinician explaining step by step to an expert clinician who is not quite at your level yet. 
                Ensure you apply the latest available evidence-based guidelines 
                and high-impact medical literature to answer the question posed by the less expert physician. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your answer to the following question: """
    elif prefix_context == "Medical Scientist":
        prefix = """According to the latest scientific 
                and high-impact medical literature, and by performing a 
                final step by step review of the response as a senior research scientist, 
                please answer the following:"""
                
    elif prefix_context == "Medications":
        prefix = """According to the latest scientific 
                and high-impact medical literature, and by performing a 
                final step by step review of the response as a senior research scientist, 
                please answer the following:"""
    elif prefix_context == "Patient Safety Expert":
        prefix = """According to the latest patient safety and quality improvement guidelines  
                and high-impact medical literature, and by performing a 
                final step by step review of the response as a patient safety expert, 
                please answer the following:"""
    else:
        prefix = ""
    return prefix






# Define function to explain code using OpenAI Codex
def answer_using_prefix(prefix, my_ask):
    completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
    model = 'gpt-3.5-turbo',
    messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': prefix + my_ask}
    ],
    temperature = temperature,   
    )
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
    "Temperature",
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
my_ask = st.text_input('Ask away!', '')
prefix = set_prefix()
if st.button("Explain"):
    output_text = answer_using_prefix(prefix, my_ask)
    # st.write("Answer", output_text)
    
    
    st.write(output_text['choices'][0]['message']['content']) # Change how you access the message content