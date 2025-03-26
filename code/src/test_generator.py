import streamlit as st
import os
#from test_case_generator import main as test_case_generator_main
#from api_test_case_generator import main as api_test_case_generator_main
#from jira_test_case_generator import main as jira_test_case_generator_main
# Get the base directory dynamically
base_dir = os.path.dirname(__file__)  # Directory of the current script
# Set up the horizontal menu
#st.title("Test Case Generator")
# Sidebar menu
#with st.sidebar:
   # st.header("Navigation")  # Sidebar title
   # menu = ["XSD Case Generator", "API Test Case Generator", "Jira Test Case Generator"]
   # choice = st.radio("Select a  Tool that generate BDD Test cases", menu)

# Sidebar parent menu
with st.sidebar:
    st.header("Main Navigation")  # Sidebar title
    parent_menu = ["Test Case Generators", "Fraudulent Detection","Loan Approval"]
    parent_choice = st.radio("Select a Section", parent_menu)

# Render content based on the selected parent menu
if parent_choice == "Test Case Generators":
    #st.title("Test Case Generators")
    # Sidebar sub-menu for Test Case Generators
    with st.sidebar:
        st.header("Test Case Tools")
        menu = ["XSD Case Generator", "API Test Case Generator", "Jira Test Case Generator","Swagger URL - Test Case Generator"]
        choice = st.radio("Select a Tool", menu)

    # Render the selected tool
    if choice == "XSD Case Generator":
        st.subheader("XSD Case Generator")
        try:
            # Dynamically construct the file path for test_case_generator.py
            file_path = os.path.join(base_dir, "test_case_generator.py")
            with open(file_path) as f:
                code = f.read()
                exec(code)  # Dynamically execute the code from index.py
        except FileNotFoundError:
            st.error("The index.py file was not found.")
        except Exception as e:
            st.error(f"An error occurred while including index.py: {e}")
    #test_case_generator_main()
    elif choice == "API Test Case Generator":
        st.subheader("API Test Case Generator")
        try:
            # Dynamically construct the file path for test_case_generator.py
            file_path = os.path.join(base_dir, "api_test_case_generator.py")
            with open(file_path) as f:
                code = f.read()
                exec(code)  # Dynamically execute the code from index.py
        except FileNotFoundError:
            st.error("The index.py file was not found.")
        except Exception as e:
            st.error(f"An error occurred while including index.py: {e}")
    elif choice == "Swagger URL - Test Case Generator":
        st.subheader("Swagger URL Test Case Generator")
        try:
            # Dynamically construct the file path for test_case_generator.py
            file_path = os.path.join(base_dir, "swagger_test_case_generator.py")
            with open(file_path) as f:
                code = f.read()
                exec(code)  # Dynamically execute the code from index.py
        except FileNotFoundError:
            st.error("The index.py file was not found.")
        except Exception as e:
            st.error(f"An error occurred while including index.py: {e}")
    #api_test_case_generator_main()
    elif choice == "Jira Test Case Generator":
        st.subheader("Jira Test Case Generator")
        try:
            # Dynamically construct the file path for test_case_generator.py
            file_path = os.path.join(base_dir, "jira_test_case_generator.py")
            with open(file_path) as f:
                code = f.read()
                exec(code)  # Dynamically execute the code from index.py
        except FileNotFoundError:
            st.error("The index.py file was not found.")
        except Exception as e:
            st.error(f"An error occurred while including index.py: {e}")
        #jira_test_case_generator_main()
elif parent_choice == "Fraudulent Detection":
    #st.title("Fraudulent Detection")
    #st.subheader("Fraudulent Detection Page Content")
    file_path = os.path.join(base_dir, "fradulent.py")
    try:
        with open(file_path) as f:
            code = f.read()
            exec(code)  # Dynamically execute the code from fraudulent.py
    except FileNotFoundError:
        st.error("The fraudulent.py file was not found.")
    except Exception as e:
        st.error(f"An error occurred while including fraudulent.py: {e}")
elif parent_choice == "Loan Approval":
    #st.title("Loan Approval")
    #st.subheader("Loan Approval Page Content")
    file_path = os.path.join(base_dir, "loan_approval.py")
    try:
        with open(file_path) as f:
            code = f.read()
            exec(code)  # Dynamically execute the code from loan_approval.py
    except FileNotFoundError:
        st.error("The loan_approval.py file was not found.")
    except Exception as e:
        st.error(f"An error occurred while including loan_approval.py: {e}")