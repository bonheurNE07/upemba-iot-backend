import logging

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    This is our Machine Learning "Brain".
    It uses an algorithm called 'Isolation Forest' to detect anomalies (weird behavior).
    Instead of hardcoding rules like "if temp > 50", the algorithm learns what "normal" 
    behavior looks like from recent data, and flags anything that looks "unusual".
    """

    def __init__(self, contamination=0.05, n_estimators=100):
        # 'contamination' is the percentage of data we expect to be anomalies (5%)
        self.contamination = contamination
        
        # 'n_estimators' is the number of "trees" in our Isolation Forest.
        # More trees = better accuracy, but takes slightly longer to compute.
        self.n_estimators = n_estimators
        
        # These are the specific sensor values the ML model will look at to learn patterns
        self.features = ["temperature", "voltage", "vib_x", "vib_y", "vib_z"]

    def train_and_predict(self, records_list):
        """
        Takes the recent sensor readings, learns from them (training), 
        and then judges the very last reading to see if it's an anomaly (prediction).
        """
        
        # 1. Safety Check: We need enough data to learn what "normal" is.
        if len(records_list) < 10:
            logger.warning("Not enough data points to train securely. Skipping.")
            # If not enough data, assume everything is perfectly normal (score 1.0)
            return 1.0, False

        # 2. Convert Data into a Table (Pandas DataFrame)
        # Pandas makes it very easy to do math on large tables of data.
        df = pd.DataFrame.from_records(records_list)[self.features]

        # 3. Handle Missing Data (Interpolation)
        # Sometimes sensors fail to send a reading (e.g., Wi-Fi drops).
        # '.interpolate' guesses the missing value by drawing a straight line between the points before and after it.
        df.interpolate(method="linear", limit_direction="both", inplace=True)
        
        # If the very first or very last values are missing, interpolation can't draw a line.
        # So we use 'ffill' (forward fill) and 'bfill' (backward fill) to copy the nearest known value.
        df.ffill(inplace=True)
        df.bfill(inplace=True)

        # 4. Standardize the Data (Normalization)
        # Temperature might be 30.0, but Vibration might be 0.05. 
        # ML algorithms get confused by vastly different scales.
        # StandardScaler forces all values to be on the same mathematical scale (around 0).
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=self.features)

        # 5. Create the Machine Learning Model
        model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=42, # Ensures we get the same result every time we run it
        )

        # 6. Train the Model ("Learn what is normal")
        # We give the model the recent history table so it learns the normal operating patterns.
        model.fit(df_scaled)

        # 7. Make a Prediction on the LATEST reading
        # 'iloc[[-1]]' gets the very last row in the table (the newest sensor reading)
        latest_reading = df_scaled.iloc[[-1]]

        # The model returns 1 if it thinks it's Normal, and -1 if it thinks it's an Anomaly
        prediction = model.predict(latest_reading)[0]
        
        # It also returns a "Score". 
        # Positive scores = very normal. Negative scores = very abnormal.
        score = model.decision_function(latest_reading)[0]

        # Convert the -1/1 prediction into a simple True/False boolean
        is_anomaly = prediction == -1

        # Return the raw mathematical score and the True/False flag
        return float(score), is_anomaly
