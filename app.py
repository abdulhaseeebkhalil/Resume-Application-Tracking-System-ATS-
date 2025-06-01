from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Set page config must be the first Streamlit command
st.set_page_config(page_title="ATS Resume EXpert")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
       background-color: #FEF3E2;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.9);
    }
    .stFileUploader > div > div {
        background-color: rgba(255, 255, 255, 0.9);
    }
    /* Custom styling for expander */
    .streamlit-expanderHeader {
        background-color: #4CAF50 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    .streamlit-expanderContent {
        background-color: white !important;
        padding: 20px !important;
        border-radius: 5px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

# def get_gemini_response(input_prompt, pdf_content, input_text):
#     response = genai.generate_text(
#         model="models/gemini-1.5-flash",
#         prompt=f"{input_prompt} {input_text} {pdf_content[0]['data']}"
#     )
#     return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Create two columns for buttons
col1, col2 = st.columns(2)

with col1:
    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("How Can I Improve my Skills")
    submit3 = st.button("Percentage match")
    submit4 = st.button("How Well Do I Fit?")
    submit5 = st.button("Highlight Key Achievements")

with col2:
    submit6 = st.button("Suggest Certifications")
    submit7 = st.button("Assess Leadership Potential")
    submit8 = st.button("Identify Transferable Skills")
    submit9 = st.button("New resume with highlights")
    submit10 = st.button("Write a cover letter for the job description")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a highly experienced Career Coach with expertise in skill development and professional growth. 
Your task is to analyze the candidate's resume in the context of the job description and provide actionable advice. 
Suggest specific skills, certifications, or experiences the candidate should focus on to better align with the job requirements. 
Highlight areas where the candidate excels and where there is room for improvement.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt4 = """
You are a professional Career Advisor with expertise in evaluating candidate fit for specific roles. 
Your task is to analyze the resume and job description to determine how well the candidate fits the role. 
Provide a detailed breakdown of alignment across skills, experience, and other job requirements. 
Conclude with a rating out of 10 that reflects the overall fit of the candidate for the role.
"""

input_prompt5 = """
You are a seasoned Resume Analyst. Your task is to extract and highlight the candidate's most significant achievements 
from their resume in the context of the job description. Focus on accomplishments that align strongly with the role 
and showcase measurable impacts.
"""

input_prompt6 = """
You are a Career Development Expert specializing in certifications and training programs. Your task is to analyze the 
resume and job description to recommend certifications that would enhance the candidate's qualifications for this role. 
Focus on industry-recognized certifications that are most relevant to the position.
"""

input_prompt7 = """
You are an HR Manager with extensive experience in leadership assessment. Your task is to evaluate the resume to determine 
the candidate's leadership potential based on their experiences, achievements, and skills. Provide a detailed assessment 
and examples from the resume that demonstrate leadership qualities.
"""

input_prompt8 = """
You are a Career Transition Specialist. Your task is to identify transferable skills from the candidate's resume that 
can be applied effectively to the specified job role. Highlight skills that are versatile and demonstrate adaptability.
"""

input_prompt9 = """
You are a Resume Analyst with expertise in resume writing. Your task is to rewrite the resume in a way that highlights the candidate's 
strengths and achievements in the context of the job description. Ensure the resume is formatted professionally and is easy to read.
"""

input_prompt10 = """
You are a Cover Letter Expert. Your task is to write a cover letter for the candidate based on the job description. 
Ensure the cover letter is tailored to the specific job and is formatted professionally and is easy to read.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        with st.expander("Analysis Results", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")
        
if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        with st.expander("Skills Improvement Suggestions", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")


if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        with st.expander("Resume Match Analysis", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")
        
if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        with st.expander("Role Fit Assessment", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")
        
if submit5:  
    if uploaded_file is not None:  
        pdf_content = input_pdf_setup(uploaded_file)  
        response = get_gemini_response(input_prompt5, pdf_content, input_text)  
        with st.expander("Key Achievements", expanded=True):
            st.markdown(response)
    else:  
        st.warning("Please upload the resume")  
if submit6:  
    if uploaded_file is not None:  
        pdf_content = input_pdf_setup(uploaded_file)  
        response = get_gemini_response(input_prompt6, pdf_content, input_text)  
        with st.expander("Certification Recommendations", expanded=True):
            st.markdown(response)
    else:  
        st.warning("Please upload the resume")  
if submit7:  
    if uploaded_file is not None:  
        pdf_content = input_pdf_setup(uploaded_file)  
        response = get_gemini_response(input_prompt7, pdf_content, input_text)  
        with st.expander("Leadership Assessment", expanded=True):
            st.markdown(response)
    else:  
        st.warning("Please upload the resume")  
if submit8:  
    if uploaded_file is not None:  
        pdf_content = input_pdf_setup(uploaded_file)  
        response = get_gemini_response(input_prompt8, pdf_content, input_text)  
        with st.expander("Transferable Skills Analysis", expanded=True):
            st.markdown(response)
    else:  
        st.warning("Please upload the resume")  
if submit9:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt9, pdf_content, input_text)
        with st.expander("Enhanced Resume", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")
elif submit10:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt10, pdf_content, input_text)
        with st.expander("Cover Letter", expanded=True):
            st.markdown(response)
    else:
        st.warning("Please upload the resume")
