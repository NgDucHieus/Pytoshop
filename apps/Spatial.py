import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def app():
    # Function for applying different spatial filters
    @st.cache_data
    def apply_filter(image, filter_type):
        if filter_type == "Mean Filter":
            kernel = np.ones((3, 3), np.float32) / 9
            filtered_image = cv2.filter2D(image, -1, kernel)

        elif filter_type == "Gaussian Filter":
            filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

        elif filter_type == "Laplacian Filter":
            laplacian = cv2.Laplacian(image, cv2.CV_64F)
            filtered_image = cv2.convertScaleAbs(laplacian)

        elif filter_type == "Unsharp Masking":
            gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
            filtered_image = cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)

        elif filter_type == "Median Filter":
            filtered_image = cv2.medianBlur(image, 5)

        elif filter_type == "Max Filter":
            kernel = np.ones((5, 5), np.uint8)
            filtered_image = cv2.dilate(image, kernel)

        elif filter_type == "Min Filter":
            kernel = np.ones((5, 5), np.uint8)
            filtered_image = cv2.erode(image, kernel)

        return filtered_image

    # Function to load image
    def load_image():
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file).convert('L'))  # Convert to grayscale
            st.image(image, caption="Uploaded Image (Grayscale)", use_container_width=True)
            return image
        else:
            st.warning("Please upload an image to proceed.")
            return None

    st.title('Image Enhancement: Spatial Filtering')

    image = load_image()

    if image is not None:
        # Tabbed interface for different filters
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Mean Filter", 
            "Gaussian Filter", 
            "Laplacian Filter", 
            "Unsharp Masking", 
            "Median Filter", 
            "Max Filter", 
            "Min Filter"
        ])

        with tab1:
            st.header("Mean Filter")
            if st.button("Apply Mean Filter", key="mean_filter"):
                filtered_image = apply_filter(image, "Mean Filter")
                st.image(filtered_image, caption="Image after Mean Filter", use_container_width=True)

        with tab2:
            st.header("Gaussian Filter")
            if st.button("Apply Gaussian Filter", key="gaussian_filter"):
                filtered_image = apply_filter(image, "Gaussian Filter")
                st.image(filtered_image, caption="Image after Gaussian Filter", use_container_width=True)

        with tab3:
            st.header("Laplacian Filter")
            if st.button("Apply Laplacian Filter", key="laplacian_filter"):
                filtered_image = apply_filter(image, "Laplacian Filter")
                st.image(filtered_image, caption="Image after Laplacian Filter", use_container_width=True)

        with tab4:
            st.header("Unsharp Masking")
            if st.button("Apply Unsharp Masking", key="unsharp_masking"):
                filtered_image = apply_filter(image, "Unsharp Masking")
                st.image(filtered_image, caption="Image after Unsharp Masking", use_container_width=True)

        with tab5:
            st.header("Median Filter")
            if st.button("Apply Median Filter", key="median_filter"):
                filtered_image = apply_filter(image, "Median Filter")
                st.image(filtered_image, caption="Image after Median Filter", use_container_width=True)

        with tab6:
            st.header("Max Filter")
            if st.button("Apply Max Filter", key="max_filter"):
                filtered_image = apply_filter(image, "Max Filter")
                st.image(filtered_image, caption="Image after Max Filter", use_container_width=True)

        with tab7:
            st.header("Min Filter")
            if st.button("Apply Min Filter", key="min_filter"):
                filtered_image = apply_filter(image, "Min Filter")
                st.image(filtered_image, caption="Image after Min Filter", use_container_width=True)
