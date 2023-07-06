import streamlit as st
from langchain import PromptTemplate
from langchain.llms import VertexAI

template = """
    Below is an email that may be poorly worder.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect
    
    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you
    - Informal: Went to Barcelona for the weekend. Lots to tell you
    
    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield, trashcan, lotion,
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park , trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.

    Below is the eamil, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}


    YOUR {dialect} RESPONSE:
"""


prompt =  PromptTemplate(
    input_variables = ["tone", "dialect", "email"],
    template =template,
)

def load_LLM():
    """Logic for loading the VertexAI """
    llm = VertexAI(temperature = 0.5)
    return llm

st.set_page_config(page_title = "Globalize Email",
                   page_icon=":Home:",
                   layout="centered",
                   initial_sidebar_state = "expanded")
st.header("Globalize Text")


col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. This tool \
                is powered by [LangChain](https://langchain.com/) and [PaLM2](https://ai.google/discover/palm2) and made by \
                [@ArkaPanda](https://github.com/ARKA1112). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")


with col2:
    st.image("https://preview.redd.it/8hm10myna6ab1.jpg?width=2048&format=pjpg&auto=webp&v=enabled&s=d1ad239f09ac1f13fb4672ae282177c5a5f06430")

st.markdown("---")
st.markdown("Enter your email to convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        "Select your tone",
        ('Formal', 'Informal')
    )

with col2:
    option_dialect = st.selectbox(
        "Select your preferred dialect",
        ('American','British','Indian')
    )

def get_text():
    input_text = st.text_area(label='Email input', label_visibility='collapsed', placeholder = 'Your Email ...', key = 'email_input')
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally  I am starts work at yours monday from dave"


st.button("*see an example*",type = 'secondary', help='click to see an example of the email you will be converting', on_click = update_text_with_example)


st.markdown("### Your converted Email")

if email_input:
    llm = load_LLM()
    
    prompt_with_email = prompt.format(tone = option_tone, dialect = option_dialect, email = email_input)
    
    formatted_email = llm(prompt_with_email)
    
    st.write(formatted_email)

st.markdown('---')
st.markdown("End")