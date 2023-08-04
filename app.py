import qp_generator.image_scan as image_scan
import qp_generator.test_generator as test_generator
import qp_generator.pdf_to_text as pdf_to_text
import streamlit as st
import ptvsd
import time

# use when run localy
# ptvsd.enable_attach(address=('localhost', 5678))
# ptvsd.wait_for_attach()

st.title('📄 Question Paper Generator')
st.caption('This app in pre-beta release. We are testing more features 😎')

result = 'Here will apear your question paper text'

# Generation settings section
with st.sidebar: 
    st.title('⚙️ Settings')
    
    st.subheader('QP Type:')

    # 'True-False', 'Another type'
    qp_type = st.selectbox('Type of input:',
        ('Test', ),
        label_visibility = 'collapsed'
    )

    if qp_type == 'Test':
        st.subheader('Number of tasks in test:')
        tasks = st.slider('Number of tasks in test', 1, 10, 4, label_visibility='collapsed')
        st.subheader('Number of answers in task:')
        answers = st.slider('Number of answers in task', 2, 6, 3, label_visibility='collapsed')


# Input type section

st.header('What input do you prefer?')  
pdf_tab, img_tab, text_tab = st.tabs(['PDF', 'Image', 'Text']) 

with pdf_tab:
    st.header('Choose a file')
    uploaded_file = st.file_uploader('Choose a file',
                                     type=['pdf'],
                                     label_visibility='collapsed')
        
    if uploaded_file is not None:
        pages_count = pdf_to_text.pages_count(uploaded_file)
        
        if pages_count > 1:
            st.header('Select pages')
            pages = st.slider(
                'Select pages',
                    1, pages_count, (1, pages_count), 
                    label_visibility='collapsed')
            st.write(f'Pages: {pages[0]} - {pages[-1]}')
        else:
            pages = (0,)

        if st.button('🖨️Make question paper', type='primary', key='make button when pdf'):
            with st.spinner('Document preparation...'):
                text = pdf_to_text.main(uploaded_file, pages)
                time.sleep(1)
            
            with st.spinner('Test editing...'):
                    result = test_generator.main(text, tasks, answers)
                    time.sleep(1)
            st.toast('Done!', icon="✅")

with img_tab:
    st.header('Choose a file')
    st.caption('сonverting images to text can take a time!')
    uploaded_files = st.file_uploader('Choose a file',
                                        type=['png', 'jpg'],
                                        accept_multiple_files=True,
                                        label_visibility='collapsed')

    if len(uploaded_files) > 0:
        text = []

        if st.button('🖨️Make question paper', type='primary', key='make button when image'):
            for uploaded_file in uploaded_files:
                image = uploaded_file.read()
                with st.spinner('Image preparation...'):
                    text.append(image_scan.main(image))
                    time.sleep(1)
            
            text = ' '.join(text)
            with st.spinner('Test editing...'):
                result = test_generator.main(text, tasks, answers)
                time.sleep(1)
            st.toast('Done!', icon="✅")
        
with text_tab:
    st.header('Input text')
    text = st.text_area('Input text', value='Paste your text here', label_visibility='collapsed')

    if st.button('🖨️Make question paper', type='primary', key='make button when text'):

        with st.spinner('Test editing...'):
            result = test_generator.main(text, tasks, answers)
            time.sleep(1)
        st.toast('Done!', icon="✅")

st.header('Result')
st.text_area('', value=result, label_visibility='collapsed', height=400)