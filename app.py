from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini with the latest model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input,pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


# Function to convert PDF to images and base64-encode them
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Convert the entire PDF to images (all pages)
            # Explicitly provide the poppler_path
            poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
            
            
            # List to hold encoded images
            pdf_parts = []

            for image in images:
                # Convert each page to bytes
                img_byte_arr=io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_byte_arr=img_byte_arr.getvalue()

                # Append each page's base64-encoded image
                pdf_parts.append({
                    'mime_type': "image/jpeg",
                    'data': base64.b64encode(img_byte_arr).decode() # encode to base64
                })

                return pdf_parts
            
        except Exception as e:
            st.error(f"Error processing PDF file: {e}")
            return None
        

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input job description

input_text=st.text_area("Job Description: ", key="input")

# Upload Resume PDF

uploaded_file=st.file_uploader("Upload your resume (PDF)...", type=['pdf'])


if uploaded_file:
    st.write("PDF Uploaded Successfully")


# Define submit buttons
submit1=st.button("Tell me about Resume")

submit2=st.button("Percentage Match")


# Input prompts for model guidance
input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job 
"""

# Process when "Tell Me About the Resume" button is clicked

if submit1:
    if uploaded_file and input_text:
        try:
            pdf_content=input_pdf_setup(uploaded_file)
            if pdf_content:
                response=get_gemini_response(input_text,pdf_content,input_prompt1)
                st.subheader("The Response is...")
                st.write(response)
                
        except Exception as e:
            st.error(f"Error processing the resume: {e}")
    else:
        st.error("Please upload a resume and enter the job description.")



# Process when "Percentage Match" button is clicked
elif submit2:
    if uploaded_file and input_text:
        try:
            pdf_content=input_pdf_setup(uploaded_file)
            if pdf_content:
                response=get_gemini_response(input_text, pdf_content, input_prompt2)
                st.subheader("The Resopnse is...")
                st.write(response)

        except Exception as e:
            st.error(f"Error processing the resume {e}")

    else:
        st.error("Please upload a resume and enter the job description.")                     




    


