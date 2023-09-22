
# import config
import app
import streamlit as st
import qp_generator.templates as templates
from qp_generator.languages_data import languages
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


@st.cache_data
def main(qp_type, text, tasks, answers, lang):
    OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

    #openai_api_key=config.openai_api_key
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

    if qp_type == languages[lang]['test']:
        temp_part = templates.test
    if qp_type == languages[lang]['open_questions']:
        temp_part = templates.open_questions

    template = """
Ты полезный помошник-ассистент, который помогает пользователю составлять {type}. 
    """ + temp_part

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt
    )

    result = chain.run({'text': text, 'num_of_q': tasks, 'num_of_a': answers, 'type': qp_type})

    return result
