import qp_generator.image_scan as image_scan
import qp_generator.test_generator as test_generator
import streamlit as st
import ptvsd
import time

# use when run localy
ptvsd.enable_attach(address=('localhost', 5678))
ptvsd.wait_for_attach()

st.title('📄 Question Paper Generator')
st.caption('This app in pre-beta release. We are testing more features 😎')

result = 'Here will apear your question paper text'

# Generation settings section
with st.sidebar: 
    st.title('⚙️ Settings')
    
    st.subheader('QP Type:')
    
    qp_type = st.selectbox('Type of input:',
        ('Test', 'True-False', 'Another type'),
        label_visibility = 'collapsed'
    )

    if qp_type == 'Test':
        st.subheader('Number of tasks in test:')
        tasks = st.slider('Number of tasks in test', 1, 10, label_visibility='collapsed')
        st.subheader('Number of answers in task:')
        answers = st.slider('Number of answers in task', 2, 6, label_visibility='collapsed')


# Input type section

st.header('What input do you prefer?')  
img_tab, pdf_tab, text_tab = st.tabs(['Image', 'PDF', 'Text']) 
with st.expander("Input settings", expanded=True):

    with img_tab:
        uploaded_files = st.file_uploader('Choose a file', type=['png', 'jpg'], accept_multiple_files=True)

        if len(uploaded_files) > 0:
            # for uploaded_file in uploaded_files:
                # image = uploaded_file.read()
                # st.image(image, caption='Uploaded image', width=256)
            text = []

            if st.button('🖨️Make question paper', type='primary', key='make button when image'):
                for uploaded_file in uploaded_files:
                    image = uploaded_file.read()
                    with st.spinner('Image preparation...'):
                        text.append(image_scan.main(image))
                        time.sleep(1)
                
                text = '\n'.join(text)
                with st.spinner('Test editing...'):
                    result = test_generator.main(text, tasks, answers)
                    time.sleep(1)
                st.toast('Done!', icon="✅")

    with pdf_tab:
        st.header('😥Not working yet(')

    with text_tab:
        text = st.text_area('Text to analyze')

        if st.button('🖨️Make question paper', type='primary', key='make button when text'):

            with st.spinner('Test editing...'):
                result = test_generator.main(text, tasks, answers)
                time.sleep(1)
            st.toast('Done!', icon="✅")

st.header('Result')
st.text_area('', value=result, label_visibility='collapsed', height=400)