import streamlit as st
import json
import os
import requests
from groq import Groq

def generate_bdd_swagger(swagger_data):
    #response = requests.get(url)
    #response.raise_for_status()
    #swagger_data = yaml.dump(response.json())
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)
    prompt = f"""
    Using the following Swagger API definition, generate BDD test scenarios using the Gherkin syntax:
    {swagger_data}
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
def generate_bdd_from_text(requirements):

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)
    prompt = f"""
    use {requirements} to generate BDD test scenarios using the Gherkin syntax:    
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")

# Streamlit app
st.title("Jira BDD Test Case Generator")
st.subheader("Upload a txt Document")

# File uploader for Swagger JSON
uploaded_file = st.file_uploader("Upload requirment document file", type=["txt"])

if uploaded_file is not None:
    try:

        # Read the uploaded text file
        requirements = uploaded_file.read().decode("utf-8").splitlines()


       # Validate the requirements
        if not requirements:
            st.error("The uploaded file is empty. Please upload a valid requirement document.")
        else:
            # Generate BDD test cases
            #output_dir = "generated_bdd_test_cases"
            test_cases = generate_bdd_from_text(requirements)
            st.text('Test cases generated successfully!')
            st.code(test_cases)
            #st.success(f"BDD test cases generated successfully! Check the '{output_dir}' directory.")
            #st.text(f"Generated test cases for {len(swagger_json.get('paths', {}))} endpoints.")
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid Swagger JSON document.")
    except Exception as e:
        st.error(f"An error occurred while processing the Swagger JSON: {e}")
else:
    st.info("Please upload a Swagger JSON file to generate test cases.")