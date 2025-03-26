import unittest
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest

class TestAnomalyDetection(unittest.TestCase):

    def setUp(self):
        # Sample transaction data for testing
        self.transaction_data = {
            'Customer_ID': ['C1'] * 10,
            'Transaction_Amount': [9000, 8000, 9500, 8700, 9200, 10000, 8900, 8800, 8600, 1000000]
        }
        self.df = pd.DataFrame(self.transaction_data)

    def test_preprocessing(self):
        # Test MinMaxScaler preprocessing
        scaler = MinMaxScaler()
        self.df['Transaction_Amount_Scaled'] = scaler.fit_transform(self.df[['Transaction_Amount']])
        self.assertTrue((self.df['Transaction_Amount_Scaled'] >= 0).all())
        self.assertTrue((self.df['Transaction_Amount_Scaled'] <= 1).all())

    def test_anomaly_detection(self):
        # Test Isolation Forest anomaly detection
        scaler = MinMaxScaler()
        self.df['Transaction_Amount_Scaled'] = scaler.fit_transform(self.df[['Transaction_Amount']])
        model = IsolationForest(contamination=0.1, random_state=42)
        self.df['Anomaly_Score'] = model.fit_predict(self.df[['Transaction_Amount_Scaled']])
        self.assertIn(-1, self.df['Anomaly_Score'].unique())  # Ensure anomalies are detected
        self.assertIn(1, self.df['Anomaly_Score'].unique())   # Ensure normal points are detected

    def test_anomaly_flagging(self):
        # Test anomaly flagging logic
        scaler = MinMaxScaler()
        self.df['Transaction_Amount_Scaled'] = scaler.fit_transform(self.df[['Transaction_Amount']])
        model = IsolationForest(contamination=0.1, random_state=42)
        self.df['Anomaly_Score'] = model.fit_predict(self.df[['Transaction_Amount_Scaled']])
        self.df['Anomaly'] = self.df['Anomaly_Score'].apply(lambda x: 'Yes' if x == -1 else 'No')
        self.assertIn('Yes', self.df['Anomaly'].unique())  # Ensure anomalies are flagged
        self.assertIn('No', self.df['Anomaly'].unique())   # Ensure normal points are flagged

if __name__ == '__main__':
    unittest.main()