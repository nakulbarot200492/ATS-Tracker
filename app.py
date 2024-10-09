from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PyPDF2 import PdfReader
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini with the latest model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

# Function to extract text from PDF using PyPDF2
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_reader = PdfReader(uploaded_file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() or ""

            return text_content.strip()  # Return extracted text

        except Exception as e:
            st.error(f"Error processing PDF file: {e}")
            return None
    else:
        st.error("No file uploaded")
        return None

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input job description
input_text = st.text_area("Job Description: ", key="input")

# Upload Resume PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=['pdf'])

if uploaded_file:
    st.write("PDF Uploaded Successfully")

# Define submit buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Input prompts for model guidance
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as percentage, then keywords missing, and last final thoughts.
"""

# Process when "Tell Me About the Resume" button is clicked
if submit1:
    if uploaded_file and input_text:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_text, pdf_content, input_prompt1)
                st.subheader("The Response is...")
                st.write(response)
                
        except Exception as e:
            st.error(f"Error processing the resume: {e}")
    else:
        st.error("Please upload a resume and enter the job description.")

# Process when "Percentage Match" button is clicked
elif submit3:
    if uploaded_file and input_text:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_text, pdf_content, input_prompt3)
                st.subheader("The Response is...")
                st.write(response)

        except Exception as e:
            st.error(f"Error processing the resume: {e}")

    else:
        st.error("Please upload a resume and enter the job description.")




   





