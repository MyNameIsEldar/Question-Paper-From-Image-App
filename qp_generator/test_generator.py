
# import config
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


@st.cache_data
def main(text, tasks, answers):
    TYPE = 'тест'
    OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

    #openai_api_key=config.openai_api_key
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

    template = """
    Ты полезный помошник-ассистент, который помогает пользователю составлять {type}. 
    Пользователь отправит тебе текст. Напиши на основе него {type}, состоящий из {num_of_q} заданий,
    в каждом из которых количество ответов равно {num_of_a}. Начни вывод так: "Тест: ". В конце теста напиши ответы к каждому из вопросов.
    В каждом вопросе должен быть ровно 1 правильный ответ. Твой ответ должен быть на русском языке.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt
    )

    result = chain.run({'text': text, 'num_of_q': tasks, 'num_of_a': answers, 'type': TYPE})

    return result
