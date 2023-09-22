import qp_generator.image_scan as image_scan
import qp_generator.test_generator as test_generator
import qp_generator.pdf_to_text as pdf_to_text
from qp_generator.languages_data import languages
import streamlit as st
import ptvsd
import time

# use when run localy
# ptvsd.enable_attach(address=('localhost', 5678))
# ptvsd.wait_for_attach()


st.set_page_config(
    page_title="Test Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://t.me/eldar_tagiev',
        'Report a bug': "https://t.me/eldar_tagiev",
        'About': """
        ## Генератор заданий

        Это приложение разработано для того, чтобы помочь студентам и пребодавателям в учебном процессе!"""
    }
)

# Generation settings section
with st.sidebar: 
    lang = st.selectbox('Language', ["🇷🇺", "🇬🇧"], label_visibility='collapsed')
    
    st.title(languages[lang]['settings'])
    
    st.subheader(languages[lang]['qp_type'])

    # 'True-False', 'Another type'
    qp_type = st.selectbox(languages[lang]['type_of_input'],
        (languages[lang]['test'],  languages[lang]['open_questions']),
        label_visibility = 'collapsed'
    )

    if qp_type == languages[lang]['test']:
        st.subheader(languages[lang]['n_o_t'])
        tasks = st.slider(languages[lang]['n_o_t'], 1, 10, 4, label_visibility='collapsed')
        st.subheader(languages[lang]['n_o_a'])
        answers = st.slider(languages[lang]['n_o_a'], 2, 6, 3, label_visibility='collapsed')

    if qp_type == languages[lang]['open_questions']:
        st.subheader(languages[lang]['n_o_t'])
        tasks = st.slider(languages[lang]['n_o_t'], 1, 20, 4, label_visibility='collapsed')
        answers = 0

st.title(languages[lang]['title'])

st.caption(languages[lang]['caption1'])
st.caption(languages[lang]['caption2'])
st.caption(languages[lang]['caption3'])

result = languages[lang]['gen_result']


# Input type section

pdf_tab, img_tab, text_tab = st.tabs([
    languages[lang]['pdf'],
    languages[lang]['image'],
    languages[lang]['text']
    ]) 

with pdf_tab:
    st.header(languages[lang]['choose_file'])
    uploaded_file = st.file_uploader(languages[lang]['choose_file'],
                                     type=['pdf'],
                                     label_visibility='collapsed')
        
    if uploaded_file is not None:
        pages_count = pdf_to_text.pages_count(uploaded_file)
        
        if pages_count > 1:
            st.header(languages[lang]['select_pages'])
            pages = st.slider(
                languages[lang]['select_pages'],
                    1, pages_count, (1, pages_count), 
                    label_visibility='collapsed')
            st.write(f'Pages: {pages[0]} - {pages[-1]}')
        else:
            pages = (0,)

        if st.button(languages[lang]['make_qp'], type='primary', key='make button when pdf'):
            with st.spinner(languages[lang]['doc_prep']):
                text = pdf_to_text.main(uploaded_file, pages)
                time.sleep(1)
            
            with st.spinner(languages[lang]['test_edit']):
                    result = test_generator.main(qp_type, text, tasks, answers, lang)
                    time.sleep(1)
            st.toast(languages[lang]['done'], icon="✅")

with img_tab:
    st.header(languages[lang]['choose_file'])
    st.caption(languages[lang]['caption_image'])
    uploaded_files = st.file_uploader(languages[lang]['choose_file'],
                                        type=['png', 'jpg'],
                                        accept_multiple_files=True,
                                        label_visibility='collapsed')

    if len(uploaded_files) > 0:
        text = []

        if st.button(languages[lang]['make_qp'], type='primary', key='make button when image'):
            for uploaded_file in uploaded_files:
                image = uploaded_file.read()
                with st.spinner(languages[lang]['image_prep']):
                    text.append(image_scan.main(image))
                    time.sleep(1)
            
            text = ' '.join(text)
            with st.spinner(languages[lang]['test_edit']):
                result = test_generator.main(qp_type, text, tasks, answers, lang)
                time.sleep(1)
            st.toast(languages[lang]['done'], icon="✅")
        
with text_tab:
    st.header(languages[lang]['input_txt'])
    text = st.text_area(languages[lang]['input_txt'], value=languages[lang]['paste_txt'], label_visibility='collapsed')

    if st.button(languages[lang]['make_qp'], type='primary', key='make button when text'):

        with st.spinner(languages[lang]['test_edit']):
            result = test_generator.main(qp_type, text, tasks, answers, lang)
            time.sleep(1)
        st.toast(languages[lang]['done'], icon="✅")

st.header(languages[lang]['result'])
st.text_area('', value=result, label_visibility='collapsed', height=400)