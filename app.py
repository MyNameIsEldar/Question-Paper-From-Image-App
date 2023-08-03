import image_scan
import test_generator
import streamlit as st
import ptvsd
import time

# use when run localy
# ptvsd.enable_attach(address=('localhost', 5678))
# ptvsd.wait_for_attach()

st.title('📄 Question Paper Generator')
st.caption('This app in pre-beta release. We are testing more features 😎')
st.header('Choose a file')

uploaded_file = st.file_uploader('', label_visibility='hidden', type=['png', 'jpg'])
if uploaded_file is not None:
    
    image = uploaded_file.getvalue()
    st.image(image, caption='Uploaded image', width=256)

    if st.button('🖨️Make test', type='primary'):

        

        with st.spinner('Image preparation...'):
            text = image_scan.main(image)
            time.sleep(1)

        with st.spinner('Test editing...'):
            result = test_generator.main(text)
            time.sleep(1)
        st.toast('Done!', icon="✅")

        st.divider()
        st.text(result)