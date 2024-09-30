import streamlit as st
from PIL import Image
from utils.text_extractor import convert_image_to_black_white_mask


def index_page():
    # Streamlit app interface
    st.title("Convertir une image manuscrite en masque noir et blanc")

    # Upload image
    uploaded_file = st.file_uploader("Choisissez une image", type=["png", "jpg", "jpeg"])

    # Slider for threshold
    threshold = st.slider("Ajustez le seuil", min_value=0, max_value=255, value=128)

    if uploaded_file is not None:
        # Load the image
        image = Image.open(uploaded_file)

        # Display original image
        st.subheader("Image originale")
        st.image(image, caption="Image originale importée", use_column_width=True)

        # Convert to black and white mask
        bw_image = convert_image_to_black_white_mask(image, threshold=threshold)

        # Display result
        st.subheader("Image en noir et blanc")
        st.image(bw_image, caption="Masque noir et blanc généré", use_column_width=True)