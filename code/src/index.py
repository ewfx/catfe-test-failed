import streamlit as st
import os
# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "index"  # Default page

# Get the base directory dynamically
base_dir = os.path.dirname(__file__)  # Directory of the current script



# Placeholder content for the WGPRT page
st.title("Welcome to the WGPRT Tool")
st.header("WGPRT - WF Generative Payment Rail Testing Tool")

# Navigation buttons to update session state

# Render content based on the selected page
if st.session_state.page == "index":
    #st.subheader("Index Page Content")
    try:
         # Dynamically construct the file path for test_case_generator.py
        file_path = os.path.join(base_dir, "test_generator.py")
        with open(file_path) as f:
            code = f.read()
            exec(code)  # Dynamically execute the code from index.py
    except FileNotFoundError:
        st.error("The index.py file was not found.")
    except Exception as e:
        st.error(f"An error occurred while including index.py: {e}")
