import streamlit as st
from PIL import Image
import cv2
import numpy as np
import copy

def app():
    DEMO_IMAGE = 'imgs/Tiger.jpg'

    def load_image(filename):
        image = cv2.imread(filename)
        return image
    
    def photo():
        st.header("Thresholding, Edge Detection and Contours")

        img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if img_file_buffer is not None:
            image = np.array(Image.open(img_file_buffer))
        else:
            demo_image = DEMO_IMAGE
            image = np.array(Image.open(demo_image))

        st.image(image, caption="Original Image", use_container_width=True)

        original = copy.deepcopy(image)

        # Convert image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Thresholding slider
        x = st.slider('Change Threshold value', min_value=50, max_value=255, key='threshold_slider')
        ret, thresh1 = cv2.threshold(image, x, 255, cv2.THRESH_BINARY)
        thresh1 = thresh1.astype(np.float64)
        st.image(thresh1, caption="Thresholded Image", use_container_width=True, clamp=True)

        # Bar chart of the image
        st.subheader("Bar Chart of the Image")
        histr = cv2.calcHist([image], [0], None, [256], [0, 256])
        st.bar_chart(histr)

        # Canny edge detection
        st.subheader("Canny Edge Detection on Image")
        edges = cv2.Canny(image, 50, 300)
        st.image(edges, caption="Edges Detected", use_container_width=True, clamp=True)

        # Contour detection
        st.subheader("Contour Detection on Image")
        y = st.slider('Change Value to Increase or Decrease Contours', 50, 255, 100, key='contour_slider')
        
        imgray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, y, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        img_with_contours = cv2.drawContours(copy.deepcopy(original), contours, -1, (0, 255, 0), 3)

        st.image(thresh, caption="Threshold for Contours", use_container_width=True, clamp=True)
        st.image(img_with_contours, caption="Image with Contours", use_container_width=True, clamp=True)

    photo()
