import streamlit as st
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

def app():
    DEMO_IMAGE = 'imgs/hieu.jpeg'

    # Function for Histogram Equalization
    @st.cache_data
    def histogram_equalization(image_array):
        if len(image_array.shape) == 3:  # Convert to grayscale if needed
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        
        equalized_img = cv2.equalizeHist(image_array)
        return equalized_img

    # Function to plot histogram
    def plot_histogram(img, title="Histogram"):
        plt.figure(figsize=(6, 4))
        plt.hist(img.ravel(), bins=256, range=[0, 256], color='black')
        plt.title(title)
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.grid(False)
        st.pyplot(plt)
        plt.clf()  # Clear the plot after displaying it to avoid overlap

    # Function for Histogram Matching
    @st.cache_data
    def histogram_matching(source_image, reference_image):
        source_values, source_counts = np.unique(source_image.ravel(), return_counts=True)
        reference_values, reference_counts = np.unique(reference_image.ravel(), return_counts=True)

        source_cdf = np.cumsum(source_counts).astype(np.float64)
        source_cdf /= source_cdf[-1]

        reference_cdf = np.cumsum(reference_counts).astype(np.float64)
        reference_cdf /= reference_cdf[-1]

        mapping = np.interp(source_cdf, reference_cdf, reference_values)
        matched_image = np.interp(source_image.ravel(), source_values, mapping)
        matched_image = matched_image.reshape(source_image.shape).astype(np.uint8)

        return matched_image

    # Load image
    def load_image():
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file))  # Convert to grayscale
            st.image(image, caption="Uploaded Image (Grayscale)", use_container_width=True)
            return image
        else:
            st.warning("Please upload an image to proceed.")
            return None

    st.title('Image Enhancement: Histogram Equalization and Matching')
    
    image = load_image()

    tab1, tab2 = st.tabs(["Histogram Equalization", "Histogram Matching"])

    # Check if image is uploaded
    if image is not None:
        with tab1:
            st.header("Histogram Equalization")
    
            if st.button("Apply Histogram Equalization", key="apply_histogram_eq"):
                new_image = histogram_equalization(image)
                
                # Display the equalized image
                st.image(new_image, caption="Image after Histogram Equalization", use_column_width=True)
                
                # Display the histogram of the equalized image
                plot_histogram(new_image, title="Histogram after Equalization")

        with tab2:
            st.header("Histogram Matching")

            reference_file = st.file_uploader("Upload a Reference Image", type=["jpg", "jpeg", "png"], key="reference")
            
            if reference_file is not None:
                reference_image = np.array(Image.open(reference_file).convert('L'))  # Convert to grayscale
                st.image(reference_image, caption="Reference Image (Grayscale)", use_container_width=True)

                if st.button("Apply Histogram Matching", key="apply_histogram_match"):
                    matched_image = histogram_matching(image, reference_image)
                    
                    # Display the histogram matched image
                    st.image(matched_image, caption="Image after Histogram Matching", use_column_width=True)
                    
                    # Display the histogram of the matched image
                    plot_histogram(matched_image, title="Histogram after Matching")
            else:
                st.warning("Please upload a reference image to proceed.")
