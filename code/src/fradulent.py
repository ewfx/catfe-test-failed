import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler

st.header("Fraudulent Transaction Detection")
st.text("Upload Transactional Data for Anomaly Detection")
st.text("This tool detects anomalies in transactional data using an Isolation Forest model.")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload Transactional Data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    try:
        data = pd.read_csv(uploaded_file)
        #st.subheader("Uploaded Data")
        #st.write(data.head())  # Display the first few rows of the data

        # Check if the data has numeric columns for anomaly detection
        numeric_columns = data.select_dtypes(include=["number"]).columns
        if len(numeric_columns) == 0:
            st.error("The uploaded file does not contain numeric columns for anomaly detection.")
        else:
            # Normalize the TransactionAmount column
            if "TransactionAmount" in numeric_columns:
                scaler = StandardScaler()
                data["TransactionAmount_Normalized"] = scaler.fit_transform(data[["TransactionAmount"]])
                numeric_columns = numeric_columns.append(pd.Index(["TransactionAmount_Normalized"]))


            # Normalize the BankBalance column (if present)
            if "BankBalance" in numeric_columns:
                st.text("Normalizing Bank Balance column...")
                data["BankBalance_Normalized"] = scaler.fit_transform(data[["BankBalance"]])
                numeric_columns = numeric_columns.append(pd.Index(["BankBalance_Normalized"]))

                # Add rule-based logic for unusually low or high bank balances
                median_balance = data["BankBalance"].median()
                data["is_unusual_balance"] = data["BankBalance"].apply(
                    lambda x: "Yes" if x < 0 or x > 5 * median_balance else "No"
                )

            # Handle rare countries
            if "Country" in data.columns:
                st.text("Encoding country column for anomaly detection...")
                country_counts = data["Country"].value_counts()
                rare_countries = country_counts[country_counts == 1].index.tolist()  # Identify rare countries
                data["is_rare_country"] = data["Country"].apply(lambda x: "Yes" if x in rare_countries else "No")

                # Encode the country column
                label_encoder = LabelEncoder()
                data["Country_Encoded"] = label_encoder.fit_transform(data["Country"])
                numeric_columns = numeric_columns.append(pd.Index(["Country_Encoded"]))

            # Train an Isolation Forest model for anomaly detection
            st.text("Performing anomaly detection...")
            model = IsolationForest(contamination=0.1, random_state=42)  # Increased contamination to 0.1
            data["anomaly_score"] = model.fit_predict(data[numeric_columns])

            # Mark anomalies
            data["is_anomaly"] = data["anomaly_score"].apply(lambda x: "Yes" if x == -1 else "No")

            # Add rule-based logic for high transaction amounts
            median_amount = data["TransactionAmount"].median()
            data["is_high_transaction"] = data["TransactionAmount"].apply(
                lambda x: "Yes" if x > 10 * median_amount else "No"
            )

            # Combine model-based and rule-based anomalies
            data["final_anomaly"] = data.apply(
                lambda row: "Yes" if row["is_anomaly"] == "Yes" or row["is_rare_country"] == "Yes" or row["is_high_transaction"] == "Yes" else "No",
                axis=1
            )

            # Display results
            st.subheader("Anomaly Detection Results")
            st.write(data[["final_anomaly", "is_rare_country", "is_high_transaction","is_unusual_balance", "Country", "TransactionAmount","BankBalance"]])

            
            # Downloadable results
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="anomaly_detection_results.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to proceed.")