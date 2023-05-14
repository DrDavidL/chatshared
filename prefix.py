#Integrating OpenAI with Streamlit: With Example  Source Code Explainer 4/29/2023 --Author Ajit Dash
import streamlit as st
import openai
import os  

if 'history' not in st.session_state:
            st.session_state.history = []

if 'output_history' not in st.session_state:
            st.session_state.output_history = []
            
if 'mcq_history' not in st.session_state:
            st.session_state.mcq_history = []

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

tab1, tab2 = st.tabs(["Chat", "Study"])

with tab1:

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
    @st.cache_data    
    def gen_mcq(specialty, sample_board_mcq, number_of_mcqs):
        mcq_completion = openai.ChatCompletion.create(
            model ='gpt-3.5-turbo',
            messages = [
                {'role': 'system', 'content': "You are a board certified expert physician in " + specialty + """ and you are asked to generate a board exam level multiple choice question.
                 You rely fully on the latest evidence based findings and terminology from the most recent clinical guidelines and consensus statements. Then, you follow best practices in question design avoiding clues in the stem wording, avoiding negative wording, and avoiding absolute terms like always or never, avoiding 
                 tricky wording, and avoiding all of the above or none of the above as answer choices. You also follow best practices in answer choice design by making sure the correct answer is
                    the same length as the distractors, and that the distractors are plausible. You also make sure that the correct answer is not the longest or shortest answer. You also make sure that the correct answer is not the most or least specific answer.
                    You also make sure that the correct answer is not the most or least inclusive answer. Perform a final step by step review of your response to ensure it is factual and based on evidence based consensus guidelines and is accurate and complete when finalizing your response.
                 """},
                {'role': 'assistant', 'content': sample_board_mcq},
                {'role': 'user', 'content': f'Please generate {number_of_mcqs} multiple choice question(s) with answer explanations at a board exam level for {specialty} using the above template modified to display nicely on a webpage. Perform a final step by step review of your preliminary response to ensure it is uses current terminology and is accurate and evidence based when finalizing your response.'}
            ],
            temperature = 0.0
            )
        return mcq_completion
      
    my_ask = st.text_area('Ask away!', height=100, key="my_ask")


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
        st.sidebar.write("Working memory is cleared; input/output still listed for you!")

    st.button("Clear Input Field", on_click=clear_text)

    if st.button("Show prompt details"):
        st.write(f'Current Prompt: {prefix} + {my_ask} \n\n')



    st.sidebar.write("Current Input History", st.session_state.history)
    st.sidebar.write("Current Output History", st.session_state.output_history)
    st.sidebar.write("Current MCQ History", st.session_state.mcq_history)
    # st.write(f'My Current Question: {my_ask}')

with tab2:
    
    specialty = st.radio("Pick your study area:", 
                            ("Allergy","Cardiology", "Clinical Informatics","Critical Care","Endocrinology", "Gastroenterology", "Hematology Oncology","Hospital Medicine", "Infectious Diseases", "Internal Medicine",
                              "Nephrology",   "Neurology", "Pulmonary",   "Rheumatology"))
    num_mcq=st.number_input("Number of MCQs to generate", min_value=1, max_value=10, value=2, step=1, key="num_mcqs")
    def set_specialty(specialty):   
        if specialty == "Allergy":
            sample_board_mcq = """**Multiple Choice Question:**

A 6-year-old boy with a history of eczema presents with his mother who reports that he recently had an episode of vomiting and hives after eating peanuts. The boy has never had a reaction to peanuts before. The mother asks what should be the next step in management. According to the latest guidelines, what is the most appropriate action?

A. Advise strict peanut avoidance
B. Prescribe an epinephrine autoinjector and advise to use it if symptoms recur after eating peanuts
C. Perform a skin prick test or measure peanut-specific IgE
D. Recommend a peanut oral immunotherapy (OIT)
E. Refer to an allergist for a supervised oral food challenge

**Answer:**

The correct answer is C. Perform a skin prick test or measure peanut-specific IgE.

According to the latest guidelines from the American Academy of Allergy, Asthma & Immunology (AAAAI) and the American College of Allergy, Asthma & Immunology (ACAAI), the first step after a suspected food allergy reaction should be to perform a diagnostic test, such as a skin prick test or measurement of food-specific IgE levels, to confirm the allergy. 

Now, let's discuss why the other options are incorrect:

A. Advising strict peanut avoidance would be premature without confirming the allergy. In fact, unnecessary avoidance can lead to nutritional deficiencies and affect quality of life.

B. Prescribing an epinephrine autoinjector might be appropriate once the peanut allergy is confirmed, but it is not the next step after a single reaction without confirmed diagnosis.

D. Peanut oral immunotherapy (OIT) might be considered for confirmed peanut allergy, but it should not be initiated without diagnostic testing.

E. Referral to an allergist for a supervised oral food challenge is typically done after skin testing or serum IgE testing suggests a food allergy, not as the first step after a single reaction.

**Review of Response:**

The question accurately presents a common clinical scenario in the practice of allergy, namely a suspected food allergy in a child, a topic that allergists should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest AAAAI and ACAAI guidelines. This question tests the candidate's knowledge about the appropriate diagnostic steps in the evaluation of a suspected food allergy, making it a suitable question for an allergy board exam."""
        if specialty == "Critical Care":
            sample_board_mcq = """**Multiple Choice Question:**

A 55-year-old male patient with severe ARDS secondary to influenza pneumonia is on mechanical ventilation. Despite optimization of ventilator settings, including a low tidal volume strategy, the patient's oxygenation remains inadequate with a PaO2/FiO2 ratio of 75. What is the most appropriate next step according to the latest guidelines?

A. Increase tidal volume to improve oxygenation
B. Initiate inhaled nitric oxide therapy
C. Start systemic corticosteroid therapy
D. Position the patient in prone
E. Increase positive end-expiratory pressure (PEEP)

**Answer:**

The correct answer is D. Position the patient in prone.

The latest Surviving Sepsis Campaign guidelines recommend prone positioning in severe ARDS patients (PaO2/FiO2 ratio less than 150) who are receiving mechanical ventilation. Prone positioning can improve ventilation-perfusion matching and reduce ventilator-induced lung injury by alleviating the pleural pressure gradient, which is typically higher in the dorsal lung regions in the supine position.

Now, let's discuss why the other options are incorrect:

A. Increasing tidal volume is not recommended as it can lead to ventilator-induced lung injury. A low tidal volume strategy is considered the standard of care for ARDS.

B. Inhaled nitric oxide is considered a rescue therapy for refractory hypoxemia, not a first-line therapy, according to the latest guidelines.

C. Systemic corticosteroid therapy might be considered in patients with ARDS, but its role is controversial and it is not considered a first-line therapy.

E. Increasing PEEP can improve oxygenation in ARDS, but it can also increase the risk of barotrauma and hemodynamic instability. It should be carefully titrated based on individual patient characteristics and response.

**Review of Response:**

The question accurately presents a typical scenario in critical care, specifically the management of a patient with severe ARDS, a topic that critical care physicians should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest Surviving Sepsis Campaign guidelines. This question tests the candidate's knowledge about the management of severe ARDS, making it a suitable question for a critical care board exam."""
        if specialty == "Endocrinology":
            sample_board_mcq = """**Multiple Choice Question:**

A 35-year-old female presents with unexplained weight gain, fatigue, and intolerance to cold. Laboratory results reveal a TSH level of 12 mIU/L (normal: 0.5-4.5 mIU/L) and a free T4 level of 0.7 ng/dL (normal: 0.9-1.7 ng/dL). These findings are consistent with primary hypothyroidism. According to the latest guidelines, what is the most appropriate next step in management?

A. Start the patient on a full replacement dose of levothyroxine
B. Repeat the thyroid function tests in 3 months
C. Start the patient on a low dose of levothyroxine and titrate up based on response
D. Refer the patient for thyroidectomy
E. Start the patient on triiodothyronine (T3) supplementation

**Answer:**

The correct answer is A. Start the patient on a full replacement dose of levothyroxine.

According to the latest American Thyroid Association (ATA) guidelines, the goal of therapy in hypothyroidism is to normalize thyroid-stimulating hormone (TSH) levels with levothyroxine. For most adults with primary hypothyroidism, the recommended starting dose of levothyroxine is a full replacement dose, typically calculated based on the patient's weight.

Now, let's discuss why the other options are incorrect:

B. Repeating the thyroid function tests in 3 months without treatment is not appropriate given the patient's symptomatic hypothyroidism and elevated TSH.

C. Starting on a low dose and titrating up may be necessary for certain patients (e.g., elderly, cardiac disease), but for most adults, a full replacement dose is the recommended starting point.

D. Thyroidectomy is not the treatment of choice for primary hypothyroidism.

E. Routine use of T3 is not recommended by the ATA for the treatment of hypothyroidism due to concerns about potential harms, including heart rhythm disturbances.

**Review of Response:**

The question accurately represents a common clinical scenario in endocrinology, specifically the management of primary hypothyroidism, a topic that endocrinologists should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest ATA guidelines. This question tests the candidate's knowledge about the appropriate treatment for primary hypothyroidism, making it a suitable question for an endocrinology board exam."""
        if specialty == "Gastroenterology":
            sample_board_mcq = """**Multiple Choice Question:**

A 60-year-old male patient with a history of alcohol use disorder presents with sudden onset of severe abdominal pain and vomiting. On examination, his abdomen is distended and tender. Serum amylase and lipase levels are elevated. An abdominal CT scan reveals diffuse enlargement of the pancreas and peripancreatic fluid collections. The patient is diagnosed with acute pancreatitis. According to the latest guidelines, what is the most appropriate initial management strategy?

A. Start the patient on prophylactic antibiotics
B. Order an endoscopic retrograde cholangiopancreatography (ERCP) immediately
C. Initiate aggressive intravenous hydration
D. Administer intravenous opioids for pain control
E. Start the patient on a high-fat diet

**Answer:**

The correct answer is C. Initiate aggressive intravenous hydration.

According to the latest guidelines from the American College of Gastroenterology (ACG), aggressive intravenous hydration is a cornerstone of the initial management of acute pancreatitis, as it helps to improve microcirculation and decrease the risk of necrosis.

Now, let's discuss why the other options are incorrect:

A. Prophylactic antibiotics are not recommended in the management of acute pancreatitis, as they have not been shown to reduce mortality or the risk of infection.

B. ERCP is not routinely performed in the initial management of acute pancreatitis, except in the case of cholangitis or persistent biliary obstruction.

D. While pain control is a critical part of the management of acute pancreatitis, aggressive intravenous hydration is a more immediate and vital step in management.

E. Dietary restrictions were previously recommended in acute pancreatitis, but more recent guidelines suggest early enteral feeding as tolerated. However, a high-fat diet is not recommended, especially in the acute phase.

**Review of Response:**

The question accurately presents a typical scenario in gastroenterology, specifically the management of a patient with acute pancreatitis, a topic that gastroenterologists should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest ACG guidelines. This question tests the candidate's knowledge about the initial management of acute pancreatitis, making it a suitable question for a gastroenterology board exam."""
        if specialty == "Hospital Medicine":
            sample_board_mcq = """**Multiple Choice Question:**

A 68-year-old male patient with a history of hypertension and diabetes presents to the hospital with chest pain. An EKG shows ST-segment elevation in leads II, III, and aVF. The patient is diagnosed with an ST-elevation myocardial infarction (STEMI). He is allergic to aspirin, which causes him to develop angioedema. According to the latest guidelines, what is the most appropriate initial antiplatelet therapy?

A. Clopidogrel
B. Ticagrelor
C. Prasugrel
D. Eptifibatide
E. Aspirin desensitization

**Answer:**

The correct answer is B. Ticagrelor.

In the setting of STEMI, dual antiplatelet therapy (DAPT) is recommended. For patients with aspirin allergy, the American College of Cardiology (ACC) and the American Heart Association (AHA) recommend using a P2Y12 inhibitor. Ticagrelor is preferred over clopidogrel due to its more potent and consistent antiplatelet effects, as shown in the PLATO trial.

Now, let's discuss why the other options are incorrect:

A. Clopidogrel is a reasonable alternative if ticagrelor is contraindicated or not tolerated, but it is not the first-line option due to its less potent and variable antiplatelet effects compared to ticagrelor.

C. Prasugrel is not recommended in the initial treatment of STEMI because it is associated with a higher risk of bleeding compared to ticagrelor and clopidogrel, especially in patients over 75 years old or those with a history of stroke or transient ischemic attack.

D. Eptifibatide is a glycoprotein IIb/IIIa inhibitor, not a P2Y12 inhibitor. It is typically used in high-risk percutaneous coronary intervention (PCI), not as an initial antiplatelet therapy in STEMI.

E. Aspirin desensitization could be considered in some patients with coronary artery disease who are allergic to aspirin, but it is not the immediate treatment of choice in a patient presenting with STEMI.

**Review of Response:**

The question accurately represents a common clinical scenario in hospital medicine, specifically the management of a patient with STEMI who is allergic to aspirin, a topic that hospitalists should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest ACC/AHA guidelines. This question tests the candidate's knowledge about the appropriate antiplatelet therapy for a patient with STEMI and aspirin allergy, making it a suitable question for a hospital medicine board exam."""
        if specialty == "Nephrology":
            sample_board_mcq = """**Multiple Choice Question:**

A 45-year-old female with type 2 diabetes mellitus and hypertension presents with proteinuria of 3.5g/day. Her serum creatinine is 1.2 mg/dL and estimated glomerular filtration rate (eGFR) is 60 mL/min/1.73m^2. Her blood pressure is 140/90 mmHg. According to the latest guidelines, what is the most appropriate initial management for this patient?

A. Start losartan
B. Start amlodipine
C. Start furosemide
D. Perform a renal biopsy
E. Start metformin

**Answer:**

The correct answer is A. Start losartan.

According to the Kidney Disease: Improving Global Outcomes (KDIGO) guidelines, patients with diabetes, hypertension, and proteinuria should be managed initially with an angiotensin receptor blocker (ARB) like losartan or an angiotensin-converting enzyme inhibitor (ACEi). These agents have been shown to reduce proteinuria and slow the progression of kidney disease.

Now, let's discuss why the other options are incorrect:

B. Amlodipine is a calcium channel blocker that can be used in the management of hypertension. However, it does not have the same protective effect on the kidneys as ARBs or ACEis in patients with diabetic kidney disease.

C. Furosemide is a loop diuretic that can help manage fluid overload in kidney disease. However, it is not the first-line treatment for proteinuria in patients with diabetic kidney disease.

D. A renal biopsy is not the first-line management for a patient with diabetes, hypertension, and proteinuria. It might be considered if there is suspicion for a non-diabetic cause of kidney disease.

E. Metformin is a first-line treatment for type 2 diabetes mellitus, but it does not directly address the patient's proteinuria or hypertension.

**Review of Response:**

The question accurately presents a typical scenario in nephrology: the management of a patient with diabetic kidney disease. The correct answer and explanations for the incorrect options align with the latest KDIGO guidelines. This question tests the candidate's knowledge about the initial management of proteinuria in a patient with diabetic kidney disease, making it a suitable question for a nephrology board exam."""
        if specialty == "Neurology":
            sample_board_mcq = """**Multiple Choice Question:**

A 58-year-old male with a history of hypertension presents with a sudden onset of right-sided weakness and slurred speech. His symptoms started 90 minutes ago. A CT scan of the head shows no hemorrhage. His blood pressure is 185/95 mmHg. According to the latest guidelines, what is the most appropriate initial management for this patient?

A. Intravenous tissue plasminogen activator (tPA)
B. Antihypertensive therapy to lower blood pressure below 140/90 mmHg
C. Immediate mechanical thrombectomy
D. Aspirin and clopidogrel
E. Wait for MRI before initiating any treatment

**Answer:**

The correct answer is A. Intravenous tissue plasminogen activator (tPA).

According to the American Heart Association/American Stroke Association guidelines, patients presenting with acute ischemic stroke symptoms within 3 hours of symptom onset, and without contraindications, should receive intravenous tPA. 

Now, let's discuss why the other options are incorrect:

B. Aggressive antihypertensive therapy in the acute phase of stroke is not recommended. It is preferred to maintain the blood pressure less than 185/110 mmHg if thrombolytic therapy is being considered.

C. Mechanical thrombectomy is indicated in certain cases of acute ischemic stroke, typically in patients with large vessel occlusion and within a certain time window. However, intravenous tPA is the first-line treatment when applicable.

D. The combination of aspirin and clopidogrel is not the first-line treatment in the acute setting of ischemic stroke. Intravenous tPA is the treatment of choice within the therapeutic window.

E. Waiting for an MRI may delay treatment unnecessarily. A non-contrast CT scan that does not show hemorrhage is sufficient for starting treatment with tPA in the appropriate clinical scenario.

**Review of Response:**

The question presents a typical scenario in neurology, specifically the management of acute ischemic stroke. The correct answer and the explanations for the incorrect options are consistent with the latest guidelines from the American Heart Association/American Stroke Association. This question tests the candidate's knowledge about the initial management of acute ischemic stroke, making it a suitable question for a neurology board exam."""
        if specialty == "Pulmonary":
            sample_board_mcq = """**Multiple Choice Question:**

A 68-year-old male with a 40-pack-year smoking history presents with a persistent cough and shortness of breath. His chest CT shows an upper lobe cavitary lesion with a spiculated margin. Sputum cytology reveals atypical cells. According to the latest guidelines, what is the most appropriate next step in management for this patient?

A. Sputum culture
B. Bronchoscopy with biopsy
C. PET scan
D. Start empiric antibiotics
E. Repeat CT scan in 3 months

**Answer:**

The correct answer is B. Bronchoscopy with biopsy.

The presence of a cavitary lesion with a spiculated margin in a patient with a significant smoking history is highly concerning for lung cancer. The finding of atypical cells on sputum cytology further increases this suspicion. The next appropriate step to confirm the diagnosis is bronchoscopy with biopsy.

Now, let's discuss why the other options are incorrect:

A. Sputum culture is useful when there is a suspicion of infection, but in this case, the clinical scenario and radiographic findings strongly suggest malignancy, not infection.

C. PET scan could be used for staging of a known malignancy, but histologic confirmation (via biopsy) is generally needed before staging.

D. Empiric antibiotics are not appropriate as the primary concern here is malignancy, not infection.

E. Given the high suspicion for malignancy, a wait-and-see approach with a repeat CT scan in 3 months is not appropriate. Prompt diagnosis and treatment are necessary.

**Review of Response:**

The question presents a typical scenario in pulmonary medicine, specifically the approach to a suspicious lung lesion. The correct answer and the explanations for the incorrect options are consistent with the latest guidelines for lung cancer diagnosis and management. This question tests the candidate's knowledge about the initial management of a suspicious lung lesion in a high-risk patient, making it a suitable question for a pulmonary board exam.
"""
        if specialty == "Clinical Informatics":
            sample_board_mcq = """**Multiple Choice Question:**

                A 300-bed community hospital is implementing a new electronic health record (EHR) system. The chief medical information officer (CMIO) is concerned about potential medication errors during the transition. Which of the following strategies would be most effective in minimizing this risk according to the latest recommendations?

                A. Conduct extensive user training prior to the system go-live
                B. Run the old and new EHR systems in parallel for the first 3 months
                C. Implement a system of double checks for all medication orders for the first month
                D. Perform a Failure Modes and Effects Analysis (FMEA) prior to system go-live
                E. Increase staffing levels for the first two weeks following go-live

                **Answer:**

                The correct answer is D. Perform a Failure Modes and Effects Analysis (FMEA) prior to system go-live.

                According to recommendations from organizations such as the Agency for Healthcare Research and Quality (AHRQ) and the Joint Commission, performing a proactive risk assessment like FMEA prior to implementing a new EHR system can help identify potential areas of concern and implement strategies to mitigate those risks. 

                Now, let's discuss why the other options are incorrect:

                A. User training is important but it alone cannot address all the potential risks associated with transitioning to a new EHR system.

                B. Running the old and new EHR systems in parallel can create confusion and increase the risk of errors, as staff may be uncertain which system to use or may inadvertently enter data into the wrong system.

                C. Implementing a system of double checks can help reduce errors, but it is labor-intensive and may not be sustainable over the long term.

                E. Increasing staffing levels can help manage the increased workload associated with a system go-live, but it does not directly address the underlying risks associated with the transition.

                **Review of Response:**

                The question accurately presents a scenario relevant to clinical informatics, specifically the transition to a new EHR system, a topic that clinical informatics professionals should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest recommendations from the AHRQ and the Joint Commission. This question tests the candidate's knowledge about risk management strategies in health IT projects, making it a suitable question for a clinical informatics board exam."""
        if specialty == 'Hematology Oncology':
            sample_board_mcq = """**Multiple Choice Question:**

                A 65-year-old woman with a history of breast cancer treated with lumpectomy and radiation therapy 5 years ago presents with a new onset of back pain. Imaging studies reveal multiple osteolytic lesions in the vertebrae. A bone marrow biopsy confirms the presence of plasma cells. Lab tests show a serum calcium level of 11.5 mg/dL (normal range: 8.5-10.2 mg/dL) and a creatinine level of 1.2 mg/dL (normal range: 0.6-1.1 mg/dL). The patient is diagnosed with multiple myeloma. According to the latest guidelines, what would be the most appropriate initial treatment for this patient?

                A. High-dose chemotherapy with autologous stem cell transplantation
                B. Combination of bortezomib, lenalidomide, and dexamethasone (VRd)
                C. Combination of cyclophosphamide, bortezomib, and dexamethasone (CyBorD)
                D. Palliative radiation therapy for spinal lesions
                E. Bisphosphonate therapy alone

                **Answer:**

                The correct answer is B. Combination of bortezomib, lenalidomide, and dexamethasone (VRd).

                According to the latest National Comprehensive Cancer Network (NCCN) guidelines, initial treatment of multiple myeloma in patients who are not candidates for immediate autologous stem cell transplantation typically involves combination therapy. The regimen of bortezomib, lenalidomide, and dexamethasone (VRd) is one of the preferred regimens. 

                Now, let's discuss why the other options are incorrect:

                A. High-dose chemotherapy with autologous stem cell transplantation is an effective treatment for multiple myeloma, but it is usually reserved for younger patients or patients with aggressive disease and good functional status. It is typically not the first-line treatment.

                C. The combination of cyclophosphamide, bortezomib, and dexamethasone (CyBorD) can be used, but VRd is generally preferred as initial therapy due to its favorable balance of efficacy and side effects.

                D. Palliative radiation therapy could be considered for localized pain control in patients with symptomatic bone lesions, but it is not sufficient as a standalone systemic treatment for multiple myeloma.

                E. Bisphosphonate therapy is used in multiple myeloma to reduce the risk of skeletal-related events but is not sufficient as a standalone systemic treatment for multiple myeloma.

                **Review of Response:**

                The question accurately presents a clinical scenario suggestive of a patient with multiple myeloma, a topic that hematology and oncology physicians should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest NCCN guidelines and standard textbooks. This question tests the candidate's knowledge about the management of multiple myeloma, making it a suitable question for a hematology and oncology board exam.
                """
        if specialty == 'Rheumatology':
            sample_board_mcq = """**Multiple Choice Question:**

                A 50-year-old woman presents with a 6-month history of morning stiffness, metacarpophalangeal joint swelling, and fatigue. Lab testing is positive for anti-cyclic citrullinated peptide (anti-CCP) antibodies and rheumatoid factor. Her C-reactive protein (CRP) is also elevated. She has been treated with methotrexate for the past 3 months, but her symptoms have not improved significantly. What is the most appropriate next step in management according to the latest guidelines?

                A. Increase the dose of methotrexate
                B. Add hydroxychloroquine
                C. Add a tumor necrosis factor (TNF) inhibitor
                D. Switch to leflunomide
                E. Add low-dose prednisone

                **Answer:**

                The correct answer is C. Add a tumor necrosis factor (TNF) inhibitor.

                This patient has rheumatoid arthritis (RA) as evidenced by the joint symptoms, the presence of anti-CCP antibodies and rheumatoid factor, and elevated CRP. According to the latest American College of Rheumatology (ACR) guidelines, if a patient has moderate to severe RA that does not respond to initial therapy with methotrexate alone, it is appropriate to add a TNF inhibitor. 

                Now, let's discuss why the other options are incorrect:

                A. Increasing the dose of methotrexate might be considered, but usually, if there's no significant improvement after 3 months, it's unlikely that merely increasing the dose will lead to significant improvement.

                B. Adding hydroxychloroquine might be considered as part of a combination strategy, but the latest guidelines suggest TNF inhibitors show better efficacy in patients with moderate to severe disease not responding to methotrexate alone.

                D. Switching to leflunomide from methotrexate is usually considered if the patient is not tolerating methotrexate, rather than in a situation where there is a lack of response.

                E. Low-dose prednisone can be used for bridging therapy or for patients with contraindications to other agents, but it is not typically used as a long-term strategy due to its side effect profile.

                **Review of Response:**

                The question accurately presents a clinical scenario suggestive of a patient with rheumatoid arthritis who is not responding to initial methotrexate therapy, a topic that rheumatology physicians should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the latest guidelines and standard textbooks. This question tests the candidate's knowledge about the management of rheumatoid arthritis, making it a suitable question for a rheumatology board exam."""
        if specialty == "Cardiology":
            sample_board_mcq = """**Multiple Choice Question:**

                A 59-year-old man with a known history of systolic heart failure presents with increasing dyspnea, orthopnea, and lower extremity edema. His blood pressure is 110/70 mmHg, heart rate is 90 beats per minute, and his EKG shows a left bundle branch block with a QRS duration of 150 milliseconds. His current medication regimen includes a beta blocker, an ACE inhibitor, and a diuretic. Which of the following is the most appropriate next step in management?

                A. Add a calcium channel blocker
                B. Add a second diuretic
                C. Add digoxin
                D. Refer for cardiac resynchronization therapy (CRT)
                E. Refer for heart transplant evaluation

                **Answer:**

                The correct answer is D. Refer for cardiac resynchronization therapy (CRT).

                This patient has heart failure with reduced ejection fraction (HFrEF) and evidence of electrical dyssynchrony on EKG (left bundle branch block with a QRS duration >150 ms). These findings suggest that he would benefit from cardiac resynchronization therapy, a treatment shown to improve symptoms and decrease mortality in patients with symptomatic HFrEF, left bundle branch block, and a QRS duration ≥150 ms.

                Now, let's discuss why the other options are incorrect:

                A. Calcium channel blockers are not typically used in HFrEF, as they can worsen heart failure symptoms.

                B. While adding a second diuretic might help manage the patient's volume status in the short term, it does not address the underlying problem of dyssynchrony, which is contributing to his heart failure symptoms.

                C. Digoxin might be considered for symptomatic management of heart failure, but it has not been shown to improve mortality like CRT has.

                E. Heart transplant evaluation is typically reserved for patients with refractory heart failure who have not responded to maximal medical therapy, including interventions like CRT.

                **Review of Response:**

                The question accurately presents a clinical scenario suggestive of a patient with heart failure who would benefit from cardiac resynchronization therapy, a topic that cardiology physicians should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the clinical guidelines and standard textbooks. This question tests the candidate's knowledge about the management of heart failure, making it a suitable question for a cardiology board exam."""     
        if specialty == "Internal Medicine":
            sample_board_mcq = """**Multiple Choice Question:**

                A 65-year-old man presents to the clinic with a three-month history of progressive exertional dyspnea. He is a former smoker with a 30 pack-year history and quit 5 years ago. His physical examination is significant for distant heart sounds and decreased breath sounds bilaterally with dullness to percussion. His chest X-ray shows bilateral pleural effusions. Thoracentesis reveals a cholesterol level of 70 mg/dL and a protein level of 4.8 g/dL in the pleural fluid. Which of the following is the most likely diagnosis?

                A. Congestive heart failure
                B. Pneumonia
                C. Pulmonary embolism
                D. Chylothorax
                E. Chronic tuberculous pleuritis

                **Answer:**

                The correct answer is E. Chronic tuberculous pleuritis.

                This patient's history of chronic progressive dyspnea, the physical exam findings, and the presence of a cholesterol-rich, protein-rich pleural effusion (often referred to as "cholesterol effusion" or "pseudochylothorax") suggest a diagnosis of chronic tuberculous pleuritis. This condition can occur as a long-term complication of healed primary tuberculosis and is characterized by very high cholesterol and protein levels in the pleural fluid.

                Now, let's discuss why the other options are incorrect:

                A. Congestive heart failure can cause bilateral pleural effusions, but the effusions are typically transudates (with low protein) rather than exudates (with high protein) like in this case.

                B. Pneumonia can lead to parapneumonic effusion, but this tends to be unilateral rather than bilateral. Moreover, the cholesterol level is not typically elevated in these effusions.

                C. Pulmonary embolism can cause pleural effusion, but it's usually unilateral and associated with other symptoms like acute onset dyspnea, chest pain, and tachycardia.

                D. Chylothorax is characterized by a milky-appearing pleural fluid due to high triglyceride content, typically resulting from thoracic duct injury. This patient's pleural fluid does not have the typical appearance, and there is no history suggestive of thoracic duct injury.

                **Review of Response:**

                The question accurately presents a clinical scenario suggestive of chronic tuberculous pleuritis, a condition that internal medicine physicians should be familiar with. The correct answer and the explanations for the incorrect options are consistent with the clinical guidelines and standard textbooks. This question tests the candidate's knowledge about the clinical presentation and differential diagnosis of pleural effusions, making it a suitable question for an internal medicine board exam."""
        if specialty == 'Infectious Diseases':
            sample_board_mcq = """**Multiple Choice Question:**

                A 32-year-old woman presents with a painful, swollen right knee after returning from a hiking trip in the Northeast United States. She also reports fever, chills, and fatigue for the past week. On examination, she has a large erythematous rash on her right thigh with a clear area in the center. Synovial fluid analysis of the knee joint reveals inflammatory findings. Which of the following is the most appropriate treatment?

                A. Doxycycline
                B. Ceftriaxone
                C. Amoxicillin-clavulanate
                D. Trimethoprim-sulfamethoxazole
                E. Azithromycin

                **Answer:**

                The correct answer is A. Doxycycline.

                This patient's presentation with a target-like rash (erythema migrans), fever, fatigue, and arthralgia after a hiking trip in the Northeast United States is suggestive of Lyme disease, which is caused by the spirochete Borrelia burgdorferi and transmitted by Ixodes ticks. Doxycycline is the first-line treatment for adults with Lyme disease.

                Now, let's discuss why the other options are incorrect:

                B. Ceftriaxone is typically used for Lyme disease when the patient has neurologic involvement or for refractory Lyme arthritis after a course of oral antibiotics. In this case, the patient doesn't have any neurological symptoms, making this option less appropriate.

                C. Amoxicillin-clavulanate is used for skin and soft tissue infections like cellulitis or animal bites. Lyme disease is not typically associated with these conditions.

                D. Trimethoprim-sulfamethoxazole is used for a variety of infections, including urinary tract infections and certain types of pneumonia, but it is not first-line for Lyme disease.

                E. Azithromycin is not the first-line treatment for Lyme disease, although it can be used in patients who are intolerant to doxycycline or amoxicillin.

                **Review of Response:**

                The question accurately presents a clinical scenario suggestive of Lyme disease, a condition that infectious disease physicians should be familiar with. 
                The correct answer and the explanations for the incorrect options are consistent with the clinical guidelines and standard textbooks. 
                This question tests the candidate's knowledge about the clinical presentation and management of Lyme disease. It covers important aspects of Lyme disease, including its typical presentation, 
                geographical association, and first-line treatment, making it a suitable question for an infectious diseases board exam."""
        
        
        return sample_board_mcq

    
    if st.button("Generate a Question"):
        sample_board_mcq = set_specialty(specialty)
        generated_mcq = gen_mcq(specialty, sample_board_mcq, num_mcq)
        st.markdown(f" {generated_mcq['choices'][0]['message']['content']}") # Change how you access the message content
        st.session_state.mcq_history.append((generated_mcq['choices'][0]['message']['content']))
    
