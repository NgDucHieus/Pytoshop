import streamlit as st
from PIL import Image
def app():
    image = Image.open('imgs/lake.jpeg')
    st.image(image, caption='Welcome to my webapp!', use_column_width=True)
    st.subheader('CSE3062	Computer Vision')
    st.subheader("ID: 22110125", anchor=None)
    st.subheader("Photoshop tool using Python and OpenCV", anchor=None)
    st.subheader("Authors", anchor=None)
    st.markdown('Nguyen Duc Hieu', unsafe_allow_html=True)
    st.subheader("Submitted to", anchor=None)
    st.markdown("Dr. Bui Huy Kien")
