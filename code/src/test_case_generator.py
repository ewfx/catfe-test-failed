import streamlit as st
from xsd_swagger_generator import generate_test_cases 
from xsd_swagger_generator import generate_api_test_cases
from swagger import generate_bdd_swagger

#st.title('WGPRT - 1')
#st.header('WF Generative Payment Rail Testing Tool')
#st.text('This tool generates test cases for the Wells Fargo Payment Rail Testing Tool.')

# Create two columns for side-by-side layout
# Createcol1, col2 = st.columns([1, 1])

# First widget: File uploader in the first column
#with col1:
st.subheader('Upload XSD File')
uploaded_file = st.file_uploader('Upload XSD File', type=['xsd'])
st.text('Please upload the XSD file that you would like to generate test cases for.')
# Button to trigger test case generation
if st.button('Generate Test Cases'):
    if uploaded_file is not None:
            # Save the uploaded file to a temporary location
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.getbuffer())

            # Call the generate_test_cases function from wgprt.py
            try:
                test_cases = generate_test_cases(temp_file_path)
                st.text('Test cases generated successfully!')
                st.code(test_cases)  # Display the generated test cases
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                # Clean up the temporary file
                import os
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
    else:
        st.error('Please upload an XSD file before generating test cases.')