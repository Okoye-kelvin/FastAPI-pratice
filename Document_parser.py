import streamlit as st
import openai
import json


def extract_applicant_details(resume_text,api_key):
    openai.api_key = api_key

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a resume-parsing assistant."},
            {"role": "user", "content": f"Extract the name, email, skills, and years of experience from this resume:\n\n{resume_text}"}
        ],
        functions=[
            {
                "name": "extract_details",
                "description": "Extract applicant details from a resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "experience_years": {"type": "number"}
                    },
                    "required": ["name", "email", "skills", "experience_years"]
                }
            }
        ],
        function_call={"name": "extract_details"}
    )

    return json.loads(response.choices[0].message.function_call.arguments)


# STREAMLIT INTERFACE
st.set_page_config(page_title="AI Document Parser", layout="centered")
st.title("📄 AI Resume Parser")

st.info("Paste your OpenAI API Key and a resume to extract name, email, skills, and experience.", icon="ℹ️")

api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
resume_text = st.text_area("📝 Paste Resume Text Here", height=250)

if st.button("Extract Details"):
    if not api_key or not resume_text:
        st.warning("Please provide both an API key and resume text.")
    else:
        try:
            details = extract_applicant_details(resume_text, api_key)
            st.success("✅ Applicant Details Extracted:")
            st.json(details)
        except Exception as e:
            st.error(f"❌ Error: {e}")
