import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Generating synthetic transaction data (replace with real data)
transaction_data = {
    'Customer_ID': ['C1'] * 10,
    'Transaction_Amount': [9000, 8000, 9500, 8700, 9200, 10000, 8900, 8800, 8600, 1000000]
}
df = pd.DataFrame(transaction_data)

# Preprocessing data
scaler = MinMaxScaler()
df['Transaction_Amount_Scaled'] = scaler.fit_transform(df[['Transaction_Amount']])

# Isolation Forest for anomaly detection
model = IsolationForest(contamination=0.1, random_state=42)
df['Anomaly_Score'] = model.fit_predict(df[['Transaction_Amount_Scaled']])

# Flag anomalies
df['Anomaly'] = df['Anomaly_Score'].apply(lambda x: 'Yes' if x == -1 else 'No')

# Display Results
print("Transaction Data with Anomalies Flagged")
print(df)

# Visualize anomalies
plt.scatter(range(len(df)), df['Transaction_Amount'], c=(df['Anomaly'] == 'Yes'), cmap='coolwarm')
plt.title("Anomaly Detection Visualization")
plt.xlabel("Transaction Number")
plt.ylabel("Transaction Amount")
plt.show()