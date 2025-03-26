import streamlit as st

# Loan scoring function
def calculate_loan_score(credit_score, annual_income, debt_to_income_ratio, employment_status, loan_amount):
    """
    Calculate the loan score based on various parameters.
    """
    # Normalize credit score (300–850 to 0–100)
    credit_score_normalized = (credit_score - 300) / 550 * 100

    # Normalize annual income (assuming max income cap of $500,000)
    max_income = 500000
    annual_income_normalized = min(annual_income / max_income * 100, 100)

    # Debt-to-Income Ratio (lower is better)
    debt_to_income_score = (1 - debt_to_income_ratio) * 100

    # Employment Status Score
    employment_status_score = {
        "Employed": 100,
        "Self-Employed": 80,
        "Unemployed": 0
    }.get(employment_status, 0)

    # Loan Amount vs Income Ratio
    loan_to_income_ratio = loan_amount / annual_income
    if loan_to_income_ratio <= 2:
        loan_to_income_score = 100
    elif loan_to_income_ratio <= 3:
        loan_to_income_score = 80
    else:
        loan_to_income_score = 50

    # Weighted loan score
    loan_score = (
        credit_score_normalized * 0.4 +
        annual_income_normalized * 0.25 +
        debt_to_income_score * 0.2 +
        employment_status_score * 0.1 +
        loan_to_income_score * 0.05
    )

    return round(loan_score, 2)

# Streamlit app
#st.title("Loan Score Evaluation")
st.header("Enter Loan Application Details")

# Input fields
credit_score = st.slider("Credit Score", 300, 850, 700)
annual_income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, value=50000)
debt_to_income_ratio = st.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.3)
employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed"])
loan_amount = st.number_input("Loan Amount ($)", min_value=5000, max_value=1000000, value=100000)

# Calculate loan score
if st.button("Evaluate Loan Score"):
    loan_score = calculate_loan_score(credit_score, annual_income, debt_to_income_ratio, employment_status, loan_amount)
    st.subheader("Loan Score")
    st.write(f"Your loan score is: {loan_score}")

    # Loan approval decision
    if loan_score >= 80:
        st.success("Loan Approved")
    elif loan_score >= 60:
        st.warning("Loan Approved with Conditions")
    else:
        st.error("Loan Rejected")