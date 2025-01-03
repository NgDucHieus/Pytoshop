import streamlit as st
import numpy as np
from PIL import Image
import cv2

def app():
    DEMO_IMAGE = 'imgs/hieu.jpeg'

    # Function for Linear Transformation
    @st.cache_data
    def linear_transformation(img, g_min, g_max):
        f_min, f_max = np.min(img), np.max(img)
        stretched = (img - f_min) * ((g_max - g_min) / (f_max - f_min)) + g_min
        return np.clip(stretched, g_min, g_max).astype(np.uint8)

    # Function for Logarithmic Transformation
    @st.cache_data
    def logarithmic_transformation(img):
        c = 255 / (np.log(1 + np.max(img)))
        log_img = c * np.log(1 + img)
        return np.clip(log_img, 0, 255).astype(np.uint8)

    # Function for Power Law Transformation (Gamma Correction)
    @st.cache_data
    def power_law_transformation(img, gamma):
        img_normalized = img / 255.0
        gamma_corrected = np.power(img_normalized, gamma)
        return (gamma_corrected * 255).astype(np.uint8)

    # Function for Thresholding
    @st.cache_data
    def thresholding(img, threshold):
        _, thresh_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return thresh_img
    # Function for Piecewise Linear Transformation (Gray-level Slicing)
    @st.cache_data
    def gray_level_slicing(img, low, high, max_intensity=255, with_background=True):
        if img is None:
            return None  # Return None if input image is invalid

        sliced_img = img.copy()
        if with_background:
            # With background: Set pixels within range to max intensity, leave others unchanged
            sliced_img[(img >= low) & (img <= high)] = max_intensity
        else:
            # Without background: Set pixels within range to max intensity, others to 0
            sliced_img[(img < low) | (img > high)] = 0
            sliced_img[(img >= low) & (img <= high)] = max_intensity

        return sliced_img

    # Function for Bit Plane Slicing
    @st.cache_data
    def bit_plane_slicing(img, bit_plane):
        """
        Extracts a specific bit plane from the image.
        :param img: Grayscale image (2D array)
        :param bit_plane: Bit plane to extract (0 = LSB, 7 = MSB)
        :return: Image representing the selected bit plane
        """
        bit_mask = 1 << bit_plane
        sliced_img = (img & bit_mask) >> bit_plane
        return (sliced_img * 255).astype(np.uint8)





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

    st.title('Image Enhancement Point Processing')
    # image = load_image()

    # # Create tabs
    # tab1, tab2, tab3, tab4,tab5,tab6= st.tabs(["Linear Transformation", 
    #                                   "Logarithmic Transformation", 
    #                                   "Power Law Transformation", 
    #                                   "Thresholding","Piecewise Linear Transformation (Gray-level Slicing)","Bit Plane Slicing"])

    # # Load image once for all tabs

    # if image is not None:
    #     with tab1:
    #         st.header("Linear Transformation")
    #         g_min = st.slider("Select Minimum Output Intensity", 0, 255, 0, key="linear_g_min")
    #         g_max = st.slider("Select Maximum Output Intensity", 0, 255, 255, key="linear_g_max")
    #         if st.button("Apply Linear Transformation", key="apply_linear"):
    #             new_image = linear_transformation(image, g_min, g_max)
    #             st.image(new_image, caption="Image after Linear Transformation",  use_container_width=True)
    #     # Code for Piecewise Linear tab
    #     # with tab5:  # Assuming tab5 is created in st.tabs()
    #     #     st.header("Piecewise Linear Transformation (Gray-level Slicing)")
    #     #     low = st.slider("Select Low Intensity Range", 0, 255, 50, key="slicing_low")
    #     #     high = st.slider("Select High Intensity Range", 0, 255, 150, key="slicing_high")
    #     #     with_background = st.checkbox("With Background", value=True, key="slicing_bg")
    #     #     if st.button("Apply Gray-level Slicing", key="apply_slicing"):
    #     #         new_image = gray_level_slicing(image, low, high, max_intensity=255, with_background=with_background)
    #     #         st.image(new_image, caption="Image after Gray-level Slicing", use_column_width=True)
    #     with tab2:
    #         st.header("Logarithmic Transformation")
    #         if st.button("Apply Logarithmic Transformation", key="apply_log"):
    #             new_image = logarithmic_transformation(image)
    #             st.image(new_image, caption="Image after Logarithmic Transformation",  use_container_width=True)

    #     with tab3:
    #         st.header("Power Law Transformation (Gamma Correction)")
    #         gamma = st.slider("Select Gamma Value", 0.1, 5.0, 1.0, key="gamma_slider")
    #         if st.button("Apply Power Law Transformation", key="apply_power_law"):
    #             new_image = power_law_transformation(image, gamma)
    #             st.image(new_image, caption="Image after Power Law Transformation",  use_container_width=True)

    #     with tab4:
    #         st.header("Thresholding")
    #         threshold_value = st.slider("Select Threshold Value", 0, 255, 128, key="threshold_slider")
            
    #         new_image = thresholding(image, threshold_value)
    #         st.image(new_image, caption="Image after Thresholding",  use_container_width=True)

    #                 # Code for Piecewise Linear tab
    #     with tab5:  # Assuming tab5 is created in st.tabs()
    #         st.header("Piecewise Linear Transformation (Gray-level Slicing)")
    #         low = st.slider("Select Low Intensity Range", 0, 255, 50, key="slicing_low")
    #         high = st.slider("Select High Intensity Range", 0, 255, 150, key="slicing_high")
    #         with_background = st.checkbox("With Background", value=True, key="slicing_bg")
    #         if st.button("Apply Gray-level Slicing", key="apply_slicing"):
    #             new_image = gray_level_slicing(image, low, high, max_intensity=255, with_background=with_background)
    #             pil_image = Image.fromarray(new_image)  # Convert NumPy array to PIL image
    #             st.image(pil_image, caption="Image after Gray-level Slicing", use_column_width=True)
    #     # Code for Bit Plane Slicing tab
    #     with tab6:  # Assuming tab6 is created in st.tabs()
    #         st.header("Bit Plane Slicing")
            
    #         bit_plane = st.slider("Select Bit Plane (0 = LSB, 7 = MSB)", 0, 7, 0, key="bit_plane_slider")
            
    #         if st.button("Apply Bit Plane Slicing", key="apply_bit_plane"):
    #             new_image = bit_plane_slicing(image, bit_plane)
    #             st.image(new_image, caption=f"Image after Bit Plane Slicing (Bit Plane {bit_plane})", use_column_width=True)

# Create grouped tabs
    image = load_image()

    tab1, tab2,tab3,tab4 = st.tabs(["Grey Level Transformation", "Thresholding","Piecewise Linear (Gray-level Slicing)","Bit Plane Slicing"])

    # Load image once for all tabs

    if image is not None:
        with tab1:
            st.header("Grey Level Transformation")
            transformation = st.radio("Select a Transformation", 
                                      ["Linear Transformation", "Logarithmic Transformation", "Power Law Transformation"])

            if transformation == "Linear Transformation":
                g_min = st.slider("Select Minimum Output Intensity", 0, 255, 0, key="linear_g_min")
                g_max = st.slider("Select Maximum Output Intensity", 0, 255, 255, key="linear_g_max")
                
                new_image = linear_transformation(image, g_min, g_max)
                st.image(new_image, caption="Image after Linear Transformation", use_column_width=True)

            elif transformation == "Logarithmic Transformation":
               
                new_image = logarithmic_transformation(image)
                st.image(new_image, caption="Image after Logarithmic Transformation", use_column_width=True)

            elif transformation == "Power Law Transformation":
                gamma = st.slider("Select Gamma Value", 0.1, 5.0, 1.0, key="gamma_slider")
                
                new_image = power_law_transformation(image, gamma)
                st.image(new_image, caption="Image after Power Law Transformation", use_column_width=True)
        with tab3:
            st.header("Piecewise Linear (Gray-level Slicing)")
            low = st.slider("Select Low Intensity Range", 0, 255, 50, key="slicing_low")
            high = st.slider("Select High Intensity Range", 0, 255, 150, key="slicing_high")
            with_background = st.checkbox("With Background", value=True, key="slicing_bg")
           
            new_image = gray_level_slicing(image, low, high, max_intensity=255, with_background=with_background)
            st.image(new_image, caption="Image after Gray-level Slicing", use_column_width=True)

               
        with tab4:
            st.header("Bit Plane Slicing")
            bit_plane = st.slider("Select Bit Plane (0 = LSB, 7 = MSB)", 0, 7, 0, key="bit_plane_slider")
            new_image = bit_plane_slicing(image, bit_plane)
            st.image(new_image, caption=f"Image after Bit Plane Slicing (Bit Plane {bit_plane})", use_column_width=True)

        with tab2:
            st.header("Thresholding")
           
          
            threshold_value = st.slider("Select Threshold Value", 0, 255, 128, key="threshold_slider")
            new_image = thresholding(image, threshold_value)
            st.image(new_image, caption="Image after Thresholding", use_column_width=True)
