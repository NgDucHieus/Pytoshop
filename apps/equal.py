import streamlit as st
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

def app():
    DEMO_IMAGE = 'imgs/hieu.jpeg'

    # Function for Linear Transformation
    @st.cache_data
    def histogram_equalization(img):
        """
        Applies histogram equalization to enhance contrast in the image.
        :param img: Grayscale image (2D array)
        :return: Image after histogram equalization
        """
        equalized_img = cv2.equalizeHist(img)
        return equalized_img
    def plot_histogram(img, title="Histogram"):
        """
        Plots the histogram of a grayscale image.
        :param img: Grayscale image (2D array)
        :param title: Title of the histogram plot
        """
        plt.figure(figsize=(6, 4))
        plt.hist(img.ravel(), bins=256, range=[0, 256], color='black')
        plt.title(title)
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.grid(False)
        st.pyplot(plt)
        plt.clf()  # Clear the plot after displaying it to avoid overlap

    


    # Load image
    def load_image():
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file))  # Convert to grayscale
            st.image(image, caption="Uploaded Image",  use_container_width=True)
            return image
        else:
            st.warning("Please upload an image to proceed.")
            return None

    st.title('Image Enhancement Histogram Equalization')
    
    image = load_image()

    tab1, tab2,tab3,tab4 = st.tabs(["Histogram Equalization", ])

    # Load image once for all tabs

    if image is not None:
        with tab1:
            st.header("Histogram Equalization")
    
            if st.button("Apply Histogram Equalization", key="apply_histogram_eq"):
                new_image = histogram_equalization(image)
                
                # Display the equalized image
                st.image(new_image, caption="Image after Histogram Equalization", use_column_width=True)
                
                # Display the histogram of the equalized image
                plot_histogram(new_image, title="Histogram after Equalization")
        with tab3:
           
               
        with tab4:
            

        with tab2:
          
