import streamlit as st
from utils.text_extractor import *
import io


def index_page():
    # Streamlit app interface
    st.title("Convertir une image manuscrite et la placer sur un fond")

    # Upload images
    uploaded_text_file = st.file_uploader("Choisissez une image de texte", type=["png", "jpg", "jpeg"])
    uploaded_bg_file = st.file_uploader("Choisissez une image de fond", type=["png", "jpg", "jpeg"])

    # Slider for threshold, erosion, dilation, and position
    threshold = st.slider("Ajustez le seuil", min_value=0, max_value=255, value=128)
    x_position = st.slider("Position X", min_value=0, max_value=1000, value=50)
    y_position = st.slider("Position Y", min_value=0, max_value=1000, value=100)

    # Slider for scale factor (to maintain aspect ratio)
    scale_factor = st.slider("Facteur d'échelle", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

    if uploaded_text_file:
        # Load images
        text_image = Image.open(uploaded_text_file)
        if uploaded_bg_file:
            background_image = Image.open(uploaded_bg_file)

        # Convert the text image to black and white, apply erosion and dilation
        bw_image = convert_image_to_black_white_mask(text_image, threshold=threshold)

        # Convert white to transparent
        transparent_text_image = convert_white_to_transparent(bw_image)

        if uploaded_bg_file:
            # Place text image on background with aspect ratio
            final_image = place_text_image_on_background_with_aspect_ratio(transparent_text_image, background_image,
                                                                           (x_position, y_position), scale_factor)

        else:
            final_image = transparent_text_image

        # Display result
        st.subheader("Image finale")
        st.image(final_image, caption="Image avec texte sur fond", use_column_width=True)

        # Add an option to download the final image
        st.subheader("Télécharger l'image finale")

        # Save the final image to a BytesIO object
        img_byte_arr = io.BytesIO()
        final_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Create a download button
        st.download_button(
            label="Télécharger l'image",
            data=img_byte_arr,
            file_name="image_finale.png",
            mime="image/png"
        )