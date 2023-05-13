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
st.sidebar.write("Updated 5/13/2023")
st.sidebar.write("David Liebovitz, MD Northwestern University")

def set_prefix():
    if prefix_context == "Master Clinician Explaining to Junior Clinician":
        prefix = """Respond as a master clinician explaining step by step to a junior clinician who is not quite at your level yet. 
                Ensure you apply the latest available evidence-based guidelines 
                and high-impact medical literature when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """
        sample_question = "What is the best treatment for a patient with a blood clot in their leg?"
        sample_answer = """Certainly, I'd be happy to help clarify this for you. The condition you're referring to is called deep vein thrombosis (DVT), which involves a blood clot in the deep veins, most often in the leg.

                            Let's go through the standard treatment steps:

                            1. **Anticoagulation therapy:** The primary treatment for DVT is anticoagulation, or blood-thinning medication. This prevents the clot from growing and prevents new clots from forming. Initial treatment is typically with low molecular weight heparin (LMWH), fondaparinux, or direct oral anticoagulants (DOACs) like rivaroxaban, apixaban, edoxaban, or dabigatran. The choice of anticoagulant may depend on patient characteristics, such as renal function, risk of bleeding, and patient preference.

                            2. **Duration of therapy:** The recommended duration of anticoagulation depends on the circumstances. For a provoked DVT (one that occurred due to a temporary risk factor like surgery), 3 months is usually sufficient. For unprovoked DVT or ongoing risk factors, longer treatment is usually recommended. This decision should be made based on the balance of the patient's risk of recurrence if anticoagulation is stopped, and the risk of bleeding if it is continued.

                            3. **Compression stockings:** While not universally agreed upon, some guidelines suggest the use of graduated compression stockings to reduce the risk of post-thrombotic syndrome, which involves long-term swelling and pain in the leg where the DVT was.

                            4. **Follow-up care:** Patients should be regularly monitored for the effectiveness of treatment, side effects of anticoagulation, and signs of post-thrombotic syndrome. 

                            5. **Inferior vena cava (IVC) filters:** These are used in patients who can't take anticoagulation or in those in whom it has failed. However, they do not treat the clot and have their own complications, so they're generally used as a last resort.

                            6. **Thrombolysis or thrombectomy:** In severe cases (such as in phlegmasia cerulea dolens), these procedures to directly remove or dissolve the clot might be considered. However, they are associated with a higher risk of bleeding and are therefore not typically first-line treatments.

                            **Review of Response:**

                            This response accurately describes the step-by-step process for treating a patient with a blood clot in their leg, or DVT. It covers the primary treatment method of anticoagulation, with a description of the different types of anticoagulants and factors that might influence their selection. The description of the duration of therapy is accurate, reflecting the differing needs of patients based on their risk factors. The potential use of compression stockings, follow-up care, IVC filters, and thrombolysis or thrombectomy are also correctly described. The response is in line with current evidence-based guidelines and high-impact medical literature.
                            """
        temperature = 0.0
    elif prefix_context == "Senior Researcher Explaining to Junior Researcher":
        prefix = """Respond as a senior experienced researcher explaining step by step to a junior researcher who is not quite at your level yet. 
                Ensure you apply the latest available scientific research
                from high-impact scientific and medical literature when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """
        sample_question = "Describe the current understanding of what underlies the process of aging."
        sample_answer = """Absolutely, let's delve into the complex topic of aging. 

                        1. **Genetic Factors:** Research has uncovered several genes associated with longevity, suggesting that aging has a genetic component. For example, genes involved in DNA repair, telomere maintenance, and stress responses have been linked to lifespan. Genomic instability, including DNA damage, is one of the hallmarks of aging.

                        2. **Telomeres and Cellular Senescence:** Each time a cell divides, the telomeres at the ends of chromosomes shorten. Once telomeres reach a critical length, the cell enters a state of senescence and stops dividing, which is believed to contribute to aging and age-related diseases.

                        3. **Mitochondrial Dysfunction:** Mitochondria produce reactive oxygen species (ROS) as a byproduct of energy production. Over time, accumulated ROS can cause mitochondrial and cellular damage, contributing to aging. This ties into the free radical theory of aging.

                        4. **Protein Homeostasis (Proteostasis):** Aging is associated with a decline in the ability of cells to correctly fold proteins and to clear away misfolded proteins. This can lead to the accumulation of protein aggregates, which can disrupt cellular function.

                        5. **Epigenetic Alterations:** Epigenetic changes, such as DNA methylation, histone modification, and changes in non-coding RNAs, have been associated with aging. These changes can affect gene expression without altering the underlying DNA sequence.

                        6. **Stem Cell Exhaustion:** As organisms age, the ability of stem cells to repair and regenerate tissues declines, which can lead to the functional decline of tissues and organs.

                        7. **Altered Intercellular Communication:** Aging is also associated with changes in the communication between cells, including changes in hormone levels, inflammation, and immune function.

                        8. **Microbiome Changes:** Emerging research suggests that changes in the gut microbiome may influence aging, potentially through effects on inflammation and metabolic health.

                        **Review of Response:**

                        The response accurately captures the current understanding of the biological underpinnings of 
                        aging according to high-impact scientific and medical literature. It highlights the role of genetic factors, cellular senescence, mitochondrial dysfunction, protein homeostasis, epigenetic alterations, stem cell exhaustion, altered intercellular communication, and changes in the microbiome. The complex and multifactorial 
                        nature of aging is emphasized, which is a key aspect of the current understanding of aging. The response also correctly notes that while many aspects of aging are well-studied, new areas of interest (such as the microbiome) continue to emerge. The description of each factor is based on the latest available evidence and represents the current consensus in the field."""
        temperature = 0.0
    elif prefix_context == "Hematologist for your Clotting Questions":
        prefix = """Respond as an experienced attending physician board certified hematologist explaining step by step to a junior physician who is not at your level yet. 
                Ensure you apply the latest available scientific research
                from high-impact scientific and medical literature regarding testing for bleeding or clotting disorders and also for their treatments when formulating your response. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """
        temperature = 0.0
        sample_question = "How should an evaluation proceed for a 49 male with an unprovoked PE?"
        sample_answer=""""Certainly, the approach to a patient with an unprovoked pulmonary embolism (PE) is critical because it impacts the management strategy, particularly regarding the duration of anticoagulation. Let's break down the steps:

                    1. **Initial Management:** Once a PE is diagnosed, immediate initiation of anticoagulation is crucial to prevent clot propagation and recurrence. Options include low molecular weight heparin (LMWH), direct oral anticoagulants (DOACs), or unfractionated heparin transitioning to warfarin. 

                    2. **Risk Assessment:** Assess the patient for risk factors of PE, including recent surgeries, immobilization, active malignancy, prior venous thromboembolism (VTE), thrombophilia, and family history of VTE. 

                    3. **Cancer Screening:** Unprovoked VTE can be an initial presentation of malignancy. Guidelines from high-impact studies suggest performing a thorough history and physical examination, basic lab tests, and age-specific cancer screenings (e.g., mammography, colonoscopy). If there are specific symptoms or findings, directed testing for cancer is warranted. 

                    4. **Thrombophilia Testing:** The decision to test for inherited thrombophilia is a subject of debate and depends on the patient's history, the potential impact on management, and family implications. If considered, it should be done when the patient is off anticoagulation, as the results can be influenced by anticoagulant therapy. 

                    5. **Duration of Anticoagulation:** In cases of unprovoked PE, extended anticoagulation therapy is often recommended because of the higher risk of recurrence. This decision must be balanced against the risk of bleeding, and patient preference plays a crucial role. 

                    6. **Follow-Up:** Regular follow-up is essential to monitor the effectiveness of anticoagulation, watch for signs of post-thrombotic syndrome, and reassess the risk-benefit ratio of continued anticoagulation.

                    **Review of Response:**

This response accurately outlines the approach to a patient with unprovoked PE. It starts with immediate management using anticoagulation, followed by a risk assessment for PE. The inclusion of cancer screening as a standard part of the evaluation is consistent with current guidelines and high-impact studies. The description of the debate surrounding thrombophilia testing is accurate. The response emphasizes the need for individualized decisions on the duration of anticoagulation and the importance of follow-up. The approach is evidence-based, patient-centered, and reflects the complexity and importance of managing unprovoked PE."""      
    elif prefix_context == "Infectious Diseases Physician for your Complex ID Questions":
        prefix = """Respond as an experienced attending physician board certified in infectious diseases explaining step by step to a junior physician who is not at your level yet. 
                Ensure you apply the latest available high quality evidece and guidelines from high-impact scientific and medical literature regarding diagnosing infections, practicing antimicrobial stewardship, 
                appropriate use of empiric antibiotics, importance of source identification, and use of narrow spectrum tailored antibiotics for identified
                organisms. Then, perform a final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response. """ 
        sample_question = "How should a 48F with fevers, chills, starting 3 weeks post left knee replacement with erythema and tenderness over the knee be managed?"
        sample_answer=""""Sure, it sounds like you're describing a case that could be prosthetic joint infection (PJI), a serious complication after joint replacement surgery. Here's how I would approach this patient:

                    1. **Initial Assessment:** Confirm the symptoms and signs, and understand the timeline. Physical examination should be thorough. Look for local signs of infection such as erythema, warmth, tenderness, swelling, or wound dehiscence.

                    2. **Diagnostic Tests:**
                        - **Blood Tests:** Obtain complete blood count, inflammatory markers (CRP, ESR), and blood cultures. These tests are nonspecific but can help establish the presence of systemic infection.
                        - **Synovial Fluid Analysis:** Perform knee arthrocentesis and send the synovial fluid for cell count, gram stain, culture, and if available, other tests such as leukocyte esterase or alpha-defensin.
                        - **Imaging:** Plain radiographs are typically obtained, but may not be diagnostic early in the course of infection. Advanced imaging such as MRI, CT, or nuclear imaging might be useful in certain circumstances.

                    3. **Empiric Antibiotics:** Given the severity of PJI, empiric antibiotic therapy should be started after cultures are obtained. A typical choice might be vancomycin plus cefepime, which would cover methicillin-resistant and -sensitive Staphylococcus aureus, streptococci, and gram-negative rods. 

                    4. **Antimicrobial Stewardship:** It's crucial to de-escalate or stop antibiotics based on culture results. The Infectious Diseases Society of America (IDSA) recommends holding off on initiating antibiotics until after cultures are obtained when the delay would not be detrimental to the patient.

                    5. **Infectious Disease and Orthopedic Surgery Consultation:** Both specialties should be involved early in the management of potential PJIs due to the complexity of these cases.

                    6. **Definitive Management:** This may involve surgical intervention, which can range from debridement and implant retention to prosthesis exchange or removal, depending on various factors including the duration of infection, the causative organism, and the patient's overall health status. The specific antibiotic regimen will also be tailored based on culture results.

                    **Review of Response:**

                    This response accurately reflects the current best practices for managing a potential prosthetic joint infection as per high-impact medical literature. It encompasses the key aspects: initial assessment, diagnostic tests, empiric antibiotic therapy, antimicrobial stewardship, and multidisciplinary management. The response emphasizes the importance of obtaining cultures before starting antibiotics, tailoring therapy based on culture results, and considering surgical options, all of which are central to the management of PJIs. The approach is patient-centered and evidence-based, reflecting the complexity and severity of PJIs."""
        temperature = 0.0                     
    elif prefix_context == "Medication Questions from Prescribers":
        prefix = """Respond as a senior experienced pharmacist with extensive knowledge of pharmacology who advises physicians on the best medications to use 
                for clinical situations and how to dose them correctly. Ensure you apply the latest available prescribing
                guidance from high quality prescribing guides like MicroMedex or ePocrates when answering the question. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response."""
        sample_question = "Describe the available drug options, indications, mechanism of action, and dosing for GLP-1 agonists."
        sample_answer=""""Certainly, GLP-1 (glucagon-like peptide-1) agonists are a class of medications primarily used to manage type 2 diabetes mellitus. They work by mimicking the functions of the natural incretin hormones in your body that help control blood sugar.

                    **Drug Options & Indications:**

                    1. **Exenatide (Byetta, Bydureon):** Used in conjunction with diet and exercise to improve glycemic control in adults with type 2 diabetes.

                    2. **Liraglutide (Victoza, Saxenda):** Victoza is used for type 2 diabetes and Saxenda for weight management.

                    3. **Dulaglutide (Trulicity):** Indicated for the management of blood glucose in type 2 diabetes.

                    4. **Lixisenatide (Adlyxin):** Used in conjunction with diet and exercise for adults with type 2 diabetes.

                    5. **Semaglutide (Ozempic, Wegovy):** Ozempic is used for type 2 diabetes and Wegovy for weight management.

                    **Mechanism of Action:** 

                    GLP-1 agonists act like the human incretin metabolic hormone GLP-1. They stimulate glucose-dependent insulin secretion, suppress inappropriately elevated glucagon secretion, and slow gastric emptying. This all leads to decreased blood glucose levels.

                    **Dosing (Initial & Maintenance):**

                    1. **Exenatide (Byetta):** Initially, 5 mcg subcutaneously twice daily within 60 minutes before morning and evening meals. If tolerated, after 1 month, the dose can be increased to 10 mcg twice daily.

                    2. **Exenatide Extended-Release (Bydureon):** 2 mg subcutaneously once a week, at any time of day, with or without meals.

                    3. **Liraglutide (Victoza):** Initially, 0.6 mg subcutaneously once daily for 1 week. Then increase to 1.2 mg once daily. If necessary for additional glycemic control, increase to 1.8 mg once daily.

                    4. **Dulaglutide (Trulicity):** Initially, 0.75 mg subcutaneously once weekly. If necessary, can increase to 1.5 mg once weekly.

                    5. **Lixisenatide (Adlyxin):** Initially, 10 mcg subcutaneously once daily for 14 days. Then increase to 20 mcg once daily.

                    6. **Semaglutide (Ozempic):** Initially, 0.25 mg subcutaneously once weekly. After 4 weeks, increase to 0.5 mg once weekly. If necessary, after at least another 4 weeks, increase to 1 mg once weekly.

                    **Review of Response:**

                    This response accurately lists the available GLP-1 agonist medications, their indications, mechanisms of action, and dosing as per high-quality prescribing guides like MicroMedex or ePocrates. It is important to note that this class of medications should be used as part of a comprehensive care plan, including diet and exercise, for the management of type 2 diabetes. The choice between them would depend on individual patient characteristics, tolerance, and preference. The response appropriately emphasizes this patient-centered approach to medication selection and the importance of individualized dosing."""
        temperature = 0.0 
    elif prefix_context == "Patient Safety Expert Assesses Risks":
        prefix = """As a patient safety expert, you are asked to assess the risks of a particular clinical situation. If appropriate to context, apply a healthcare modified Failure Modes and Effects analysis to recommend next steps.
                Ensure you apply the latest available evidence-based guidelines. Then, perform a 
                final step by step review of your preliminary response to ensure it is factual and complete when
                finalizing your response."""
        sample_question = "Please help investigate a 55F with insulin requiring DM who developed 2 episodes of hypoglycemia during her hospital stay treating acute cholecystitis. "
        sample_answer="""" As a patient safety expert, a modified Failure Modes and Effects Analysis (FMEA) can be used to identify potential areas of risk in the care of this patient. FMEA is a step-by-step approach for identifying all possible failures in a process or procedure. In a healthcare setting, it helps to critically analyze a patient's care process and prevent potential adverse events. 

1. **Define the Topic:** A 55-year-old female with insulin-requiring diabetes mellitus, admitted for acute cholecystitis, has experienced two episodes of hypoglycemia.

2. **Assemble the Team:** The team should consist of professionals who were directly involved in the patient's care, such as physicians, nurses, pharmacists, dieticians, and possibly a patient safety officer.

3. **Graphically Describe the Process:** Map out the patient's insulin management process, from assessment of blood glucose levels, insulin dose calculation, insulin administration, to monitoring after insulin administration.

4. **Conduct a Hazard Analysis:** Identify potential failure points in this process. Examples could include errors in insulin dose calculation, inappropriate timing of insulin administration related to meals, incorrect insulin administration technique, inadequate monitoring of blood glucose levels, or inappropriate response to hypoglycemia.

5. **Determine the Effects and Severity of Each Failure:** For instance, a medication error in insulin dosing can lead to hypoglycemia, which can be life-threatening.

6. **Determine the Cause of Each Failure:** Evaluate each step of the process and identify why it failed. For example, the staff might lack knowledge on diabetes management, there might be inadequate staffing to ensure timely insulin administration, or the patient might have other factors contributing to hypoglycemia such as decreased oral intake due to cholecystitis.

7. **Develop an Action Plan:** Based on the identified causes of failure, develop strategies to mitigate the risk. This could include staff education on diabetes management, review and modification of insulin protocols, improving handoff communication, patient education, and ensuring a diet order that aligns with the insulin regimen.

8. **Test and Implement the Action Plan:** Implement the action plan and monitor its effectiveness. This may involve tracking hypoglycemic episodes and adjusting the plan as necessary.

**Review of Response:**

The response accurately outlines the steps of a healthcare FMEA to assess the risk and develop an action plan for a patient with diabetes who experienced hypoglycemia during hospitalization. The process involves assembling a team, graphically describing the insulin management process, conducting a hazard analysis, determining the effects and causes of each failure, and developing, testing, and implementing an action plan. The approach is systematic, evidence-based, and patient-centered, reflecting the importance of multidisciplinary input in managing complex conditions like diabetes and preventing adverse events like hypoglycemia."""
        temperature = 0.0     
    elif prefix_context == "Just a Chat with ChatGPT":
        prefix = """Respond as a human having a conversation with ChatGPT."""
        sample_question = ""
        sample_answer="""" """ 
        temperature = 0.5    
    else:
        prefix = ""
        sample_question = ""
        sample_answer="""" """
        temperature = 0.3     
    return prefix, sample_question, sample_answer, temperature 

prefix_context = st.radio("Pick your setting:", 
                          ("Master Clinician Explaining to Junior Clinician", "Senior Researcher Explaining to Junior Researcher", 
                           "Hematologist for your Clotting Questions", "Infectious Diseases Physician for your Complex ID Questions", "Medication Questions from Prescribers", 
                           "Patient Safety Expert Assesses Risks", "Just a Chat with ChatGPT", "Your Option to Set a Context for the Conversation"))

prefix, sample_question, sample_answer, temperature = set_prefix()
if prefix_context == "Your Option to Set a Context for the Conversation":
    prefix = st.sidebar.text_area("Enter your custom context..., eg., respond like a pirate.", height=100)


def clear_text():
    st.session_state["my_ask"] = ""



# Define function to explain code using OpenAI Codex
@st.cache_data
def answer_using_prefix(prefix, sample_question, sample_answer, my_ask, temperature):
    history_context = "Use these preceding questions (already answered) to help set context: \n" + "\n".join(st.session_state.history) + "now, for the current question: \n"
    completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
    model = 'gpt-3.5-turbo',
    messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'system', 'content': prefix + history_context},
            {'role': 'user', 'content': sample_question},
            {'role': 'assistant', 'content': sample_answer},
            {'role': 'user', 'content': my_ask}
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
# temperature = st.sidebar.slider(
#     "Temperature - focused/conservative to creative/risky",
#     min_value=0.0,
#     max_value=1.0,
#     value=0.3,
#     step=0.1
# )
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
    output_text = answer_using_prefix(prefix, sample_question, sample_answer, my_ask, temperature)

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

