from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
import fitz 
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")


st.set_page_config(page_title="ATS Resume Expert 📖", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stTextArea, .stButton {
            margin-bottom: 15px;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

st.title("ATS Resume Expert 📖")
st.write("Optimize your resume to match the job description and increase your chances of landing an interview.")


def get_gemini_response(input_text, pdf_content, prompt):
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = pdf_doc[0]
        pix = page.get_pixmap()
        
        img_bytes_arr = io.BytesIO()
        img_bytes_arr.write(pix.tobytes("png"))
        
        pdf_part = [
            {
                "mime_type": "image/png",
                "data": base64.b64encode(img_bytes_arr.getvalue()).decode()
            }
        ]
        
        return pdf_part
    else:
        raise FileNotFoundError("No file uploaded")

st.markdown("### 📄 Job Description")
input_text = st.text_area("Enter the job description...", height=150, key="input_text")

st.markdown("### 📂 Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume file uploaded successfully!")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    submit1 = st.button("Generate Resume Summary")
with col2:
    submit2 = st.button("Suggest Skill Improvements")
with col3:
    submit3 = st.button("Identify Missing Keywords")
with col4:
    submit4 = st.button("Check ATS Match Percentage")

# Define prompts
input_prompt1 = """
Please analyze the provided resume and generate a comprehensive summary. 
Highlight the candidate's key strengths, relevant experiences, notable achievements, and core skills. Additionally,
provide insights on the candidate's overall profile quality, including any standout features that make them a strong fit for roles in their field. If possible, also comment on areas where the resume could be enhanced to better align with provided job description.
""" 

input_prompt2 = """
Review the provided resume and suggest areas for skill improvement that would enhance the candidate's qualifications. Identify any in-demand skills or certifications relevant to their field that are missing or could be strengthened. Additionally, provide recommendations on practical steps, courses, or experiences the candidate could pursue to further develop their expertise and make their profile more competitive.
"""

input_prompt3 = """
Examine the provided resume and identify any important keywords, skills, or industry-specific terms that may be missing according to the provided job description. Suggest additional keywords or phrases that would make the resume more aligned with job descriptions and improve its relevance for applicant tracking systems (ATS) and recruiters.
"""

input_prompt4 = """
You are a skilled ATS (applicant tracking system) scanner with a deep understanding of the job description and the resume. Your task is to evaluate the resume and the job description and provide the percentage match of the resume with the job description. First, output the result as a percentage and then list the keywords missing in the resume according to the job description.
"""

if submit1:
    if input_text == "":
        st.error("Please enter the job description.")
    elif uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("📋 Resume Summary")
        st.write(response)

if submit2:
    if input_text == "":
        st.error("Please enter the job description.")
    elif uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("💡 Skill Improvement Suggestions")
        st.write(response)

if submit3:
    if input_text == "":
        st.error("Please enter the job description.")
    elif uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("🔑 Missing Keywords")
        st.write(response)

if submit4:
    if input_text == "":
        st.error("Please enter the job description.")
    elif uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("📊 ATS Match Percentage")
        st.write(response)

st.markdown("---")
st.markdown("Thank you for using **ATS Resume Expert**! Improve your resume and enhance your job search experience! 🔍")
