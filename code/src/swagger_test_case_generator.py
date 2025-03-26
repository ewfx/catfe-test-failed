import streamlit as st
import os
from swagger import generate_bdd_swagger
st.subheader('Provide Swagger URL')
swagger_url = st.text_input('Enter the Swagger URL for your REST APIs:')
st.text('Please provide a valid Swagger URL to generate automation test cases.')
if st.button('Generate BDD Test Cases'):
    if swagger_url:
    # Call the generate_api_test_cases function from wgprt.py
        try:
            api_test_cases = generate_bdd_swagger(swagger_url)
            st.text('API test cases generated successfully!')
            st.code(api_test_cases)  # Display the generated API test cases
        except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error('Please provide a valid Swagger URL before generating API test cases.')