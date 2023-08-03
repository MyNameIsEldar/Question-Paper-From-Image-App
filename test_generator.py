
import config
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


@st.cache_data
def main(text):
    TASKS_NUMBER = 4
    ANSWERS_IN_TASK = 3
    TYPE = 'тест'

    llm = ChatOpenAI(openai_api_key=config.openai_api_key, temperature=0.7, )

    template = """Ты полезный помошник-ассистент, который помогает пользователю составлять {type}. 
    Пользователь отправит тебе текст. Напиши на основе него {type}, состоящий из {num_of_q} заданий,
    в каждом из которых количество ответов равно {num_of_a}"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt
    )

    result = chain.run({'text': text, 'num_of_q': TASKS_NUMBER, 'num_of_a': ANSWERS_IN_TASK, 'type': TYPE})

    return result
