from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("google_API_key"))

model = genai.GenerativeModel('gemini-1.5-flash')

#Getting response from gemini
def get_gemini_respones(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file): # Get the image information in bytes format
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type, #Type of uploaded_file
                "data": bytes_data 
            }
        ]
        return image_parts 
    else:
        raise FileNotFoundError("No file uploaded")

# Configuring Streamlit
st.set_page_config(page_title = "Multi-Language Invoice Extractor")
st.header("Multi-Language Invoice Extractor")
input = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("Choose an Image...", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
submit = st.button("Tell me about the Invoice")

#Sample input_prompt
input_prompt = """You are an expert in understanding invoices. We will upload an image of invoice and you have to answer my questions based on that uploaded image of invoice."""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_respones(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)