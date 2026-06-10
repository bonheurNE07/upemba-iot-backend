import logging

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Service for detecting anomalies in IoT sensor streams using Isolation Forest.
    Designed to fit over a rolling window of recent historical readings for a specific equipment.
    """

    def __init__(self, contamination=0.05, n_estimators=100):
        # contamination is the expected proportion of outliers in the dataset
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.features = ["temperature", "voltage", "vib_x", "vib_y", "vib_z"]

    def train_and_predict(self, records_list):
        """
        Takes a chronological list of dictionaries containing recent SensorReadings,
        dynamically trains the Isolation Forest on the rolling window data,
        and returns the anomaly prediction strictly for the most recent reading.

        Returns:
            anomaly_score (float): The IsolationForest decision_function score
            is_anomaly (bool): True if an anomaly is detected (-1 prediction)
        """
        if len(records_list) < 10:
            logger.warning(
                "Not enough data points to train Isolation Forest securely. Skipping.",
            )
            # Default to normal prediction (1.0) if we don't have enough operational history
            return 1.0, False

        # Extract only the necessary telemetry features into a Pandas DataFrame
        df = pd.DataFrame.from_records(records_list)[self.features]

        # 1. Data Ingestion & Preprocessing: Interpolation
        # Handle network dropouts by interpolating missing values in the rolling window
        df.interpolate(method="linear", limit_direction="both", inplace=True)
        # Fallback for remaining NaNs (e.g., if interpolation couldn't fill everything)
        df.fillna(method="ffill", inplace=True)
        df.fillna(method="bfill", inplace=True)

        # 2. Data Ingestion & Preprocessing: Normalization
        # Use StandardScaler to ensure all features are evaluated on a uniform mathematical scale
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=self.features)

        # Initialize the Unsupervised ML model
        model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=42,
        )

        # Fit the model on the entire rolling window to learn the "normal" vibration/thermal profiles
        model.fit(df_scaled)

        # Isolate the latest dataset row to evaluate current health
        latest_reading = df_scaled.iloc[[-1]]

        # Predict: 1 for normal, -1 for anomaly
        prediction = model.predict(latest_reading)[0]
        # Get raw anomaly score (negative is anomalous, positive is normal)
        score = model.decision_function(latest_reading)[0]

        is_anomaly = prediction == -1

        return float(score), is_anomaly
