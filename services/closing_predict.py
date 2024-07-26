from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import numpy as np
import joblib
from constants import *
import requests

def closing_predict(pair_id, model, scaler, input_size):

    try:
        api_url = gecko_terminal.format(pair_id=pair_id)
        response = requests.get(api_url)
        data = response.json()
        
        data = data["data"]["attributes"]["ohlcv_list"][0]
        ohlcv = np.array(data[1:]).reshape(1, -1)

        # Scale the data
        ohlcv_scaled = scaler.transform(ohlcv)

        # Convert to PyTorch tensor
        ohlcv_tensor = torch.tensor(ohlcv_scaled, dtype=torch.float32).view(1, -1, input_size)

        # Make prediction
        with torch.no_grad():
            prediction = model(ohlcv_tensor).numpy()

        # Inverse transform the prediction
        zeros_pred = np.zeros((prediction.shape[0], 5))
        zeros_pred[:, 3] = prediction.flatten()
        prediction_scaled = scaler.inverse_transform(zeros_pred)[:, 3]

        return jsonify({'predicted_close': prediction_scaled[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    