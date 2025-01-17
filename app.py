import streamlit as st
from PIL import Image
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Function to load Gemini pro vision model and get response
def get_gemini_response(input_template,image,input_prompt):
  # loading the gemini model
  model=genai.GenerativeModel("gemini-1.5-flash")

  response= model.generate_content([input_template,image[0],input_prompt])
  return response.text


def input_image_setup(uploaded_file):
  if uploaded_file is not None:
    
    bytes_data = uploaded_file.getvalue() # read the image file in bytes
    
    image_parts = [
      {
        "mime_type": uploaded_file.type,
        "data": bytes_data
      }
    ]
    
    return image_parts
  else:
    raise FileNotFoundError("No image uploaded")
  
  
  
##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit=st.button("Tell me about the image")



input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """


## If ask button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)